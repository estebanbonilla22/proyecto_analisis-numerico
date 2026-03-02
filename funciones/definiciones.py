import numpy as np

# ====== EJERCICIO 1 ======
def funcion_t(lambda_val: float) -> float:
    """T(λ) = 2.5 + 0.8λ² - 3.2λ + ln(λ + 1)"""
    return 2.5 + 0.8 * lambda_val**2 - 3.2 * lambda_val + np.log(lambda_val + 1)


def derivada_t(lambda_val: float) -> float:
    """T'(λ) = 1.6λ - 3.2 + 1/(λ+1)"""
    return 1.6 * lambda_val - 3.2 + 1 / (lambda_val + 1)


# ====== EJERCICIO 2 ======
def eficiencia_e(x: float) -> float:
    """E(x) = x^3 - 6x^2 + 11x - 6.5"""
    return x**3 - 6 * x**2 + 11 * x - 6.5


# ====== EJERCICIO 3 ======
def g_crecimiento_bd(x: float) -> float:
    """g(x) = 0.5 cos(x) + 1.5"""
    return 0.5 * np.cos(x) + 1.5


def g_crecimiento_bd_derivada(x: float) -> float:
    """g'(x) = -0.5 sin(x)"""
    return -0.5 * np.sin(x)


# ====== EJERCICIO 4 ======
def tiempo_threads(n: float) -> float:
    """T(n) = n^3 - 8n^2 + 20n - 16"""
    return n**3 - 8 * n**2 + 20 * n - 16


def tiempo_threads_derivada(n: float) -> float:
    """T'(n) = 3n^2 - 16n + 20"""
    return 3 * n**2 - 16 * n + 20


# ====== EJERCICIO 5 ======
def modelo_financiero_p(x: float) -> float:
    """P(x) = x e^(-x/2) - 0.3"""
    return x * np.exp(-x / 2.0) - 0.3


def modelo_financiero_p_derivada(x: float) -> float:
    """P'(x) = e^(-x/2) (1 - x/2)"""
    return np.exp(-x / 2.0) * (1 - x / 2.0)