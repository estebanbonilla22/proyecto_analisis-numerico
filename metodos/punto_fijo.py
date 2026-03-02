from __future__ import annotations

from typing import Callable, Dict, List
import time


def iteracion_punto_fijo(
    g: Callable[[float], float],
    x0: float,
    tolerancia: float,
    max_iter: int,
    limite_divergencia: float = 1e6
) -> Dict:
    """Iteración de punto fijo para x = g(x).

    Criterios de parada:
    - |x_{n+1} - x_n| < tolerancia
    - o máximo de iteraciones

    Además, detecta divergencia si |x_n| supera un límite.
    """
    inicio = time.time()

    tabla: List[Dict] = []
    x_prev = x0
    convergio = False
    mensaje = "Máximo de iteraciones alcanzado."

    for n in range(1, max_iter + 1):
        gx = g(x_prev)
        diff = abs(gx - x_prev)
        err_rel = diff / abs(gx) if gx != 0 else float("inf")

        tabla.append({
            "n": n,
            "x_n": x_prev,
            "g_xn": gx,
            "diff": diff,
            "error_rel": err_rel
        })

        if diff < tolerancia:
            convergio = True
            mensaje = "Convergencia alcanzada por tolerancia."
            x_prev = gx
            break

        x_prev = gx

        if abs(x_prev) > limite_divergencia:
            convergio = False
            mensaje = "Divergencia detectada: |x_n| excede el límite."
            break

    fin = time.time()
    raiz = x_prev

    error_final = tabla[-1]["diff"] if tabla else float("inf")
    return {
        "metodo": "Punto Fijo",
        "raiz": raiz,
        "iteraciones": len(tabla),
        "error_final": error_final,
        "tiempo": fin - inicio,
        "convergio": convergio,
        "mensaje": mensaje,
        "tabla": tabla,
        "evals_f": len(tabla)  # evaluaciones de g
    }
