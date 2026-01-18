import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Leer el CSV
df = pd.read_csv('resultados_analisis.csv')

# Filtrar por categoría desarrollo_profesional
df_prof = df[df['Categoria'] == 'desarrollo_profesional']

# Crear diccionario para asignar letras
nombres_letras = {
    'Ferias de Empleo y Prácticas Especializadas': 'A',
    'Talleres de Habilidades Profesionales Esenciales': 'B',
    'Talleres de Herramientas Profesionales (Workshops IEEE)': 'C',
    'Proyectos Interdisciplinarios (Hackathons / Challenges IEEE)': 'D',
    'Charlas con Profesionales Destacados (IEEE Technical Talks)': 'E',
    'Visitas Técnicas a Empresas (IEEE Industrial Visits)': 'F',
    'Programas de Mentoría Personalizada (IEEE Mentoring Program)': 'G'
}

nombres_completos = {
    'A': 'Ferias de Empleo y Prácticas Especializadas',
    'B': 'Talleres de Habilidades Profesionales Esenciales',
    'C': 'Talleres de Herramientas Profesionales (Workshops IEEE)',
    'D': 'Proyectos Interdisciplinarios (Hackathons / Challenges IEEE)',
    'E': 'Charlas con Profesionales Destacados (IEEE Technical Talks)',
    'F': 'Visitas Técnicas a Empresas (IEEE Industrial Visits)',
    'G': 'Programas de Mentoría Personalizada (IEEE Mentoring Program)'
}

df_prof['Alt_Letra'] = df_prof['Alternativa'].map(nombres_letras)

# Crear figura con 3 subgráficos
fig, axes = plt.subplots(1, 3, figsize=(16, 8))
fig.suptitle('Comparación de Métodos de Agregación - Desarrollo Profesional', 
             fontsize=16, fontweight='bold', y=0.98)

metodos = ['Borda', 'Kemeny-Young', 'Schulze']
colores_metodos = ['#2C2C2C', '#666666', '#A6A6A6']  # Escala de grises profesional

for idx, metodo in enumerate(metodos):
    datos = df_prof[df_prof['Metodo'] == metodo].sort_values('Posicion')
    
    ax = axes[idx]
    letras = datos['Alt_Letra'].values
    puntajes = datos['Puntaje'].astype(float).values
    
    barras = ax.barh(letras, puntajes, color=colores_metodos[idx], alpha=0.9, 
                     edgecolor='black', linewidth=1.2)
    
    # Agregar valores en las barras
    for barra in barras:
        ancho = barra.get_width()
        ax.text(ancho, barra.get_y() + barra.get_height()/2., 
                f'{int(ancho)}', ha='left', va='center', fontsize=14, 
                fontweight='bold', color='black')
    
    ax.set_xlabel('Puntaje', fontsize=14, fontweight='bold')
    ax.set_title(f'Método: {metodo}', fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    ax.tick_params(axis='y', labelsize=16)
    ax.tick_params(axis='x', labelsize=13, colors='black')
    for label in ax.get_yticklabels():
        label.set_fontweight('bold')
        label.set_fontsize(16)
    for label in ax.get_xticklabels():
        label.set_fontweight('bold')
        label.set_fontsize(13)
    ax.grid(True, alpha=0.3, axis='x', linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('grafico_comparativo_metodos.png', dpi=300, bbox_inches='tight')
print("Gráfico guardado como 'grafico_comparativo_metodos.png'")
plt.show()
