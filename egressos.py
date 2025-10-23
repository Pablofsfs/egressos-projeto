import pandas as pd
import yagmail
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import csv
from datetime import datetime

# Configurações do e-mail
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
            raise ValueError("As colunas 'nome' e/ou 'email' não foram encontradas. Verifique o cabeçalho do CSV.")

        yag = yagmail.SMTP(user=REMETENTE, password=SENHA)
        total = len(egressos)

        for i, row in egressos.iterrows():
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

        # Envia confirmação para o próprio remetente
        resumo = f"Foram enviados {total} e-mails com sucesso usando o arquivo '{os.path.basename(arquivo_selecionado)}'."
        yag.send(to=REMETENTE, subject="Resumo de envio Fatec", contents=resumo)

        # Salva histórico
        with open(HISTORICO_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow([os.path.basename(arquivo_selecionado), datetime.now().strftime('%d/%m/%Y %H:%M'), total, "Sucesso"])

        carregar_historico()
        messagebox.showinfo("Sucesso", resumo)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def selecionar_arquivo():
    global arquivo_selecionado
    caminho = filedialog.askopenfilename(title="Selecione o CSV", filetypes=[("CSV files", "*.csv")])
    if caminho:
        arquivo_selecionado = caminho
        label_arquivo.config(text=f"Arquivo: {os.path.basename(caminho)}")
        status_label.config(text=f"Carregado em {datetime.now().strftime('%d/%m/%Y %H:%M')}")

def excluir_arquivo():
    global arquivo_selecionado
    arquivo_selecionado = None
    label_arquivo.config(text="Nenhum arquivo selecionado")
    status_label.config(text="")

def carregar_historico():
    for row in historico_tree.get_children():
        historico_tree.delete(row)

    if os.path.exists(HISTORICO_PATH):
        with open(HISTORICO_PATH, newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            for linha in reader:
                historico_tree.insert("", "end", values=linha)

# Função para ordenar a Treeview
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

# Interface gráfica
root = tk.Tk()
root.title("Envio de E-mails - Fatec Zona Leste")
root.geometry("650x620")
root.configure(bg="#ffffff")

# Topo vermelho
topo = tk.Frame(root, bg="#990000", height=60)
topo.pack(fill="x")

titulo = tk.Label(topo, text="Envio de E-mails para Egressos", bg="#990000", fg="white", font=("Times New Roman", 16, "bold"))
titulo.pack(pady=15)

# Instruções
label_instrucao = tk.Label(root, text="Selecione o arquivo CSV com os dados dos egressos:", bg="#ffffff", fg="#333333", font=("Times New Roman", 12))
label_instrucao.pack(pady=10)

# Botões
botoes_frame = tk.Frame(root, bg="#ffffff")
botoes_frame.pack(pady=5)

btn_selecionar = tk.Button(botoes_frame, text="Selecionar CSV", command=selecionar_arquivo, bg="#990000", fg="white", font=("Times New Roman", 11, "bold"), width=15)
btn_selecionar.grid(row=0, column=0, padx=5)

btn_enviar = tk.Button(botoes_frame, text="Enviar E-mails", command=lambda: threading.Thread(target=enviar_emails).start(), bg="#006600", fg="white", font=("Times New Roman", 11, "bold"), width=15)
btn_enviar.grid(row=0, column=1, padx=5)

btn_excluir = tk.Button(botoes_frame, text="Excluir Arquivo", command=excluir_arquivo, bg="#990000", fg="white", font=("Times New Roman", 11, "bold"), width=15)
btn_excluir.grid(row=0, column=2, padx=5)

# Labels de status
label_arquivo = tk.Label(root, text="Nenhum arquivo selecionado", bg="#ffffff", fg="#333333", font=("Times New Roman", 11))
label_arquivo.pack(pady=5)

status_label = tk.Label(root, text="", bg="#ffffff", fg="#666666", font=("Times New Roman", 10))
status_label.pack(pady=5)

# Estilo da tabela
style = ttk.Style()
style.configure("Custom.Treeview", borderwidth=1, relief="solid", font=("Times New Roman", 10))
style.configure("Custom.Treeview.Heading", font=("Times New Roman", 11, "bold"))

# Histórico
label_hist = tk.Label(root, text="Histórico de Envios:", bg="#ffffff", fg="#333333", font=("Times New Roman", 12, "bold"))
label_hist.pack(pady=10)

historico_tree = ttk.Treeview(root, columns=("Arquivo", "Data", "Total", "Status"), show="headings", height=6, style="Custom.Treeview")
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

# Rodapé
rodape = tk.Frame(root, bg="#990000", height=40)
rodape.pack(side="bottom", fill="x")

rodape_label = tk.Label(rodape, text="Fatec Zona Leste © 2025", bg="#990000", fg="white", font=("Times New Roman", 10))
rodape_label.pack(pady=10)

root.mainloop()
