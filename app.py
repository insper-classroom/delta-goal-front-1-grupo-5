import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from funcoes import *
from PIL import Image

# Dados de exemplo para autenticação
usuarios_cadastrados = {
    'usuario1': 'senha123',
    'usuario2': 'senha456',
    '1':'1'
}

# Função para verificar as credenciais
def verifica_credenciais(username, senha):
    return usuarios_cadastrados.get(username) == senha

# Função para adicionar novos usuários
def adicionar_usuario(username, senha):
    if username not in usuarios_cadastrados:
        usuarios_cadastrados[username] = senha
        return True
    return False

# Função principal para o aplicativo
def main():
    if 'usuario' not in st.session_state or st.session_state.usuario is None:
        login_cadastro()
    elif 'ir_para_analise' in st.session_state and st.session_state['ir_para_analise']:
        st.session_state['ir_para_analise'] = False
        dashboard_analise()
    else:
        paginas()

def login_cadastro():
    
    # st.set_page_config(layout="wide")
    with open("design/style/styles.css") as d:
        st.markdown(f"<style>{d.read()}</style>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2,1,2])

    with col1:
        image = Image.open('design/photos/logo.webp')
        st.image(image)
        st.subheader('Artificial Intelligence to monitor players every instant of every match')


    with col3:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        with tab1:
            st.header("Login")
            email = st.text_input("E-mail:", key="login_email")
            senha = st.text_input("Senha:", type='password', key="login_password")
            
            # Use uma chave diferente para o text_input e o session_state
            clube_input = st.text_input("Clube:", key="clube_input")

            if st.button("Login"):
                if 'clube' not in st.session_state or st.session_state['clube'] != clube_input:
                    st.session_state['clube'] = clube_input
                
                response = login(email, senha)
                if response.ok:
                    st.success("Login bem-sucedido!")
                    st.session_state.usuario = email
                    st.rerun()
                else:
                    st.error("Credenciais inválidas. Tente novamente.")

        with tab2:
            st.header("Sign Up")
            new_email = st.text_input("E-mail:", key="new_email")
            new_password = st.text_input("Senha:", type='password', key="new_password")
            new_time = st.text_input("Clube:", key="new_time")

            if st.button("Sign Up"):
                response = cadastra_usuario(new_email, new_password, new_time)
                if response.ok:
                    st.success("Usuário cadastrado com sucesso!")
                else:
                    st.error(response.text)


# Função para exibir a página inicial
def pagina_inicial():
    st.title("Página Inicial")
    st.write("Bem-vindo à página inicial. Selecione uma opção na barra lateral para navegar.")

# Função para exibir a página de visualização de dados
def pagina_dados():
    st.title("Visualização de Dados")
    df = pd.DataFrame({
        'X': [1, 2, 3, 4, 5],
        'Y': [10, 11, 12, 13, 14],
        'Z': [20, 21, 22, 23, 24]
    })
    st.dataframe(df)
    st.title("Exemplo de Plotly no Streamlit")

    # Gráfico de dispersão interativo usando Plotly Express
    fig = px.scatter(df, x='X', y='Y', size='Z', title='Gráfico de Dispersão Interativo')
    st.plotly_chart(fig)

    dados = {'Categoria': ['A', 'B', 'C', 'D'],
         'Valores': [30, 40, 20, 10]}
    df_2 = pd.DataFrame(dados)

    # Título do aplicativo
    st.title("Exemplo de Gráfico de Pizza no Streamlit")

    # Gráfico de pizza interativo usando Plotly Express
    fig = px.pie(df_2, values='Valores', names='Categoria', title='Gráfico de Pizza Interativo')
    st.plotly_chart(fig)


# Função para exibir a página de configurações
def pagina_configuracoes():
    st.title("Configurações")
    # Adicione configurações ou opções aqui

def pagina_partidas(partidas):
    st.title(f"Partidas")

    if 'clube' in st.session_state:
        clube_usuario = st.session_state['clube']
        st.write(f"O clube do usuário é: {clube_usuario}")
    else:
        st.write("Clube não definido ou não informado.")
   
    df_partidas = pd.DataFrame(partidas)
    df_partidas['data'] = pd.to_datetime(df_partidas['data'], format='%d/%m/%Y').dt.date

    adversarios = ["Todos"] + sorted(df_partidas['adversario'].unique().tolist())
    adversario_selecionado = st.selectbox("Selecione o Adversário", adversarios)

    min_data, max_data = df_partidas['data'].min(), df_partidas['data'].max()
    data_inicial, data_final = st.slider(
        "Selecione o Intervalo de Datas",
        min_value=min_data,
        max_value=max_data,
        value=(min_data, max_data),
        format="DD/MM/YYYY"
    )

    df_filtrado = df_partidas.copy()
    if adversario_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['adversario'] == adversario_selecionado]
    df_filtrado = df_filtrado[(df_filtrado['data'] >= data_inicial) & (df_filtrado['data'] <= data_final)]

    for index, partida in df_filtrado.iterrows():
        with st.expander(f"{partida['clube']} vs {partida['adversario']} - {partida['data'].strftime('%d/%m/%Y')}"):
            st.write(f"Resultado: {partida['resultado']}")

            # Usando uma chave de estado separada para o botão
            if st.button("Ir para a Página de Análise", key=f"botao_analise_{index}"):
                st.session_state['ir_para_analise'] = True

def dashboard_analise():
    st.title("Dashboard")

    if st.button("Voltar para Análises de Jogos"):
        st.session_state['opcao_pagina'] = "Partidas" 
        st.experimental_rerun()
    
# Função principal para controlar a navegação entre as páginas
def paginas():
    st.sidebar.title("Dashboard")
    opcoes = ["Página Inicial", "Quebra de linha de defesa", "Cruzamento", "Partidas"]
    opcao_pagina = st.sidebar.radio("Escolha a Página:", opcoes, index=opcoes.index(st.session_state.get('opcao_pagina', 'Página Inicial')))

    # Condicional para 'Página de Análise'
    if st.session_state.get('opcao_pagina') == "Página de Análise":
        dashboard_analise()
    else:
        # Carregando a página selecionada
        if opcao_pagina == "Página Inicial":
            pagina_inicial()
        elif opcao_pagina == "Quebra de linha de defesa":
            pagina_dados()
        elif opcao_pagina == "Cruzamento":
            pagina_configuracoes()
        elif opcao_pagina == "Partidas":
            dados_partidas = partidas()
            pagina_partidas(dados_partidas)



# Chamando a função principal para iniciar o aplicativo
if __name__ == "__main__":
    main()
