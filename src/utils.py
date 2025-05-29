import os, sys
from tkinter import messagebox

def resource_path(relative_path):
    base = getattr(sys, '_MEIPASS', os.path.abspath('.'))
    return os.path.join(base, relative_path)

def confirm_logout():
    return messagebox.askyesno("Confirmação de Logout", "Deseja deslogar do Tiny?")

def confirm_exit():
    return messagebox.askyesno("Encerramento do Script", "Deseja encerrar o script?")

