"""
mapa.py
Representación visual del escenario "Ruta de barco entre puertos evitando
zonas de tormenta".

Se utiliza matplotlib para mostrar:
- Mar navegable.
- Zonas de tormenta (celdas no transitables).
- Puerto de origen y puerto(s) meta.
- Nodos explorados por cada algoritmo.
- Ruta final encontrada.

El mapa se modela como una cuadrícula. Cada estado es una coordenada
(fila, columna).
"""

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


# Caracteres usados en la representación:
# 0 = mar navegable
# 1 = zona de tormenta (obstáculo)
# S = puerto inicial
# G = puerto meta
#
# El algoritmo trabaja internamente con coordenadas, por lo que S y G
# solamente sirven para visualizar el escenario.

MAPA = [
    "000000000000000000",
    "000001111100000000",
    "000001111100000000",
    "000001111100000000",
    "000001110000000000",
    "000001110011111000",
    "000000000011111000",
    "000111100011111000",
    "000111100000000000",
    "000111100000000000",
    "000000000000000000",
    "000000000000000000",
]

INICIO = (10, 1)
METAS = [(1, 16)]


def crear_mapa():
    """Convierte el mapa textual en una matriz de enteros."""
    return [[int(celda) for celda in fila] for fila in MAPA]


def dibujar_escenario(
    ruta_gbfs=None,
    ruta_astar=None,
    explorados_gbfs=None,
    explorados_astar=None,
    titulo="Ruta de barco entre puertos",
    mostrar=True,
):
    """
    Dibuja el escenario y, opcionalmente, las exploraciones y rutas.

    ruta_gbfs / ruta_astar:
        Listas de coordenadas [(fila, columna), ...].

    explorados_gbfs / explorados_astar:
        Conjuntos o listas de coordenadas expandidas.
    """
    matriz = crear_mapa()
    filas = len(matriz)
    columnas = len(matriz[0])

    fig, ax = plt.subplots(figsize=(14, 8))

    # Colormap simple:
    # 0 -> mar
    # 1 -> tormenta
    cmap = ListedColormap(["#dff3ff", "#e05a5a"])
    ax.imshow(matriz, cmap=cmap, vmin=0, vmax=1)

    # Dibujar exploración. Se hace primero para que las rutas queden encima.
    if explorados_gbfs:
        for fila, columna in explorados_gbfs:
            if (fila, columna) not in METAS and (fila, columna) != INICIO:
                ax.scatter(
                    columna, fila, s=95, marker="o",
                    facecolors="none", edgecolors="#2c7fb8",
                    linewidths=1.3, alpha=0.65
                )

    if explorados_astar:
        for fila, columna in explorados_astar:
            if (fila, columna) not in METAS and (fila, columna) != INICIO:
                ax.scatter(
                    columna, fila, s=48, marker="s",
                    facecolors="none", edgecolors="#8c4bb3",
                    linewidths=1.0, alpha=0.55
                )

    # Rutas finales.
    if ruta_gbfs:
        xs = [columna for fila, columna in ruta_gbfs]
        ys = [fila for fila, columna in ruta_gbfs]
        ax.plot(xs, ys, color="#2c7fb8", linewidth=3.5, marker="o", markersize=4.5,
                label="Ruta GBFS")

    if ruta_astar:
        xs = [columna for fila, columna in ruta_astar]
        ys = [fila for fila, columna in ruta_astar]
        ax.plot(xs, ys, color="#8c4bb3", linewidth=3.5, marker="s", markersize=4.0,
                label="Ruta A*")

    # Puerto inicial.
    ax.scatter(
        INICIO[1], INICIO[0], s=240, marker="o",
        facecolors="#2ca25f", edgecolors="black", linewidths=1.5,
        zorder=10
    )
    ax.text(
        INICIO[1], INICIO[0] - 0.55, "INICIO",
        ha="center", va="center", fontweight="bold", zorder=11
    )

    # Puertos meta.
    for meta in METAS:
        ax.scatter(
            meta[1], meta[0], s=260, marker="*",
            facecolors="#ffd92f", edgecolors="black", linewidths=1.5,
            zorder=10
        )
        ax.text(
            meta[1], meta[0] - 0.55, "META",
            ha="center", va="center", fontweight="bold", zorder=11
        )

    # Cuadrícula para distinguir estados.
    ax.set_xticks(range(columnas))
    ax.set_yticks(range(filas))
    ax.set_xticklabels(range(columnas))
    ax.set_yticklabels(range(filas))
    ax.grid(which="major", color="white", linewidth=1.0, alpha=0.75)

    ax.set_xlabel("Columna")
    ax.set_ylabel("Fila")
    ax.set_title(titulo, fontsize=15, fontweight="bold")

    elementos = [
        Patch(facecolor="#dff3ff", edgecolor="black", label="Mar navegable"),
        Patch(facecolor="#e05a5a", edgecolor="black", label="Zona de tormenta"),
        Line2D([0], [0], marker="o", color="#2c7fb8",
               markerfacecolor="none", linestyle="None",
               label="Nodos expandidos GBFS"),
        Line2D([0], [0], marker="s", color="#8c4bb3",
               markerfacecolor="none", linestyle="None",
               label="Nodos expandidos A*"),
        Line2D([0], [0], marker="o", color="black",
               markerfacecolor="#2ca25f", linestyle="None",
               markersize=9, label="Puerto inicial"),
        Line2D([0], [0], marker="*", color="black",
               markerfacecolor="#ffd92f", linestyle="None",
               markersize=11, label="Puerto meta"),
    ]

    if ruta_gbfs:
        elementos.append(Line2D([0], [0], color="#2c7fb8",
                                linewidth=3, label="Ruta GBFS"))
    if ruta_astar:
        elementos.append(Line2D([0], [0], color="#8c4bb3",
                                linewidth=3, label="Ruta A*"))

    ax.legend(handles=elementos, loc="upper center",
              bbox_to_anchor=(0.5, -0.09), ncol=3)

    plt.tight_layout()

    if mostrar:
        plt.show()

    return fig, ax
