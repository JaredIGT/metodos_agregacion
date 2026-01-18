import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Leer el CSV
df = pd.read_csv('resultados_analisis.csv')

# Filtrar por categoría bienestar_estudiantil
df_bien = df[df['Categoria'] == 'bienestar_estudiantil']

# Crear diccionario para asignar letras (ajustar según alternativas)
nombres_letras = {}
alternativas_unicas = df_bien['Alternativa'].unique()
for i, alt in enumerate(alternativas_unicas):
    nombres_letras[alt] = chr(65 + i)  # A, B, C, D, etc.

df_bien['Alt_Letra'] = df_bien['Alternativa'].map(nombres_letras)

# Crear figura con 3 subgráficos
fig, axes = plt.subplots(1, 3, figsize=(16, 8))
fig.suptitle('Comparación de Métodos de Agregación - Bienestar Estudiantil', 
             fontsize=16, fontweight='bold', y=0.98)

metodos = ['Borda', 'Kemeny-Young', 'Schulze']
colores_metodos = ['#2C2C2C', '#666666', '#A6A6A6']

for idx, metodo in enumerate(metodos):
    datos = df_bien[df_bien['Metodo'] == metodo].sort_values('Posicion')
    
    ax = axes[idx]
    letras = datos['Alt_Letra'].values
    puntajes = datos['Puntaje'].astype(float).values
    
    barras = ax.barh(letras, puntajes, color=colores_metodos[idx], alpha=0.9, 
                     edgecolor='black', linewidth=1.2)
    
    # Agregar valores en las barras
    for barra, puntaje in zip(barras, puntajes):
        ancho = barra.get_width()
        # Ajustar posición del texto según si es positivo o negativo
        if puntaje >= 0:
            x_pos = ancho
            ha_align = 'left'
        else:
            x_pos = ancho + 5
            ha_align = 'left'
        ax.text(x_pos, barra.get_y() + barra.get_height()/2., 
                f'{int(puntaje)}', ha=ha_align, va='center', fontsize=14, 
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
    ax.axvline(x=0, color='black', linewidth=0.8)

plt.tight_layout()
plt.savefig('grafico_bienestar.png', dpi=300, bbox_inches='tight')
print("Gráfico guardado como 'grafico_bienestar.png'")
plt.show()
