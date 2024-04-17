Dashboard de Base de Currículos de PCD
======================================

Este é um projeto de dashboard desenvolvido em Python utilizando a biblioteca Streamlit. O objetivo deste projeto é fornecer uma interface para explorar uma base de currículos de Pessoas com Deficiência (PCD), facilitando a análise e seleção de candidatos por recrutadores.

Funcionalidades Principais
--------------------------

*   **Filtros Avançados**: Os usuários podem filtrar os currículos por diversos critérios, incluindo UF (Unidade Federativa), formação acadêmica, interesse de regime de trabalho, cargo atual e área de interesse.
    
*   **Visualização de Dados**: O dashboard oferece visualizações interativas dos dados, incluindo gráficos de barras horizontais e gráficos de pizza, que fornecem insights sobre características demográficas, interesses profissionais e outras informações relevantes dos candidatos.
    
*   **Exportação de Dados**: Recrutadores podem exportar os currículos filtrados para análises mais detalhadas.

*   **Segurança**: O acesso a base é feito por variáveis de ambiente diretamente no streamlit cloud, portando é impossível recriar esse código, pode-se baixar o arquivo
csv que fica disponível no site para tentar recriar o projeto para fins de estudo

CSS
--------------

Esse projeto faz uso extenso de CSS para modificar algumas funcionalidades do streamlit, tais como:

1. Trocar a fonte do site

    ```
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');


       {font-family: 'Montserrat';}
    ```

2. Desativar todas as interações com o gráfico PLOTLY


    ```
    .drag { /* */
            pointer-events: none !important;
        }
    ```

3. Desativar a barra de menus que o plotly deixa no gráfico

    ```
    .modebar-container { 
          display: none;
            }
    ```

Pré-Requisitos
--------------

*   Python 3.x
*   Pacotes Python listados no arquivo `requirements.txt`
*   Conta no Google Cloud com permissões para acesso aos dados na planilha Google Sheets

Instalação e Uso
----------------

1.  Clone o repositório:
    
    
    ```
    git clone https://github.com/seu_usuario/seu_repositorio.git`
    ```
    
2.  Instale as dependências:
    
    
    ```
    pip install -r requirements.txt`
    ```
    
3.  Configure as variáveis de ambiente:
    
    *   Crie um arquivo `.env` na raiz do projeto com as chaves de API do google sheets caso prefira fazer o método original
    

4.  Execute o aplicativo Streamlit:
    
    
    ```
    streamlit run main.py`
    ```
    
5.  Acesse o aplicativo através do navegador web utilizando o link gerado pelo Streamlit.
    

Autoria e Contribuição
----------------------

*   Este projeto foi criado por [Isabela Espezim](https://www.linkedin.com/in/isabelaespezim/).
*   O dashboard foi desenvolvido por [Thales Rudolph](https://www.linkedin.com/in/thales-rudolph-b7511a16a/).

Licença
-------

Este projeto é distribuído sob a licença MIT. Consulte o arquivo `LICENSE` para obter mais informações.