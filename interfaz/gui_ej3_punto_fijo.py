from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from funciones.definiciones import g_crecimiento_bd
from metodos.punto_fijo import iteracion_punto_fijo


def fmt_float(x: float) -> str:
    if x == 0:
        return "0.00000000"
    if abs(x) < 1e-6:
        return f"{x:.8e}"
    return f"{x:.8f}"


class VentanaEjercicio3:
    """Ejercicio 3: Crecimiento de BD - Método de Punto Fijo."""

    X0S = [0.5, 1.0, 1.5, 2.0]

    def __init__(self, root: tk.Toplevel):
        self.root = root
        self.root.title("Ejercicio 3 - Punto Fijo (Crecimiento BD)")
        self.root.geometry("1100x700")

        self._build_input()
        self._build_table()
        self._build_plots()
        self._build_final()

        self._plot_compare_errors()

    def _build_input(self) -> None:
        frame = ttk.LabelFrame(self.root, text="Parámetros")
        frame.pack(fill="x", padx=10, pady=8)

        ttk.Label(frame, text="x0:").grid(row=0, column=0, sticky="w", padx=6, pady=4)
        self.combo_x0 = ttk.Combobox(frame, values=[str(v) for v in self.X0S], state="readonly", width=10)
        self.combo_x0.current(1)
        self.combo_x0.grid(row=0, column=1, sticky="w", padx=6, pady=4)

        ttk.Label(frame, text="Tolerancia:").grid(row=0, column=2, sticky="w", padx=6, pady=4)
        self.entry_tol = ttk.Entry(frame, width=12)
        self.entry_tol.insert(0, "1e-8")
        self.entry_tol.grid(row=0, column=3, sticky="w", padx=6, pady=4)

        ttk.Label(frame, text="Max iter:").grid(row=0, column=4, sticky="w", padx=6, pady=4)
        self.entry_iter = ttk.Entry(frame, width=10)
        self.entry_iter.insert(0, "100")
        self.entry_iter.grid(row=0, column=5, sticky="w", padx=6, pady=4)

        self.lbl_cond = ttk.Label(frame, text="Condición |g'(x)| < 1: |g'(x)| <= 0.5 < 1 (se cumple).")
        self.lbl_cond.grid(row=1, column=0, columnspan=6, sticky="w", padx=6, pady=4)

        ttk.Button(frame, text="Calcular (x0)", command=self.calcular_uno).grid(row=2, column=0, columnspan=3, padx=6, pady=6, sticky="we")
        ttk.Button(frame, text="Comparar x0", command=self._plot_compare_errors).grid(row=2, column=3, columnspan=3, padx=6, pady=6, sticky="we")

    def _build_table(self) -> None:
        frame = ttk.LabelFrame(self.root, text="Tabla (x0 seleccionado)")
        frame.pack(fill="both", expand=True, padx=10, pady=6)

        cols = ("n", "x_n", "g(x_n)", "|x_n - g(x_n)|", "error_rel")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=170, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        sb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

    def _build_plots(self) -> None:
        frame = ttk.LabelFrame(self.root, text="Gráficas")
        frame.pack(fill="both", expand=True, padx=10, pady=6)

        self.fig1 = plt.Figure(figsize=(5.2, 3.4), dpi=100)
        self.ax1 = self.fig1.add_subplot(111)
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=frame)
        self.canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

        self.fig2 = plt.Figure(figsize=(5.2, 3.4), dpi=100)
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

    def calcular_uno(self) -> None:
        try:
            x0 = float(self.combo_x0.get())
            tol = float(self.entry_tol.get())
            max_iter = int(float(self.entry_iter.get()))
            if tol <= 0 or max_iter <= 0:
                raise ValueError("tolerancia/max_iter deben ser positivos.")
        except Exception as e:
            messagebox.showerror("Error", f"Parámetros inválidos: {e}")
            return

        res = iteracion_punto_fijo(g_crecimiento_bd, x0, tol, max_iter)

        self._clear_table()
        for r in res["tabla"]:
            self.tree.insert("", "end", values=(r["n"], fmt_float(r["x_n"]), fmt_float(r["g_xn"]), fmt_float(r["diff"]), fmt_float(r["error_rel"])))

        self.lbl_raiz.config(text=f"Raíz aproximada: {fmt_float(res['raiz'])}")
        self.lbl_iters.config(text=f"Iteraciones: {res['iteraciones']}")
        self.lbl_error.config(text=f"Error final: {fmt_float(res['error_final'])}")
        self.lbl_msg.config(text=f"Estado: {res['mensaje']} (t={res['tiempo']:.6f}s)")

        self._plot_cobweb(res["tabla"])

    def _plot_cobweb(self, tabla: List[Dict]) -> None:
        self.ax1.clear()
        xs = np.linspace(0, 3, 400)
        self.ax1.plot(xs, xs, label="y=x")
        self.ax1.plot(xs, g_crecimiento_bd(xs), label="y=g(x)")

        if tabla:
            x = tabla[0]["x_n"]
            for row in tabla[:30]:
                gx = row["g_xn"]
                self.ax1.plot([x, x], [x, gx])
                self.ax1.plot([x, gx], [gx, gx])
                x = gx

        self.ax1.set_title("Cobweb plot")
        self.ax1.set_xlabel("x")
        self.ax1.set_ylabel("y")
        self.ax1.grid(True, alpha=0.25)
        self.ax1.legend()
        self.canvas1.draw()

    def _plot_compare_errors(self) -> None:
        self.ax2.clear()
        try:
            tol = float(self.entry_tol.get())
            max_iter = int(float(self.entry_iter.get()))
        except Exception:
            tol, max_iter = 1e-8, 100

        for x0 in self.X0S:
            res = iteracion_punto_fijo(g_crecimiento_bd, x0, tol, max_iter)
            errs = [r["diff"] for r in res["tabla"]]
            self.ax2.plot(range(1, len(errs)+1), errs, label=f"x0={x0}")

        self.ax2.set_yscale("log")
        self.ax2.set_title("Convergencia del error (comparación x0)")
        self.ax2.set_xlabel("Iteración")
        self.ax2.set_ylabel("|x_{n+1}-x_n| (log)")
        self.ax2.grid(True, alpha=0.25)
        self.ax2.legend()
        self.canvas2.draw()
