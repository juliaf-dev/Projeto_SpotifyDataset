import pandas as pd
import streamlit as st

@st.cache_data
def carregar_dados():
    # Carrega o dataset do Spotify
    df_original = pd.read_csv('./dataset/spotify_data clean.csv')
    
    df = pd.DataFrame()
    
    # Mapeamento das colunas do dataset do Spotify
    df['track_name'] = df_original['track_name']
    df['artist_name'] = df_original['artist_name']
    df['artist_popularity'] = df_original['artist_popularity']
    df['artist_followers'] = df_original['artist_followers']
    df['artist_genres'] = df_original['artist_genres']
    df['album_name'] = df_original['album_name']
    df['album_release_date'] = df_original['album_release_date']
    df['album_type'] = df_original['album_type']
    df['track_popularity'] = df_original['track_popularity']
    df['track_duration_min'] = df_original['track_duration_min']
    df['explicit'] = df_original['explicit']
    
    # Limpeza e transformações básicas
    df['explicit'] = df['explicit'].map({True: 'Sim', False: 'Não'})
    df['explicit'] = df['explicit'].fillna('Não informado')
    
    # Converter data de lançamento para datetime
    df['album_release_date'] = pd.to_datetime(df['album_release_date'], errors='coerce')
    
    # Remover linhas com valores nulos em colunas críticas
    df.dropna(subset=['track_name', 'artist_name'], inplace=True)
    
    return df

@st.cache_data
def obter_tipos_album():
    return ['album', 'single', 'compilation']

@st.cache_data
def obter_status_explicit():
    return ['Sim', 'Não']

@st.cache_data
def obter_generos_artistas(df):
    # Extrair e limpar gêneros
    generos = df['artist_genres'].dropna().unique()
    todos_generos = []
    for genero_str in generos:
        if genero_str != 'N/A':
            if ',' in genero_str:
                todos_generos.extend([g.strip() for g in genero_str.split(',')])
            else:
                todos_generos.append(genero_str.strip())
    
    return sorted(list(set([g for g in todos_generos if g and g != 'N/A'])))

@st.cache_data
def obter_artistas(df):
    return sorted(df['artist_name'].unique().tolist())

@st.cache_data
def obter_albuns(df):
    return sorted(df['album_name'].unique().tolist())