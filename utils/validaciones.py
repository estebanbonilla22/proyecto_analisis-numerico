def validar_intervalo(f, a: float, b: float) -> None:
    """
    Valida que el intervalo tenga cambio de signo.
    """
    if f(a) * f(b) > 0:
        raise ValueError("El intervalo no contiene una raíz (no hay cambio de signo).")