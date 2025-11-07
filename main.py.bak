import tkinter as tk
import time
from views.tela_principal import criar_tela_principal

def mostrar_splash(root):
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    splash.geometry("400x300+500+200")
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
