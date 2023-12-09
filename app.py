import streamlit as st
import pandas as pd
import plotly.express as px
from funcoes import *
import os 
from PIL import Image
from datetime import date
from time import sleep
from cruzamentos.dashboard import *
import json 
from IPython.display import HTML
from rupturas.campo_caio import *
from rupturas.dashboard import *


# 1- Função principal para o aplicativo
def main():
        # Inicialize os atributos se ainda não estiverem presentes
    if 'desfechos_rep' not in st.session_state:
        st.session_state.desfechos_rep = None
    if 'zonas' not in st.session_state:
        st.session_state.zonas = None
    
    if 'jogador' not in st.session_state:
        st.session_state.jogador = None
    if 'time' not in st.session_state:
        st.session_state.time = None
    if 'usuario' not in st.session_state or st.session_state.usuario is None:
        # st.set_page_config(layout="centered")
        login_cadastro()
    elif 'ir_para_analise' in st.session_state and st.session_state['ir_para_analise']:
        with open('quebra.json', 'r') as f:
            data = json.load(f)
            time = 'Palmeiras'
            id = '5'

        st.session_state['ir_para_analise'] = True
        trata_dados(data, st.session_state.time, id, st.session_state.zonas, st.session_state.jogador, st.session_state.desfechos_rep)
        
    else:
        st.set_page_config(layout="wide")
        paginas()

    

# 2- Vídeo
def pega_dados_videos(path_dado):

    file = open(path_dado)
    data = json.load(file)
    return data 
  
def converter_tempo_para_segundos(tempo_str):
    if not tempo_str:
        return None

    horas, minutos, segundos = map(int, tempo_str.split(':'))

    return horas * 3600 + minutos * 60 + segundos

def trata_video_ruptura(data_rupturas):
    
    tempos_rupturas = []
    for time_id, time_data in data_rupturas["time"].items():
        rupturas = time_data["rupturas"]
        if time_id == "1":
            for ruptura in rupturas:
                inicio_ruptura = ruptura["inicio_ruptura"]
                tempos_rupturas.append(converter_tempo_para_segundos(inicio_ruptura))
                tempos_rupturas.sort()

    dic_tempo_rupturas = {} #a key representa o numero da ruptura e a tupla o inicio e final do video em segundos 
    numero_ruptura = 1
    for ruptura_tempo_sec in tempos_rupturas:
        inicio_video = ruptura_tempo_sec - 5
        final_video = ruptura_tempo_sec + 5
        dic_tempo_rupturas[numero_ruptura] = (inicio_video,final_video)
        numero_ruptura += 1

    return dic_tempo_rupturas

def trata_video_cruzamentos(data_cruzamentos):

    tempo_video_cruzamentos = {}
    instantes_cruzamentos = []

    for time_id, time_data in data_cruzamentos['time'].items():
        for cruzamento in time_data['rupturas']:
            if time_id == "1":
                instantes_cruzamentos.append(cruzamento['instante_cruzamento'])

    numero_cruzamento = 1 
    for tempo in instantes_cruzamentos:
        tempo_segundos = converter_tempo_para_segundos(tempo)
        inicio_video = tempo_segundos -5 
        final_video =  tempo_segundos + 5
        tempo_video_cruzamentos[numero_cruzamento] = (inicio_video,final_video)
        numero_cruzamento += 1
    return tempo_video_cruzamentos

# 3- Dados
def trata_dados(dados, time, id, zona, jogador, desfecho):
        if zona != None:
            valor = dados['time'][id]['zonas'][zona]
            zonas = zona
            novo_zonas = {f'{zona}': valor}
            dados['time'][id]['zonas'] = novo_zonas
            dados['time'][id]['rupturas'] = [ruptura for ruptura in dados['time'][id]['rupturas'] if ruptura['zona_defesa'] == zona]            
        #Filtro por desfecho
        if desfecho != None:
            dados['time'][id]['rupturas'] = [ruptura for ruptura in dados['time'][id]['rupturas'] if ruptura['desfecho'] == desfecho]
            
        #Filtro por jogador
        if jogador != None:
            dados['time'][id]['rupturas'] = [ruptura for ruptura in dados['time'][id]['rupturas'] if ruptura['nome_jogador_ruptura'] == jogador]
        
    #jogadores numero de rupturas
        dicionario_rupturas = [{}]
        total_rupturas = {}
        total_desfechos = {}
        contador = 0
        porcentagem_campo = {}
        pocentagem_campo_final = {}
        desfechos = {}
        zonas_campo = {}
        for ruptura in dados['time'][id]['rupturas']:
            instante_ruptura = ruptura.get('instante_ruptura', None)

            if not any(item.get('instante_ruptura') == instante_ruptura for item in dicionario_rupturas):
                novo_registro = {
                    "Jogada": contador,
                    "inicio_ruptura": ruptura.get('inicio_ruptura', None),
                    'zona': ruptura.get('zona_defesa', None),
                    'desfecho': ruptura.get('desfecho', None),
                    'nome_jogador_ruptura': ruptura.get('nome_jogador_ruptura', None)
                }
                dicionario_rupturas.append(novo_registro)
                if novo_registro['zona'] not in zonas_campo:
                    zonas_campo[novo_registro['zona']] = 1
                else:
                    zonas_campo[novo_registro['zona']] += 1
                
                
            if ruptura['desfecho'] not in desfechos:
                desfechos[ruptura['desfecho']] = 1
            else:
                desfechos[ruptura['desfecho']] += 1

            if ruptura['nome_jogador_ruptura'] not in total_rupturas:
                total_rupturas[ruptura['nome_jogador_ruptura']] = 1
            else:
                total_rupturas[ruptura['nome_jogador_ruptura']] += 1
            
            contador += 1 

        # Desfechos Lista
    
        dados['time'][id]['desfechos'] = desfechos

        total_desfechos = dados['time'][id]['desfechos']

        df = pd.DataFrame(list(total_desfechos.items()), columns=['Desfecho', 'Quantidade'])
        df['Porcentagem'] = (df['Quantidade'] / df['Quantidade'].sum()) * 100
        cores_personalizadas = ['#FF9999', '#66B2FF', '#99FF99']
        ######
        zonas = ['Zona 1', 'Zona 1 - B', 'Zona 2', 'Zona 2 - B']
        for zona in zonas_campo:
            if zona in zonas:
                porcentagem_campo[zona] = zonas_campo[zona]
        total = sum(porcentagem_campo.values())
        porcentagens_zonas = [porcentagem_campo[zona] / total * 100 if zona in porcentagem_campo else 0 for zona in zonas]
        for zona, porcentagem in zip(zonas, porcentagens_zonas):
            pocentagem_campo_final[zona] = f'{porcentagem:.2f}%' 
            
        
        ##########
        dashboards(cores_personalizadas, dicionario_rupturas, total_rupturas, df, pocentagem_campo_final, dados, id)


def filtro_rup(dados, df_desfechos, id):
            time = ['Nenhum']
            desfechos = ['Nenhum']
            jogadores = ['Nenhum']

            dados_zona = dados["time"][id]["zonas"]
            zonas = ['Nenhum']
            for zona in dados_zona.keys():
                if not zona.startswith("desfechos"):
                    zonas.append(zona)
            for times in dados['time']:
                time.append(dados['time'][times]['nome'])
            for desfecho in dados['time'][id]['desfechos']:
                desfechos.append(desfecho)
            for jogador in df_desfechos:
                jogadores.append(jogador)
            with st.expander("Filtros"):
                col1, col2 = st.columns(2)
                with col1:
                    Zona_rup = st.selectbox('Filtro por zona', zonas)
                    
                    Desfecho = st.selectbox('Filtro por Desfecho', desfechos)
                    
                with col2:
                    Jogador = st.selectbox('Filtro por Jogador', jogadores)
                    
                    Time = st.selectbox('Filtro por time', time)
              
                if st.button('Filtrar'):
                    if Desfecho == 'Nenhum':
                        Desfecho = None
                    if Zona_rup == 'Nenhum':
                        Zona_rup = None
                    if Jogador == 'Nenhum':
                        Jogador = None
                    st.session_state.desfechos_rep = Desfecho
                    st.session_state.zonas = Zona_rup
                    st.session_state.jogador = Jogador
                    st.session_state.time = Time
                    st.session_state['ir_para_analise'] = True
                    st.rerun()
                if st.button('Limpar Filtros'):
                    st.session_state.desfechos_rep = None
                    st.session_state.zonas = None
                    st.session_state.jogador = None
                    st.session_state.time = None
                    st.rerun()
                Zona_rup = None
                Desfecho =  None
                Jogador = None
                Time = None



# 4- DashBoards
def dashboards(cores_personalizadas, df_rupturas, df_desfechos, contagem_desfechos, lista_porcentagem, dados, id):
    with open("design/style/dashboard.css") as d:
        st.markdown(f"<style>{d.read()}</style>", unsafe_allow_html=True)
    
    if st.button(f"Voltar"):
        st.session_state['ir_para_analise'] = False
        st.rerun()
    

    image = Image.open('design/photos/logo.webp')
    st.image(image)


    st.subheader(f"{nome_primeiro_time} x {nome_segundo_time}")

    tab1, tab2 = st.tabs(["Rupturas", "Cruzamentos"])
    with tab1:
        with open("design/style/rupturas.css") as d:
            st.markdown(f"<style>{d.read()}</style>", unsafe_allow_html=True)
        json_rupturas = json.dumps(dados,indent=4,separators=(',', ': ')).encode('utf-8')
        st.download_button(
        label= "Baixar Rupturas",
        data = json_rupturas,
        file_name = "rupturas.json",
        mime="application/json"
        )

        filtro_rup(dados,df_desfechos, id)
        col1, space, col2 = st.columns([8,1,8])
        with col1:
            figura = desenhar_campo(lista_porcentagem)
            st.pyplot(figura)
            fig = px.pie(contagem_desfechos, names='Desfecho', values='Quantidade', title='Quantidade de Desfechos', hover_data=['Porcentagem'])
            st.plotly_chart(fig, use_container_width=True)
            st.write('Quantidade de desfechos por jogador')
            st.dataframe(df_desfechos, width=250)

        with col2:
            quantidade = []
            for i in range(len(df_rupturas)-1):
                quantidade.append(i+1)
            st.subheader("Lances")
            tempos_rupturas = trata_video_ruptura(pega_dados_videos("quebra.json"))
            jogada = st.selectbox('Lista de rupturas',quantidade,key=quantidade)
            st.write("---")

            # st.write('You selected:', jogada)

            start_time = None
            if jogada in quantidade:
                start_time = tempos_rupturas[jogada][0]

            if start_time is not None:
                st.write(f"Tempo inicial selecionado: {start_time}")

                video_url = f"https://drive.google.com/file/d/1vWm45opnuiYNN0s1FFKx8DBekp-YX30R/preview?t={start_time}"

                st.write(f"Reproduzindo o vídeo a partir de {start_time} segundos:")
                st.write(HTML(f'<iframe src="{video_url}" width="640" height="360"></iframe>'))
                
            else:
                st.warning("Chave selecionada não encontrada no dicionário.")

            st.dataframe(df_rupturas)

    with tab2:
        dashboard_cruzamento()

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
        email = st.text_input("E-mail:", key="login_email", placeholder="Insira seu e-mail")
        senha = st.text_input("Senha:", type='password', key="login_password", placeholder="Insira sua senha")
        clube_input = st.text_input("Clube:", key="clube_input", placeholder="Insira seu clube")

        if st.button("Login"):
            if 'clube' not in st.session_state or st.session_state['clube'] != clube_input:
                st.session_state['clube'] = clube_input
            
            response = login(email, senha, clube_input)
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

    image = Image.open('design/photos/logo.webp')
    st.image(image)
    inicial, col2, end = st.columns([1,2,1])
    with col2:
        if 'clube' in st.session_state:
            clube_usuario = st.session_state['clube']
            st.title(f"Estatísticas Delta Goal - {clube_usuario}")
        else:
            st.title(f"Partidas")
            st.write("Clube não definido ou não informado.")

    inicial,col1,end = st.columns([1,3,1])
    with col1:
        st.write('---')
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
        
        st.write('---')

    df_filtrado = df_partidas.copy()
    if adversario_selecionado != "Todos os Adversários":
        df_filtrado = df_filtrado[df_filtrado['adversario'] == adversario_selecionado]
    df_filtrado = df_filtrado[(df_filtrado['data'] >= data_inicial) & (df_filtrado['data'] <= data_final)]

    # st.subheader("Lista de Partidas")
    for index, partida in df_filtrado.iterrows():
        inicial,col1,space,col2,col3,end = st.columns([3,2,0.66,5,2,3])
        with col1:
            st.subheader(f"{partida['data'].strftime('%d/%m/%Y')}")
        with col2:
            st.subheader(f"{partida['clube']} {partida['resultado']} {partida['adversario']}")
        with col3:
            if st.button('Estatísticas', key=f'botao_analise_{index}'):
                st.session_state['ir_para_analise'] = True
                
                st.rerun()

# 7- Controle de navegação entre as páginas
def paginas():
    dados_partidas = partidas()
    pagina_partidas(dados_partidas)

# Chamando a função principal para iniciar o aplicativo
if __name__ == "__main__":
    main()