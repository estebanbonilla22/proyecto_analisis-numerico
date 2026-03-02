import tkinter as tk
from tkinter import ttk, messagebox
import time
from typing import Callable, Dict, List

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from funciones.definiciones import eficiencia_e, derivada_t
from metodos.biseccion import metodo_biseccion
from metodos.falsa_posicion import metodo_falsa_posicion
from utils.validaciones import validar_intervalo, validar_numeros

from interfaz.gui_ej3_punto_fijo import VentanaEjercicio3
from interfaz.gui_ej4_newton import VentanaEjercicio4
from interfaz.gui_ej5_secante import VentanaEjercicio5


def fmt_float(x: float) -> str:
    # minimum 8 decimals; scientific for very small
    if x == 0:
        return "0.00000000"
    if abs(x) < 1e-6:
        return f"{x:.8e}"
    return f"{x:.8f}"


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Métodos Numéricos - Comparación (Bisección vs Falsa Posición)")

        # Guardamos los textos EXACTOS para poder seleccionarlos desde botones
        self._KEY_EJ2 = "Ejercicio 2: E(x) = x^3 - 6x^2 + 11x - 6.5"
        self._KEY_EJ1 = "Ejercicio 1: T'(λ) (opcional)"

        self.funciones = {
            self._KEY_EJ2: eficiencia_e,
            self._KEY_EJ1: derivada_t,
        }

        self._build_input_panel()
        self._build_table()
        self._build_plots()
        self._build_final_panel()

    # -----------------------------
    # Helpers para los nuevos botones
    # -----------------------------
    def _set_entry(self, entry: ttk.Entry, value: str) -> None:
        entry.delete(0, "end")
        entry.insert(0, value)

    def cargar_ejercicio_1(self) -> None:
        """Carga parámetros del Ejercicio 1 (Guía) en la interfaz."""
        self.combo_func.set(self._KEY_EJ1)
        self._set_entry(self.entry_a, "0.5")
        self._set_entry(self.entry_b, "2.5")
        self._set_entry(self.entry_tol, "1e-6")
        self._set_entry(self.entry_iter, "100")
        # Ej 1 es Bisección según la guía
        self.combo_modo.set("Solo Bisección")

    def cargar_ejercicio_2(self) -> None:
        """Carga parámetros del Ejercicio 2 (Guía) en la interfaz."""
        self.combo_func.set(self._KEY_EJ2)
        self._set_entry(self.entry_a, "2")
        self._set_entry(self.entry_b, "4")
        self._set_entry(self.entry_tol, "1e-7")
        self._set_entry(self.entry_iter, "100")
        # Ej 2 pide comparar con bisección
        self.combo_modo.set("Comparar (Bisección vs Falsa Posición)")

    def _build_input_panel(self) -> None:
        frame = ttk.LabelFrame(self.root, text="Input")
        frame.pack(fill="x", padx=10, pady=8)

        ttk.Label(frame, text="Función:").grid(row=0, column=0, sticky="w", padx=6, pady=4)
        self.combo_func = ttk.Combobox(frame, values=list(self.funciones.keys()), state="readonly", width=55)
        self.combo_func.current(0)
        self.combo_func.grid(row=0, column=1, columnspan=3, sticky="we", padx=6, pady=4)

        ttk.Label(frame, text="a:").grid(row=1, column=0, sticky="w", padx=6, pady=4)
        self.entry_a = ttk.Entry(frame, width=12)
        self.entry_a.insert(0, "2")
        self.entry_a.grid(row=1, column=1, sticky="w", padx=6, pady=4)

        ttk.Label(frame, text="b:").grid(row=1, column=2, sticky="w", padx=6, pady=4)
        self.entry_b = ttk.Entry(frame, width=12)
        self.entry_b.insert(0, "4")
        self.entry_b.grid(row=1, column=3, sticky="w", padx=6, pady=4)

        ttk.Label(frame, text="Tolerancia:").grid(row=2, column=0, sticky="w", padx=6, pady=4)
        self.entry_tol = ttk.Entry(frame, width=12)
        self.entry_tol.insert(0, "1e-7")
        self.entry_tol.grid(row=2, column=1, sticky="w", padx=6, pady=4)

        ttk.Label(frame, text="Max iter:").grid(row=2, column=2, sticky="w", padx=6, pady=4)
        self.entry_iter = ttk.Entry(frame, width=12)
        self.entry_iter.insert(0, "100")
        self.entry_iter.grid(row=2, column=3, sticky="w", padx=6, pady=4)

        ttk.Label(frame, text="Modo:").grid(row=3, column=0, sticky="w", padx=6, pady=4)
        self.combo_modo = ttk.Combobox(
            frame,
            values=["Comparar (Bisección vs Falsa Posición)", "Solo Bisección", "Solo Falsa Posición"],
            state="readonly",
            width=35
        )
        self.combo_modo.current(0)
        self.combo_modo.grid(row=3, column=1, sticky="w", padx=6, pady=4)

        # --- NUEVO: Botones directos para Ej 1 y Ej 2 (solo cargan parámetros) ---
        ttk.Button(frame, text="Cargar Ejercicio 1", command=self.cargar_ejercicio_1)\
            .grid(row=3, column=2, padx=6, pady=4, sticky="we")
        ttk.Button(frame, text="Cargar Ejercicio 2", command=self.cargar_ejercicio_2)\
            .grid(row=3, column=3, padx=6, pady=4, sticky="we")

        ttk.Button(frame, text="Calcular", command=self.calcular).grid(
            row=4, column=0, columnspan=2, padx=6, pady=6, sticky="we"
        )
        ttk.Button(frame, text="Limpiar", command=self.limpiar).grid(
            row=4, column=2, columnspan=2, padx=6, pady=6, sticky="we"
        )

        # Ventanas para Ejercicios 3, 4 y 5 (no modifica Ej 1-2)
        ttk.Button(frame, text="Abrir Ejercicio 3 (Punto Fijo)", command=self.abrir_ej3)\
            .grid(row=5, column=0, columnspan=2, padx=6, pady=6, sticky="we")
        ttk.Button(frame, text="Abrir Ejercicio 4 (Newton)", command=self.abrir_ej4)\
            .grid(row=5, column=2, columnspan=2, padx=6, pady=6, sticky="we")
        ttk.Button(frame, text="Abrir Ejercicio 5 (Secante)", command=self.abrir_ej5)\
            .grid(row=6, column=0, columnspan=4, padx=6, pady=6, sticky="we")

        frame.columnconfigure(1, weight=1)

    def _build_table(self) -> None:
        frame = ttk.LabelFrame(self.root, text="Tabla Comparativa (iteraciones, valores, errores)")
        frame.pack(fill="both", expand=True, padx=10, pady=8)

        cols = ("metodo", "n", "a", "b", "c", "f(c)", "error_abs", "error_rel_%")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)

        headings = {
            "metodo": "Método",
            "n": "n",
            "a": "a",
            "b": "b",
            "c": "c",
            "f(c)": "f(c)",
            "error_abs": "Error abs",
            "error_rel_%": "Error rel (%)",
        }

        for col in cols:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=110, anchor="center")

        self.tree.column("metodo", width=140, anchor="center")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _build_plots(self) -> None:
        frame = ttk.LabelFrame(self.root, text="Gráficas")
        frame.pack(fill="both", expand=True, padx=10, pady=8)

        self.fig = plt.Figure(figsize=(10, 4), dpi=100)
        self.ax_func = self.fig.add_subplot(1, 2, 1)
        self.ax_err = self.fig.add_subplot(1, 2, 2)

        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _build_final_panel(self) -> None:
        frame = ttk.LabelFrame(self.root, text="Resultados finales")
        frame.pack(fill="x", padx=10, pady=8)

        self.lbl_final = ttk.Label(frame, text="(aquí aparecerán las métricas)")
        self.lbl_final.pack(anchor="w", padx=8, pady=6)

        self.lbl_analysis = ttk.Label(frame, text="")
        self.lbl_analysis.pack(anchor="w", padx=8, pady=2)

    def _get_inputs(self) -> Dict:
        f = self.funciones[self.combo_func.get()]
        a = float(self.entry_a.get())
        b = float(self.entry_b.get())
        tol = float(self.entry_tol.get())
        max_iter = int(self.entry_iter.get())
        validar_numeros(a, b, tol, max_iter)
        validar_intervalo(f, a, b)
        return {"f": f, "a": a, "b": b, "tol": tol, "max_iter": max_iter}

    def calcular(self) -> None:
        try:
            inp = self._get_inputs()
            f: Callable[[float], float] = inp["f"]
            a, b, tol, max_iter = inp["a"], inp["b"], inp["tol"], inp["max_iter"]
            modo = self.combo_modo.get()

            if modo == "Solo Bisección":
                res_b = metodo_biseccion(f, a, b, tol, max_iter)
                self._render([res_b], f, a, b)

            elif modo == "Solo Falsa Posición":
                res_fp = metodo_falsa_posicion(f, a, b, tol, max_iter)
                self._render([res_fp], f, a, b)

            else:
                res_b = metodo_biseccion(f, a, b, tol, max_iter)
                res_fp = metodo_falsa_posicion(f, a, b, tol, max_iter)
                self._render([res_b, res_fp], f, a, b)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _render(self, resultados: List[Dict], f: Callable[[float], float], a: float, b: float) -> None:
        self._render_table(resultados)
        self._render_plots(resultados, f, a, b)
        self._render_final(resultados)

    def _render_table(self, resultados: List[Dict]) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)

        # interleave rows: method name on each row
        for res in resultados:
            metodo = res["metodo"]
            for fila in res["tabla"]:
                err_rel_pct = fila["error_rel"] * 100 if np.isfinite(fila["error_rel"]) else float("inf")
                self.tree.insert("", "end", values=(
                    metodo,
                    fila["n"],
                    fmt_float(fila["a"]),
                    fmt_float(fila["b"]),
                    fmt_float(fila["c"]),
                    f"{fila['f_c']:.8e}",
                    f"{fila['error_abs']:.8e}",
                    f"{err_rel_pct:.6f}",
                ))

    def _render_plots(self, resultados: List[Dict], f: Callable[[float], float], a: float, b: float) -> None:
        self.ax_func.clear()
        self.ax_err.clear()

        # Function plot
        x = np.linspace(a, b, 600)
        y = np.array([f(xi) for xi in x], dtype=float)

        self.ax_func.plot(x, y)
        self.ax_func.axhline(0.0)
        self.ax_func.set_title("f(x) + iteraciones")
        self.ax_func.set_xlabel("x")
        self.ax_func.set_ylabel("f(x)")

        # plot iteration points per method
        for res in resultados:
            pts = [r["c"] for r in res["tabla"]]
            vals = [f(p) for p in pts]
            self.ax_func.scatter(pts, vals, s=20, label=res["metodo"])

        self.ax_func.legend()

        # Error convergence (absolute error) in log scale
        self.ax_err.set_title("Convergencia del error (abs) - escala log")
        self.ax_err.set_xlabel("Iteración")
        self.ax_err.set_ylabel("Error abs")
        self.ax_err.set_yscale("log")

        for res in resultados:
            errs = [r["error_abs"] for r in res["tabla"] if r["error_abs"] > 0]
            if len(errs) > 0:
                self.ax_err.plot(range(1, len(errs) + 1), errs, label=res["metodo"])

        self.ax_err.legend()
        self.canvas.draw()

    def _render_final(self, resultados: List[Dict]) -> None:
        lines = []
        for res in resultados:
            lines.append(
                f"{res['metodo']}: raíz≈{res['raiz']:.10f}, iter={res['iteraciones']}, "
                f"err_final={res['error_final']:.2e}, tiempo={res['tiempo']:.6f}s"
            )

        self.lbl_final.config(text=" | ".join(lines))

        # simple analysis
        if len(resultados) == 2:
            r1, r2 = resultados[0], resultados[1]
            faster = min(resultados, key=lambda r: (r["iteraciones"], r["tiempo"]))
            other = r2 if faster is r1 else r1

            analysis = (
                f"Análisis: Converge más rápido **{faster['metodo']}** "
                f"(menos iteraciones/tiempo). En general, Falsa Posición suele mejorar "
                f"porque usa interpolación lineal, mientras Bisección parte el intervalo a la mitad. "
                f"Pero Falsa Posición puede estancarse si un extremo queda casi fijo."
            )
            self.lbl_analysis.config(text=analysis)
        else:
            self.lbl_analysis.config(text="")

    def limpiar(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.ax_func.clear()
        self.ax_err.clear()
        self.canvas.draw()
        self.lbl_final.config(text="(aquí aparecerán las métricas)")
        self.lbl_analysis.config(text="")

    def abrir_ej3(self) -> None:
        win = tk.Toplevel(self.root)
        VentanaEjercicio3(win)

    def abrir_ej4(self) -> None:
        win = tk.Toplevel(self.root)
        VentanaEjercicio4(win)

    def abrir_ej5(self) -> None:
        win = tk.Toplevel(self.root)
        VentanaEjercicio5(win)