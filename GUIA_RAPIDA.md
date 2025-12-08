# GUÍA RÁPIDA: CÓMO USAR LOS ARCHIVOS GENERADOS

## Para la Sección 4.4.1 - Ranking Grupal por Cada Método

### Paso 1: Copiar las Tablas
Abre `TABLAS_PARA_DOCUMENTO.txt` y copia directamente:
- **Tablas 5-7** para Desarrollo Profesional
- **Tablas 8-10** para Infraestructura Académica  
- **Tablas 11-13** para Bienestar Estudiantil

### Paso 2: Insertar las Figuras
Inserta estas imágenes PNG en tu documento:
- `figura_desarrollo_profesional.png` → Rankings comparativos de Desarrollo Profesional
- `figura_infraestructura_academica.png` → Rankings comparativos de Infraestructura Académica
- `figura_bienestar_estudiantil.png` → Rankings comparativos de Bienestar Estudiantil

---

## Para la Sección 4.4.2 - Distancias Respecto a Rankings Individuales

### Paso 1: Copiar el Contenido
Abre `DISTANCIAS_INDIVIDUALES_TABLAS.md` - contiene:
- Introducción completa sobre representatividad
- **Tabla 14**: Kendall Tau promedio (ranking grupal vs 54 individuales)
- **Tabla 15**: Spearman promedio (ranking grupal vs 54 individuales)
- **Tabla 16**: Footrule promedio (ranking grupal vs 54 individuales)
- **Tabla 17**: Resumen consolidado de los 3 métodos
- Interpretaciones detalladas para cada tabla
- Conclusiones del análisis de representatividad

### Paso 2: Insertar las Figuras de Distancias
Inserta estas imágenes PNG (300 DPI):
- `figura_kendall_individuales.png` → Figura 8: Kendall Tau por escenario
- `figura_spearman_individuales.png` → Figura 9: Spearman por escenario
- `figura_footrule_individuales.png` → Figura 10: Footrule por escenario
- `figura_comparativa_individuales.png` → Figura 11: Comparativa general de métodos

---

## Archivos de Datos

### Archivos Esenciales:
- **`Formul.xlsx`**: Datos originales (54 respuestas de estudiantes)
- **`resultados_analisis.xlsx`**: Rankings grupales por método y escenario
- **`distancias_rankings_individuales.xlsx`**: Distancias correctas (grupal vs individuales)

### Código:
- **`main.py`**: Script completo de análisis con los 3 métodos de agregación

---

## Figura Adicional (Opcional)

Si deseas mostrar la convergencia entre métodos:
- `figura_consenso.png`: Visualización de que los 3 métodos producen ganadores idénticos en cada escenario

---

## Verificación de Calidad

✅ Todas las figuras están a **300 DPI** (apto para impresión)  
✅ Formato **PNG** compatible con todos los editores  
✅ Títulos y etiquetas claros en todas las figuras  
✅ Tablas en **Markdown** (fácil copiar y pegar)  
✅ Distancias calculadas correctamente (ranking grupal vs 54 individuales)

---

## Estructura de Numeración de Tablas

```
Sección 4.4.1 (Rankings Grupales por Método)
├── Tabla 5: Borda - Desarrollo Profesional
├── Tabla 6: Schulze - Desarrollo Profesional
├── Tabla 7: Kemeny-Young - Desarrollo Profesional
├── Tabla 8: Borda - Infraestructura Académica
├── Tabla 9: Schulze - Infraestructura Académica
├── Tabla 10: Kemeny-Young - Infraestructura Académica
├── Tabla 11: Borda - Bienestar Estudiantil
├── Tabla 12: Schulze - Bienestar Estudiantil
└── Tabla 13: Kemeny-Young - Bienestar Estudiantil

Sección 4.4.2 (Distancias Respecto a Rankings Individuales)
├── Tabla 14: Kendall Tau promedio por escenario
├── Tabla 15: Spearman promedio por escenario
├── Tabla 16: Footrule promedio por escenario
└── Tabla 17: Resumen comparativo de métodos
```

---

## Mensajes Clave para tu Reporte

### Para 4.4.1 - Convergencia de Métodos
*"Los tres métodos de agregación (Borda, Schulze y Kemeny-Young) convergen completamente en los ganadores de cada escenario, lo que refuerza la validez y robustez de los resultados obtenidos."*

**Ganadores por Escenario:**
- **Desarrollo Profesional**: Ferias de Empleo y Prácticas Especializadas
- **Infraestructura Académica**: Renovación de laboratorios especializados
- **Bienestar Estudiantil**: Programas deportivos y recreativos

### Para 4.4.2 - Representatividad
*"Las distancias promedio entre los rankings grupales y los 54 rankings individuales indican alta representatividad. Con Kendall Tau promedio de ~0.41 (59% de concordancia), Spearman de ~0.65, y Footrule de ~13 (de un máximo de 28), los métodos capturan efectivamente las preferencias agregadas del grupo respetando la diversidad individual de opiniones."*

**Mejor Desempeño**: El método Schulze muestra las menores distancias promedio en 2 de 3 métricas (Kendall Tau=0.4071, Spearman=0.6499).

---

## Información Técnica del Análisis

- **Respuestas Analizadas**: 54 estudiantes (sin filtros)
- **Métodos de Agregación**: Borda Count, Schulze, Kemeny-Young
- **Escenarios Evaluados**: 3 (Desarrollo Profesional, Infraestructura Académica, Bienestar Estudiantil)
- **Alternativas por Escenario**: 7
- **Métricas de Distancia**: Kendall Tau, Spearman (ρ), Footrule
- **Cálculo de Distancias**: Promedio de distancias entre ranking grupal y cada uno de los 54 rankings individuales
- **Fecha de Análisis**: Diciembre 2025

---

## Soporte Técnico

Si necesitas modificar el análisis:
- **Regenerar con filtros**: Edita `main.py` y ejecuta con filtros específicos (semestre, género, etc.)
- **Ajustar visualizaciones**: Modifica colores, tamaños de fuente en las secciones de `matplotlib`
- **Recalcular distancias**: Los scripts están en `main.py` listos para ejecutar
- **Cambiar formato de salida**: Exporta a CSV, JSON, o diferentes formatos de imagen

**Código fuente**: Todo disponible en `main.py` con comentarios detallados

---

**Generado por**: Sistema de Análisis de Rankings
**Última actualización**: 7 de diciembre de 2025
