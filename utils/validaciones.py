from typing import Callable


def validar_intervalo(f: Callable[[float], float], a: float, b: float) -> None:
    """Checks sign change f(a)*f(b) < 0."""
    fa = f(a)
    fb = f(b)
    if fa == 0 or fb == 0:
        return
    if fa * fb > 0:
        raise ValueError("Invalid interval: f(a) and f(b) must have opposite signs.")


def validar_numeros(a: float, b: float, tolerancia: float, max_iter: int) -> None:
    if tolerancia <= 0:
        raise ValueError("Tolerance must be > 0.")
    if max_iter <= 0:
        raise ValueError("Max iterations must be > 0.")
    if a >= b:
        raise ValueError("Interval must satisfy a < b.")