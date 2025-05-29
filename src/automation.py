import pyautogui

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.utils import confirm_logout

from tkinter import messagebox
from ttkbootstrap.constants import NORMAL

def iniciar_navegador():
    options = Options()
    options.add_argument("--start-maximized")
    navegador = webdriver.Chrome(options=options)
    print('Navegador iniciado...')
    return navegador

def acessar_site(navegador):
    try:
        navegador.get('https://accounts.tiny.com.br/realms/tiny/protocol/openid-connect/auth?client_id=tiny-webapp&redirect_uri=https://erp.tiny.com.br/login&scope=openid&response_type=code')
        print('Acessando o site do Tiny...')
    except Exception as e:
        print('❌ Erro ao acessar o site:', e)

def realizar_login(navegador, username, password):
    try:
        WebDriverWait(navegador,10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='username']"))).send_keys(username)
        print('✅ Login inserido')

        botao_avancar = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Avançar')]")))
        botao_avancar.click()

        WebDriverWait(navegador,10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='password']"))).send_keys(password)
        print('✅ Senha inserida')

        botao_entrar = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Entrar')]")))
        botao_entrar.click()

        try:
            segundo_botao = WebDriverWait(navegador, 3).until(
                EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-primary' and contains(text(), 'login')]")))
            if segundo_botao.is_displayed():
                segundo_botao.click()
                print('✅ Segundo login clicado')
        except Exception:
            print('🔸 Segundo login não necessário, seguindo...')
            time.sleep(5)
        pyautogui.press('enter')
        print('✅ Enter pressionado para fechar pop-up')
        time.sleep(3)
        try:
            segundo_botao = WebDriverWait(navegador, 3).until(
                EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-primary' and contains(text(), 'login')]")))
            if segundo_botao.is_displayed():
                segundo_botao.click()
                print('✅ Terceiro login clicado')
        except Exception:
            print('🔸 Terceiro login não necessário, seguindo...')
            time.sleep(3)    
    except Exception as e:
        print(f'❌ Erro ao realizar o login: {e}')

def link_anuncios(navegador):
    try:
        navegador.get('https://erp.tiny.com.br/anuncios')
        WebDriverWait(navegador,10)
        print('✅ Página de anúncios acessada')
    except Exception as e:
        print(f'❌ Erro ao acessar a página de anúncios: {e}')

def anuncios_opcoes(navegador, marketplace, mlb, max_tentativas=3):
    print(f"Marketplace recebido na função: {marketplace}")
    marketplaces = {
        'ML_FILIAL MG': "//*[@id='widgets-anuncios']/div/div/div/div/div[3]/div[2]/div/a",
        'ML_NE SHOP': "//*[@id='widgets-anuncios']/div/div/div[1]/div/div[3]/div[2]/div/a",
        'ML_NEVENDAS': "//*[@id='widgets-anuncios']/div/div/div[2]/div/div[3]/div[2]/div/a",
        'ML_NESHOP LEDS': "//*[@id='widgets-anuncios']/div/div/div[3]/div/div[3]/div[2]/div/a"
    }
    if marketplace not in marketplaces:
        print(f"⚠️ Marketplace '{marketplace}' não encontrado na lista!")
        return  
    xpath = marketplaces[marketplace]
    for tentativa in range(1, max_tentativas + 1):
        try:
            navegador.get('https://erp.tiny.com.br/anuncios')
            print(f"🔄 Tentativa {tentativa} de acessar marketplace: {marketplace}")

            elemento = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath)))
            elemento.click()
            print(f"✅ Acessando anúncios do marketplace: {marketplace}")
            time.sleep(3)

            botao_importar_anuncio_xpath = "//*[@id='page-wrapper']/div[3]/div[2]/div[1]/div[1]/div/div[1]/button"
            botao_importar_anuncio = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, botao_importar_anuncio_xpath)))
            botao_importar_anuncio.click()
            print("✅ Botão de importar anúncio clicado")
            time.sleep(3)

            radio = navegador.find_element(By.XPATH, "//input[@type='radio' and @value='I']")
            navegador.execute_script("arguments[0].click();", radio)
            print("✅ Opção de importação marcada")
            time.sleep(3)

            colar_mlb = WebDriverWait(navegador, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='bs-modal']/div/div/div/div[2]/div[1]/div[3]/div[1]/div/div/div[4]/input")))
            colar_mlb.clear()
            colar_mlb.send_keys(mlb)
            print(f'✅ Colado o MLB: {mlb}')

            WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='bs-modal']/div/div/div/div[3]/button[4]"))).click()
            print("✅ Importação confirmada")
            time.sleep(3)
            break  
        except Exception as e:
            print(f"⚠️ Erro na tentativa {tentativa}: {e}")
            time.sleep(5)  
            if tentativa == max_tentativas:
                print(f"❌ Falha ao acessar marketplace '{marketplace}' após {max_tentativas} tentativas!")
    print("🔄 Retornando à página de anúncios...")

    navegador.get('https://erp.tiny.com.br/anuncios')
    WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("✅ Página de anúncios recarregada!")

def marcar_skus(navegador, sku, marketplace):  
    print(f"Marketplace recebido na função: {marketplace}")
    marketplaces_2 = {
        'ML_FILIAL MG': "//*[@id='widgets-anuncios']/div/div/div/div/div[3]/div[2]/div/a",
        'ML_NE SHOP': "//*[@id='widgets-anuncios']/div/div/div[1]/div/div[3]/div[2]/div/a",
        'ML_NEVENDAS': "//*[@id='widgets-anuncios']/div/div/div[2]/div/div[3]/div[2]/div/a",
        'ML_NESHOP LEDS': "//*[@id='widgets-anuncios']/div/div/div[3]/div/div[3]/div[2]/div/a"
    }
    if marketplace not in marketplaces_2:
        print(f"⚠️ Marketplace '{marketplace}' não encontrado na lista!")
        return  
    try:
        xpath = marketplaces_2[marketplace]
        elemento = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        elemento.click()
        print(f"✅ Acessando anúncios do marketplace: {marketplace}")

        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    except:
        return
    
    time.sleep(5)
    filtros = WebDriverWait(navegador,10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "a.filter-label.filter-toggle[data-label='avancado']")))
    filtros.click()

    filtro_naorelacionados = WebDriverWait(navegador,10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='filtroRelacionados']/option[3]")))
    filtro_naorelacionados.click()

    filtros_aplicar = WebDriverWait(navegador,10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "button.btn.btn-primary.filter-apply")))
    filtros_aplicar.click()

def marcar_checkbox(navegador):
    try:
        wait = WebDriverWait(navegador, 10)
            
        elemento_pai = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//th[contains(@class, 'checkbox-datatable')]")))
        navegador.execute_script("arguments[0].click();", elemento_pai)
        print("✅ Checkbox marcado!")

    except Exception as e2:
        print(f"❌ Erro ao marcar via JavaScript: {e2}")
        time.sleep(3)

    
    mais_acoes = WebDriverWait(navegador,10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='page-wrapper']/div[3]/div[2]/div[4]/div[2]/div[3]/div[2]/button")))
    mais_acoes.click()

    relacionar_anuncios = WebDriverWait(navegador,10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='page-wrapper']/div[3]/div[2]/div[4]/div[2]/div[3]/div[2]/div/ul/li[4]/a")))
    relacionar_anuncios.click()
    time.sleep(3)

    relacionar_botao = WebDriverWait(navegador,10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='relacionarAnunciosPopup']/div/div/div[3]/button[2]")))
    relacionar_botao.click()
    time.sleep(5)

    fechar_botao = WebDriverWait(navegador,10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='relacionarAnunciosPopup']/div/div/div[3]/button[5]")))
    fechar_botao.click()

def tela_produtos(navegador, sku):
    try:
        navegador.get('https://erp.tiny.com.br/produtos#list')
        WebDriverWait(navegador,10)
        print('✅ Página produtos acessada')
        
        campo_pesquisa = WebDriverWait(navegador,10).until(
            EC.visibility_of_element_located((By.ID,"pesquisa-mini")))
        campo_pesquisa.send_keys(sku)
        time.sleep(2)
        print(f"🔍 Pesquisando o SKU: {sku}")

        campo_pesquisa.send_keys(Keys.RETURN)
        print("✅ Clicou no botão de busca.")
        time.sleep(3)

        WebDriverWait(navegador,10).until(
            EC.visibility_of_element_located((By.XPATH, "//table/tbody/tr[1]/td[4]"))
        ).click()
        print(f"✅ Clicou no SKU: {sku}")
        try:
            WebDriverWait(navegador,10).until(
                EC.visibility_of_element_located((By.XPATH,"//*[@id='page-wrapper']/div[5]/div[1]/div/div[2]/button"))).click()
            print("✅ Clicou no botão 'Mais Ações'")
            time.sleep(2)

            WebDriverWait(navegador,10).until(
                EC.visibility_of_element_located((By.XPATH,"//*[@id='im_14']/a"))).click()
            print("✅ Clicou no botão 'Enviar estoque ao E-commerce'")
            time.sleep(2)

            WebDriverWait(navegador,10).until(
                EC.visibility_of_element_located((By.XPATH,"//*[@id='bs-modal']/div/div/div/div[2]/div[3]/div[2]/div/button/span"))).click()
            print("✅ Clicou em 'Selecionar um ou mais'")
            time.sleep(3)
        except Exception as e:
            print(f'❌ Erro ao clicar no botão "Selecionar um ou mais": {e}')

        try:
            checkbox = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox' and @value='multiselect-all']")))
            checkbox.click()
            print("✅ Checkbox marcado!")
            time.sleep(3)
        except Exception as e:
            print(f"❌ Erro ao marcar checkbox diretamente: {e}")

            try:
                checkbox = navegador.find_element(By.XPATH, "//input[@type='checkbox' and @value='multiselect-all']")
                navegador.execute_script("arguments[0].click();", checkbox)
                print("⚠️ Checkbox marcado via JavaScript!")
            except Exception as e:
                print(f"❌ Erro ao marcar checkbox via JavaScript: {e}")
                try:
                    elemento_pai = navegador.find_element(By.XPATH, "//li[contains(@class, 'multiselect-all')]/a")
                    navegador.execute_script("arguments[0].click();", elemento_pai)
                    print("⚠️ Checkbox marcado ao clicar no elemento pai!")
                except Exception as e:
                    print(f"❌ Erro ao marcar checkbox clicando no elemento pai: {e}")
                time.sleep(3)
    except Exception as e:
        print(f'❌ Erro ao pesquisar produtos: {e}')

def botao_selecionar(navegador):
    try:
        botao_selecionar = WebDriverWait(navegador,10).until(
            EC.visibility_of_element_located((By.XPATH,"//*[@id='bs-modal']/div/div/div/div[3]/button[2]")))
        botao_selecionar.click()
        print("✅ Clicou em 'Selecionar'")
        time.sleep(2)

        enviar = WebDriverWait(navegador,10).until(
            EC.visibility_of_element_located((By.XPATH,"//*[@id='btn-sincronizar-estoques-ecommerce']")))
        enviar.click()
        print("✅ Clicou em 'Enviar'")
        time.sleep(20)

        WebDriverWait(navegador,10).until(
            EC.visibility_of_element_located((By.XPATH,"//*[@id='bs-modal']/div/div/div/div[3]/button[7]"))).click()
        print('✅ Clicou em "Fechar"')
        
    except Exception as e:
        print(f'❌ Erro ao clicar em "Selecionar": {e}')
def logout_tiny(navegador):
    if confirm_logout():
        menu_botao = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='main-menu']/div[2]/div[1]/div[1]/div[2]/ul/li[4]/a/div/div/div")))
        menu_botao.click()

        logout_button = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='main-menu']/div[2]/div[2]/nav[6]/div[2]/a")))
        logout_button.click()
        print("✅ Logout realizado com sucesso!")

    else:
        print("✖️ Logout cancelado pelo usuário.")

def run_automation(dados, username, password,
                   window, text_mlbs, entry_sku,
                   combobox, btn_enviar):
    try:
        navegador = iniciar_navegador()
        acessar_site(navegador)
        realizar_login(navegador, username, password)
        link_anuncios(navegador)
        
        for sku, mlb, marketplace in dados:
            anuncios_opcoes(navegador, marketplace, mlb)
        
        marcar_skus(navegador, sku, marketplace)
        try:
            marcar_checkbox(navegador)
        except Exception as e:
            print(f"⚠️ Nenhum SKU relacionado ou erro na marcação de checkbox: {e}")
        if dados:
            tela_produtos(navegador, dados[0][0])
        botao_selecionar(navegador)
        logout_tiny(navegador)

    except Exception as e:
        print("❌ Erro na automação:", e)

    finally:
        
        def after_logout_actions():
            fechar = messagebox.askyesno(
                "Encerrar Automação",
                "Deseja encerrar o navegador?"
            )
            if fechar:
                try:
                    navegador.quit()
                except:
                    pass

            btn_enviar.config(state=NORMAL, text="Iniciar Automação")
            entry_sku.delete(0, 'end')
            combobox.set("ML_NE SHOP")
            messagebox.showinfo(
                "Pronto",
                "Automação finalizada! Você pode executar novamente."
            )
        window.after(0, after_logout_actions)