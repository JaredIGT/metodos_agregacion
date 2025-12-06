import pandas as pd
import numpy as np
from itertools import permutations
import tkinter as tk
from tkinter import ttk, messagebox
import os


# ==================== MÉTODOS DE AGREGACIÓN DE RANKINGS ====================

def schulze(candidatos, votos):
    """
    Método Schulze para agregar rankings.
    Retorna ranking completo y matriz de fuerza.
    """
    n = len(candidatos)
    if n == 0:
        return [], {}

    index = {c: i for i, c in enumerate(candidatos)}

    # Matriz de preferencias por pares
    d = [[0] * n for _ in range(n)]
    for voto in votos:
        for i in range(n):
            for j in range(i + 1, n):
                a = index[voto[i]]
                b = index[voto[j]]
                d[a][b] += 1

    # Matriz de fuerza de caminos
    p = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                p[i][j] = d[i][j] if d[i][j] > d[j][i] else 0

    # Floyd–Warshall modificado
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if i != j and i != k and j != k:
                    p[i][j] = max(p[i][j], min(p[i][k], p[k][j]))

    # Calcular fuerza neta
    fuerza_neta = {}
    for i in range(n):
        fuerza_positiva = sum(p[i][j] for j in range(n) if i != j)
        fuerza_negativa = sum(p[j][i] for j in range(n) if i != j)
        fuerza_neta[candidatos[i]] = fuerza_positiva - fuerza_negativa

    # Ordenar por fuerza neta descendente
    ranking_schulze = sorted(candidatos, key=lambda x: fuerza_neta[x], reverse=True)

    return ranking_schulze, fuerza_neta


def kemeny_young(candidatos, votos):
    """
    Método Kemeny-Young para agregar rankings.
    """
    n = len(candidatos)
    if n == 0:
        return [], {}, 0, {}

    index = {c: i for i, c in enumerate(candidatos)}

    # Matriz de preferencias por pares
    d = [[0] * n for _ in range(n)]
    for voto in votos:
        for i in range(n):
            for j in range(i + 1, n):
                a = index[voto[i]]
                b = index[voto[j]]
                d[a][b] += 1

    # Calcular puntajes para cada alternativa
    puntajes_kemeny = {c: 0 for c in candidatos}
    for i in range(n):
        for j in range(n):
            if i != j:
                if d[i][j] > d[j][i]:
                    puntajes_kemeny[candidatos[i]] += d[i][j] - d[j][i]

    # Encontrar ranking óptimo
    best_score = -1
    best_rankings = []

    for perm in permutations(candidatos):
        score = 0
        for i in range(n):
            for j in range(i + 1, n):
                a = index[perm[i]]
                b = index[perm[j]]
                score += d[a][b]

        if score > best_score:
            best_score = score
            best_rankings = [list(perm)]
        elif score == best_score:
            best_rankings.append(list(perm))

    # Tomar el primer ranking óptimo
    ranking_kemeny = best_rankings[0] if best_rankings else []

    # Posiciones en el ranking
    posiciones_kemeny = {alt: i + 1 for i, alt in enumerate(ranking_kemeny)}

    return ranking_kemeny, puntajes_kemeny, best_score, posiciones_kemeny


def borda(candidatos, votos):
    """
    Método Borda para agregar rankings.
    """
    n = len(candidatos)
    if n == 0:
        return [], {}, []

    scores = {c: 0 for c in candidatos}

    for voto in votos:
        for pos, candidato in enumerate(voto):
            scores[candidato] += (n - 1 - pos)

    # Ordenar por puntaje descendente
    ranking_borda = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    alternativas_ordenadas = [item[0] for item in ranking_borda]
    puntajes_ordenados = {item[0]: item[1] for item in ranking_borda}

    return alternativas_ordenadas, puntajes_ordenados, ranking_borda


# ==================== PROCESAMIENTO CON FILTROS ====================

def procesar_con_filtros(df, filtros=None):
    """
    Procesa el DataFrame con filtros demográficos opcionales.

    Args:
        df: DataFrame con los datos
        filtros: Diccionario con filtros. Ejemplo:
            {
                'rango_edad': ['20-22', '23-25'],
                'genero': ['Masculino'],
                'facultad': ['FIEC'],
                'carrera': ['Computación']
            }
    """
    if filtros is None:
        filtros = {}

    # Aplicar filtros
    df_filtrado = df.copy()

    if 'rango_edad' in filtros and filtros['rango_edad']:
        df_filtrado = df_filtrado[df_filtrado['¿Cuál es su rango de edad?'].isin(filtros['rango_edad'])]

    if 'genero' in filtros and filtros['genero']:
        df_filtrado = df_filtrado[df_filtrado['Género:'].isin(filtros['genero'])]

    if 'facultad' in filtros and filtros['facultad']:
        df_filtrado = df_filtrado[df_filtrado['¿A que facultad perteneces?'].isin(filtros['facultad'])]

    if 'carrera' in filtros and filtros['carrera']:
        # Filtrar por carrera (buscar en todas las columnas de carrera)
        mask = pd.Series([False] * len(df_filtrado))
        carrera_cols = [col for col in df.columns if 'carrera' in col.lower() and 'estudiando' in col.lower()]

        for col in carrera_cols:
            mask = mask | df_filtrado[col].isin(filtros['carrera'])

        df_filtrado = df_filtrado[mask]

    print(f"\n{'=' * 80}")
    print(f"DATOS FILTRADOS:")
    print(f"{'=' * 80}")
    print(f"Total respuestas originales: {len(df)}")
    print(f"Total respuestas filtradas: {len(df_filtrado)}")

    if len(df_filtrado) == 0:
        print("⚠️  No hay datos después de aplicar los filtros")
        return {}

    # Mostrar distribución demográfica filtrada
    if 'rango_edad' in filtros:
        print(f"\nDistribución por rango de edad (filtrado):")
        print(df_filtrado['¿Cuál es su rango de edad?'].value_counts())

    if 'genero' in filtros:
        print(f"\nDistribución por género (filtrado):")
        print(df_filtrado['Género:'].value_counts())

    if 'facultad' in filtros:
        print(f"\nDistribución por facultad (filtrado):")
        print(df_filtrado['¿A que facultad perteneces?'].value_counts())

    return df_filtrado


def extraer_nombre_corto(nombre_largo):
    """Extrae nombre corto de las alternativas."""
    if '[' in str(nombre_largo) and ']' in str(nombre_largo):
        return str(nombre_largo).split('[')[-1].split(']')[0].strip()
    return str(nombre_largo)[:50]


def aplicar_metodos_a_categoria(alternativas, rankings_individuales):
    """Aplica los tres métodos a un conjunto de rankings."""
    resultados = {}

    # 1. BORDA
    try:
        ranking_borda, puntajes_borda, ranking_completo_borda = borda(alternativas, rankings_individuales)
        resultados['borda'] = {
            'ranking': ranking_borda,
            'puntajes': puntajes_borda,
            'ranking_completo': ranking_completo_borda
        }
    except Exception as e:
        print(f"Error en Borda: {e}")
        resultados['borda'] = None

    # 2. KEMENY-YOUNG
    try:
        ranking_kemeny, puntajes_kemeny, score_kemeny, posiciones_kemeny = kemeny_young(alternativas,
                                                                                        rankings_individuales)
        resultados['kemeny'] = {
            'ranking': ranking_kemeny,
            'puntajes': puntajes_kemeny,
            'score_total': score_kemeny,
            'posiciones': posiciones_kemeny
        }
    except Exception as e:
        print(f"Error en Kemeny-Young: {e}")
        resultados['kemeny'] = None

    # 3. SCHULZE
    try:
        ranking_schulze, fuerzas_schulze = schulze(alternativas, rankings_individuales)
        resultados['schulze'] = {
            'ranking': ranking_schulze,
            'fuerzas': fuerzas_schulze
        }
    except Exception as e:
        print(f"Error en Schulze: {e}")
        resultados['schulze'] = None

    return resultados


def procesar_categorias(df_filtrado):
    """Procesa las tres categorías principales."""
    # Identificar categorías
    categorias = {
        'desarrollo_profesional': [],
        'infraestructura_academica': [],
        'bienestar_estudiantil': []
    }

    for col in df_filtrado.columns:
        col_str = str(col)
        if 'potenciar tu desarrollo profesional' in col_str:
            categorias['desarrollo_profesional'].append(col)
        elif 'mejorar la infraestructura académica' in col_str:
            categorias['infraestructura_academica'].append(col)
        elif 'potenciar el bienestar estudiantil' in col_str:
            categorias['bienestar_estudiantil'].append(col)

    resultados_totales = {}

    for categoria_nombre, columnas in categorias.items():
        if not columnas:
            continue

        print(f"\n{'=' * 60}")
        print(f"CATEGORÍA: {categoria_nombre.replace('_', ' ').title()}")
        print(f"{'=' * 60}")

        alternativas = [extraer_nombre_corto(col) for col in columnas]
        print(f"Alternativas encontradas: {len(alternativas)}")

        # Recolectar rankings individuales
        rankings_individuales = []

        for _, fila in df_filtrado.iterrows():
            priorizaciones = {}
            for col, alt in zip(columnas, alternativas):
                valor = fila.get(col)
                if pd.notna(valor):
                    try:
                        priorizaciones[alt] = int(float(valor))
                    except:
                        priorizaciones[alt] = None
                else:
                    priorizaciones[alt] = None

            # Solo incluir respuestas completas
            if all(v is not None for v in priorizaciones.values()):
                ranking_ordenado = sorted(priorizaciones.keys(), key=lambda x: priorizaciones[x])
                rankings_individuales.append(ranking_ordenado)

        print(f"Rankings individuales válidos: {len(rankings_individuales)}")

        if len(rankings_individuales) < 2:
            print("⚠️  Insuficientes datos para análisis")
            continue

        # Aplicar métodos
        resultados_categoria = aplicar_metodos_a_categoria(alternativas, rankings_individuales)

        # Mostrar resultados
        for metodo, resultado in resultados_categoria.items():
            if resultado:
                if 'ranking' in resultado and resultado['ranking']:
                    print(f"\n{metodo.upper()}:")
                    print(f"  Ganador: {resultado['ranking'][0]}")
                    if metodo == 'borda' and 'puntajes' in resultado:
                        print(f"  Puntaje ganador: {resultado['puntajes'].get(resultado['ranking'][0], 'N/A')}")

        resultados_totales[categoria_nombre] = {
            'alternativas': alternativas,
            'num_respuestas': len(rankings_individuales),
            'resultados': resultados_categoria,
            'rankings_individuales': rankings_individuales
        }

    return resultados_totales


# ==================== INTERFAZ GRÁFICA PARA FILTROS ====================

class FiltroApp:
    def __init__(self, df):
        self.df = df
        self.root = tk.Tk()
        self.root.title("Filtros Demográficos - Análisis de Rankings")
        self.root.geometry("600x700")

        # Variables para filtros
        self.filtros = {
            'rango_edad': [],
            'genero': [],
            'facultad': [],
            'carrera': []
        }

        self.setup_ui()

    def setup_ui(self):
        # Título
        title_label = ttk.Label(self.root, text="FILTROS DEMOGRÁFICOS",
                                font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 1. RANGO DE EDAD
        ttk.Label(main_frame, text="Rango de Edad:", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky=tk.W,
                                                                                      pady=(0, 5))

        self.edad_vars = {}
        edades = sorted(self.df['¿Cuál es su rango de edad?'].dropna().unique())
        for i, edad in enumerate(edades):
            var = tk.BooleanVar()
            self.edad_vars[edad] = var
            cb = ttk.Checkbutton(main_frame, text=edad, variable=var)
            cb.grid(row=1 + i // 3, column=i % 3, sticky=tk.W, padx=5)

        # Separador
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(row=5, column=0, columnspan=3, sticky=tk.EW, pady=10)

        # 2. GÉNERO
        ttk.Label(main_frame, text="Género:", font=("Arial", 11, "bold")).grid(row=6, column=0, sticky=tk.W,
                                                                               pady=(0, 5))

        self.genero_vars = {}
        generos = sorted(self.df['Género:'].dropna().unique())
        for i, genero in enumerate(generos):
            var = tk.BooleanVar()
            self.genero_vars[genero] = var
            cb = ttk.Checkbutton(main_frame, text=genero, variable=var)
            cb.grid(row=7, column=i, sticky=tk.W, padx=5)

        # Separador
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(row=8, column=0, columnspan=3, sticky=tk.EW, pady=10)

        # 3. FACULTAD
        ttk.Label(main_frame, text="Facultad:", font=("Arial", 11, "bold")).grid(row=9, column=0, sticky=tk.W,
                                                                                 pady=(0, 5))

        self.facultad_vars = {}
        facultades = sorted(self.df['¿A que facultad perteneces?'].dropna().unique())

        # Frame con scroll para facultades
        facultad_frame = ttk.Frame(main_frame)
        facultad_frame.grid(row=10, column=0, columnspan=3, sticky=tk.W)

        canvas = tk.Canvas(facultad_frame, height=100)
        scrollbar = ttk.Scrollbar(facultad_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for i, facultad in enumerate(facultades):
            var = tk.BooleanVar()
            self.facultad_vars[facultad] = var
            cb = ttk.Checkbutton(scrollable_frame, text=facultad, variable=var)
            cb.pack(anchor=tk.W, padx=5, pady=2)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Separador
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(row=11, column=0, columnspan=3, sticky=tk.EW, pady=10)

        # 4. CARRERA
        ttk.Label(main_frame, text="Carrera (opcional):", font=("Arial", 11, "bold")).grid(row=12, column=0,
                                                                                           sticky=tk.W, pady=(0, 5))

        # Obtener todas las carreras únicas
        todas_carreras = set()
        carrera_cols = [col for col in self.df.columns if 'carrera' in col.lower() and 'estudiando' in col.lower()]
        for col in carrera_cols:
            carreras_col = self.df[col].dropna().unique()
            for carrera in carreras_col:
                if carrera and str(carrera).strip():
                    todas_carreras.add(str(carrera).strip())

        self.carrera_vars = {}
        carreras_lista = sorted(todas_carreras)

        # Entry para búsqueda
        carrera_search_frame = ttk.Frame(main_frame)
        carrera_search_frame.grid(row=13, column=0, columnspan=3, sticky=tk.EW, pady=(0, 5))

        ttk.Label(carrera_search_frame, text="Buscar:").pack(side=tk.LEFT, padx=(0, 5))
        self.carrera_search_var = tk.StringVar()
        self.carrera_search_var.trace('w', self.filtrar_carreras)
        search_entry = ttk.Entry(carrera_search_frame, textvariable=self.carrera_search_var, width=30)
        search_entry.pack(side=tk.LEFT)

        # Listbox para carreras
        carrera_list_frame = ttk.Frame(main_frame)
        carrera_list_frame.grid(row=14, column=0, columnspan=3, sticky=tk.NSEW, pady=(0, 10))

        self.carrera_listbox = tk.Listbox(carrera_list_frame, selectmode=tk.MULTIPLE, height=6)
        scrollbar_carrera = ttk.Scrollbar(carrera_list_frame, orient=tk.VERTICAL, command=self.carrera_listbox.yview)
        self.carrera_listbox.configure(yscrollcommand=scrollbar_carrera.set)

        self.carrera_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_carrera.pack(side=tk.RIGHT, fill=tk.Y)

        # Almacenar todas las carreras
        self.todas_carreras_lista = carreras_lista
        self.actualizar_lista_carreras(carreras_lista)

        # Botones
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Aplicar Filtros y Analizar",
                   command=self.aplicar_filtros).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="Seleccionar Todo",
                   command=self.seleccionar_todo).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="Limpiar Todo",
                   command=self.limpiar_todo).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="Salir",
                   command=self.root.quit).pack(side=tk.LEFT, padx=5)

        # Configurar grid weights
        for i in range(3):
            main_frame.columnconfigure(i, weight=1)

    def actualizar_lista_carreras(self, carreras):
        """Actualiza la lista de carreras en el Listbox."""
        self.carrera_listbox.delete(0, tk.END)
        for carrera in carreras:
            self.carrera_listbox.insert(tk.END, carrera)

    def filtrar_carreras(self, *args):
        """Filtra las carreras según el texto de búsqueda."""
        busqueda = self.carrera_search_var.get().lower()
        if busqueda:
            carreras_filtradas = [c for c in self.todas_carreras_lista if busqueda in c.lower()]
        else:
            carreras_filtradas = self.todas_carreras_lista

        self.actualizar_lista_carreras(carreras_filtradas)

    def seleccionar_todo(self):
        """Selecciona todas las opciones en todos los filtros."""
        for var in self.edad_vars.values():
            var.set(True)
        for var in self.genero_vars.values():
            var.set(True)
        for var in self.facultad_vars.values():
            var.set(True)
        # Para carreras, seleccionar todas las visibles
        self.carrera_listbox.selection_set(0, tk.END)

    def limpiar_todo(self):
        """Limpia todas las selecciones."""
        for var in self.edad_vars.values():
            var.set(False)
        for var in self.genero_vars.values():
            var.set(False)
        for var in self.facultad_vars.values():
            var.set(False)
        self.carrera_listbox.selection_clear(0, tk.END)
        self.carrera_search_var.set("")
        self.actualizar_lista_carreras(self.todas_carreras_lista)

    def aplicar_filtros(self):
        """Aplica los filtros seleccionados."""
        # Obtener rangos de edad seleccionados
        self.filtros['rango_edad'] = [edad for edad, var in self.edad_vars.items() if var.get()]

        # Obtener géneros seleccionados
        self.filtros['genero'] = [genero for genero, var in self.genero_vars.items() if var.get()]

        # Obtener facultades seleccionadas
        self.filtros['facultad'] = [facultad for facultad, var in self.facultad_vars.items() if var.get()]

        # Obtener carreras seleccionadas
        selecciones = self.carrera_listbox.curselection()
        self.filtros['carrera'] = [self.carrera_listbox.get(i) for i in selecciones]

        # Verificar que al menos haya algún criterio seleccionado
        total_selecciones = (len(self.filtros['rango_edad']) +
                             len(self.filtros['genero']) +
                             len(self.filtros['facultad']) +
                             len(self.filtros['carrera']))

        if total_selecciones == 0:
            messagebox.showwarning("Advertencia",
                                   "No has seleccionado ningún filtro. Se analizarán todos los datos.")
            # Establecer filtros vacíos para procesar todo
            self.filtros = {k: [] for k in self.filtros}

        print("\nFiltros aplicados:")
        for key, value in self.filtros.items():
            if value:
                print(f"  {key}: {value}")

        self.root.destroy()


# ==================== FUNCIÓN PRINCIPAL ====================

def main():
    print("=" * 80)
    print("SISTEMA DE ANÁLISIS DE RANKINGS CON FILTROS DEMOGRÁFICOS")
    print("=" * 80)

    try:
        # Leer archivo Excel
        if not os.path.exists('Formul.xlsx'):
            print("ERROR: No se encontró el archivo 'Formul.xlsx'")
            print("Asegúrate de que el archivo esté en el mismo directorio.")
            return

        df = pd.read_excel('Formul.xlsx', sheet_name='Respuestas de formulario 1')
        df.columns = [str(col).strip() for col in df.columns]

        print(f"✓ Archivo cargado exitosamente")
        print(f"✓ Total de respuestas: {len(df)}")

        # Mostrar interfaz para filtros
        print("\nAbriendo interfaz de filtros...")
        app = FiltroApp(df)
        app.root.mainloop()

        # Aplicar filtros
        df_filtrado = procesar_con_filtros(df, app.filtros)

        if len(df_filtrado) == 0:
            print("\n⚠️  No hay datos después de aplicar los filtros.")
            respuesta = input("¿Deseas analizar todos los datos sin filtros? (s/n): ")
            if respuesta.lower() == 's':
                df_filtrado = df
                print("Analizando todos los datos sin filtros...")
            else:
                return

        # Procesar categorías
        resultados = procesar_categorias(df_filtrado)

        if not resultados:
            print("\n⚠️  No se pudieron procesar los datos.")
            return

        # Guardar resultados en Excel
        print(f"\n{'=' * 80}")
        print("GUARDANDO RESULTADOS...")
        print(f"{'=' * 80}")

        with pd.ExcelWriter('resultados_analisis.xlsx') as writer:
            for categoria, datos in resultados.items():
                # Crear hoja para esta categoría
                filas = []

                # Agregar resultados de cada método
                for metodo_nombre, metodo_resultados in datos['resultados'].items():
                    if not metodo_resultados:
                        continue

                    if metodo_nombre == 'borda' and 'ranking_completo' in metodo_resultados:
                        for i, (alt, puntaje) in enumerate(metodo_resultados['ranking_completo'], 1):
                            filas.append({
                                'Categoria': categoria,
                                'Metodo': 'Borda',
                                'Alternativa': alt,
                                'Puntaje': puntaje,
                                'Posicion': i,
                                'Tipo': 'Puntaje Borda'
                            })

                    elif metodo_nombre == 'kemeny' and 'posiciones' in metodo_resultados:
                        for alt, pos in metodo_resultados['posiciones'].items():
                            filas.append({
                                'Categoria': categoria,
                                'Metodo': 'Kemeny-Young',
                                'Alternativa': alt,
                                'Puntaje': metodo_resultados['puntajes'].get(alt, 0),
                                'Posicion': pos,
                                'Tipo': 'Puntaje Kemeny'
                            })

                    elif metodo_nombre == 'schulze' and 'ranking' in metodo_resultados:
                        for i, alt in enumerate(metodo_resultados['ranking'], 1):
                            filas.append({
                                'Categoria': categoria,
                                'Metodo': 'Schulze',
                                'Alternativa': alt,
                                'Puntaje': metodo_resultados['fuerzas'].get(alt, 0),
                                'Posicion': i,
                                'Tipo': 'Fuerza Neta Schulze'
                            })

                if filas:
                    df_categoria = pd.DataFrame(filas)
                    # Ordenar por método y posición
                    df_categoria = df_categoria.sort_values(['Metodo', 'Posicion'])
                    sheet_name = categoria[:31]  # Limitar a 31 caracteres
                    df_categoria.to_excel(writer, sheet_name=sheet_name, index=False)

            # Hoja de resumen
            resumen_filas = []
            for categoria, datos in resultados.items():
                for metodo_nombre, metodo_resultados in datos['resultados'].items():
                    if metodo_resultados and 'ranking' in metodo_resultados and metodo_resultados['ranking']:
                        resumen_filas.append({
                            'Categoria': categoria.replace('_', ' ').title(),
                            'Metodo': metodo_nombre.title(),
                            'Ganador': metodo_resultados['ranking'][0],
                            'Num_Respuestas': datos['num_respuestas'],
                            'Total_Alternativas': len(datos['alternativas'])
                        })

            if resumen_filas:
                df_resumen = pd.DataFrame(resumen_filas)
                df_resumen.to_excel(writer, sheet_name='RESUMEN', index=False)

        print("✓ Resultados guardados en 'resultados_analisis.xlsx'")

        # Mostrar archivo generado
        print(f"\n{'=' * 80}")
        print("ARCHIVOS GENERADOS:")
        print(f"{'=' * 80}")
        print("1. resultados_analisis.xlsx - Resultados completos de los 3 métodos")
        print("\nContenido:")
        for categoria in resultados.keys():
            print(f"  - Hoja '{categoria[:31]}': Resultados para {categoria.replace('_', ' ')}")
        print("  - Hoja 'RESUMEN': Resumen comparativo")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()