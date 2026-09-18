"""
main.py
Ejecuta GBFS y A* sobre el mismo escenario y compara:

- Camino encontrado.
- Costo total.
- Nodos expandidos.
- Máximo de nodos en frontera.
- Tiempo de ejecución.

Además muestra visualmente las rutas y los nodos explorados.
"""

from time import perf_counter
from mapa import INICIO, METAS, dibujar_escenario
from algoritmos import gbfs, a_estrella


def ejecutar_con_tiempo(funcion):
    """Ejecuta un algoritmo y mide su tiempo de ejecución."""
    inicio = perf_counter()
    resultado = funcion()
    fin = perf_counter()

    resultado["tiempo_ms"] = (fin - inicio) * 1000
    return resultado


def formato_ruta(ruta):
    """Convierte una lista de coordenadas en texto."""
    if ruta is None:
        return "No se encontró una ruta"

    return " -> ".join(f"({f},{c})" for f, c in ruta)


def imprimir_resultado(resultado):
    print("\n" + "=" * 65)
    print(resultado["algoritmo"])
    print("=" * 65)
    print("Camino encontrado :", formato_ruta(resultado["ruta"]))
    print("Costo total       :", resultado["costo"])
    print("Nodos expandidos  :", resultado["nodos_expandidos"])
    print("Máx. frontera     :", resultado["nodos_en_frontera"])
    print("Tiempo de ejecución: %.6f ms" % resultado["tiempo_ms"])


def main():
    print("=" * 65)
    print("RUTA DE BARCO ENTRE PUERTOS")
    print("Búsqueda informada: GBFS vs A*")
    print("=" * 65)
    print(f"Estado inicial: {INICIO}")
    print(f"Estado(s) meta: {METAS}")
    print("\nAcciones: arriba, abajo, izquierda, derecha")
    print("Costo de cada movimiento: 1")
    print("Heurística: distancia Manhattan")

    # Los dos algoritmos se ejecutan sobre exactamente el mismo mapa.
    resultado_gbfs = ejecutar_con_tiempo(gbfs)
    resultado_astar = ejecutar_con_tiempo(a_estrella)

    imprimir_resultado(resultado_gbfs)
    imprimir_resultado(resultado_astar)

    # Tabla comparativa.
    print("\n" + "=" * 95)
    print("TABLA COMPARATIVA")
    print("=" * 95)

    encabezado = (
        f"{'Algoritmo':<28}"
        f"{'Costo':>10}"
        f"{'Expandidos':>15}"
        f"{'Máx. frontera':>18}"
        f"{'Tiempo (ms)':>15}"
    )
    print(encabezado)
    print("-" * 95)

    for resultado in (resultado_gbfs, resultado_astar):
        print(
            f"{resultado['algoritmo']:<28}"
            f"{resultado['costo']:>10}"
            f"{resultado['nodos_expandidos']:>15}"
            f"{resultado['nodos_en_frontera']:>18}"
            f"{resultado['tiempo_ms']:>15.6f}"
        )

    print("-" * 95)

    # La comparación de costos se muestra como dato, sin asumir
    # de antemano que GBFS o A* tendrán necesariamente rutas diferentes.
    if (
        resultado_gbfs["ruta"] is not None
        and resultado_astar["ruta"] is not None
    ):
        print("\nComparación de caminos:")
        print("GBFS:", formato_ruta(resultado_gbfs["ruta"]))
        print("A*  :", formato_ruta(resultado_astar["ruta"]))

        if resultado_gbfs["costo"] == resultado_astar["costo"]:
            print("\nAmbos encontraron una ruta con el mismo costo.")
        else:
            print(
                "\nLos costos encontrados son diferentes. "
                "A* utiliza g(n) + h(n), mientras GBFS utiliza solo h(n)."
            )

    # Visualización final.
    dibujar_escenario(
        ruta_gbfs=resultado_gbfs["ruta"],
        ruta_astar=resultado_astar["ruta"],
        explorados_gbfs=resultado_gbfs["explorados"],
        explorados_astar=resultado_astar["explorados"],
        titulo="Comparación visual: GBFS vs A*",
    )


if __name__ == "__main__":
    main()
