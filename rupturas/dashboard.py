# import streamlit as st
# import plotly.express as px
# from funcoes import *
# import os 
# from cruzamentos.dashboard import *
# import json 
# from rupturas.campo_caio import *

# def pega_dados_videos(path_dado):

#     file = open(path_dado)
#     data = json.load(file)
#     return data 

# def converter_tempo_para_segundos(tempo_str):
#     if not tempo_str:
#         return None

#     horas, minutos, segundos = map(int, tempo_str.split(':'))

#     return horas * 3600 + minutos * 60 + segundos

# def trata_video_ruptura(data_rupturas):
    
#     tempos_rupturas = []
#     for time_id, time_data in data_rupturas["time"].items():
#         rupturas = time_data["rupturas"]
#         if time_id == "1":
#             for ruptura in rupturas:
#                 inicio_ruptura = ruptura["inicio_ruptura"]
#                 tempos_rupturas.append(converter_tempo_para_segundos(inicio_ruptura))
#                 tempos_rupturas.sort()

#     dic_tempo_rupturas = {} #a key representa o numero da ruptura e a tupla o inicio e final do video em segundos 
#     numero_ruptura = 1
#     for ruptura_tempo_sec in tempos_rupturas:
#         inicio_video = ruptura_tempo_sec - 5
#         final_video = ruptura_tempo_sec + 5
#         dic_tempo_rupturas[numero_ruptura] = (inicio_video,final_video)
#         numero_ruptura += 1

#     return dic_tempo_rupturas

# def dashboard_quebra(cores_personalizadas, df_rupturas, df_desfechos, contagem_desfechos, lista_porcentagem, dados):
#     with open("design/style/rupturas.css") as d:
#         st.markdown(f"<style>{d.read()}</style>", unsafe_allow_html=True)


#     col1, space, col2 = st.columns([8,1,8])
#     with col1:
#         figura = desenhar_campo(lista_porcentagem)
#         # st.pyplot(figura)

#         # coluna1, coluna2 = st.columns([1,1])
#         # with coluna1:
#         fig = px.pie(contagem_desfechos, names='Desfecho', values='Quantidade', title='Quantidade de Desfechos', hover_data=['Porcentagem'])
#         st.plotly_chart(fig, use_container_width=True)
#         # with coluna2:
#         st.write('Quantidade de desfechos por jogador')
#         st.dataframe(df_desfechos, width=250)

#     with col2:
#         quantidade = []
#         for i in range(len(df_rupturas)-1):
#             quantidade.append(i+1)
#         st.subheader("Lances")
#         tempos_rupturas = trata_video_ruptura(pega_dados_videos("quebra.json"))
#         jogada = st.selectbox('Lista de rupturas', quantidade, key=quantidade)
#         st.write("---")
#         start_time = None

#         if jogada in quantidade:
#             start_time = tempos_rupturas[jogada][0]

#         if start_time is not None:
#             st.write(f"Tempo inicial selecionado: {start_time}")

#             video_url = f"https://drive.google.com/file/d/1vWm45opnuiYNN0s1FFKx8DBekp-YX30R/preview?t={start_time}"

#             st.write(f"Reproduzindo o vídeo a partir de {start_time} segundos:")
#             st.write("---")
#             st.write(HTML(f'<iframe src="{video_url}" width="640" height="360"></iframe>'))
            
#         else:
#             st.warning("Chave selecionada não encontrada no dicionário.")

#         st.dataframe(df_rupturas)
#         # st.write('You selected:', jogada)
