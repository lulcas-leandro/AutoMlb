import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from ttkbootstrap.constants import LINK

import threading

from src.utils import resource_path
from src.automation import run_automation

def capturar_dados():
    window = tb.Window(title="Entrada de Dados para Automação MLB", themename="yeti")
    window.iconbitmap(resource_path("assets/assistente-de-robo.ico"))
    window.geometry("750x550")
    window.resizable(False, False)

    tb.Label(window, text="Cole os MLBs (separados por espaço ou linha):")\
      .grid(row=0, column=0, padx=10, pady=(15,5), sticky="w")
    text_mlbs = ScrolledText(window, width=50, height=16, font=("Segoe UI", 10))
    text_mlbs.grid(row=0, column=1, padx=10, pady=(15,5))

    tb.Label(window, text="Digite o SKU:")\
      .grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_sku = tb.Entry(window, width=50)
    entry_sku.grid(row=2, column=1, padx=10, pady=5)

    tb.Label(window, text="Selecione o Marketplace:")\
      .grid(row=3, column=0, padx=10, pady=5, sticky="w")
    combobox_marketplace = tb.Combobox(
        window,
        values=["ML_NE SHOP", "ML_NEVENDAS", "ML_NESHOP LEDS",'ML_FILIAL MG'],
        width=47
    )
    combobox_marketplace.grid(row=3, column=1, padx=10, pady=5)
    combobox_marketplace.set("ML_NE SHOP")

    tb.Label(window, text="Usuario Tiny:")\
      .grid(row=4, column=0, padx=10, pady=5, sticky="w")
    entry_user = tb.Entry(window, width=50)
    entry_user.grid(row=4, column=1, padx=10, pady=5)

    tb.Label(window, text="Senha Tiny:")\
      .grid(row=5, column=0, padx=10, pady=5, sticky="w")
    entry_pass = tb.Entry(window, width=50, show="*")
    entry_pass.grid(row=5, column=1, padx=10, pady=5)

    btn_enviar = tb.Button(window, text="Iniciar Automação", bootstyle=SUCCESS)
    btn_enviar.grid(row=6, column=0, columnspan=2, pady=20)

    def enviar():
        mlbs_str = text_mlbs.get("1.0", "end").strip()
        sku_val = entry_sku.get().strip()
        marketplace_val = combobox_marketplace.get().strip()
        if not mlbs_str or not sku_val or not marketplace_val:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return
        user_val = entry_user.get().strip()
        pass_val = entry_pass.get().strip()
        if not user_val or not pass_val:
            messagebox.showerror("Erro", "Informe usuário e senha do Tiny.")
            return

        mlb_list = [x for x in mlbs_str.split() if x.strip()]
        dados = [(sku_val, mlb, marketplace_val) for mlb in mlb_list]

        btn_enviar.config(state=DISABLED, text="Executando...")

        threading.Thread(
            target=run_automation,
            args=(dados, user_val, pass_val,
             window, text_mlbs, entry_sku,
           combobox_marketplace, btn_enviar),
            daemon=True
        ).start()

    btn_enviar.config(command=enviar)
    window.mainloop()
