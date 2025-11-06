import time

def enviar_emails(arquivo_csv):
    if not arquivo_csv:
        print("Nenhum arquivo selecionado para envio.")
        return

    print(f"Iniciando envio de e-mails com {arquivo_csv}...")
    time.sleep(2)  # Simula tempo de envio
    print("E-mails enviados com sucesso.")
