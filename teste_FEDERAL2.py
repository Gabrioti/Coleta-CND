import time

'''from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options'''

from selenium.webdriver.common.by import By 


def recolher_federal(CNPJ, site, navegador):
    
    navegador.get(site)
    navegador.maximize_window()
    time.sleep(5)

    #Botão de aceitar cookies
    try:
        botoes = navegador.find_elements(By.XPATH, '//*[@id="card0"]/div/div[2]/button[2]') 
        if botoes:
            # Clica no primeiro item da lista
            botoes[0].click()
        else:
             # Se a lista estiver vazia, ele simplesmente ignora e pula essa part
            pass
    except:
        pass

    time.sleep(2)

    #Clique no campo de CNPJ e insere o valor
    try:
        campo_cnpj = navegador.find_element(By.XPATH, "//input[@name='niContribuinte']")
        if campo_cnpj:
            campo_cnpj.click()
            time.sleep(2)
            campo_cnpj.send_keys(CNPJ)
        else:
            print(f"Erro: Campo de CNPJ não encontrado para o site {site}. Pulando...")
            return # Esse 'return' encerra essa função e volta pro loop principal pra tentar o próximo CNPJ
    except:
        print(f"Erro: Campo de CNPJ não encontrado para o site {site}. Pulando...")
        return # Esse 'return' encerra essa função e volta pro loop principal pra tentar o próximo CNPJ
    
    time.sleep(2)

    botao_consultar = navegador.find_element(By.XPATH, "//button[@type='button' and contains(@class, 'secondary btn-acao')]")
    botao_consultar.click()
    print("Passo 1")
    time.sleep(2)
    if navegador.find_element(By.XPATH, '//div[@class="description" and @aria-hidden="false"]'):
        print(navegador.find_element(By.XPATH, '//div[@class="description" and @aria-hidden="false"]').text)
    input("Pressione Enter para continuar...")
    botao_consultar2 = navegador.find_element(By.XPATH, "//button[@type='button' and contains(@class, 'btn-acao')]")
    botao_consultar2.click()
    print("Passo 2")
    input("Pressione Enter para continuar...")
    botao_emitir = navegador.find_element(By.XPATH, "//button[@type='button' and contains(@title, 'segunda via')]")
    botao_emitir.click()
    print("Passo 3")
    input("Pressione Enter para continuar...")


