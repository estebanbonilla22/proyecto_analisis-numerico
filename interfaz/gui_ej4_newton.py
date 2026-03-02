from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from funciones.definiciones import tiempo_threads, tiempo_threads_derivada
from metodos.newton import metodo_newton_raphson


def fmt_float(x: float) -> str:
    if x == 0:
        return "0.00000000"
    if abs(x) < 1e-6:
        return f"{x:.8e}"
    return f"{x:.8f}"


class VentanaEjercicio4:
    """Ejercicio 4: Newton-Raphson para T(n)=0 + gráficas de tangentes y error."""

    def __init__(self, root: tk.Toplevel):
        self.root = root
        self.root.title("Ejercicio 4 - Newton-Raphson (Concurrencia)")
        self.root.geometry("1150x720")

        self._build_input()
        self._build_table()
        self._build_plots()
        self._build_final()

    def _build_input(self) -> None:
        frame = ttk.LabelFrame(self.root, text="Parámetros")
        frame.pack(fill="x", padx=10, pady=8)

        ttk.Label(frame, text="n0:").grid(row=0, column=0, sticky="w", padx=6, pady=4)
        self.entry_x0 = ttk.Entry(frame, width=12)
        self.entry_x0.insert(0, "3.0")
        self.entry_x0.grid(row=0, column=1, sticky="w", padx=6, pady=4)

        ttk.Label(frame, text="Tolerancia:").grid(row=0, column=2, sticky="w", padx=6, pady=4)
        self.entry_tol = ttk.Entry(frame, width=12)
        self.entry_tol.insert(0, "1e-10")
        self.entry_tol.grid(row=0, column=3, sticky="w", padx=6, pady=4)

        ttk.Label(frame, text="Max iter:").grid(row=0, column=4, sticky="w", padx=6, pady=4)
        self.entry_iter = ttk.Entry(frame, width=10)
        self.entry_iter.insert(0, "100")
        self.entry_iter.grid(row=0, column=5, sticky="w", padx=6, pady=4)

        ttk.Button(frame, text="Calcular", command=self.calcular).grid(row=1, column=0, columnspan=3, padx=6, pady=6, sticky="we")
        ttk.Button(frame, text="Probar n0: 1,2,3,5", command=self.probar_iniciales).grid(row=1, column=3, columnspan=3, padx=6, pady=6, sticky="we")

    def _build_table(self) -> None:
        frame = ttk.LabelFrame(self.root, text="Tabla de iteraciones")
        frame.pack(fill="both", expand=True, padx=10, pady=6)

        cols = ("n", "x_n", "f(x_n)", "f'(x_n)", "x_{n+1}", "error_abs", "error_rel")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

    def _build_plots(self) -> None:
        frame = ttk.LabelFrame(self.root, text="Gráficas")
        frame.pack(fill="both", expand=True, padx=10, pady=6)

        self.fig1 = plt.Figure(figsize=(5.4, 3.4), dpi=100)
        self.ax1 = self.fig1.add_subplot(111)
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=frame)
        self.canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

        self.fig2 = plt.Figure(figsize=(5.4, 3.4), dpi=100)
        self.ax2 = self.fig2.add_subplot(111)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=frame)
        self.canvas2.get_tk_widget().pack(side="left", fill="both", expand=True)

    def _build_final(self) -> None:
        frame = ttk.LabelFrame(self.root, text="Resultados finales")
        frame.pack(fill="x", padx=10, pady=8)

        self.lbl_raiz = ttk.Label(frame, text="Raíz aproximada: -")
        self.lbl_raiz.grid(row=0, column=0, sticky="w", padx=6, pady=3)
        self.lbl_iters = ttk.Label(frame, text="Iteraciones: -")
        self.lbl_iters.grid(row=0, column=1, sticky="w", padx=6, pady=3)
        self.lbl_error = ttk.Label(frame, text="Error final: -")
        self.lbl_error.grid(row=0, column=2, sticky="w", padx=6, pady=3)
        self.lbl_msg = ttk.Label(frame, text="Estado: -")
        self.lbl_msg.grid(row=1, column=0, columnspan=3, sticky="w", padx=6, pady=3)

    def _clear_table(self) -> None:
        for it in self.tree.get_children():
            self.tree.delete(it)

    def calcular(self) -> None:
        try:
            x0 = float(self.entry_x0.get())
            tol = float(self.entry_tol.get())
            max_iter = int(float(self.entry_iter.get()))
            if tol <= 0 or max_iter <= 0:
                raise ValueError("tolerancia/max_iter deben ser positivos.")
        except Exception as e:
            messagebox.showerror("Error", f"Parámetros inválidos: {e}")
            return

        res = metodo_newton_raphson(tiempo_threads, tiempo_threads_derivada, x0, tol, max_iter)

        self._clear_table()
        for r in res["tabla"]:
            self.tree.insert("", "end", values=(
                r["n"], fmt_float(r["x_n"]), fmt_float(r["f_xn"]), fmt_float(r["df_xn"]),
                fmt_float(r["x_next"]), fmt_float(r["error_abs"]), fmt_float(r["error_rel"])
            ))

        self.lbl_raiz.config(text=f"Raíz aproximada: {fmt_float(res['raiz'])}")
        self.lbl_iters.config(text=f"Iteraciones: {res['iteraciones']}")
        self.lbl_error.config(text=f"Error final: {fmt_float(res['error_final'])}")
        self.lbl_msg.config(text=f"Estado: {res['mensaje']} (t={res['tiempo']:.6f}s)")

        self._plot_funcion_y_tangentes(res["tabla"])
        self._plot_error_log(res["tabla"])

    def probar_iniciales(self) -> None:
        iniciales = [1.0, 2.0, 3.0, 5.0]
        try:
            tol = float(self.entry_tol.get())
            max_iter = int(float(self.entry_iter.get()))
        except Exception:
            tol, max_iter = 1e-10, 100

        msg = "Comparación por n0:\n"
        for x0 in iniciales:
            res = metodo_newton_raphson(tiempo_threads, tiempo_threads_derivada, x0, tol, max_iter)
            msg += f"- n0={x0}: iter={res['iteraciones']}, error={res['error_final']:.3e}, convergio={res['convergio']}\n"
        messagebox.showinfo("Comparación", msg)

    def _plot_funcion_y_tangentes(self, tabla: List[Dict]) -> None:
        self.ax1.clear()
        xs = np.linspace(-1, 8, 600)
        self.ax1.plot(xs, tiempo_threads(xs), label="T(n)")
        self.ax1.axhline(0, linewidth=1)

        for r in tabla[:10]:
            x_n, f_n, df_n = r["x_n"], r["f_xn"], r["df_xn"]
            xt = np.linspace(x_n - 1.5, x_n + 1.5, 60)
            yt = f_n + df_n * (xt - x_n)
            self.ax1.plot(xt, yt, linestyle="--")
            self.ax1.plot([x_n], [f_n], marker="o")

        if tabla:
            self.ax1.plot([tabla[-1]["x_next"]], [0], marker="x", markersize=9, label="Raíz aprox.")
        self.ax1.set_title("Función y tangentes (Newton)")
        self.ax1.set_xlabel("n")
        self.ax1.set_ylabel("T(n)")
        self.ax1.grid(True, alpha=0.25)
        self.ax1.legend()
        self.canvas1.draw()

    def _plot_error_log(self, tabla: List[Dict]) -> None:
        self.ax2.clear()
        errs = [r["error_abs"] for r in tabla]
        self.ax2.plot(range(1, len(errs)+1), errs, label="Error absoluto")
        self.ax2.set_yscale("log")
        self.ax2.set_title("Convergencia del error (log)")
        self.ax2.set_xlabel("Iteración")
        self.ax2.set_ylabel("|x_{n+1}-x_n| (log)")
        self.ax2.grid(True, alpha=0.25)
        self.ax2.legend()
        self.canvas2.draw()
