import pandas as pd
import yagmail
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

# Configurações do e-mail
REMETENTE = "estagioteste045@gmail.com"
SENHA = "xvhp iefx pqfj kjog"
ASSUNTO = "Sua trajetória na Fatec Zona Leste continua fazendo história 💙"

# Função para encontrar coluna por nome aproximado
def encontrar_coluna(colunas, termos_possiveis):
    for termo in termos_possiveis:
        for coluna in colunas:
            if termo.lower() in coluna.lower():
                return coluna
    return None

# Função principal de envio
def enviar_emails(caminho_csv, barra, root):
    try:
        egressos = pd.read_csv(caminho_csv, sep=';', encoding='utf-8')
        egressos.columns = egressos.columns.str.strip()

        # Detecta colunas principais
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
            barra['value'] = ((i + 1) / total) * 100
            root.update_idletasks()

        messagebox.showinfo("Sucesso", "Todos os e-mails foram enviados com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Interface gráfica
def iniciar_envio():
    caminho = filedialog.askopenfilename(title="Selecione o CSV", filetypes=[("CSV files", "*.csv")])
    if caminho:
        barra = ttk.Progressbar(root, length=300, mode='determinate')
        barra.pack(pady=10)
        threading.Thread(target=enviar_emails, args=(caminho, barra, root)).start()

root = tk.Tk()
root.title("Envio de E-mails - Fatec Zona Leste")
root.geometry("400x200")

label = tk.Label(root, text="Clique abaixo para selecionar o arquivo CSV dos egressos:")
label.pack(pady=20)

botao = tk.Button(root, text="Selecionar CSV e Enviar", command=iniciar_envio)
botao.pack()

root.mainloop()
