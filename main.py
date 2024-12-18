import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd  # Importando o pandas para manipulação de dados

def extrair_nomes_empresas(url, classe_div):
    """
    Faz scraping em uma página e retorna uma lista de nomes de empresas.
    """
    # Fazer o request HTTP
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Lista para armazenar os nomes das empresas
        lista_empresas = []

        # Encontrar todas as 'div' com a classe especificada
        empresas = soup.find_all('div', class_=classe_div)

        # Extrair e limpar o texto
        for empresa in empresas:
            nomes = empresa.text.strip().splitlines()  # Divide por linhas
            for nome in nomes:
                if nome.strip():  # Ignora linhas vazias
                    lista_empresas.append(nome.strip())

        return lista_empresas
    else:
        print(f"Erro ao acessar a página: {response.status_code}")
        return []

def buscar_linkedin_cnpj_selenium(lista_empresas):
    linkedin_dict = {}
    cnpj_dict = {}

    # Configuração do Selenium para usar o ChromeDriver com webdriver_manager
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Roda sem abrir o navegador
    options.add_argument("--disable-gpu")  # Desativa a aceleração de GPU (opcional)
    
    # Inicializa o WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    for empresa in lista_empresas:
        try:
            # Buscar o LinkedIn da empresa
            query_linkedin = f"{empresa} site:linkedin.com"
            google_url = f"https://www.google.com/search?q={query_linkedin}"
            driver.get(google_url)
            time.sleep(2)
            links = driver.find_elements(By.XPATH, "//a[contains(@href, 'linkedin.com')]")
            
            linkedin_url = "Não encontrado"
            if links:
                linkedin_url = links[0].get_attribute("href")
            
            # Buscar o CNPJ da empresa
            query_cnpj = f"{empresa} CNPJ"
            google_url = f"https://www.google.com/search?q={query_cnpj}"
            driver.get(google_url)
            time.sleep(2)
            links = driver.find_elements(By.XPATH, "//a[contains(@href, 'cnpj')]")
            
            cnpj_encontrado = "Não encontrado"
            if links:
                for link in links:
                    href = link.get_attribute("href")
                    if "cnpj" in href:  # Verifica se o link contém CNPJ
                        cnpj_encontrado = href
                        break
            
            linkedin_dict[empresa] = linkedin_url
            cnpj_dict[empresa] = cnpj_encontrado
            print(f"LinkedIn de '{empresa}': {linkedin_url}, CNPJ: {cnpj_encontrado}")
        
        except Exception as e:
            print(f"Erro ao buscar dados para '{empresa}': {e}")
            linkedin_dict[empresa] = "Erro"
            cnpj_dict[empresa] = "Erro"
    
    driver.quit()  # Encerra o navegador
    return linkedin_dict, cnpj_dict

# Exemplo de URL e classe para extração de empresas
url = 'https://assespro-sp.org.br/associadas/'  # Substitua pela URL correta
classe_div = 'entry-content'  # Substitua pela classe correta, se necessário

# Extrair as empresas da página
empresas = extrair_nomes_empresas(url, classe_div)

# Chamar a função para buscar os LinkedIn e CNPJ das empresas
linkedin_empresas, cnpj_empresas = buscar_linkedin_cnpj_selenium(empresas)

# Criar um DataFrame com os resultados
df = pd.DataFrame({
    "Empresa": list(linkedin_empresas.keys()),
    "LinkedIn": list(linkedin_empresas.values()),
    "CNPJ": list(cnpj_empresas.values())
})

# Salvar o DataFrame em um arquivo Excel
df.to_excel("empresas_linkedin_cnpj.xlsx", index=False)

print("\nArquivo Excel gerado com sucesso!")