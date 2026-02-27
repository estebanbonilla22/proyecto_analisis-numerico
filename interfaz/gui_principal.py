import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from metodos.biseccion import metodo_biseccion
from funciones.definiciones import derivada
from utils.validaciones import validar_intervalo


class App:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Método de Bisección - Optimización Hash Table")

        self.crear_panel_entrada()
        self.crear_tabla()
        self.crear_graficas()
        self.crear_panel_resultados()

    def crear_panel_entrada(self):
        frame = tk.Frame(self.root)
        frame.pack()

        tk.Label(frame, text="a:").grid(row=0, column=0)
        self.entry_a = tk.Entry(frame)
        self.entry_a.insert(0, "0.5")
        self.entry_a.grid(row=0, column=1)

        tk.Label(frame, text="b:").grid(row=0, column=2)
        self.entry_b = tk.Entry(frame)
        self.entry_b.insert(0, "2.5")
        self.entry_b.grid(row=0, column=3)

        tk.Label(frame, text="Tolerancia:").grid(row=1, column=0)
        self.entry_tol = tk.Entry(frame)
        self.entry_tol.insert(0, "1e-6")
        self.entry_tol.grid(row=1, column=1)

        tk.Label(frame, text="Iteraciones Máx:").grid(row=1, column=2)
        self.entry_iter = tk.Entry(frame)
        self.entry_iter.insert(0, "100")
        self.entry_iter.grid(row=1, column=3)

        tk.Button(frame, text="Calcular", command=self.calcular).grid(row=2, column=0, columnspan=2)
        tk.Button(frame, text="Limpiar", command=self.limpiar).grid(row=2, column=2, columnspan=2)

    def crear_tabla(self):
        self.tree = ttk.Treeview(self.root, columns=("n", "a", "b", "c", "f_c", "error_abs", "error_rel"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack()

    def crear_graficas(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

    def crear_panel_resultados(self):
        self.label_resultado = tk.Label(self.root, text="")
        self.label_resultado.pack()

    def calcular(self):
        try:
            a = float(self.entry_a.get())
            b = float(self.entry_b.get())
            tol = float(self.entry_tol.get())
            max_iter = int(self.entry_iter.get())

            validar_intervalo(derivada, a, b)

            resultado = metodo_biseccion(derivada, a, b, tol, max_iter)

            self.mostrar_tabla(resultado["tabla"])
            self.mostrar_graficas(resultado["tabla"])
            self.mostrar_resultado_final(resultado)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mostrar_tabla(self, datos):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for fila in datos:
            self.tree.insert("", "end", values=(
                fila["n"],
                f"{fila['a']:.8f}",
                f"{fila['b']:.8f}",
                f"{fila['c']:.8f}",
                f"{fila['f_c']:.8e}",
                f"{fila['error_abs']:.8e}",
                f"{fila['error_rel']:.8e}",
            ))

    def mostrar_graficas(self, datos):
        self.ax1.clear()
        self.ax2.clear()

        x = np.linspace(0.5, 2.5, 400)
        y = [derivada(i) for i in x]

        self.ax1.plot(x, y)
        self.ax1.axhline(0)
        puntos = [fila["c"] for fila in datos]
        self.ax1.scatter(puntos, [derivada(p) for p in puntos], color="red")
        self.ax1.set_title("Función y Convergencia")

        errores = [fila["error_abs"] for fila in datos if fila["error_abs"] > 0]
        self.ax2.plot(range(1, len(errores) + 1), errores)
        self.ax2.set_yscale("log")
        self.ax2.set_title("Convergencia del Error")

        self.canvas.draw()

    def mostrar_resultado_final(self, resultado):
        self.label_resultado.config(
            text=f"Raíz: {resultado['raiz']:.8f} | Iteraciones: {resultado['iteraciones']} | "
                 f"Error Final: {resultado['error_final']:.2e} | Tiempo: {resultado['tiempo']:.6f}s"
        )

    def limpiar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.ax1.clear()
        self.ax2.clear()
        self.canvas.draw()
        self.label_resultado.config(text="")