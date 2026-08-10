import glob 
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By # <- Importação necessária para buscar elementos!


# --- 2. NAVEGAÇÃO E CLIQUES ---
def recolher_estadual(CNPJ, site, navegador, pasta_download):
    # Passo A: Entrar no site onde os botões estão
    navegador.get(site) 
    navegador.maximize_window()

    aba_principal = navegador.current_window_handle

    # Pausa rápida para a página carregar completamente (o ideal é usar WebDriverWait, mas o sleep quebra um galho para testar)
    time.sleep(3) 

    # Passo B: Clicar em um botão para abrir a seção de relatórios (Exemplo de XPath de um botão de menu)
    navegador.find_element('xpath', '//*[@id="Certidao.TipoDocumentoCNPJ"]').click() #
    print("\033[32mBotão CNPJ clicado\033[0m")

    time.sleep(2) # Espera a nova tela carregar
    navegador.find_element('xpath', '//*[@id="Certidao.NumeroDocumentoCNPJ"]').send_keys(CNPJ)
    print(f"\033[32mCNPJ inserido: {CNPJ}\033[0m")
    time.sleep(2)
    # Procura o botão de Emitir
    botoes_emitir = navegador.find_elements(By.XPATH, "//input[@value='Emitir']")

    if botoes_emitir:
        botoes_emitir[0].click()
        print("\033[32mBotão Emitir clicado\033[0m")
    else:
        print("\033[31mBotão de Emitir não encontrado!\033[0m")

    WebDriverWait(navegador, 10).until(EC.number_of_windows_to_be(2)) 

    # PASSO C: MUDANDO DE ABA ---

    # 1. Pegamos uma lista com todas as abas que o navegador abriu até agora
    abas_abertas = navegador.window_handles

    # 2. Mudamos o foco do Selenium para a última aba da lista (índice -1), que é a aba nova. Se uma nova aba realmente abriu, mudamos para ela
    if len(abas_abertas) > 1:
        navegador.switch_to.window(abas_abertas[-1])

    time.sleep(2)

    # 3. Agora sim, clicamos no botão final (o Selenium já está olhando para a aba certa!)
    botoes_final = navegador.find_elements(By.XPATH, '//*[@id="Certidao.ConfirmaNomeContribuinteSim"]')
    if botoes_final:
        botoes_final[0].click()
        print("\033[32mBotão de Confirmação clicado na nova aba\033[0m")
    else:
        print("\033[32mBotão de Confirmação não encontrado na nova aba!\033[0m")

    time.sleep(2)

    if len(navegador.window_handles) > 1:
        navegador.close()

    navegador.switch_to.window(aba_principal)

            # 1. Usa o curinga *.asp para listar todos os arquivos com essa extensão na pasta
    arquivos_asp = glob.glob(os.path.join(pasta_download, "*.asp"))

    # 2. Verifica se a lista não está vazia (ou seja, se encontrou pelo menos um arquivo)
    if arquivos_asp:
        # 3. Pega o arquivo mais recente baixado (muito útil se a pasta tiver downloads velhos)
        caminho_antigo = max(arquivos_asp, key=os.path.getctime)
        
        # 4. Define o novo nome como PDF
        caminho_novo = os.path.join(pasta_download, f"certidao_{CNPJ}.pdf") 
        
        # Se já existir um PDF com esse nome de testes anteriores, apaga para evitar erro
        if os.path.exists(caminho_novo):
            os.remove(caminho_novo)
            
        # 5. Renomeia o arquivo
        os.rename(caminho_antigo, caminho_novo)
        print(f"\033[32mSucesso! O arquivo {os.path.basename(caminho_antigo)} foi renomeado para certidao_{CNPJ}.pdf\033[0m")
        
    else:
        print("\033[31mNenhum arquivo .asp foi encontrado na pasta. O download pode ter falhado ou demorado muito.\033[0m")

    print(f"\033[34mEstadual recolhida para o CNPJ: {CNPJ}\033[0m")
    

    



    





