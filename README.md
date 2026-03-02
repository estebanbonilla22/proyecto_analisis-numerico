# Optimización Hash Table - Método de Bisección
# ejercicio 1
Proyecto desarrollado para encontrar el factor de carga óptimo (λ)
que minimiza el tiempo promedio de búsqueda en una hash table.

Se implementa el método de Bisección sobre la derivada de la función.
# ejercicio 2
Balanceo de carga con N servidores. Se busca resolver:

E(x) = x^3 - 6x^2 + 11x - 6.5 = 0

en el intervalo [2, 4].

<<<<<<< HEAD
# ejercicio 3

Predicción de crecimiento de base de datos mediante el Método de Punto Fijo. Se resuelve la ecuación x = 0.5 cos(x) + 1.5, analizando la convergencia según el valor inicial y verificando la condición |g'(x)| < 1.

Método implementado

Punto Fijo

# ejercicio 4

Análisis de concurrencia usando el Método de Newton-Raphson. Se resuelve T(n) = n^3 - 8n^2 + 20n - 16 = 0, calculando la derivada analíticamente y verificando la convergencia cuadrática.

Método implementado

Newton-Raphson

# ejercicio 5

Predicción de escalabilidad usando el Método de la Secante. Se resuelve P(x) = x e^(-x/2) - 0.3 = 0 y se compara el desempeño con Newton-Raphson en términos de iteraciones y evaluaciones de función.

Método implementado

Secante

=======
>>>>>>> 238e7780fde820f098b58b8105a5030a8da34793
## Métodos implementados
- Falsa Posición (Regla Falsa)
## Instalación

pip install -r requirements.txt

## Ejecución

python main.py

## Qué muestra la interfaz
- Tabla comparativa de iteraciones (n, a, b, c, f(c), error abs, error rel %)
- Gráfica de f(x) con puntos de iteración
- Gráfica de convergencia del error (escala log)
- Métricas: iteraciones, error final, tiempo
## Autor
Esteban bonilla
Mariana Gonzales
Alejandro Ospina