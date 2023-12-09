import streamlit as st
import requests
import json
import requests

# URL do servidor Flask
url = "https://grupo-5-sprint-027e13457cd0.herokuapp.com"

def cadastra_usuario(email, senha, clube):
    payload = {"email": email, "senha": senha, "clube": clube}
    response = requests.post(f"{url}/cadastro", json=payload)
    return response

def login(email, senha, clube):
    payload = {"email": email, "senha": senha, "clube": clube}
    response = requests.post(f"{url}/login", json=payload)
    global id_user_atual
    if 'usuario' in response.headers:
        id_user_atual = str(response.headers['usuario'])
    else:
        id_user_atual = None 
    return response

def partidas():
    global id_user_atual
    try:
        headers = {'usuario': id_user_atual}
        response = requests.get(f"{url}/partidas", headers=headers)
        response.raise_for_status()  
        if response.ok:
            return response.json()  
        else:
            st.error("Erro ao obter dados das partidas. Redirecionando para o login.")
            st.experimental_rerun()  
            
    except requests.RequestException as e:
        st.error(f"Erro de requisição: {e}")
        st.experimental_rerun() 

def obter_clube_usuario():
    try:
        header = {'usuario': id_user_atual}
        response = requests.get(f"{url}/get_clube",headers=header)
        response.raise_for_status()
        return response.json()['clube']
    except requests.RequestException as e:
        print(f"Erro ao obter o clube: {e}")
        return None