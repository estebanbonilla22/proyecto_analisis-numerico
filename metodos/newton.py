from __future__ import annotations

from typing import Callable, Dict, List
import time


def metodo_newton_raphson(
    f: Callable[[float], float],
    df: Callable[[float], float],
    x0: float,
    tolerancia: float,
    max_iter: int
) -> Dict:
    """Newton-Raphson para f(x)=0.

    Criterios de parada:
    - |x_{n+1} - x_n| < tolerancia
    - |f(x_n)| < tolerancia
    - o máximo de iteraciones

    Valida df(x_n) != 0 en cada iteración.
    """
    inicio = time.time()
    tabla: List[Dict] = []

    x_prev = x0
    convergio = False
    mensaje = "Máximo de iteraciones alcanzado."

    evals_f = 0
    evals_df = 0

    for n in range(1, max_iter + 1):
        fx = f(x_prev); evals_f += 1
        dfx = df(x_prev); evals_df += 1

        if dfx == 0:
            mensaje = "Fallo: f'(x_n) = 0 (división por cero)."
            break

        x_next = x_prev - fx / dfx
        err_abs = abs(x_next - x_prev)
        err_rel = err_abs / abs(x_next) if x_next != 0 else float("inf")

        tabla.append({
            "n": n,
            "x_n": x_prev,
            "f_xn": fx,
            "df_xn": dfx,
            "x_next": x_next,
            "error_abs": err_abs,
            "error_rel": err_rel
        })

        if abs(fx) < tolerancia or err_abs < tolerancia:
            convergio = True
            mensaje = "Convergencia alcanzada por tolerancia."
            x_prev = x_next
            break

        x_prev = x_next

    fin = time.time()
    raiz = x_prev
    error_final = tabla[-1]["error_abs"] if tabla else float("inf")

    return {
        "metodo": "Newton-Raphson",
        "raiz": raiz,
        "iteraciones": len(tabla),
        "error_final": error_final,
        "tiempo": fin - inicio,
        "convergio": convergio,
        "mensaje": mensaje,
        "tabla": tabla,
        "evals_f": evals_f,
        "evals_df": evals_df
    }
