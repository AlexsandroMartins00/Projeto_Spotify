import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar o dataset
data = pd.read_csv('spotify_songs_dataset.csv')

# Traduzir os nomes das colunas para português
data.rename(columns={
    'song_id': 'ID_Musica',
    'song_title': 'Titulo_Musica',
    'artist': 'Artista',
    'album': 'ALbum',
    'genre': 'Genero',
    'release_date': 'Data_Lancamento',
    'duration': 'Duracao',
    'popularity': 'Popularidade',
    'stream': 'Stream',
    'language': 'Idioma',
    'explicit_content': 'Conteudo_explicito',
    'label': 'Produtora',
    'composer': 'Compositor',
    'producer': "Produtor",
    'collaboration': 'Colaborador'

}, inplace=True)

# Configuração do app Streamlit
st.title("Visualização de Dados de Lista de Musica do Spotify")

# Barra lateral para opções de filtragem
st.sidebar.header("Opções de Filtro")

# Filtro por País (com busca)
pais_selecionado = st.sidebar.selectbox(
    "Selecione o Genero", 
    options=data["Genero"].unique(),
    index=0
)

# Filtro por Importação ou Exportação
tipo_selecionado = st.sidebar.radio(
    "Artista", 
    options=data["Artista"].unique()
)

# Filtro por Categoria
categorias_selecionadas = st.sidebar.multiselect(
    "Selecione a Musica",
    options=data["Titulo_Musica"].unique(),
    default=data["Titulo_Musica"].unique()
)

# Aplicar filtros ao dataset
dados_filtrados = data[(data["Genero"] == pais_selecionado) & 
                       (data["Artista"] == tipo_selecionado) & 
                       (data["Titulo_Musica"].isin(categorias_selecionadas))]

# Exibir dados filtrados
st.write(f"### Dados Filtrados para {pais_selecionado}", dados_filtrados)

# Visualização 1: uantidade de Musica por Genero
quantidade_por_categoria = dados_filtrados.groupby("Titulo_Musica")["Genero"].sum().reset_index()
fig_quantidade = px.bar(quantidade_por_categoria, x="Titulo_Musica", y="Genero", 
                        title=f"Quantidade de Musica por Genero- {pais_selecionado}")
st.plotly_chart(fig_quantidade)

# Visualização 2:Popularidade do Artista
valor_por_categoria = dados_filtrados.groupby("Artista")["Popularidade"].sum().reset_index()
fig_valor = px.pie(valor_por_categoria, names="Artista", values="Popularidade", 
                   title=f"Popularidade do Artista - {pais_selecionado}")
st.plotly_chart(fig_valor)

# Visualização 3: Popularidade por data de Lançamento
dados_filtrados['Data_Lancamento'] = pd.to_datetime(dados_filtrados['Data_Lancamento'])
peso_ao_longo_tempo = dados_filtrados.groupby("Data_Lancamento")["Popularidade"].sum().reset_index()
fig_peso = px.line(peso_ao_longo_tempo, x="Data_Lancamento", y="Popularidade", 
                   title=f"Popularidade por data de Lançamento - {pais_selecionado}")
st.plotly_chart(fig_peso)

# Rodapé
st.write("Esta aplicação utiliza Pandas, Plotly e Streamlit para visualização de dados.")
