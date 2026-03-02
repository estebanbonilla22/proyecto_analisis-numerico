from __future__ import annotations

from typing import Callable, Dict, List
import time


def metodo_secante(
    f: Callable[[float], float],
    x0: float,
    x1: float,
    tolerancia: float,
    max_iter: int
) -> Dict:
    """Método de la secante para f(x)=0.

    Criterios de parada:
    - |x_{n+1} - x_n| < tolerancia
    - o máximo de iteraciones

    Valida f(x_n) - f(x_{n-1}) != 0.
    """
    inicio = time.time()
    tabla: List[Dict] = []

    x_prev = x0
    x_curr = x1

    convergio = False
    mensaje = "Máximo de iteraciones alcanzado."
    evals_f = 0

    f_prev = f(x_prev); evals_f += 1
    f_curr = f(x_curr); evals_f += 1

    for n in range(1, max_iter + 1):
        denom = (f_curr - f_prev)
        if denom == 0:
            mensaje = "Fallo: f(x_n) - f(x_{n-1}) = 0 (división por cero)."
            break

        x_next = x_curr - f_curr * (x_curr - x_prev) / denom
        err_abs = abs(x_next - x_curr)

        tabla.append({
            "n": n,
            "x_prev": x_prev,
            "x_curr": x_curr,
            "f_prev": f_prev,
            "f_curr": f_curr,
            "x_next": x_next,
            "error_abs": err_abs
        })

        if err_abs < tolerancia:
            convergio = True
            mensaje = "Convergencia alcanzada por tolerancia."
            x_curr = x_next
            break

        # shift
        x_prev, f_prev = x_curr, f_curr
        x_curr = x_next
        f_curr = f(x_curr); evals_f += 1

    fin = time.time()
    raiz = x_curr
    error_final = tabla[-1]["error_abs"] if tabla else float("inf")

    return {
        "metodo": "Secante",
        "raiz": raiz,
        "iteraciones": len(tabla),
        "error_final": error_final,
        "tiempo": fin - inicio,
        "convergio": convergio,
        "mensaje": mensaje,
        "tabla": tabla,
        "evals_f": evals_f
    }
