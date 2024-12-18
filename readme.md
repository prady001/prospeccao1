# Scraping de Empresas - LinkedIn e informações gerais das empresas

Este projeto realiza o scraping de informações de empresas a partir de uma página da web. O script coleta os nomes das empresas, busca seus perfis no LinkedIn e os links com informações da empresa, e então salva os dados em um arquivo Excel.

## Funcionalidades

- **Extração de Empresas**: O script faz o scraping de uma página web para extrair os nomes das empresas.
- **Busca de LinkedIn e CNPJ**: Utilizando o Selenium, o script realiza buscas no Google para encontrar os links do LinkedIn e informações de CNPJ de cada empresa.
- **Exportação para Excel**: Os dados são organizados em um DataFrame do Pandas e salvos em um arquivo Excel.

## Pré-requisitos

Para executar este projeto, você precisará ter Python 3.x instalado. Além disso, o projeto utiliza as seguintes bibliotecas:

- `requests`: Para fazer requisições HTTP.
- `beautifulsoup4`: Para parsing de HTML e extração de dados.
- `selenium`: Para automação de navegação no navegador.
- `webdriver-manager`: Para gerenciar o WebDriver do Chrome.
- `pandas`: Para manipulação e exportação dos dados.
- `openpyxl`: Para salvar os dados em formato Excel.

## Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/prady001/prospeccao1.git
