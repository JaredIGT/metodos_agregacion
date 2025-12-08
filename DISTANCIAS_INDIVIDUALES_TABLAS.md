# SECCIÓN 4.4.2: DISTANCIAS RESPECTO A RANKINGS INDIVIDUALES

## Introducción

Esta sección presenta el análisis de **representatividad** de los rankings grupales generados por cada método de agregación. Se calculó la distancia promedio entre el ranking grupal de cada método y los **54 rankings individuales** proporcionados por los estudiantes.

Un valor de distancia **más bajo** indica que el ranking grupal **representa mejor** las preferencias del grupo, minimizando las discrepancias con las opiniones individuales.

Se utilizaron tres métricas de distancia:
- **Kendall Tau**: Mide la proporción de pares discordantes entre rankings
- **Spearman**: Correlación basada en diferencias de posiciones al cuadrado
- **Footrule**: Suma de diferencias absolutas de posiciones

---

## Tabla 14: Distancia Promedio Kendall Tau

**Descripción**: Promedio de distancias Kendall Tau entre el ranking grupal de cada método y los 54 rankings individuales.

| Escenario | Borda | Schulze | Kemeny-Young |
|-----------|-------|---------|--------------|
| Desarrollo Profesional | 0.4444 | 0.4356 | 0.4356 |
| Infraestructura Académica | 0.3898 | 0.3898 | 0.3898 |
| Bienestar Estudiantil | 0.3977 | 0.3959 | 0.3959 |
| **PROMEDIO GENERAL** | **0.4106** | **0.4071** | **0.4071** |

**Interpretación**: 
- **Infraestructura Académica** muestra el mayor consenso grupal (0.3898), con todos los métodos convergiendo al mismo resultado
- **Schulze** y **Kemeny-Young** tienen desempeño prácticamente idéntico en todos los escenarios
- **Borda** muestra ligera mayor distancia en Desarrollo Profesional (0.4444 vs 0.4356)
- Los valores moderados (0.39-0.44) indican diversidad razonable de opiniones individuales

---

## Tabla 15: Distancia Promedio Spearman

**Descripción**: Promedio de distancias Spearman entre el ranking grupal de cada método y los 54 rankings individuales.

| Escenario | Borda | Schulze | Kemeny-Young |
|-----------|-------|---------|--------------|
| Desarrollo Profesional | 0.7560 | 0.7480 | 0.7480 |
| Infraestructura Académica | 0.5985 | 0.5985 | 0.5985 |
| Bienestar Estudiantil | 0.6164 | 0.6032 | 0.6124 |
| **PROMEDIO GENERAL** | **0.6570** | **0.6499** | **0.6530** |

**Interpretación**: 
- **Schulze** muestra la menor distancia promedio general (0.6499), sugiriendo mejor ajuste a las preferencias individuales
- **Desarrollo Profesional** presenta mayor variabilidad (0.75), indicando opiniones más heterogéneas
- **Infraestructura Académica** mantiene el mayor consenso con Spearman=0.5985
- En Bienestar Estudiantil, Schulze aventaja a Borda (0.6032 vs 0.6164)

---

## Tabla 16: Distancia Promedio Footrule

**Descripción**: Promedio de distancias Footrule entre el ranking grupal de cada método y los 54 rankings individuales. Mide la suma de desplazamientos absolutos en posiciones.

| Escenario | Borda | Schulze | Kemeny-Young |
|-----------|-------|---------|--------------|
| Desarrollo Profesional | 14.04 | 14.11 | 14.11 |
| Infraestructura Académica | 12.74 | 12.74 | 12.74 |
| Bienestar Estudiantil | 13.00 | 12.89 | 12.93 |
| **PROMEDIO GENERAL** | **13.26** | **13.25** | **13.26** |

**Interpretación**: 
- **Infraestructura Académica** presenta el menor desplazamiento promedio (12.74), confirmando alto consenso
- **Schulze** alcanza el mejor desempeño general con 13.25 (vs 13.26 de Borda y Kemeny-Young)
- En Bienestar Estudiantil, Schulze muestra ventaja clara (12.89 vs 13.00 de Borda)
- Los valores cercanos entre métodos indican que todos producen rankings representativos

---

## Tabla 17: Resumen Comparativo de Métodos

**Descripción**: Promedio de distancias consolidado para los 3 escenarios (162 comparaciones totales: 3 escenarios × 54 participantes).

| Método | Kendall Tau | Spearman | Footrule |
|--------|-------------|----------|----------|
| Borda | 0.4106 | 0.6570 | 13.26 |
| Schulze | **0.4071** | **0.6499** | **13.25** |
| Kemeny-Young | **0.4071** | 0.6530 | 13.26 |

**Interpretación General**:
- **Schulze** obtiene el mejor desempeño en 2 de 3 métricas (Kendall Tau y Spearman)
- **Kemeny-Young** empata con Schulze en Kendall Tau
- Las diferencias son mínimas (< 1.1%), indicando que los tres métodos son **altamente representativos**
- La convergencia entre métodos valida la robustez del análisis

---

## Figuras de Distancias Respecto a Rankings Individuales

### Figura 8: Distancia Kendall Tau por Escenario
*[Insertar figura_kendall_individuales.png]*

**Descripción**: Comparación de distancias Kendall Tau promedio entre los rankings grupales de cada método y los 54 rankings individuales, desglosado por escenario.

---

### Figura 9: Distancia Spearman por Escenario
*[Insertar figura_spearman_individuales.png]*

**Descripción**: Comparación de distancias Spearman promedio entre los rankings grupales de cada método y los 54 rankings individuales, desglosado por escenario.

---

### Figura 10: Distancia Footrule por Escenario
*[Insertar figura_footrule_individuales.png]*

**Descripción**: Comparación de distancias Footrule promedio (suma de desplazamientos absolutos) entre los rankings grupales y los 54 rankings individuales, desglosado por escenario.

---

### Figura 11: Comparativa General de Métodos
*[Insertar figura_comparativa_individuales.png]*

**Descripción**: Vista consolidada del desempeño de cada método de agregación a través de las tres métricas de distancia, promediando los 3 escenarios. Nota: Footrule se divide entre 20 para facilitar la visualización comparativa.

---

## Conclusiones

1. **Representatividad Alta**: Las distancias moderadas (Kendall Tau ~0.40, Footrule ~13) indican que los rankings grupales capturan bien la tendencia general, respetando la diversidad de opiniones.

2. **Convergencia de Métodos**: Schulze y Kemeny-Young producen resultados prácticamente idénticos, mientras que Borda presenta diferencias mínimas.

3. **Mejor Desempeño**: Schulze muestra ventaja marginal en términos de minimizar distancias respecto a rankings individuales.

4. **Consenso por Escenario**: 
   - **Infraestructura Académica**: Mayor consenso grupal (distancias más bajas)
   - **Desarrollo Profesional**: Mayor heterogeneidad de preferencias
   - **Bienestar Estudiantil**: Consenso intermedio

5. **Validación de Resultados**: La consistencia entre los tres métodos de agregación y las tres métricas de distancia valida la robustez del análisis y los rankings grupales generados.
