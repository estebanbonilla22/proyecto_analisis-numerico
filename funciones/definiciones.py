import numpy as np


def funcion(lambda_val: float) -> float:
    """
    Función original del problema.
    """
    return 2.5 + 0.8 * lambda_val**2 - 3.2 * lambda_val + np.log(lambda_val + 1)


def derivada(lambda_val: float) -> float:
    """
    Derivada de la función.
    Se usa para encontrar el mínimo (f'(λ)=0).
    """
    return 1.6 * lambda_val - 3.2 + 1 / (lambda_val + 1)