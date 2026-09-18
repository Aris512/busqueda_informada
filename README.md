# 🚢 Ruta de Barco entre Puertos: Búsqueda Informada (GBFS vs. A*)

Este proyecto implementa y compara dos algoritmos clásicos de búsqueda informada en Inteligencia Artificial: **Greedy Best-First Search (GBFS)** y **A\*** (A estrella).

El escenario modela la navegación de un barco que debe zarpar desde un puerto inicial hasta un puerto meta a través de una cuadrícula marítima, esquivando zonas de tormenta (obstáculos) y minimizando el costo del trayecto.

---

## 📋 Tabla de Contenidos
1. [Características del Proyecto](#-características-del-proyecto)
2. [Estructura del Repositorio](#-estructura-del-repositorio)
3. [Requisitos Previos](#-requisitos-previos)
4. [Instalación y Configuración](#-instalación-y-configuración)
5. [Uso y Ejecución](#-uso-y-ejecución)
6. [Formulación del Problema](#-formulación-del-problema)
7. [Métricas Comparativas](#-métricas-comparativas)

---

## ✨ Características del Proyecto

- **Algoritmos implementados**:
  - **GBFS (Greedy Best-First Search)**: Utiliza únicamente la función heurística $f(n) = h(n)$ para guiar la búsqueda de forma voraz.
  - **A\***: Utiliza la función de evaluación $f(n) = g(n) + h(n)$, combinando el costo acumulado real con la estimación heurística.
- **Heurística implementada**: Distancia Manhattan, la cual es **admisible** y **consistente** para movimientos ortogonales en cuadrícula con costo unitario.
- **Visualización Gráfica**: Interfaz interactiva mediante **Matplotlib** que ilustra:
  - Cuadrícula con mar navegable y celdas bloqueadas por tormenta.
  - Nodos explorados/expandidos por cada algoritmo.
  - Trayectoria final trazada por cada estrategia.
  - Puertos de inicio y destino.
- **Reporte y Métricas en Consola**: Tabla comparativa con costo, nodos expandidos, tamaño máximo de la frontera y tiempo de ejecución en milisegundos.

---

## 📁 Estructura del Repositorio

```text
busqueda_informada/
├── algoritmos.py       # Lógica de búsqueda (GBFS, A*), transiciones y heurística
├── mapa.py             # Definición de la matriz, inicio/meta y visualización con Matplotlib
├── main.py             # Script principal: ejecuta algoritmos, genera métricas y gráfico
├── requirements.txt    # Dependencias del proyecto (matplotlib)
├── .gitignore          # Reglas de exclusión para Git (archivos temporales, venv, pycache)
└── README.md           # Documentación e instrucciones de instalación
```

---

## ⚙️ Requisitos Previos

- **Python**: Versión 3.8 o superior (probado con Python 3.10+ y 3.13).
- **Gestor de paquetes `pip`** actualizado.

---

## 🚀 Instalación y Configuración

Sigue estos pasos para configurar el entorno y ejecutar el proyecto:

### 1. Clonar o descargar el repositorio
Si utilizas Git:
```bash
git clone <URL_DEL_REPOSITORIO>
cd busqueda_informada
```
O simplemente abre una terminal en la carpeta raíz del proyecto.


---

### 2. Instalar las dependencias

Con el entorno virtual activado (o directamente en tu instalación global de Python), instala las librerías necesarias ejecutando:

```bash
pip install -r requirements.txt
```

> **Nota:** La dependencia principal es `matplotlib>=3.7`.

---

## 3. Uso y Ejecución

Para iniciar la simulación y generar la comparativa, ejecuta el script principal:

```bash
python main.py
```

### Salida esperada:
1. **En la consola:**
   - Detalle de la ejecución de GBFS (camino, costo, nodos expandidos, frontera, tiempo).
   - Detalle de la ejecución de A*.
   - Tabla comparativa resumen con ambos algoritmos.
2. **En ventana gráfica (Matplotlib):**
   - Se abrirá una ventana con el mapa navegable, identificando con colores y marcadores el punto de partida, la meta, las zonas de tormenta, los nodos expandidos por GBFS y A*, y el camino final calculado por cada uno.

---

##  Formulación del Problema

- **Espacio de Estados**: Coordenadas `(fila, columna)` dentro de la cuadrícula marítima.
- **Estado Inicial**: Coordenada del puerto de salida (`(10, 1)`).
- **Estado(s) Meta**: Coordenada del puerto de llegada (`(1, 16)`).
- **Acciones / Operadores**: Moverse en 4 direcciones ortogonales (Arriba, Abajo, Izquierda, Derecha).
- **Función de Costo**: Cada movimiento tiene un costo uniforme de $c = 1$.
- **Heurística**: Distancia Manhattan:
  $$h(n) = |\text{fila}_n - \text{fila}_{\text{meta}}| + |\text{columna}_n - \text{columna}_{\text{meta}}|$$
  Dado que cada paso cuesta 1 y no existen movimientos diagonales, $h(n)$ nunca sobreestima el costo real restante, asegurando que A* sea admisible y óptimo.

---

##  Métricas Comparativas

Al ejecutar el programa se evalúan:
- **Costo total**: Suma del costo de las acciones del camino solución.
- **Nodos expandidos**: Cantidad de estados retirados de la frontera para generar sus sucesores.
- **Máximo de nodos en frontera**: Medida de consumo de memoria del algoritmo en su punto máximo.
- **Tiempo de ejecución (ms)**: Tiempo total que toma la búsqueda en completarse.
