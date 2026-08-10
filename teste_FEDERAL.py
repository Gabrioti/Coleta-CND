import time
from selenium.webdriver.common.by import By 


def recolher_federal(CNPJ, site, navegador):
    
    navegador.get(site)
    #navegador.maximize_window()
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

    # Clique no botão de Emitir Certidão
    try:
        botao_emitir = navegador.find_elements(By.XPATH, "//button[@type='submit']")
        if botao_emitir:
            botao_emitir[0].click()
            if navegador.find_element(By.XPATH, '//div[@class="description" and @aria-hidden="false"]'):
                    print(navegador.find_element(By.XPATH, '//div[@class="description" and @aria-hidden="false"]').text)
                    return # Esse 'return' encerra essa função e volta pro loop principal pra tentar o próximo CNPJ
            else:
                if navegador.find_element(By.XPATH, '//button[contains(@class, "br-button secondary btn-acao")]'):
                    botao_emitir_certidao = navegador.find_element(By.XPATH, '//button[contains(@class, "br-button secondary btn-acao")]')
                    botao_emitir_certidao.click()
                    #adicionar o resto do código para baixar a certidão aqui
                    time.sleep(2)
                else:
                    if navegador.find_element(By.XPATH, '//button[contains(@class, "br-button primary btn-acao")]'): 
                            botao_consultar_certidao = navegador.find_element(By.XPATH, '//button[contains(@class, "br-button primary btn-acao")]')
                            botao_consultar_certidao.click()
                            time.sleep(2)
                    else:
                        if navegador.find_element(By.XPATH, '//div[@class="description" and @aria-hidden="false"]'):
                            print(navegador.find_element(By.XPATH, '//div[@class="description" and @aria-hidden="false"]').text)
                            return # Esse 'return' encerra essa função e volta pro loop principal pra tentar o próximo CNPJ
        else:
            print(f"Erro: Botão de emitir certidão não encontrado para o site {site}. Pulando...")
            return # Esse 'return' encerra essa função e volta pro loop principal pra tentar o próximo CNPJ
    except:
        print(f"Erro: Botão de emitir certidão não encontrado para o site {site}. Pulando...")
        return # Esse 'return' encerra essa função e volta pro loop principal pra tentar o próximo CNPJ

    time.sleep(5) # Dando um tempo maior para o site processar e a página seguinte ou alerta carregar
    
    # 2. Blindando a verificação do alerta
    alerta_erro = navegador.find_elements(By.XPATH, '//*[@id="alert-content"]/div')
    
    if alerta_erro:
        print("Certidão não encontrada para o CNPJ:", CNPJ)
    else:
        print("Certidão encontrada ou sem alertas para o CNPJ:", CNPJ)
        # Aqui você colocaria o código que faz o download caso dê certo

    print("Federal recolhida para o CNPJ:", CNPJ)

