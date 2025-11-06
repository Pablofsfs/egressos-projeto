import csv
import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import yagmail

# Configurações do e-mail
REMETENTE = "estagioteste045@gmail.com"
SENHA = "ewwf rqbf dysq xotv"
ASSUNTO = "Sua trajetória na Fatec Zona Leste continua fazendo história 💙"
HISTORICO_PATH = "historico_envios.csv"

def mostrar_envio_popup():
    popup = tk.Toplevel()
    popup.title("Enviando e-mails...")
    popup.geometry("300x100")
    popup.configure(bg="white")
    popup.resizable(False, False)

    label = tk.Label(popup, text="Enviando e-mails, aguarde...", font=("Arial", 12), bg="white")
    label.pack(pady=20)

    popup.update()
    return popup

def encontrar_coluna(colunas, candidatos):
    for nome in colunas:
        if nome.strip().lower() in [c.strip().lower() for c in candidatos]:
            return nome
    return None

def enviar_emails(arquivo_csv):
    if not arquivo_csv or not os.path.exists(arquivo_csv):
        messagebox.showerror("Erro", "Nenhum arquivo válido selecionado.")
        return

    popup = mostrar_envio_popup()

    try:
        egressos = pd.read_csv(arquivo_csv, sep=';', encoding='utf-8')
        coluna_nome = encontrar_coluna(egressos.columns, ['nome', 'name'])
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

            try:
                yag.send(to=email, subject=ASSUNTO, contents=corpo)
                print(f"Enviado para: {email}")
            except Exception as e:
                print(f"Erro ao enviar para {email}: {e}")

        # Envia resumo para o próprio remetente
        resumo = f"Foram enviados {total} e-mails com sucesso usando o arquivo '{os.path.basename(arquivo_csv)}'."
        yag.send(to=REMETENTE, subject="Resumo de envio Fatec", contents=resumo)

        registrar_historico(os.path.basename(arquivo_csv), total, "Sucesso")

    except Exception as e:
        print(f"Erro geral no envio: {e}")
        registrar_historico(os.path.basename(arquivo_csv), 0, "Erro")

    popup.destroy()

def registrar_historico(nome_arquivo, total, status):
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    linha = f"{nome_arquivo};{data};{total};{status}\n"

    try:
        with open(HISTORICO_PATH, "a", encoding="utf-8") as f:
            f.write(linha)
        print("Histórico atualizado.")
    except Exception as e:
        print(f"Erro ao registrar histórico: {e}")
