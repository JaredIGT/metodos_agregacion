import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo Excel
df = pd.read_excel('Formul.xlsx')

# Usar el nombre correcto de la columna para facultad
col_facultad = '¿A que facultad perteneces?'
conteo = df[col_facultad].value_counts().sort_values(ascending=False)

# Graficar y guardar imagen
plt.figure(figsize=(8,5))
conteo.plot(kind='barh', color='gray')
plt.xlabel('Número de Estudiantes', fontsize=14, fontweight='bold')
plt.ylabel('Facultad', fontsize=14, fontweight='bold')
plt.title('Distribución de Participantes por Facultad', fontsize=16, fontweight='bold')
for i, v in enumerate(conteo):
    plt.text(v + 0.2, i, str(v), va='center')
plt.tight_layout()
plt.savefig('distribucion_facultad.png', dpi=300)
plt.close()
print('Imagen guardada como distribucion_facultad.png')
