import os
import sys
import tkinter as tk
from views.tela_modal import abrir_modal
from views.tela_envio import configurar_treeview

def caminho_relativo(arquivo):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, arquivo)
    return arquivo

def centralizar_janela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

def criar_tela_principal(root):
    root.title("Envio de E-mails - Fatec Zona Leste")
    centralizar_janela(root, 700, 550)  # tela principal centralizada
    root.configure(bg="#ffffff")
    root.iconbitmap(caminho_relativo("assets/FATEC_ZONA_LESTE.ico"))

    topo = tk.Frame(root, bg="#990000", height=60)
    topo.pack(fill="x")

    titulo = tk.Label(topo, text="Envio de E-mails para Egressos", bg="#990000", fg="white", font=("Times New Roman", 16, "bold"))
    titulo.pack(pady=15)

    btn_abrir_modal = tk.Button(root, text="Selecionar CSV", command=lambda: abrir_modal(root), bg="#990000", fg="white", font=("Times New Roman", 12, "bold"), width=20)
    btn_abrir_modal.pack(pady=15)

    label_hist = tk.Label(root, text="Histórico de Envios:", bg="#ffffff", fg="#333333", font=("Times New Roman", 12, "bold"))
    label_hist.pack(pady=10)

    configurar_treeview(root)

    rodape = tk.Frame(root, bg="#990000", height=40)
    rodape.pack(side="bottom", fill="x")

    rodape_label = tk.Label(rodape, text="Fatec Zona Leste © 2025  \n Desenvolvido por Pablo Sena", bg="#990000", fg="white", font=("Times New Roman", 10))
    rodape_label.pack(pady=10)
