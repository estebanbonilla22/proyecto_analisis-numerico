from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from funciones.definiciones import modelo_financiero_p, modelo_financiero_p_derivada
from metodos.secante import metodo_secante
from metodos.newton import metodo_newton_raphson


def fmt_float(x: float) -> str:
    if x == 0:
        return "0.00000000"
    if abs(x) < 1e-6:
        return f"{x:.8e}"
    return f"{x:.8f}"


class VentanaEjercicio5:
    """Ejercicio 5: Secante + comparación con Newton-Raphson."""

    def __init__(self, root: tk.Toplevel):
        self.root = root
        self.root.title("Ejercicio 5 - Secante vs Newton (Modelo Financiero)")
        self.root.geometry("1200x740")

        self._build_input()
        self._build_tables()
        self._build_plots()
        self._build_final()

    def _build_input(self) -> None:
        frame = ttk.LabelFrame(self.root, text="Parámetros")
        frame.pack(fill="x", padx=10, pady=8)

        ttk.Label(frame, text="Secante x0:").grid(row=0, column=0, sticky="w", padx=6, pady=4)
        self.entry_x0 = ttk.Entry(frame, width=12); self.entry_x0.insert(0, "0.5")
        self.entry_x0.grid(row=0, column=1, sticky="w", padx=6, pady=4)

        ttk.Label(frame, text="Secante x1:").grid(row=0, column=2, sticky="w", padx=6, pady=4)
        self.entry_x1 = ttk.Entry(frame, width=12); self.entry_x1.insert(0, "1.0")
        self.entry_x1.grid(row=0, column=3, sticky="w", padx=6, pady=4)

        ttk.Label(frame, text="Newton x0:").grid(row=0, column=4, sticky="w", padx=6, pady=4)
        self.entry_x0n = ttk.Entry(frame, width=12); self.entry_x0n.insert(0, "1.0")
        self.entry_x0n.grid(row=0, column=5, sticky="w", padx=6, pady=4)

        ttk.Label(frame, text="Tolerancia:").grid(row=1, column=0, sticky="w", padx=6, pady=4)
        self.entry_tol = ttk.Entry(frame, width=12); self.entry_tol.insert(0, "1e-9")
        self.entry_tol.grid(row=1, column=1, sticky="w", padx=6, pady=4)

        ttk.Label(frame, text="Max iter:").grid(row=1, column=2, sticky="w", padx=6, pady=4)
        self.entry_iter = ttk.Entry(frame, width=12); self.entry_iter.insert(0, "100")
        self.entry_iter.grid(row=1, column=3, sticky="w", padx=6, pady=4)

        ttk.Button(frame, text="Calcular y comparar", command=self.calcular)            .grid(row=2, column=0, columnspan=6, padx=6, pady=6, sticky="we")

    def _build_tables(self) -> None:
        frame = ttk.LabelFrame(self.root, text="Tablas")
        frame.pack(fill="both", expand=True, padx=10, pady=6)

        sec = ttk.LabelFrame(frame, text="Secante")
        sec.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        cols_s = ("n","x_{n-1}","x_n","f(x_{n-1})","f(x_n)","x_{n+1}","error")
        self.tree_s = ttk.Treeview(sec, columns=cols_s, show="headings", height=10)
        for c in cols_s:
            self.tree_s.heading(c, text=c); self.tree_s.column(c, width=140, anchor="center")
        self.tree_s.pack(side="left", fill="both", expand=True)
        sb_s = ttk.Scrollbar(sec, orient="vertical", command=self.tree_s.yview)
        self.tree_s.configure(yscrollcommand=sb_s.set); sb_s.pack(side="right", fill="y")

        new = ttk.LabelFrame(frame, text="Newton-Raphson")
        new.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        cols_n = ("n","x_n","f(x_n)","f'(x_n)","x_{n+1}","error_abs")
        self.tree_n = ttk.Treeview(new, columns=cols_n, show="headings", height=10)
        for c in cols_n:
            self.tree_n.heading(c, text=c); self.tree_n.column(c, width=140, anchor="center")
        self.tree_n.pack(side="left", fill="both", expand=True)
        sb_n = ttk.Scrollbar(new, orient="vertical", command=self.tree_n.yview)
        self.tree_n.configure(yscrollcommand=sb_n.set); sb_n.pack(side="right", fill="y")

    def _build_plots(self) -> None:
        frame = ttk.LabelFrame(self.root, text="Gráficas")
        frame.pack(fill="both", expand=True, padx=10, pady=6)

        self.fig1 = plt.Figure(figsize=(5.6, 3.4), dpi=100)
        self.ax1 = self.fig1.add_subplot(111)
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=frame)
        self.canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

        self.fig2 = plt.Figure(figsize=(5.6, 3.4), dpi=100)
        self.ax2 = self.fig2.add_subplot(111)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=frame)
        self.canvas2.get_tk_widget().pack(side="left", fill="both", expand=True)

    def _build_final(self) -> None:
        frame = ttk.LabelFrame(self.root, text="Métricas finales")
        frame.pack(fill="x", padx=10, pady=8)
        self.lbl_sec = ttk.Label(frame, text="Secante: -"); self.lbl_sec.grid(row=0, column=0, sticky="w", padx=6, pady=3)
        self.lbl_new = ttk.Label(frame, text="Newton: -"); self.lbl_new.grid(row=1, column=0, sticky="w", padx=6, pady=3)
        self.lbl_conc = ttk.Label(frame, text="Conclusión: -"); self.lbl_conc.grid(row=2, column=0, sticky="w", padx=6, pady=3)

    def _clear_tables(self) -> None:
        for t in (self.tree_s, self.tree_n):
            for it in t.get_children():
                t.delete(it)

    def calcular(self) -> None:
        try:
            x0 = float(self.entry_x0.get())
            x1 = float(self.entry_x1.get())
            x0n = float(self.entry_x0n.get())
            tol = float(self.entry_tol.get())
            max_iter = int(float(self.entry_iter.get()))
            if tol <= 0 or max_iter <= 0:
                raise ValueError("tolerancia/max_iter deben ser positivos.")
        except Exception as e:
            messagebox.showerror("Error", f"Parámetros inválidos: {e}")
            return

        res_s = metodo_secante(modelo_financiero_p, x0, x1, tol, max_iter)
        res_n = metodo_newton_raphson(modelo_financiero_p, modelo_financiero_p_derivada, x0n, tol, max_iter)

        self._clear_tables()

        for r in res_s["tabla"]:
            self.tree_s.insert("", "end", values=(r["n"], fmt_float(r["x_prev"]), fmt_float(r["x_curr"]),
                                                 fmt_float(r["f_prev"]), fmt_float(r["f_curr"]),
                                                 fmt_float(r["x_next"]), fmt_float(r["error_abs"])))
        for r in res_n["tabla"]:
            self.tree_n.insert("", "end", values=(r["n"], fmt_float(r["x_n"]), fmt_float(r["f_xn"]),
                                                 fmt_float(r["df_xn"]), fmt_float(r["x_next"]), fmt_float(r["error_abs"])))

        self._plot_funcion_y_secantes(res_s["tabla"], raiz=res_s["raiz"])
        self._plot_errores(res_s["tabla"], res_n["tabla"])

        self.lbl_sec.config(text=f"Secante: raíz={fmt_float(res_s['raiz'])}, iter={res_s['iteraciones']}, evals_f={res_s.get('evals_f','-')}, t={res_s['tiempo']:.6f}s")
        self.lbl_new.config(text=f"Newton: raíz={fmt_float(res_n['raiz'])}, iter={res_n['iteraciones']}, evals_f={res_n.get('evals_f','-')}, evals_df={res_n.get('evals_df','-')}, t={res_n['tiempo']:.6f}s")

        conc = "Newton suele requerir menos iteraciones, pero necesita derivada. Secante evita derivadas y es buena alternativa si derivar es costoso/complicado."
        self.lbl_conc.config(text=f"Conclusión: {conc}")

    def _plot_funcion_y_secantes(self, tabla: List[Dict], raiz: float) -> None:
        self.ax1.clear()
        xs = np.linspace(0, 6, 600)
        self.ax1.plot(xs, modelo_financiero_p(xs), label="P(x)")
        self.ax1.axhline(0, linewidth=1)

        # Secantes (primeras 8)
        for r in tabla[:8]:
            x0, x1 = r["x_prev"], r["x_curr"]
            y0, y1 = r["f_prev"], r["f_curr"]
            self.ax1.plot([x0, x1], [y0, y1], linestyle="--")
            self.ax1.plot([x0, x1], [y0, y1], marker="o", linestyle="")

        self.ax1.plot([raiz], [0], marker="x", markersize=9, label="Raíz aprox.")
        self.ax1.set_title("Función y secantes")
        self.ax1.set_xlabel("x (miles de usuarios)")
        self.ax1.set_ylabel("P(x)")
        self.ax1.grid(True, alpha=0.25)
        self.ax1.legend()
        self.canvas1.draw()

    def _plot_errores(self, tabla_s: List[Dict], tabla_n: List[Dict]) -> None:
        self.ax2.clear()
        es = [r["error_abs"] for r in tabla_s]
        en = [r["error_abs"] for r in tabla_n]
        self.ax2.plot(range(1, len(es)+1), es, label="Secante")
        self.ax2.plot(range(1, len(en)+1), en, label="Newton")
        self.ax2.set_yscale("log")
        self.ax2.set_title("Convergencia del error (log)")
        self.ax2.set_xlabel("Iteración")
        self.ax2.set_ylabel("Error absoluto (log)")
        self.ax2.grid(True, alpha=0.25)
        self.ax2.legend()
        self.canvas2.draw()
