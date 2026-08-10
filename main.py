import json # Essa biblioteca permite que você trabalhe com arquivos JSON, que são muito usados para armazenar dados de forma estruturada.
import concurrent.futures # Essa biblioteca permite que você execute várias tarefas ao mesmo tempo, em paralelo.
import os # Essa biblioteca permite que você interaja com o sistema operacional, como criar pastas, apagar arquivos, etc.
import glob # Essa biblioteca permite que você busque arquivos usando padrões, como "*.pdf" para todos os PDFs.

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 

import teste_ESTADUAL
import teste_FEDERAL
import teste_FGTS

CNPJ = ["37382081000141","57201446000100"]

site = [
        "https://www.sefaz.go.gov.br/Certidao/Emissao/",
        "https://servicos.receitafederal.gov.br/servico/certidoes/#/home/cnpj",
        "https://consulta-crf.caixa.gov.br/consultacrf/pages/consultaEmpregador.jsf"
]

pasta_download = r"C:\Users\FAGabrioti\Desktop\CNDs"


def criar_navegador_configurado():
    """Função auxiliar para gerar navegadores idênticos e isolados"""
    opcoes = Options()

    # Argumentos originais de segurança
    opcoes.add_argument('--safebrowsing-disable-download-protection')
    opcoes.add_argument('--safebrowsing-disable-extension-blacklist')
    opcoes.add_argument('--ignore-certificate-errors')
    opcoes.add_argument('--disable-features=InsecureDownloadWarnings')

    # NOVO: Argumento que força o Chrome a "clicar" em imprimir automaticamente sem mostrar a tela
    opcoes.add_argument('--kiosk-printing')

    pasta_download = r"C:\Users\FAGabrioti\Desktop\CNDs"

    # NOVO: Configuração que diz ao Chrome que o destino da impressão é "Salvar como PDF"
    app_state = {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": ""
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }

    preferencias = {
        # Suas configurações originais
        "download.default_directory": pasta_download,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True,
        "safebrowsing.enabled": False,                      # <- Ligamos a navegação segura para o Chrome não reclamar...
        "safebrowsing.disable_download_protection": True,   # <- ...mas desligamos a proteção de download!
        "profile.default_content_setting_values.automatic_downloads": 1,
        
        # NOVO: Desabilita o visualizador de PDF interno do Chrome por precaução extra
        "plugins.plugins_disabled": ["Chrome PDF Viewer"],
        
        # NOVO: Injeta as configurações de "Salvar como PDF" no perfil do Chrome
        "printing.print_preview_sticky_settings.appState": json.dumps(app_state),
        
        # NOVO: Define o diretório padrão para onde os arquivos "Salvos como PDF" vão
        "savefile.default_directory": pasta_download
    }

    opcoes.add_experimental_option("prefs", preferencias)
    opcoes.add_experimental_option("detach", True)

    servico = Service(ChromeDriverManager().install())

    # IMPORTANTE: Removi o "detach: True" para que o código Python consiga fechar as janelas no final
    return webdriver.Chrome(service=servico, options=opcoes)



def principal():
    # Loop passando por cada CNPJ
    for i in range(len(CNPJ)):
        print(f"\033[33m\n--- Iniciando coletas simultâneas para o CNPJ {CNPJ[i]} ---\033[0m")
        
        # 1. Criamos 3 navegadores independentes
        nav_estadual = criar_navegador_configurado()
        nav_estadual.maximize_window()

        nav_federal = criar_navegador_configurado()
        nav_federal.maximize_window()

        nav_fgts = criar_navegador_configurado()
        nav_fgts.maximize_window()

        nav_estadual.execute_cdp_cmd('Page.setDownloadBehavior', {
                'behavior': 'allow', 
                'downloadPath': pasta_download
        })

        nav_federal.execute_cdp_cmd('Page.setDownloadBehavior', {
                'behavior': 'allow', 
                'downloadPath': pasta_download
                })
        
        nav_fgts.execute_cdp_cmd('Page.setDownloadBehavior', {
                'behavior': 'allow', 
                'downloadPath': pasta_download
                })

        # 2. Abrimos as 3 pistas de corrida (max_workers=3)
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            
            # 3. Disparamos as três funções ao mesmo tempo, passando um navegador exclusivo para cada uma
            tarefa_est = executor.submit(teste_ESTADUAL.recolher_estadual, CNPJ[i], site[0], nav_estadual, pasta_download)
            tarefa_fed = executor.submit(teste_FEDERAL.recolher_federal, CNPJ[i], site[1], nav_federal)
            tarefa_fgts = executor.submit(teste_FGTS.recolher_FGTS, CNPJ[i], site[2], nav_fgts)
            
            # 4. O código vai ficar pausado nesta linha até que as três tarefas terminem!
            concurrent.futures.wait([tarefa_est, tarefa_fed,tarefa_fgts])  
        
        # 5. Após as três terminarem (ou darem erro), fechamos os 3 navegadores
        nav_estadual.quit()
        nav_federal.quit()
        nav_fgts.quit()

        # --- LIMPEZA DE ARQUIVOS INDESEJADOS ---

        # 1. Busca qualquer arquivo que termine com .htm ou .html na pasta
        arquivos_lixo = glob.glob(os.path.join(pasta_download, "*.htm*"))

        # 2. Percorre a lista e apaga um por um
        for lixo in arquivos_lixo:
            try:
                os.remove(lixo)
                print(f"\033[33mLixo apagado com sucesso: {os.path.basename(lixo)}\033[0m")
            except Exception as e:
                print(f"\033[33mNão foi possível apagar o arquivo {lixo}: {e}\033[0m")

        print(f"\033[33mColetas finalizadas para o CNPJ {CNPJ[i]}!\033[0m\n")

if __name__ == "__main__":
    principal()