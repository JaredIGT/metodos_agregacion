import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Leer el Excel (hoja infraestructura_academica)
df = pd.read_excel('resultados_analisis.xlsx', sheet_name='infraestructura_academica')

# Filtrar por categoría infraestructura_academica
df_infra = df[df['Categoria'] == 'infraestructura_academica']

# Crear diccionario para asignar letras (ajustar según alternativas)
nombres_letras = {}
alternativas_unicas = df_infra['Alternativa'].unique()
for i, alt in enumerate(alternativas_unicas):
    nombres_letras[alt] = chr(65 + i)  # A, B, C, D, etc.

df_infra['Alt_Letra'] = df_infra['Alternativa'].map(nombres_letras)

# Crear figura con 3 subgráficos
fig, axes = plt.subplots(1, 3, figsize=(16, 8))
fig.suptitle('Comparación de Métodos de Agregación - Infraestructura Académica', 
             fontsize=16, fontweight='bold', y=0.98)

metodos = ['Borda', 'Kemeny-Young', 'Schulze']
colores_metodos = ['#2C2C2C', '#666666', '#A6A6A6']

for idx, metodo in enumerate(metodos):
    datos = df_infra[df_infra['Metodo'] == metodo].sort_values('Posicion')
    
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
plt.savefig('grafico_infraestructura.png', dpi=300, bbox_inches='tight')
print("Gráfico guardado como 'grafico_infraestructura.png'")
plt.show()
