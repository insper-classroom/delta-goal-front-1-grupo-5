import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from funcoes import *
from dashboard import *
from moviepy.editor import VideoFileClip
import os 
from PIL import Image
from datetime import date

# Dados de exemplo para autenticação

# Função principal para o aplicativo
def main():
    if 'usuario' not in st.session_state or st.session_state.usuario is None:
        login_cadastro()
    else:
        paginas()



def converter_tempo_para_segundos(tempo_str):
    if not tempo_str:
        return None

    horas, minutos, segundos = map(int, tempo_str.split(':'))

    return horas * 3600 + minutos * 60 + segundos

def trata_video(data_rupturas,click):
    
    df_rupturas = pd.DataFrame(data_rupturas)
    dic_tempo_rupturas = {} #a key representa o numero da ruptura e a tupla o inicio e final do video em segundos 
    numero_ruptura = 1
    for ruptura_tempo_sec in df_rupturas["inicio_ruptura"]:
        inicio_video = converter_tempo_para_segundos(ruptura_tempo_sec) - 5
        final_video = converter_tempo_para_segundos(ruptura_tempo_sec) + 5
        dic_tempo_rupturas[numero_ruptura] = (inicio_video,final_video)
        numero_ruptura += 1

    #Front DashBoard
def dashboard_quebra(cores_personalizadas, df_rupturas, df_desfechos, contagem_desfechos):
    if st.button("Voltar"):
        paginas('Partidas')
        # Gráfico de pizza interativo usando Plotly Express com cores personalizadas
    col1, col2 = st.columns(2)
    with col1:
        st.header("Geral")
        fig = px.pie(df_rupturas, names='Desfecho', values='Quantidade', title='Quantidade de Desfechos', hover_data=['Porcentagem'])
        st.plotly_chart(fig)
        st.dataframe(df_desfechos) 
        
    with col2:
        st.dataframe(contagem_desfechos) 
        pass

def login_cadastro():

    with open("design/style/login.css") as d:
        st.markdown(f"<style>{d.read()}</style>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2,1,2])

    with col1:
        image = Image.open('design/photos/logo.webp')
        st.image(image)


    with col3:
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

    with open("design/style/partidas.css") as d:
        st.markdown(f"<style>{d.read()}</style>", unsafe_allow_html=True)

    with open("design/style/sidebar.css") as d:
        st.markdown(f"<style>{d.read()}</style>", unsafe_allow_html=True)

    if 'clube' in st.session_state:
        clube_usuario = st.session_state['clube']
        st.title(f"{clube_usuario}")
    else:
        st.title(f"Partidas")
        st.write("Clube não definido ou não informado.")
    
    st.subheader("Filtro") 
    partidas_dic = partidas['partidas'][0]
    df_partidas = pd.DataFrame(partidas_dic)
    df_partidas['data'] = pd.to_datetime(df_partidas['data'], format='%d/%m/%Y').dt.date

    adversarios = ["Todos os Adversários"] + sorted(df_partidas['adversario'].unique().tolist())
    adversario_selecionado = st.selectbox("", adversarios)
    min_data, max_data = df_partidas['data'].min(), date.today()
    data_inicial, data_final = st.slider(
        "",
        min_value=min_data,
        max_value=max_data,
        value=(min_data, max_data),
        format="DD/MM/YYYY"
    )

    st.subheader("Partidas")
    
    df_filtrado = df_partidas.copy()
    if adversario_selecionado != "Todos os Adversários":
        df_filtrado = df_filtrado[df_filtrado['adversario'] == adversario_selecionado]
    df_filtrado = df_filtrado[(df_filtrado['data'] >= data_inicial) & (df_filtrado['data'] <= data_final)]

    for index, partida in df_filtrado.iterrows():
        with st.expander(f"{partida['clube']} vs {partida['adversario']} - {partida['data'].strftime('%d/%m/%Y')}"):
            st.write(f"Resultado: {partida['resultado']}")

            # Usando uma chave de estado separada para o botão
            if st.button("Ir para a Página de Análise", key=f"botao_analise_{index}"):
                st.session_state['ir_para_analise'] = True
                resultado = dados(partida['clube'], partida['adversario'], partida['data'].strftime('%d/%m/%Y'))
                df = pd.DataFrame(resultado[0])
def cortar_clipes(arquivo_video, tempos_clipes, pasta_saida="videos_rupturasPalmeirasxBragantino_12.12.12"):
    
    if not os.path.exists(pasta_saida):
        os.makedirs(f"{pasta_saida}")

    for numero_clipe, (inicio, fim) in tempos_clipes.items():
        nome_arquivo_saida = os.path.join(pasta_saida, f"ruptura_{numero_clipe}_{pasta_saida}.mp4")

        if not os.path.exists(nome_arquivo_saida):
            print(f"Cortando clipe {numero_clipe}_{pasta_saida}...")
            cortar_video(arquivo_video, inicio, fim, nome_arquivo_saida)
        else:
            print(f"Arquivo {nome_arquivo_saida} já existe. Pulando...")

def cortar_video(arquivo_video, inicio, fim, nome_arquivo_saida):

    video = VideoFileClip(arquivo_video)

    video_cortado = video.subclip(inicio, fim)

    video_cortado.write_videofile(nome_arquivo_saida, codec="libx264")

def video_teste():
    st.title("Colocando o vídeo teste")

    rupturas_disponiveis = [1, 2, 3, 4, 5, 6, 7]  
    escolha_ruptura = st.selectbox("Escolha o número da ruptura", rupturas_disponiveis)

    nome_arquivo = f"videos_rupturasPalmeirasxBragantino_12.12.12/ruptura_{escolha_ruptura}_videos_rupturasPalmeirasxBragantino_12.12.12.mp4"

    if os.path.exists(nome_arquivo):
        video_file = open(nome_arquivo, 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)
    else:
        st.error(f"O arquivo {nome_arquivo} não foi encontrado.")

# Função principal para controlar a navegação entre as páginas
def paginas(opcao=None):
    opcao_pagina = opcao
    sidebar_image = 'design/photos/Delta_Goal_NEGATIVO.png'  
    st.sidebar.image(sidebar_image, width=200)
    st.sidebar.subheader("")
    opcoes = ["Partidas", "Rupturas", "Cruzamento", "Video_teste", "DashBoard"]
    
    opcao_pagina = st.sidebar.radio("", opcoes, index=opcoes.index(st.session_state.get('opcao_pagina', 'Partidas')), key="pagina_radio")

    # Carregando a página selecionada
    if opcao_pagina == "Rupturas":
        pass
    elif opcao_pagina == "Cruzamento":
        pagina_configuracoes()
    elif opcao_pagina == "Partidas":
        dados_partidas = partidas()
        pagina_partidas(dados_partidas)
    elif opcao_pagina == "Video_teste":
            video_teste()
    elif opcao_pagina == "DashBoard":
        pass
    else:
        st.error("Página não encontrada.")



# Chamando a função principal para iniciar o aplicativo
if __name__ == "__main__":
    main()