import tkinter as tk
import time
from views.tela_principal import criar_tela_principal

def centralizar_janela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

def mostrar_splash(root):
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    centralizar_janela(splash, 400, 300)  # splash centralizada
    splash.configure(bg="#990000")

    label = tk.Label(splash, text="Fatec Zona Leste", font=("Arial", 24), fg="white", bg="#990000")
    label.pack(expand=True)

    splash.update()
    time.sleep(2.5)  # tempo de exibição
    splash.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # esconde a janela principal
    mostrar_splash(root)
    root.deiconify()  # mostra a janela principal depois da splash
    criar_tela_principal(root)
    root.mainloop()
