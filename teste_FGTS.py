import time
from selenium.webdriver.common.keys import Keys

def recolher_FGTS(CNPJ, site, navegador):

    navegador.get(site)
    #navegador.maximize_window()
    navegador.minimize_window()

    time.sleep(2)

    try:
        botao_inicio = navegador.find_element('xpath','//*[@id="mainForm:txtInscricao1"]')
        if botao_inicio:
            botao_inicio.click()
            pass
        else:
            print(f"\033[34mErro: Botão de início não encontrado para o site {site}. Pulando...\033[0m")
            return # Esse 'return' encerra essa função e volta pro loop principal pra tentar o próximo CNPJ
    except:
        pass

    time.sleep(2)

    try:
        botao2 = navegador.find_element('xpath','//*[@id="mainForm:txtInscricao1"]')
        if botao2:
            botao2.click()
            pass
        else:
            print(f"\033[34mErro: Botão de início não encontrado para o site {site}. Pulando...\033[0m")
            return # Esse 'return' encerra essa função e volta pro loop principal pra tentar o próximo CNPJ
    except:
        pass

    time.sleep(2)

    try:
        botao3 = navegador.find_element('xpath','//*[@id="mainForm:txtInscricao1"]')
        if botao3:
            botao3.send_keys(CNPJ)
            pass
        else:
            print(f"\033[34mErro: Botão de início não encontrado para o site {site}. Pulando...\033[0m")
            return # Esse 'return' encerra essa função e volta pro loop principal pra tentar o próximo CNPJ
    except:
        pass

    time.sleep(2)

    try:
        botao4 = navegador.find_element('xpath', '//*[@id="mainForm:uf"]')
        if botao4:
            botao4.click()
            pass
        else:
            print(f"\033[34mErro: Botão de início não encontrado para o site {site}. Pulando...\033[0m")
            return # Esse 'return' encerra essa função e volta pro loop principal pra tentar o próximo CNPJ
    except:
        pass

    time.sleep(2)


    try:
        botao5 = navegador.find_element('xpath', '//*[@id="mainForm:uf"]')
        if botao5:
            botao5.send_keys(Keys.ARROW_DOWN * 9)
            pass
        else:
            print(f"\033[34mErro: Botão de início não encontrado para o site {site}. Pulando...\033[0m")
            return # Esse 'return' encerra essa função e volta pro loop principal pra tentar o próximo CNPJ
    except:
        pass

    time.sleep(2)

    try:
        botao6 = navegador.find_element('xpath', '//*[@id="mainForm:btnConsultar"]')
        if botao6:
            botao6.click()
            pass
        else:
            print(f"\033[34mErro: Botão de início não encontrado para o site {site}. Pulando...\033[0m")
            return # Esse 'return' encerra essa função e volta pro loop principal pra tentar o próximo CNPJ
    except:
        pass

    time.sleep(2)

    try:
        if navegador.find_element('xpath', '//span[@class="feedback-text"]'):
            texto_erro = navegador.find_element('xpath', '//span[@class="feedback-text"]').text
            texto_erro = texto_erro.text.lower()

            if texto_erro == "não foi possível verificar a regularidade junto à caixa":
                print(f"\033[34mErro: {texto_erro}\033[0m")
                navegador.find_element('xpath', '//*[@id="mainForm:btnVoltar"]').click()  # Clica no botão "Voltar"
                
                return # Esse 'return' encerra essa função e volta pro loop principal pra tentar o próximo CNPJ  .
    except:
        pass

    time.sleep(2)

    try:
        botao7 = navegador.find_element('xpath', '//*[@id="mainForm:j_id76"]')
        if botao7:
            botao7.click()
            pass
        else:
            print(f"\033[34mErro: Botão de início não encontrado para o site {site}. Pulando...\033[0m")
            return # Esse 'return' encerra essa função e volta pro loop principal pra tentar o próximo CNPJ
    except:
        pass

    time.sleep(2)

    try:
        botao8 = navegador.find_element('xpath', '//*[@id="mainForm:btnVisualizar"]')
        if botao8:
            botao8.click()
            pass
        else:
            print(f"\033[34mErro: Botão de início não encontrado para o site {site}. Pulando...\033[0m")
            return # Esse 'return' encerra essa função e volta pro loop principal pra tentar o próximo CNPJ
    except:
        pass

    time.sleep(2)

    try:
        botao9 = navegador.find_element('xpath', '//*[@id="mainForm:btImprimir4"]')
        if botao9:
            botao9.click()
            pass
        else:
            print(f"\033[34mErro: Botão de início não encontrado para o site {site}. Pulando...\033[0m")
            return # Esse 'return' encerra essa função e volta pro loop principal pra tentar o próximo CNPJ
    except:
        pass

    print(f"\033[34mFGTS recolhida para o CNPJ: {CNPJ}\033[0m")
