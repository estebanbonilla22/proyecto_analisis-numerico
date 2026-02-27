import numpy as np


# ====== EXERCISE 1 (optional, if you keep it) ======
def funcion_t(lambda_val: float) -> float:
    """T(λ) = 2.5 + 0.8λ² - 3.2λ + ln(λ + 1)"""
    return 2.5 + 0.8 * lambda_val**2 - 3.2 * lambda_val + np.log(lambda_val + 1)


def derivada_t(lambda_val: float) -> float:
    """Derivative: T'(λ) = 1.6λ - 3.2 + 1/(λ+1)"""
    return 1.6 * lambda_val - 3.2 + 1 / (lambda_val + 1)


# ====== EXERCISE 2 ======
def eficiencia_e(x: float) -> float:
    """E(x) = x^3 - 6x^2 + 11x - 6.5"""
    return x**3 - 6 * x**2 + 11 * x - 6.5