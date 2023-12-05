import streamlit as st
import pandas as pd
import plotly.express as px
from funcoes import *
from dashboard import *
from moviepy.editor import VideoFileClip
import os 
from PIL import Image
from datetime import date
from time import sleep

# 1- Função principal para o aplicativo
def main():
    if 'usuario' not in st.session_state or st.session_state.usuario is None:
        login_cadastro()
    elif 'ir_para_analise' in st.session_state and st.session_state['ir_para_analise']:
        st.session_state['ir_para_analise'] = False
        with open('dados/quebra.json', 'r') as f:
            data = json.load(f)
            time = 'Palmeiras'
            id = '1'
        trata_dados(data, time, id, 'quebra')
    else:
        paginas()


# 2- Vídeo
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

# 3- Dados
def trata_dados(dados, time, id, tipo):
    #jogadores numero de rupturas
        dicionario_rupturas = [{}]
        total_rupturas = {}
        total_desfechos = {}
        for ruptura in dados['time'][id]['rupturas']:
            instante_ruptura = ruptura.get('instante_ruptura', None)
            if not any(item.get('instante_ruptura') == instante_ruptura for item in dicionario_rupturas):
                novo_registro = {
                    "instante_ruptura": instante_ruptura,
                    "inicio_ruptura": ruptura.get('inicio_ruptura', None),
                    'zona': ruptura.get('zona_defesa', None),
                    'desfecho': ruptura.get('desfecho', None),
                    'nome_jogador_ruptura': ruptura.get('nome_jogador_ruptura', None)
                }
                dicionario_rupturas.append(novo_registro)
                # Agora dicionario_rupturas deve conter a lista desejada de dicionários
                # print(dicionario_rupturas)
            for i in range(len(dicionario_rupturas)):
                if ruptura['instante_ruptura'] not in dicionario_rupturas[i]:
                  if ruptura['nome_jogador_ruptura'] not in total_rupturas:
                    total_rupturas[ruptura['nome_jogador_ruptura']] = 0
                  total_rupturas[ruptura['nome_jogador_ruptura']] += 1
        #Desfechos Lista  
        
        total_desfechos = dados['time'][id]['desfechos']
        df = pd.DataFrame(list(total_desfechos.items()), columns=['Desfecho', 'Quantidade'])
        df['Porcentagem'] = (df['Quantidade'] / df['Quantidade'].sum()) * 100
        cores_personalizadas = ['#FF9999', '#66B2FF', '#99FF99']
        ######
        dashboard_quebra(cores_personalizadas, dicionario_rupturas, total_rupturas, df, dados)

# 4- DashBoard
def dashboard_quebra(cores_personalizadas, df_rupturas, df_desfechos, contagem_desfechos,dados):
    if st.button("Voltar"):
        st.session_state['ir_para_analise'] = True
        # Gráfico de pizza interativo usando Plotly Express com cores personalizadas
    json_rupturas = json.dumps(dados,indent=4,separators=(',', ': ')).encode('utf-8')
    st.download_button(
        label= "Baixar Rupturas",
        data = json_rupturas,
        file_name = "rupturas.json",
        mime="application/json"
    )
    col1, col2 = st.columns(2)

    with col1:
        st.header("Geral")
        fig = px.pie(contagem_desfechos, names='Desfecho', values='Quantidade', title='Quantidade de Desfechos', hover_data=['Porcentagem'])
        st.plotly_chart(fig)
        st.dataframe(df_desfechos) 
        
    with col2:
        st.dataframe(df_rupturas) 
        pass

# 5- Login
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
                sleep(0.5)
                st.session_state.usuario = email
                st.rerun()
            else:
                st.error("Credenciais inválidas. Tente novamente.")

# 6- Partidas
def pagina_partidas(partidas):

    with open("design/style/partidas.css") as d:
        st.markdown(f"<style>{d.read()}</style>", unsafe_allow_html=True)

    with open("design/style/sidebar.css") as d:
        st.markdown(f"<style>{d.read()}</style>", unsafe_allow_html=True)

    if 'clube' in st.session_state:
        clube_usuario = st.session_state['clube']
        st.title(f"Estatísticas Delta Goal - {clube_usuario}")
    else:
        st.title(f"Partidas")
        st.write("Clube não definido ou não informado.")

    st.subheader("Filtros Avançados") 
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

    st.subheader("Lista de Partidas")

    df_filtrado = df_partidas.copy()
    if adversario_selecionado != "Todos os Adversários":
        df_filtrado = df_filtrado[df_filtrado['adversario'] == adversario_selecionado]
    df_filtrado = df_filtrado[(df_filtrado['data'] >= data_inicial) & (df_filtrado['data'] <= data_final)]

    for index, partida in df_filtrado.iterrows():
        col1,space,col2,col3 = st.columns([2,0.66,5,2])
        with col1:
            st.subheader(f"{partida['data'].strftime('%d/%m/%Y')}")
        with col2:
            st.subheader(f"{partida['clube']} {partida['resultado']} {partida['adversario']}")
        with col3:
            if st.button('Estatísticas', key=f'botao_analise_{index}'):
                st.session_state['ir_para_analise'] = True
                st.rerun()
            # st.write(f"Resultado: {partida['resultado']}")
            # Usando uma chave de estado separada para o botão
            # if st.button("Estatísticas da Partida", key=f"botao_analise_{index}"):
                # st.session_state['ir_para_analise'] = True

# 7- Controle de navegação entre as páginas
def paginas():
    sidebar_image = 'design/photos/Delta_Goal_NEGATIVO.png'  
    st.sidebar.image(sidebar_image, width=200)
    st.sidebar.subheader("")
    
    opcoes = ["Partidas", "Cruzamentos", "Vídeos"]
    opcao_pagina = st.sidebar.radio("", opcoes, index=opcoes.index(st.session_state.get('opcao_pagina', 'Partidas')))

    # Carregando a página selecionada
    if opcao_pagina == "Partidas":
        dados_partidas = partidas()
        pagina_partidas(dados_partidas)
    elif opcao_pagina == "Cruzamentos":
        from cruzamentos.exibe_cruz import dash_cruzamento
        dash_cruzamento()
    elif opcao_pagina == "Vídeos":
            video_teste()
    else:
        st.error("Página não encontrada.")

# Chamando a função principal para iniciar o aplicativo
if __name__ == "__main__":
    main()