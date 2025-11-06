import pandas as pd
import yagmail
import os
import csv
from datetime import datetime
from tkinter import messagebox
from views.tela_envio import carregar_historico

REMETENTE = "estagioteste045@gmail.com"
SENHA = "ewwf rqbf dysq xotv"
ASSUNTO = "Sua trajetória na Fatec Zona Leste continua fazendo história 💙"
HISTORICO_PATH = "historico_envios.csv"

def encontrar_coluna(colunas, termos_possiveis):
    for termo in termos_possiveis:
        for coluna in colunas:
            if termo.lower() in coluna.lower():
                return coluna
    return None

def enviar_emails(arquivo_selecionado):
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
