Métodos Numéricos con Interfaz Gráfica

Aplicación desarrollada en Python que implementa cinco métodos numéricos para la resolución de ecuaciones no lineales, utilizando una interfaz gráfica interactiva construida con Tkinter y Matplotlib.

El sistema permite visualizar:

tablas de iteración

aproximaciones sucesivas

gráficas de la función

convergencia del error

comparación entre métodos numéricos

Este proyecto fue desarrollado como parte del curso de Análisis Numérico.

Ejercicios Implementados
Ejercicio 1 — Optimización de Hash Table (Método de Bisección)

Se busca encontrar el factor de carga óptimo (λ) que minimiza el tiempo promedio de búsqueda en una hash table dentro de un sistema de caché distribuido.

La función utilizada es:

T(λ) = 2.5 + 0.8λ² − 3.2λ + ln(λ + 1)

El método aplicado es Bisección, que divide iterativamente el intervalo de búsqueda hasta encontrar una aproximación de la raíz con una tolerancia determinada.

Ejercicio 2 — Balanceo de Carga en Servidores

Se modela la eficiencia de un sistema distribuido mediante la ecuación:

E(x) = x³ − 6x² + 11x − 6.5

La solución se busca dentro del intervalo:

[2, 4]

En este ejercicio se implementan y comparan dos métodos:

Bisección

Falsa Posición (Regla Falsa)

El objetivo es analizar cuál método converge más rápido.

Ejercicio 3 — Crecimiento de Base de Datos (Método de Punto Fijo)

Se modela el crecimiento de una base de datos mediante la ecuación:

x = 0.5 cos(x) + 1.5

Este problema se resuelve utilizando el método de Punto Fijo, evaluando:

la convergencia del algoritmo

el impacto del valor inicial

la condición de convergencia

|g'(x)| < 1
Ejercicio 4 — Análisis de Concurrencia (Método de Newton-Raphson)

Se analiza el punto donde el beneficio del paralelismo se equilibra con el overhead de sincronización en un sistema paralelo.

La función es:

T(n) = n³ − 8n² + 20n − 16

Se calcula la derivada analítica:

T'(n) = 3n² − 16n + 20

El método utilizado es Newton-Raphson, conocido por su convergencia cuadrática.

Ejercicio 5 — Predicción de Escalabilidad (Método de la Secante)

Se analiza el punto donde el costo de infraestructura iguala los ingresos en una plataforma cloud.

La función utilizada es:

P(x) = x e^(−x/2) − 0.3

El método implementado es Secante, que aproxima la derivada utilizando dos puntos consecutivos.

También se compara su desempeño con el método Newton-Raphson.

Métodos Numéricos Implementados

El proyecto incluye la implementación de los siguientes algoritmos:

Método de Bisección

Método de Falsa Posición

Método de Punto Fijo

Método de Newton-Raphson

Método de Secante

Cada algoritmo calcula:

aproximaciones iterativas

error absoluto

error relativo

validación de condiciones matemáticas

control de convergencia

Características de la Interfaz

La aplicación incluye una interfaz gráfica interactiva que contiene:

Panel de Entrada

Permite ingresar:

intervalos iniciales

valores iniciales

tolerancia

número máximo de iteraciones

Tabla de Iteraciones

Muestra:

número de iteración

aproximación actual

valor de la función

error absoluto

error relativo

Visualización Gráfica

Se generan automáticamente:

gráfica de la función evaluada

puntos correspondientes a cada iteración

gráfica de convergencia del error en escala logarítmica

Métricas Finales

El sistema reporta:

raíz aproximada encontrada

número total de iteraciones

error final alcanzado

tiempo de ejecución

número de evaluaciones de función

Tecnologías Utilizadas

Lenguaje principal:

Python

Librerías utilizadas:

numpy
matplotlib
tkinter
sympy
time
Estructura del Proyecto
proyecto_metodos_numericos/

metodos/
    __init__.py
    biseccion.py
    falsa_posicion.py
    punto_fijo.py
    newton.py
    secante.py

funciones/
    __init__.py
    definiciones.py

interfaz/
    __init__.py
    gui_principal.py

utils/
    __init__.py
    validaciones.py

tests/
    test_metodos.py

main.py
requirements.txt
README.md
Instalación

Clonar el repositorio:

git clone <url_del_repositorio>
cd proyecto_metodos_numericos

Instalar dependencias:

pip install -r requirements.txt
Ejecución

Para ejecutar la aplicación:

python main.py

Esto abrirá la interfaz gráfica del sistema, donde se pueden ejecutar todos los ejercicios.

Resultados del Sistema

El programa permite analizar visualmente:

el proceso iterativo de cada método

la convergencia hacia la raíz

la comparación entre distintos algoritmos numéricos

Las gráficas y tablas permiten comprender el comportamiento de cada método y su eficiencia.

Autor

Proyecto académico desarrollado por:

Esteban Bonilla

Mariana González

Alejandro Ospina

Curso: Análisis Numérico

Licencia

Proyecto desarrollado con fines académicos y educativos.
- Gráfica de f(x) con puntos de iteración
- Gráfica de convergencia del error (escala log)
- Métricas: iteraciones, error final, tiempo
## Autor
Esteban bonilla
Mariana Gonzales
Alejandro Ospina
