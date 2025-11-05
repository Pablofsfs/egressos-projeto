import pandas as pd
import yagmail
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import csv
from datetime import datetime

REMETENTE = "estagioteste045@gmail.com"
SENHA = "ewwf rqbf dysq xotv"
ASSUNTO = "Sua trajetória na Fatec Zona Leste continua fazendo história 💙"
HISTORICO_PATH = "historico_envios.csv"

arquivo_selecionado = None

def encontrar_coluna(colunas, termos_possiveis):
    for termo in termos_possiveis:
        for coluna in colunas:
            if termo.lower() in coluna.lower():
                return coluna
    return None

def enviar_emails():
    try:
        if not arquivo_selecionado:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado.")
            return

        egressos = pd.read_csv(arquivo_selecionado, sep=';', encoding='utf-8')
        egressos.columns = egressos.columns.str.strip()

        coluna_nome = encontrar_coluna(egressos.columns, ['nome', 'nome completo'])
        coluna_email = encontrar_coluna(egressos.columns, ['email', 'e-mail'])

        if not coluna_nome or not coluna_email:
            raise ValueError("As colunas 'nome' e/ou 'email' não foram encontradas.")

        yag = yagmail.SMTP(user=REMETENTE, password=SENHA)
        total = len(egressos)

        for _, row in egressos.iterrows():
            nome = row[coluna_nome]
            email = row[coluna_email]

            corpo = f"""
Olá, {nome}!

Você fez parte de uma jornada que transforma vidas — a da Fatec Zona Leste. E agora, queremos continuar escrevendo essa história com você.

Estamos realizando um levantamento especial com nossos egressos para entender melhor os caminhos que nossos ex-alunos trilharam após a graduação. Sua experiência é valiosa e inspiradora, e pode ajudar a fortalecer ainda mais nossa comunidade acadêmica.

📲 Por isso, convidamos você a preencher um breve requerimento diretamente pelo nosso aplicativo. É rápido, prático e faz toda a diferença!

A Fatec Zona Leste se orgulha de cada profissional que passou por aqui — e você é parte fundamental dessa trajetória de excelência. Contamos com sua participação!

Com carinho,  
Equipe Fatec Zona Leste
            """

            yag.send(to=email, subject=ASSUNTO, contents=corpo)

        yag.send(to=REMETENTE, subject="Resumo de envio Fatec", contents=f"Foram enviados {total} e-mails com sucesso usando o arquivo '{os.path.basename(arquivo_selecionado)}'.")

        with open(HISTORICO_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow([os.path.basename(arquivo_selecionado), datetime.now().strftime('%d/%m/%Y %H:%M'), total, "Sucesso"])

        carregar_historico()
        messagebox.showinfo("Sucesso", f"{total} e-mails enviados com sucesso.")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def abrir_modal():
    modal = tk.Toplevel(root)
    modal.iconbitmap(r"C:\Users\FATEC ZONA LESTE\Documents\GitHub\egressos-projeto\FATEC_ZONA_LESTE.ico")
    modal.title("Gerenciar CSV")
    modal.geometry("550x350")
    modal.configure(bg="#ffffff")
    modal.grab_set()

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

    def mostrar_csv_modal(df):
        for widget in frame_csv_modal.winfo_children():
            widget.destroy()

        tree = ttk.Treeview(frame_csv_modal, columns=list(df.columns), show="headings", height=12, style="Custom.Treeview")
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=160)

        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack(pady=5)

    # Layout do modal
    label_arquivo_modal = tk.Label(modal, text="Nenhum arquivo selecionado", bg="#ffffff", fg="#333333", font=("Times New Roman", 11))
    label_arquivo_modal.pack(pady=10)

    botoes_modal = tk.Frame(modal, bg="#ffffff")
    botoes_modal.pack(pady=5)

    btn_selecionar_modal = tk.Button(botoes_modal, text="Selecionar Arquivo", command=selecionar_arquivo_modal, bg="#990000", fg="white", font=("Times New Roman", 11, "bold"), width=18)
    btn_selecionar_modal.grid(row=0, column=0, padx=5)

    btn_enviar_modal = tk.Button(botoes_modal, text="Enviar E-mails", command=lambda: threading.Thread(target=enviar_emails).start(), bg="#006600", fg="white", font=("Times New Roman", 11, "bold"), width=18)
    btn_enviar_modal.grid(row=0, column=1, padx=5)

    btn_excluir_modal = tk.Button(botoes_modal, text="Excluir Arquivo", command=excluir_arquivo_modal, bg="#990000", fg="white", font=("Times New Roman", 11, "bold"), width=18)
    btn_excluir_modal.grid(row=0, column=2, padx=5)

    btn_fechar_modal = tk.Button(modal, text="Fechar", command=modal.destroy, bg="#666666", fg="white", font=("Times New Roman", 11), width=12)
    btn_fechar_modal.pack(pady=10)

    frame_csv_modal = tk.Frame(modal, bg="#ffffff")
    frame_csv_modal.pack(pady=10)

def carregar_historico():
    for row in historico_tree.get_children():
        historico_tree.delete(row)

    if os.path.exists(HISTORICO_PATH):
        with open(HISTORICO_PATH, newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            for linha in reader:
                historico_tree.insert("", "end", values=linha)

def ordenar_treeview(coluna, reverso):
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

# Interface principal
root = tk.Tk()

root.iconbitmap(r"C:\Users\FATEC ZONA LESTE\Documents\GitHub\egressos-projeto\FATEC_ZONA_LESTE.ico")

root.title("Envio de E-mails - Fatec Zona Leste")
root.geometry("700x550")
root.configure(bg="#ffffff")

topo = tk.Frame(root, bg="#990000", height=60)
topo.pack(fill="x")

titulo = tk.Label(topo, text="Envio de E-mails para Egressos", bg="#990000", fg="white", font=("Times New Roman", 16, "bold"))
titulo.pack(pady=15)

btn_abrir_modal = tk.Button(root, text="Selecionar CSV", command=abrir_modal, bg="#990000", fg="white", font=("Times New Roman", 12, "bold"), width=20)
btn_abrir_modal.pack(pady=15)

label_hist = tk.Label(root, text="Histórico de Envios:", bg="#ffffff", fg="#333333", font=("Times New Roman", 12, "bold"))
label_hist.pack(pady=10)

style = ttk.Style()
style.configure("Custom.Treeview", borderwidth=1, relief="solid", font=("Times New Roman", 10))
style.configure("Custom.Treeview.Heading", font=("Times New Roman", 11, "bold"))

historico_tree = ttk.Treeview(root, columns=("Arquivo", "Data", "Total", "Status"), show="headings", height=8, style="Custom.Treeview")
historico_tree.heading("Arquivo", text="Arquivo", command=lambda: ordenar_treeview("Arquivo", False))
historico_tree.heading("Data", text="Data", command=lambda: ordenar_treeview("Data", False))
historico_tree.heading("Total", text="Total", command=lambda: ordenar_treeview("Total", False))
historico_tree.heading("Status", text="Status", command=lambda: ordenar_treeview("Status", False))

historico_tree.column("Arquivo", anchor="w", width=200)
historico_tree.column("Data", anchor="center", width=140)
historico_tree.column("Total", anchor="center", width=80)
historico_tree.column("Status", anchor="center", width=100)

historico_tree.pack(pady=5)

carregar_historico()

# Rodapé institucional
rodape = tk.Frame(root, bg="#990000", height=40)
rodape.pack(side="bottom", fill="x")

rodape_label = tk.Label(rodape, text="Fatec Zona Leste © 2025  \n Desenvolvido por Pablo Sena", bg="#990000", fg="white", font=("Times New Roman", 10))
rodape_label.pack(pady=10)

root.mainloop()
