import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import os
import threading
from envio import enviar_emails
from views.tela_envio import carregar_historico

arquivo_selecionado = None

def centralizar_janela(janela, largura=600, altura=400):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)

    janela.geometry(f"{largura}x{altura}+{x}+{y}")


def abrir_modal(root):
    global arquivo_selecionado
    modal.iconbitmap(caminho_relativo("assets/FATEC_ZONA_LESTE.ico"))
    modal = tk.Toplevel(root)
    modal.title("Gerenciar CSV")
    modal.geometry("600x400")
    modal.configure(bg="#ffffff")
    modal.grab_set()

    label_arquivo_modal = tk.Label(modal, text="Nenhum arquivo selecionado", bg="#ffffff", fg="#333333", font=("Times New Roman", 11))
    label_arquivo_modal.pack(pady=10)

    frame_csv_modal = tk.Frame(modal, bg="#ffffff")
    frame_csv_modal.pack(pady=10, fill="both", expand=True)

    def mostrar_csv_modal(df):
        for widget in frame_csv_modal.winfo_children():
            widget.destroy()

        tree = ttk.Treeview(frame_csv_modal, columns=list(df.columns), show="headings", height=12)
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=160)

        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack(pady=5, fill="both", expand=True)

    def selecionar_arquivo_modal():
        global arquivo_selecionado
        caminho = filedialog.askopenfilename(title="Selecione o CSV", filetypes=[("CSV files", "*.csv")])
        if caminho:
            arquivo_selecionado = caminho
            label_arquivo_modal.config(text=f"Arquivo: {os.path.basename(caminho)}")
            try:
                df = pd.read_csv(caminho, sep=';', encoding='utf-8')
                mostrar_csv_modal(df)
            except Exception as e:
                messagebox.showerror("Erro ao carregar CSV", f"O arquivo não pôde ser exibido: {e}")

    def excluir_arquivo_modal():
        global arquivo_selecionado
        arquivo_selecionado = None
        label_arquivo_modal.config(text="Nenhum arquivo selecionado")
        for widget in frame_csv_modal.winfo_children():
            widget.destroy()

    def enviar_e_atualizar():
        enviar_emails(arquivo_selecionado)
        carregar_historico()

    botoes_modal = tk.Frame(modal, bg="#ffffff")
    botoes_modal.pack(pady=5)

    btn_selecionar_modal = tk.Button(botoes_modal, text="Selecionar Arquivo", command=selecionar_arquivo_modal, bg="#990000", fg="white", font=("Times New Roman", 11, "bold"), width=18)
    btn_selecionar_modal.grid(row=0, column=0, padx=5)

    btn_enviar_modal = tk.Button(botoes_modal, text="Enviar E-mails", command=lambda: threading.Thread(target=enviar_e_atualizar).start(), bg="#006600", fg="white", font=("Times New Roman", 11, "bold"), width=18)
    btn_enviar_modal.grid(row=0, column=1, padx=5)

    btn_excluir_modal = tk.Button(botoes_modal, text="Excluir Arquivo", command=excluir_arquivo_modal, bg="#990000", fg="white", font=("Times New Roman", 11, "bold"), width=18)
    btn_excluir_modal.grid(row=0, column=2, padx=5)

    btn_fechar_modal = tk.Button(modal, text="Fechar", command=modal.destroy, bg="#666666", fg="white", font=("Times New Roman", 11), width=12)
    btn_fechar_modal.pack(pady=10)
