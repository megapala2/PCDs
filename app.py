import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
import gspread
import os
import requests
import plotly.express as px
from unidecode import unidecode
import re


load_dotenv()

GENERO = {
'Cisgênero: Identidade de gênero correspondente a que foi atribuída no nascimento': 'Cisgênero',
'Transgênero: Identidade de gênero oposta ao sexo biológico': 'Transgênero',
'Não binário: Identidade de gênero não estabelecida.': 'Não binário',
'Prefere não dizer': 'Prefere não dizer',
}

CARGOS = [
    "Auxiliar",
    "Estudante",
    "Analista",
    "Gerente",
    "Especialista",
    "Consultor",
    "Aprendiz",
    "Supervisor",
    "Coordenador",
    "Diretor/Vice Diretor",
    "Presidente/Ceo",
    "Autônomo",
    "Não estou empregado no momento",
    "Assistente",
    "Estagiário",
    "Outros",
    "Trainee"
]

INTERESSE = [
    "Administrativo",
    "Recursos Humanos",
    "Saúde",
    "Controladoria",
    "Financeiro",
    "Logística",
    "Operações",
    "Planejamento Financeiro",
    "Tributário",
    "Bibliotecário",
    "Comercial",
    "Vendas",
    "Atacado",
    "Varejo",
    "Atendimento ao cliente",
    "Auditoria",
    "Ouvidoria",
    "Arquiteto",
    "Projetos",
    "Produção",
    "Tecnologia",
    "Marketing",
    "Pesquisas e Desenvolvimento",
    "Treinamento e Desenvolvimento",
    "Comunicação",
    "Garantia de Qualidade",
    "Crédito",
    "Desenvolvimento de negócios",
    "Estratégia",
    "Exportação",
    "Imports",
    "Inteligência de Mercado",
    "Legal",
    "Tesouraria",
    "Contabilidade",
    "Seguros",
    "Cobrança",
    "Manutenção",
    "Outros"
]

TRABALHO = [
    "Presencial",
    "Remoto",
    "Híbrido"
]

UF = {
    'ACRE': 'AC',
    'ALAGOAS': 'AL',
    'AMAPA': 'AP',
    'AMAZONAS': 'AM',
    'BAHIA': 'BA',
    'CEARA': 'CE',
    'DISTRITO FEDERAL': 'DF',
    'ESPIRITO SANTO': 'ES',
    'GOIAS': 'GO',
    'MARANHAO': 'MA',
    'MATO GROSSO': 'MT',
    'MATO GROSSO DO SUL': 'MS',
    'MINAS GERAIS': 'MG',
    'PARA': 'PA',
    'PARAIBA': 'PB',
    'PARANA': 'PR',
    'PERNAMBUCO': 'PE',
    'PIAUI': 'PI',
    'RIO DE JANEIRO': 'RJ',
    'RIO GRANDE DO NORTE': 'RN',
    'RIO GRANDE DO SUL': 'RS',
    'RONDONIA': 'RO',
    'RORAIMA': 'RR',
    'SANTA CATARINA': 'SC',
    'SAO PAULO': 'SP',
    'SERGIPE': 'SE',
    'TOCANTINS': 'TO',
    'ESPIRITO SANTOS': 'ES',
}

FAIXAS = [
    "16 a 18 anos",
    "19 a 20 anos",
    "21 a 25 anos",
    "26 a 29 anos",
    "30 a 39 anos",
    "40 a 49 anos",
    "50 a 59 anos",
    "60 a 69 anos",
    "70 a 79 anos"
]

FORMACAO = [
    'Pós graduação ou MBA',
    'Ensino superior completo',
    'Ensino médio completo',
    'Ensino superior incompleto',
    'Ensino fundamental incompleto',
    'Mestrado',
    'Ensino fundamental completo',
    'Ensino médio incompleto',
    'Doutorado',
    'Pós Mestrado',
    'Especialização',
    'Pós Doutorado'
]

class gdoc:

   
    def authorize():

       
        id_cliente = os.getenv("client_id")
        segredo_cliente = os.getenv("client_secret")
        refresh_tkn = os.getenv('refresh_token')

        url = 'https://oauth2.googleapis.com/token'
        data = {
            'client_id': id_cliente,
            'client_secret': segredo_cliente,
            'refresh_token': refresh_tkn,
            'grant_type': 'refresh_token'
        }

        response = requests.post(url, data=data)

        if response.status_code == 200:
            token_info = response.json()
            
            credentials = Credentials(
                token=token_info['access_token'],
                refresh_token= refresh_tkn,
                token_uri='https://oauth2.googleapis.com/token',
                client_id= id_cliente,
                client_secret= segredo_cliente
            )
            return credentials
        else:
            st.info("Erro:", response.status_code)

   
    def credential():
        creds = None
        token_path = 'assets/token.json'

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path)
        else:
            
            creds = gdoc.authorize()
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        if not creds or not creds.valid:
            creds = gdoc.authorize()

        # Salve as credenciais para uso futuro
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
        return creds


    @st.cache_data(ttl='1d')
    def client_data():
        creds = gdoc.credential()
        gs = gspread.authorize(creds)
        planilha = gs.open_by_key(os.getenv('planilha_pcd_id'))
        worksheet = planilha.worksheet('PCD')
        resultado = worksheet.get_all_records()
        resultado = pd.DataFrame(resultado)

        return resultado

class stpage:

    def init():
        
        st.set_page_config(layout='wide', page_icon='♿', page_title='PCDs Online Brasil')
        st.sidebar.title('PCDs Online Brasil')
        logo_container = st.sidebar.container(height=200, border=False)

        css_file='styles/main.css'

        with open(css_file) as f:
         st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
         

        logo_container.image('assets/logo.png')
        st.sidebar.write('---------------------------')
        
       
        

        
    
    def sidefilters():

        side_container = st.sidebar.container(border=True)
        side_container2 = st.sidebar.container(border=False)
        side_container3 = st.sidebar.container(border=True)

        with side_container2:
           st.write('\n')
       
           
           
       
        search_box = side_container.text_input('Procurar', key="searchBar", help=r'Você pode digitar qualquer termo que seja procurar os dados, exemplo: "SP", "AUXILIAR", etc ')

        with side_container.popover('Filtro avançado', use_container_width=True):
            col1, col2 = st.columns(2)  # Divide o espaço em duas colunas

    # Multiselects na primeira coluna
        with col1:
            st.session_state.UF = st.multiselect(label='UF 🏙️', options=UF.values())
            st.session_state.ensino = st.multiselect(label='Ensino 🎓', options=FORMACAO)
            st.session_state.interesse = st.multiselect(label='Interesse 🤔', options=INTERESSE)

        # Multiselects na segunda coluna
        with col2:
            st.session_state.trabalho = st.multiselect(label='Modelo Trabalho 💼', options=TRABALHO)
            st.session_state.cargos = st.multiselect(label='Cargo 👔', options=CARGOS)
            
        
        with side_container3.popover('Envie seu currículo!', use_container_width=True):
            st.info('https://docs.google.com/forms/d/e/1FAIpQLSdh8hyiSDKGIxyHKxV5y6Jp3hXS-PE0AouDArg_ntIkfYyH0A/viewform?fbzx=1835398047016580018')
        
        with side_container3.popover('Créditos desse projeto:', use_container_width=True):
            st.info('Administradora do projeto: https://www.linkedin.com/in/isabelaespezim/')
            st.info('Criador desse dashboard: https://www.linkedin.com/in/thales-rudolph')

        
        
        
        return search_box
    
    def expand_df(df):
    
        with st.expander('Base de currículos PCDs - 2024'):
            st.warning('Os dados mostrados são limitados para ficarem de acordo com a LGPD')
            st.warning('Recrutador! Entre em contato com a administradora do projeto para ter acesso a base completa: https://www.linkedin.com/in/isabelaespezim/')
            st.info(f'Total de currículos: {len(df)}')
            st.data_editor(df, use_container_width=True, hide_index=True, disabled=True, column_order=("Idade", "UF", "Cargo", "Área de interesse", "Formação", "Modelo de trabalho"))

class cleaner:
    
    @st.cache_data(ttl='1d')
    def df_treatment():

        df = gdoc.client_data()

        df = df.rename(columns={
            r'Número do CID (consta no laudo médico)': 'CID', 
            'Estado que reside': 'UF', 
            'Qual raça você se identifica?': 'Etnia',
            'Qual seu cargo atual?': 'Cargo',
            'Qual sua formação?': 'Formação',
            'Qual seu interesse de regime de trabalho': 'Interesse',
            'Qual sua expectativa salarial?': 'Expectativa Salarial',
            'Tipo de deficiência:': 'Deficiência'

            })
        
        df = df.drop(columns=['CID', 'Possui alguma limitação?', 'Interesse', 'Gênero'])
        
        df['Cidade'] = df['Cidade'].apply(lambda x: x.strip() if isinstance(x, str) else x)
        df['Bairro'] = df['Bairro'].apply(lambda x: x.strip() if isinstance(x, str) else x)

        df['Cidade'] = df['Cidade'].apply(lambda x: unidecode(x).upper() if isinstance(x, str) else x)
        df['Bairro'] = df['Bairro'].apply(lambda x: unidecode(x).upper() if isinstance(x, str) else x)
        df['UF'] = df['UF'].apply(lambda x: unidecode(x).upper() if isinstance(x, str) else x)

        
        df['Idade'] = df['Idade'].apply(lambda x: cleaner.categorize_age(x))
        df['Idade'] = df['Idade'].apply(lambda x: x.strip() if isinstance(x, str) else x)

        
        df['Deficiência'] = df['Deficiência'].replace({'Transtorno do Espectro Autista': 'Autismo'})
        df['UF'] = df['UF'].replace(UF)
        
        return df
    
    def categorize_age(age):
        if isinstance(age, int):
            if 40 <= age <= 49:
                return "40 a 49 anos"
            elif 30 <= age <= 39:
                return "30 a 39 anos"
            elif 26 <= age <= 29:
                return "26 a 29 anos"
            elif 50 <= age <= 59:
                return "50 a 59 anos"
            elif 21 <= age <= 25:
                return "21 a 25 anos"
            elif 60 <= age <= 69:
                return "60 a 69 anos"
            elif 16 <= age <= 18:
                return "16 a 18 anos"
            elif 70 <= age <= 79:
                return "70 a 79 anos"
            elif 19 <= age <= 20:
                return "19 a 20 anos"
            else:
                return "Out of range"
        elif isinstance(age, str) and len(age) < 12:
            try:
                age = int(''.join(re.findall(r'\d+', age)))
                return cleaner.categorize_age(age)
            except (TypeError, ValueError):
                age = 'NA'
                return age
        else:
           
            return age
        
    def mask(df, search: str):

        if search:
            mask = df.apply(lambda coluna: coluna.astype(str).str.contains(search, case=False, na=False)).any(axis=1)
            df = df[mask]
        
        if st.session_state.UF:
             for valor in st.session_state.UF:
                if 'UF' in df.columns:
                    mask = df['UF'].astype(str).str.contains(valor, case=False, na=False)
                    df = df[mask]
        
        if st.session_state.ensino:
            for valor in st.session_state.ensino:
                 if 'Formação' in df.columns:
                    mask = df['Formação'].astype(str).str.contains(valor, case=False, na=False)
                    df = df[mask]
        
        if st.session_state.trabalho:
            for valor in st.session_state.trabalho:
                if 'Modelo de trabalho' in df.columns:
                    mask = df['Modelo de trabalho'].astype(str).str.contains(valor, case=False, na=False)
                    df = df[mask]
        
        if st.session_state.cargos:
            for valor in st.session_state.cargos:
                if 'Cargo' in df.columns:
                    mask = df['Cargo'].astype(str).str.contains(valor, case=False, na=False)
                    df = df[mask]

        if st.session_state.interesse:
            for valor in st.session_state.interesse:
                 if 'Área de interesse' in df.columns:
                    mask = df['Área de interesse'].astype(str).str.contains(valor, case=False, na=False)
                    df = df[mask]


        return df

class newdf:
    def contar_valores(df, coluna, lista):
        
        contagem = {valor: 0 for valor in lista}
        
        for indice, linha in df.iterrows():
            valores_celula = linha[coluna]
            
            if isinstance(valores_celula, list):
                for valor in valores_celula:
                    if valor in lista:
                        contagem[valor] += 1
            elif valores_celula in lista:
                contagem[valores_celula] += 1
        
        # Criar DataFrame a partir do dicionário de contagens
        df_contagem = pd.DataFrame(list(contagem.items()), columns=['Valor', 'Contagem'])
        
        return df_contagem
    
class dashboard:
    def dash(df):

        container_dash = st.container(border=True)
        
        container_uf = container_dash.container(border=False)
        container_uf2 = container_dash.container(border=False)
        #container_uf3 = container_dash.container(border=False)
        dash_coluna1, dash_coluna2 = container_dash.columns(2)

        dashpop_coluna1, dashpop_coluna2, dashpop_coluna3, dashpop_coluna4 = container_uf.columns(4)
        dashpop_coluna5, dashpop_coluna6, dashpop_coluna7, dashpop_coluna8 = container_uf2.columns(4)
        #dashpop_coluna9, dashpop_coluna10, dashpop_coluna11, dashpop_coluna12, = container_uf3.columns(4)

        with dashpop_coluna1.popover('Cidade 🏙️', use_container_width=True):
             dashboard.pop_plot(df,  x='count', y='Cidade', orientation='h')

        #with dashpop_coluna2.popover('Bairro 🏘️', use_container_width=True):
        #     dashboard.pop_plot(df,  x='count', y='Bairro', orientation='h')
        
        with dashpop_coluna3.popover('Etnia 🌍', use_container_width=True):
             dashboard.pop_plot_pizza(df,  x='count', y='Etnia', orientation='h')
        
        with dashpop_coluna4.popover('Deficiência ♿', use_container_width=True):
             dashboard.pop_plot(df,  x='count', y='Deficiência', orientation='h')

        with dashpop_coluna5.popover('Formação 🎓', use_container_width=True):
            dashboard.pop_plot(df,  x='count', y='Formação', orientation='h')
        
        with dashpop_coluna6.popover('Pretensão 💵', use_container_width=True):
            dashboard.pop_plot(df,  x='count', y='Expectativa Salarial', orientation='h')
        
        with dashpop_coluna7.popover('Cargo Atual 👔', use_container_width=True):
            cargo= pd.DataFrame(newdf.contar_valores(df, 'Cargo', CARGOS))
            dashboard.pop_plot(cargo,  x='Contagem', y='Valor', orientation='h', news=0)
        
        with dashpop_coluna8.popover('Modelo Trabalho 💼', use_container_width=True):
            modelo= pd.DataFrame(newdf.contar_valores(df, 'Modelo de trabalho', TRABALHO))
            dashboard.pop_plot_pizza(modelo,  x='Contagem', y='Valor', orientation='h', news=0)

        with dashpop_coluna2.popover('Interesse 🤔', use_container_width=True):
            interesses= pd.DataFrame(newdf.contar_valores(df, 'Área de interesse', INTERESSE))
            dashboard.pop_plot(interesses,  x='Contagem', y='Valor', orientation='h', news=0, largest=1)

            
    

        dashboard.plot(df, dash_coluna1,  x='count', y='UF', orientation='h')
        dashboard.plot(df, dash_coluna2,  x='count', y='Idade', orientation='h')
        

    
    def plot(df,dash_coluna, x: str, y: str, orientation: str):

       
        fig = px.bar(df[y].value_counts().reset_index(), x=x, y=y, orientation=orientation, height=650)
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        fig.update_traces(marker_line_color = 'black',marker_line_width = 1, opacity = 1)
        fig.update_yaxes(title_text='')
        fig.update_xaxes(title_text='')
        fig.update_traces(marker=dict(line=dict(width=1, color='Black')))

        

        
        dash_coluna.plotly_chart(fig, use_container_width=True)
    
     
     
    def pop_plot(df, x: str, y: str, orientation: str, news: int = 1, largest: int = 0):

        if news == 1:
            df = pd.DataFrame(df[y].value_counts().reset_index())
            df = df.nlargest(15, 'count')
            
        
        if largest == 1:
            df = df.nlargest(15, 'Contagem')

        df[y] = df[y].apply(lambda x: unidecode(x).upper() if isinstance(x, str) else x)

        fig = px.bar(df, x=x, y=y, orientation=orientation )
        
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=500)
        fig.update_traces(marker_line_color = 'black',marker_line_width = 1, opacity = 1)
        fig.update_yaxes(title_text='')
        fig.update_xaxes(title_text='')
        fig.update_traces(marker=dict(line=dict(width=1, color='Black')))

        
      

        st.plotly_chart(fig, use_container_width=True)
    
    def pop_plot_pizza(df, x: str, y: str, orientation: str, news: int=1):

        colors = ['#2196f3', '#6dc6ff', '#58b0d9', '#0b8bcf', '#7537b1']
        
        if news==1:
            df = pd.DataFrame(df[y].value_counts().reset_index())
        

        df[y] = df[y].apply(lambda x: unidecode(x).upper() if isinstance(x, str) else x)

        fig = px.pie(df, names=y, values=x, width=400, color_discrete_sequence=colors)
        
        
        fig.update_traces(marker_line_color = 'black',marker_line_width = 1, opacity = 1)
        fig.for_each_xaxis(lambda x: x.update(showgrid=True))
        fig.update_yaxes(showgrid=True, title_text='')
        fig.update_xaxes(title_text='')

        
        st.write(fig, use_container_width=True)

def main():

    stpage.init()

    search = stpage.sidefilters()

    df = cleaner.df_treatment()
    df = cleaner.mask(df, search=search)



    stpage.expand_df(df)

    dashboard.dash(df)
    



if __name__ == '__main__':

    main()