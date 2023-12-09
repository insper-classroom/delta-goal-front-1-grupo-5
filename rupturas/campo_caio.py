import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st

# Função para desenhar o campo de futebol com um quadrado abrangendo os quadrados selecionados
def desenhar_campo(Lista_porcentagem=None):
    if Lista_porcentagem is None:
        return None
    fig, ax = plt.subplots(figsize=(8, 5))

    # Definindo o tamanho do campo
    largura_campo = 100
    altura_campo = 60

    # Desenhando o campo de futebol com a cor verde
    retangulo_campo = patches.Rectangle((0, 0), largura_campo, altura_campo, linewidth=2, edgecolor='black', facecolor='#529F40')
    ax.add_patch(retangulo_campo)

    retangulo_central = patches.Rectangle(((largura_campo/5)*2, 0), largura_campo/5, altura_campo, linewidth=2, edgecolor='black', facecolor='#62ba17')
    ax.add_patch(retangulo_central)

    # Dividindo o campo em 5 partes com linhas verticais
    for i in range(1, 5):
        plt.plot([i * largura_campo / 5, i * largura_campo / 5], [0, altura_campo], color='black')

    circulo_central = patches.Circle((largura_campo/2, altura_campo/2), radius=5, edgecolor="white", facecolor='none')
    ax.add_patch(circulo_central)

    circulo_bola = patches.Circle((largura_campo/2, altura_campo/2), radius=0.4, edgecolor="white", facecolor='white')
    ax.add_patch(circulo_bola)

    linha = patches.Rectangle((largura_campo/2, 0), 0, altura_campo, linewidth=1, edgecolor='white', facecolor='none')
    linha.set_facecolor('white')
    ax.add_patch(linha)

    # Adicionando retângulos representando as áreas do campo
    altura_area = altura_campo / 2.5  # Ajuste para um meio-termo
    
    # area_lado_esquerdo = patches.Rectangle((-5, altura_campo / 2 - altura_area / 2), largura_campo / 5, altura_area, linewidth=2, edgecolor='white', facecolor='none')
    # area_goleiro_esquerdo = patches.Rectangle((-1,22), largura_campo / 14, 16, linewidth=2, edgecolor='white', facecolor='none')

    # area_lado_direito = patches.Rectangle(((largura_campo - largura_campo / 5)*1.06, altura_campo / 2 - altura_area / 2), largura_campo / 5, altura_area, linewidth=2, edgecolor='white', facecolor='none')
    # area_goleiro_direito = patches.Rectangle((94.2,22), largura_campo / 14, 16, linewidth=2, edgecolor='white', facecolor='none')


    nomes_das_chaves = Lista_porcentagem.keys()
    chaves = []
    for chave in nomes_das_chaves:
        chaves.append(chave)

    plt.text(6.5, 33.3, f"{Lista_porcentagem[2]}", fontsize=10, color='White') 
    plt.text(24, 33.3, f"{Lista_porcentagem[4]}", fontsize=10, color='White') 
    plt.text(50, 33.3,f"", fontsize=10, color='black') 
    plt.text(66, 33.3, f"{Lista_porcentagem[0]}", fontsize=10, color='White') 
    plt.text(84, 33.3, f"{Lista_porcentagem[6]}", fontsize=10, color='White')
    

    plt.text(2, 26, f"  {Lista_porcentagem[1]}", fontsize=14, color='White') 
    plt.text(22, 26, f"  {Lista_porcentagem[3]}", fontsize=14, color='White') 
    plt.text(42, 26, f" ", fontsize=14, color='black') 
    plt.text(62, 26, f"  {Lista_porcentagem[5]}", fontsize=14, color='White') 
    plt.text(82, 26, f"  {Lista_porcentagem[7]}", fontsize=14, color='White') 

    # ax.add_patch(area_lado_esquerdo)
    # ax.add_patch(area_goleiro_esquerdo)
    # ax.add_patch(area_lado_direito)
    # ax.add_patch(area_goleiro_direito)

    retangulo_campo = patches.Rectangle((0, 0), largura_campo, altura_campo, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(retangulo_campo)

    # Configurações do gráfico
    plt.xlim(-5, largura_campo + 5)
    plt.ylim(-5, altura_campo + 5)
    plt.axis('off')

    return fig

# Exibindo o campo de futebol com o quadrado abrangente no Streamlit
figura = desenhar_campo()
st.pyplot(figura)
