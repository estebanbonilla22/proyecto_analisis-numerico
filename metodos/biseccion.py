from typing import Callable, List, Dict
import time


def metodo_biseccion(
    f: Callable[[float], float],
    a: float,
    b: float,
    tolerancia: float,
    max_iter: int
) -> Dict:
    """
    Implementación del método de bisección.
    """

    inicio = time.time()
    resultados: List[Dict] = []
    c_anterior = None

    for n in range(1, max_iter + 1):
        c = (a + b) / 2
        f_c = f(c)

        if c_anterior is not None:
            error_abs = abs(c - c_anterior)
            error_rel = error_abs / abs(c)
        else:
            error_abs = 0
            error_rel = 0

        resultados.append({
            "n": n,
            "a": a,
            "b": b,
            "c": c,
            "f_c": f_c,
            "error_abs": error_abs,
            "error_rel": error_rel
        })

        if abs(f_c) < tolerancia or error_abs < tolerancia:
            break

        if f(a) * f_c < 0:
            b = c
        else:
            a = c

        c_anterior = c

    fin = time.time()

    return {
        "raiz": c,
        "iteraciones": n,
        "error_final": error_abs,
        "tiempo": fin - inicio,
        "tabla": resultados
    }