"""
ESCENARIO:
Un barco debe navegar desde un puerto inicial hasta un puerto meta,
evitando zonas de tormenta.

La heurística es:
    h(n) = |fila_n - fila_meta| + |columna_n - columna_meta|


También es consistente:
    h(n) <= costo(n,n') + h(n')

para cualquier movimiento permitido n -> n'. Por lo tanto, para A*,
la heurística permite mantener la propiedad de optimalidad bajo este
modelo de costos positivos.
"""

from heapq import heappush, heappop
from math import inf
from mapa import crear_mapa, INICIO, METAS


# Acciones/operadores.
MOVIMIENTOS = [
    (-1, 0),  # arriba
    (1, 0),   # abajo
    (0, -1),  # izquierda
    (0, 1),   # derecha
]


def dentro_del_mapa(estado, mapa):
    """Comprueba si una coordenada pertenece a la cuadrícula."""
    fila, columna = estado
    return (
        0 <= fila < len(mapa)
        and 0 <= columna < len(mapa[0])
    )


def transiciones(estado, mapa):
    """
    Devuelve los estados vecinos alcanzables y el costo de cada acción.

    Una celda con valor 1 corresponde a una tormenta y no puede ser
    atravesada.
    """
    fila, columna = estado
    vecinos = []

    for df, dc in MOVIMIENTOS:
        siguiente = (fila + df, columna + dc)

        if dentro_del_mapa(siguiente, mapa):
            f, c = siguiente

            # 1 significa zona de tormenta.
            if mapa[f][c] == 0:
                # Cada movimiento cuesta 1.
                vecinos.append((siguiente, 1))

    return vecinos


def heuristica(estado, metas=METAS):
    """
    h(n): distancia Manhattan hasta la meta más cercana.

    Como solamente hay movimientos ortogonales y cada paso cuesta 1,
    esta heurística nunca sobreestima el costo real restante.
    """
    fila, columna = estado

    return min(
        abs(fila - meta[0]) + abs(columna - meta[1])
        for meta in metas
    )


def reconstruir_ruta(came_from, estado_final):
    """Reconstruye la ruta desde la meta hasta el inicio."""
    ruta = [estado_final]

    while ruta[-1] in came_from:
        ruta.append(came_from[ruta[-1]])

    ruta.reverse()
    return ruta


def costo_ruta(ruta):
    """En este escenario cada movimiento cuesta 1."""
    if not ruta:
        return inf
    return len(ruta) - 1


def gbfs(inicio=INICIO, metas=METAS):
    """
    Greedy Best-First Search. Función de evaluación: f(n) = h(n)
    """
    mapa = crear_mapa()
    # (prioridad, contador, estado)
    # El contador evita problemas de desempate entre coordenadas.
    "lista de estado qeu estan pendientes a explorar"
    frontera = [] 
    contador = 0
    "agregamos el estado inicial"
    heappush(frontera, (heuristica(inicio, metas), contador, inicio))

    came_from = {}
    visitados = set()
    expandidos = []
    max_frontera = 1

    while frontera:
        "se extare el que posee menor prioridad h(n)"
        _, _, actual = heappop(frontera)


        if actual in visitados:
            continue

        "el nodo se considera expandido al retirarlo de la frontera"
        visitados.add(actual)
        expandidos.append(actual)
        "si el estado actual es la meta, se reconstruye la ruta."
        if actual in metas:
            ruta = reconstruir_ruta(came_from, actual)
            return {
                "algoritmo": "Greedy Best-First Search",
                "ruta": ruta,
                "costo": costo_ruta(ruta),
                "nodos_expandidos": len(expandidos),
                "nodos_en_frontera": max_frontera,
                "frontera_final": len(frontera),
                "explorados": expandidos,
            }
        "expandir los vecinos, se entregan vecinos validos por el metodo de transiciones"
        for vecino, _ in transiciones(actual, mapa):

            "sino esta dentro de la lista de los visitados ni tampoco de came_from, se agrega + de donde proviene"
            if vecino not in visitados and vecino not in came_from:
                came_from[vecino] = actual
                contador += 1

                # GBFS solamente usa h(n).
                prioridad = heuristica(vecino, metas)
                heappush(frontera, (prioridad, contador, vecino))

        max_frontera = max(max_frontera, len(frontera))

    return {
        "algoritmo": "Greedy Best-First Search",
        "ruta": None,
        "costo": inf,
        "nodos_expandidos": len(expandidos),
        "nodos_en_frontera": max_frontera,
        "frontera_final": len(frontera),
        "explorados": expandidos,
    }


def a_estrella(inicio=INICIO, metas=METAS):
    """Función:f(n) = g(n) + h(n)  g(n): costo real acumulado desde el inicio y  h(n): estimación del costo restante.
    """
    mapa = crear_mapa()

    frontera = []
    contador = 0
    "incio tiene un costo acumulado 0"
    g_score = {inicio: 0}
    came_from = {}
    "agregamos el estado inicial"
    f_inicial = heuristica(inicio, metas)
    heappush(frontera, (f_inicial, contador, inicio))

    expandidos = []
    cerrados = set()
    max_frontera = 1

    while frontera:
        "se extrae el menor valor de f(n)"
        _, _, actual = heappop(frontera)

        if actual in cerrados:
            continue

        # Con heurística consistente, cuando A* extrae el nodo
        # podemos cerrarlo sin necesidad de reabrirlo.
        cerrados.add(actual)
        expandidos.append(actual)

        if actual in metas:
            ruta = reconstruir_ruta(came_from, actual)
            return {
                "algoritmo": "A*",
                "ruta": ruta,
                "costo": g_score[actual],
                "nodos_expandidos": len(expandidos),
                "nodos_en_frontera": max_frontera,
                "frontera_final": len(frontera),
                "explorados": expandidos,
            }
        
        "se calcula el costo de cada vecino"
        for vecino, costo in transiciones(actual, mapa):
            if vecino in cerrados:
                continue

            costo_tentativo = g_score[actual] + costo

            "solo actualizamos si se encuentram una ruta más barata"
            if costo_tentativo < g_score.get(vecino, inf):
                came_from[vecino] = actual
                g_score[vecino] = costo_tentativo
                "utiliza el g(n) + h(n) para el calculo de prioridad de un vecino"
                f_score = costo_tentativo + heuristica(vecino, metas)

                contador += 1
                "lo agregamos a frontera para luego ser explorado"
                heappush(
                    frontera,
                    (f_score, contador, vecino)
                )

        max_frontera = max(max_frontera, len(frontera))

    return {
        "algoritmo": "A*",
        "ruta": None,
        "costo": inf,
        "nodos_expandidos": len(expandidos),
        "nodos_en_frontera": max_frontera,
        "frontera_final": len(frontera),
        "explorados": expandidos,
    }
