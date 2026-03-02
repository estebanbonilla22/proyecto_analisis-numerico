from typing import Callable, Dict, List
import time


def metodo_biseccion(
    f: Callable[[float], float],
    a: float,
    b: float,
    tolerancia: float,
    max_iter: int
) -> Dict:
    """
    Bisection method for f(x)=0 on [a,b].
    Stops by tolerance on |f(c)| or absolute step error.
    """
    inicio = time.time()
    tabla: List[Dict] = []
    c_prev = None

    fa = f(a)
    fb = f(b)

    for n in range(1, max_iter + 1):
        c = (a + b) / 2.0
        fc = f(c)

        if c_prev is None:
            err_abs = 0.0
            err_rel = 0.0
        else:
            err_abs = abs(c - c_prev)
            err_rel = err_abs / abs(c) if c != 0 else float("inf")

        tabla.append({
            "n": n, "a": a, "b": b, "c": c, "f_c": fc,
            "error_abs": err_abs, "error_rel": err_rel
        })

        # stop criteria
        if abs(fc) < tolerancia or (c_prev is not None and err_abs < tolerancia):
            break

        # interval update
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

        c_prev = c

    fin = time.time()
    return {
        "metodo": "Bisección",
        "raiz": c,
        "iteraciones": n,
        "error_final": tabla[-1]["error_abs"],
        "tiempo": fin - inicio,
        "tabla": tabla
    }