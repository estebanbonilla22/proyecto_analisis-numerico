from typing import Callable, Dict, List
import time


def metodo_falsa_posicion(
    f: Callable[[float], float],
    a: float,
    b: float,
    tolerancia: float,
    max_iter: int
) -> Dict:
    """
    False Position (Regula Falsi) for f(x)=0 on [a,b].

    c = b - f(b)*(b-a)/(f(b)-f(a))

    Stops by tolerance on |f(c)| or absolute step error.
    Handles division by zero if f(b) == f(a).
    """
    inicio = time.time()
    tabla: List[Dict] = []
    c_prev = None

    fa = f(a)
    fb = f(b)

    for n in range(1, max_iter + 1):
        denom = (fb - fa)
        if denom == 0:
            raise ZeroDivisionError("Division by zero: f(b) - f(a) = 0 in False Position.")

        c = b - fb * (b - a) / denom
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

        if abs(fc) < tolerancia or (c_prev is not None and err_abs < tolerancia):
            break

        # update interval keeping the sign change
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

        c_prev = c

    fin = time.time()
    return {
        "metodo": "Falsa Posición",
        "raiz": c,
        "iteraciones": n,
        "error_final": tabla[-1]["error_abs"],
        "tiempo": fin - inicio,
        "tabla": tabla
    }