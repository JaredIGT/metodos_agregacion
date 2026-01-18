import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo Excel
df = pd.read_excel('Formul.xlsx')

# Unir todas las columnas de carrera en una sola serie
carrera_cols = [col for col in df.columns if 'carrera est' in col]
carreras = pd.concat([df[col].dropna() for col in carrera_cols])
conteo = carreras.value_counts().sort_values(ascending=False)

# Graficar y guardar imagen
plt.figure(figsize=(8,6))
conteo.plot(kind='barh', color='gray')
plt.xlabel('Número de Estudiantes', fontsize=14, fontweight='bold')
plt.ylabel('Carrera', fontsize=14, fontweight='bold')
plt.title('Distribución de Participantes por Carrera', fontsize=16, fontweight='bold')
for i, v in enumerate(conteo):
    plt.text(v + 0.2, i, str(v), va='center')
plt.tight_layout(rect=(0, 0, 1, 1))
plt.savefig('distribucion_carrera.png', dpi=300)
plt.close()
print('Imagen guardada como distribucion_carrera.png')
