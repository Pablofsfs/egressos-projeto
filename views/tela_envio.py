import tkinter as tk
from tkinter import ttk
import csv
import os
from datetime import datetime

HISTORICO_PATH = "historico_envios.csv"
historico_tree = None

def configurar_treeview(root):
    global historico_tree

    style = ttk.Style()
    style.configure("Custom.Treeview", borderwidth=1, relief="solid", font=("Times New Roman", 10))
    style.configure("Custom.Treeview.Heading", font=("Times New Roman", 11, "bold"))

    historico_tree = ttk.Treeview(root, columns=("Arquivo", "Data", "Total", "Status"), show="headings", height=8, style="Custom.Treeview")
    for col in ("Arquivo", "Data", "Total", "Status"):
        historico_tree.heading(col, text=col, command=lambda c=col: ordenar_treeview(c, False))

    historico_tree.column("Arquivo", anchor="w", width=200)
    historico_tree.column("Data", anchor="center", width=140)
    historico_tree.column("Total", anchor="center", width=80)
    historico_tree.column("Status", anchor="center", width=100)

    historico_tree.pack(pady=5)
    carregar_historico()

    return historico_tree

def carregar_historico():
    global historico_tree
    for row in historico_tree.get_children():
        historico_tree.delete(row)

    if os.path.exists(HISTORICO_PATH):
        with open(HISTORICO_PATH, newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            for linha in reader:
                historico_tree.insert("", "end", values=linha)

def ordenar_treeview(coluna, reverso):
    global historico_tree
    dados = [(historico_tree.set(k, coluna), k) for k in historico_tree.get_children()]
    try:
        if coluna == "Total":
            dados.sort(key=lambda t: int(t[0]), reverse=reverso)
        elif coluna == "Data":
            dados.sort(key=lambda t: datetime.strptime(t[0], "%d/%m/%Y %H:%M"), reverse=reverso)
        else:
            dados.sort(key=lambda t: t[0].lower(), reverse=reverso)
    except:
        dados.sort(reverse=reverso)

    for index, (val, k) in enumerate(dados):
        historico_tree.move(k, '', index)

    historico_tree.heading(coluna, command=lambda: ordenar_treeview(coluna, not reverso))
