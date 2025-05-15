import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def iniciar_navegador():
    options = Options()
    options.add_argument("--start-maximized")
    navegador = webdriver.Chrome(options=options)
    print('Navegador iniciado em tela cheia')
    return navegador

def acessar_site(navegador):
    try:
        navegador.get(
            'https://accounts.tiny.com.br/realms/tiny/protocol/openid-connect/auth?'
            'client_id=tiny-webapp&redirect_uri=https://erp.tiny.com.br/login&'
            'scope=openid&response_type=code'
        )
        print('Acessando o site do Tiny...')
    except Exception as e:
        print('❌ Erro ao acessar o site:', e)

def realizar_login(navegador, username, password):
    try:
        WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='username']"))
        ).send_keys(username)
        print('✅ Login inserido')
        time.sleep(1)

        botao = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Avançar')]") )
        )
        botao.click()

        WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='password']"))
        ).send_keys(password)
        print('✅ Senha inserida')
        time.sleep(1)

        botao = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Entrar')]") )
        )
        botao.click()
        time.sleep(3)
        try:
            segundo_botao = WebDriverWait(navegador, 3).until(
                EC.presence_of_element_located((By.XPATH,
                    "//button[@class='btn btn-primary' and contains(text(), 'login')]") )
            )
            if segundo_botao.is_displayed():
                segundo_botao.click()
                print('✅ Segundo login clicado')
        except Exception:
            print('🔸 Segundo login não necessário, seguindo...')
            time.sleep(5)

        pyautogui.press('enter')
        print('✅ Enter pressionado para fechar pop-up')
        time.sleep(5)

        try:
            terceiro_botao = WebDriverWait(navegador, 3).until(
                EC.presence_of_element_located((By.XPATH,
                    "//button[@class='btn btn-primary' and contains(text(), 'login')]") )
            )
            if terceiro_botao.is_displayed():
                terceiro_botao.click()
                print('✅ Terceiro login clicado')
        except Exception:
            print('🔸 Terceiro login não necessário, seguindo...')
            time.sleep(3)
    except Exception as e:
        print(f'❌ Erro ao realizar o login: {e}')

def link_anuncios(navegador):
    try:
        navegador.get('https://erp.tiny.com.br/anuncios')
        WebDriverWait(navegador, 10)
        print('Página de anúncios acessada')
        time.sleep(5)
    except Exception as e:
        print(f'❌ Erro ao acessar a página de anúncios: {e}')

def anuncios_opcoes(navegador, marketplace, mlb, max_tentativas=3):
    print(f"Marketplace recebido na função: {marketplace}")
    marketplaces = {
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
            time.sleep(5)
            print(f"🔄 Tentativa {tentativa} de acessar marketplace: {marketplace}")
            elemento = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            elemento.click()
            print(f"✅ Acessando anúncios do marketplace: {marketplace}")
            time.sleep(3)

            botao_importar = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                    "//*[@id='page-wrapper']/div[3]/div[2]/div[1]/div[1]/div/div[1]/button") )
            )
            botao_importar.click()
            print("✅ Botão de importar anúncio clicado")
            time.sleep(3)

            radio = navegador.find_element(By.XPATH, "//input[@type='radio' and @value='I']")
            navegador.execute_script("arguments[0].click();", radio)
            print("✅ Opção de importação marcada")
            time.sleep(5)

            colar_mlb = WebDriverWait(navegador, 10).until(
                EC.visibility_of_element_located((By.XPATH,
                    "//*[@id='bs-modal']/div/div/div/div[2]/div[1]/div[3]/div[1]/div/div/div[4]/input") )
            )
            colar_mlb.clear()
            colar_mlb.send_keys(mlb)
            print(f'✅ Colado o MLB: {mlb}')
            time.sleep(5)

            WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                    "//*[@id='bs-modal']/div/div/div/div[3]/button[4]") )
            ).click()
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
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    print("✅ Página de anúncios recarregada!")
    time.sleep(5)

def marcar_skus(navegador, sku, marketplace):
    print(f"Marketplace recebido na função: {marketplace}")
    marketplaces_2 = {
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
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        elemento.click()
        print(f"✅ Acessando anúncios do marketplace: {marketplace}")
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(3)
    except:
        return
    filtros = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH,
            "//*[@id='page-wrapper']/div[3]/div[2]/div[1]/div[3]/ul/li[1]/a") )
    )
    filtros.click()
    time.sleep(3)
    filtro_naorelacionados = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH,
            "//*[@id='filtroRelacionados']/option[3]") )
    )
    filtro_naorelacionados.click()
    time.sleep(3)
    filtros_aplicar = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH,
            "//*[@id='page-wrapper']/div[3]/div[2]/div[1]/div[3]/ul/li[1]/div/div[5]/button[1]") )
    )
    filtros_aplicar.click()
    time.sleep(3)

def marcar_checkbox(navegador, sku, mlbs):
    for mlb in mlbs:
        try:
            primeiro_botao = navegador.find_element(By.CSS_SELECTOR, 'tr:first-child .ctx-menu-wrapper button')
            primeiro_botao.click()
            time.sleep(3)
            relacionar_anuncio = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='im_12']/a"))
            )
            navegador.execute_script("arguments[0].click();", relacionar_anuncio)
            time.sleep(3)
            print('Clicou em relacionar anuncio')

            colar_sku = WebDriverWait(navegador, 10).until(
                EC.visibility_of_element_located((By.XPATH,
                    "//input[@placeholder='Pesquise por nome, código (SKU) ou GTIN/EAN']") )
            )
            colar_sku.clear()
            colar_sku.send_keys(sku)
            time.sleep(3)
            print('Colou o sku')

            pesquisar_sku = WebDriverWait(navegador, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='bs-modal']/div/div/div/div[2]/div[2]/div[1]/div/div/span[2]/button")))
            pesquisar_sku.click()
            time.sleep(3)
            radio2 = navegador.find_element(By.XPATH, "(//input[@type='radio' and @name='id-produto-rel-anuncio'])[1]")
            navegador.execute_script("arguments[0].click();", radio2)
            print('Marcou radio')
            time.sleep(3)

            botao_continuar = WebDriverWait(navegador, 10).until(
                EC.visibility_of_element_located((By.XPATH,
                    "//*[@id='bs-modal']/div/div/div/div[3]/button[1]") )
            )
            botao_continuar.click()
            print('Clicou em continuar')
            time.sleep(3)

            botao_relacionar = WebDriverWait(navegador, 10).until(
                EC.visibility_of_element_located((By.XPATH,
                    "//*[@id='bs-modal']/div/div/div/div[3]/button[2]") )
            )
            botao_relacionar.click()
            print('Clicou em relacionar')
            time.sleep(3)
            print(f'Anúncio relacionado para o MLB: {mlb}')
        except Exception as e:
            print(f'Erro ao relacionar anúncio para o MLB {mlb}: {e}')

def tela_produtos(navegador, sku):
    try:
        navegador.get('https://erp.tiny.com.br/produtos#list')
        WebDriverWait(navegador, 10)
        print('Página produtos acessada')
        time.sleep(5)
        campo_pesquisa = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located((By.ID, "pesquisa-mini"))
        )
        campo_pesquisa.send_keys(sku)
        print(f"Pesquisando o SKU: {sku}")
        campo_pesquisa.send_keys(Keys.RETURN)
        time.sleep(5)
        WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//table/tbody/tr[1]/td[4]"))
        ).click()
        time.sleep(5)
        try:
            WebDriverWait(navegador, 10).until(
                EC.visibility_of_element_located((By.XPATH,
                    "//*[@id='page-wrapper']/div[5]/div[1]/div/div[2]/button") )
            ).click()
            print("Clicou no botão 'Mais Ações'")
            time.sleep(5)
            WebDriverWait(navegador, 10).until(
                EC.visibility_of_element_located((By.XPATH,
                    "//*[@id='im_14']/a") )
            ).click()
            print("Clicou no botão 'Enviar estoque ao E-commerce'")
            time.sleep(5)
            WebDriverWait(navegador, 10).until(
                EC.visibility_of_element_located((By.XPATH,
                    "//*[@id='bs-modal']/div/div/div/div[2]/div[3]/div[2]/div/button/span") )
            ).click()
            print("Clicou em 'Selecionar um ou mais'")
            time.sleep(3)
        except Exception as e:
            print(f'❌ Erro ao clicar no botão "Selecionar um ou mais": {e}')
        try:
            checkbox = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                    "//input[@type='checkbox' and @value='multiselect-all']") )
            )
            checkbox.click()
            print("✅ Checkbox marcado!")
            time.sleep(5)
        except Exception as e:
            print(f"❌ Erro ao marcar checkbox diretamente: {e}")
            try:
                elemento_pai = navegador.find_element(By.XPATH,
                    "//li[contains(@class, 'multiselect-all')]/a")
                navegador.execute_script("arguments[0].click();", elemento_pai)
                print("⚠️ Checkbox marcado ao clicar no elemento pai!")
            except Exception as e:
                print(f"❌ Erro ao marcar checkbox clicando no elemento pai: {e}")
    except Exception as e:
        print(f'❌ Erro ao pesquisar produtos: {e}')

def botao_selecionar(navegador):
    try:
        botao_selecionar = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located((By.XPATH,
                "//*[@id='bs-modal']/div/div/div/div[3]/button[2]") )
        )
        botao_selecionar.click()
        print("Clicou em 'Selecionar'")
        time.sleep(5)
        enviar = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located((By.XPATH,
                "//*[@id='btn-sincronizar-estoques-ecommerce']") )
        )
        enviar.click()
        print("✅ Clicou em 'Enviar'")
        time.sleep(25)
        WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located((By.XPATH,
                "//*[@id='bs-modal']/div/div/div/div[3]/button[7]") )
        ).click()
        print("Clicou em 'Fechar'")
        time.sleep(5)
    except Exception as e:
        print(f'❌ Erro ao clicar em "Selecionar": {e}')

def run_automation(mlbs, sku, marketplace, user, password):
    navegador = iniciar_navegador()
    try:
        acessar_site(navegador)
        realizar_login(navegador, user, password)
        link_anuncios(navegador)

        for mlb in mlbs:
            anuncios_opcoes(navegador, marketplace, mlb)

        
        for mlb in mlbs:
            marcar_skus(navegador, sku, marketplace)

        
        marcar_checkbox(navegador, sku, mlbs)

        
        if mlbs:
            tela_produtos(navegador, sku)
        botao_selecionar(navegador)
        try:
            navegador.quit()
            print("Logout automático finalizado.")
        except:
            pass
    except Exception as e:
        print(f"❌ Erro na automação: {e}")
    finally:
        try:
            navegador.quit()
        except:
            pass