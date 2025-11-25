import streamlit as st
import plotly.express as px
import pandas as pd
from utils.carrega_dados import carregar_dados

st.set_page_config(
    page_title='Análise por Artista',
    page_icon='🎵',
    layout='wide'
)

st.title('🎵 Análise Detalhada por Artista')

# Carrega os dados
df = carregar_dados()

# =============================================
# FILTROS PARA SELEÇÃO DO ARTISTA
# =============================================

st.sidebar.header('🎯 Filtros de Artista')

# Seleção do artista
artistas_ordenados = sorted(df['artist_name'].unique())
artista_selecionado = st.sidebar.selectbox(
    'Selecione um Artista:',
    artistas_ordenados,
    index=0
)

# Filtrar dados do artista selecionado
df_artista = df[df['artist_name'] == artista_selecionado]

# =============================================
# MÉTRICAS DO ARTISTA
# =============================================

st.header(f'📊 Estatísticas de {artista_selecionado}')

if not df_artista.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_musicas = len(df_artista)
        st.metric("Total de Músicas", total_musicas)
    
    with col2:
        popularidade_artista = df_artista['artist_popularity'].iloc[0]
        st.metric("Popularidade do Artista", f"{popularidade_artista}/100")
    
    with col3:
        seguidores = df_artista['artist_followers'].iloc[0]
        st.metric("Seguidores", f"{seguidores:,}")
    
    with col4:
        albuns_unicos = df_artista['album_name'].nunique()
        st.metric("Álbuns Únicos", albuns_unicos)

    # =============================================
    # GRÁFICO 1: POPULARIDADE DAS MÚSICAS DO ARTISTA
    # =============================================

    st.subheader('📈 Popularidade das Músicas')

    # Ordenar por popularidade
    df_artista_sorted = df_artista.sort_values('track_popularity', ascending=True)

    fig_popularidade = px.bar(
        df_artista_sorted,
        y='track_name',
        x='track_popularity',
        orientation='h',
        title=f'Popularidade das Músicas de {artista_selecionado}',
        labels={'track_popularity': 'Popularidade', 'track_name': 'Música'},
        color='track_popularity',
        color_continuous_scale='viridis'
    )

    fig_popularidade.update_layout(
        yaxis_title_text='Música',
        xaxis_title_text='Popularidade (0-100)',
        height=400,
        margin=dict(t=80)
    )
    st.plotly_chart(fig_popularidade, use_container_width=True)

    # =============================================
    # GRÁFICO 2: DURAÇÃO DAS MÚSICAS
    # =============================================

    st.subheader('⏱️ Duração das Músicas')

    fig_duracao = px.bar(
        df_artista_sorted,
        y='track_name',
        x='track_duration_min',
        orientation='h',
        title=f'Duração das Músicas de {artista_selecionado}',
        labels={'track_duration_min': 'Duração (minutos)', 'track_name': 'Música'},
        color='track_duration_min',
        color_continuous_scale='blues'
    )

    fig_duracao.update_layout(
        yaxis_title_text='Música',
        xaxis_title_text='Duração (minutos)',
        height=400,
        margin=dict(t=80)
    )
    st.plotly_chart(fig_duracao, use_container_width=True)

    # =============================================
    # GRÁFICO 3: DISTRIBUIÇÃO POR ÁLBUM
    # =============================================

    st.subheader('💿 Distribuição por Álbum')

    # Contar músicas por álbum
    df_albuns_artista = df_artista['album_name'].value_counts().reset_index()
    df_albuns_artista.columns = ['Album', 'Quantidade']

    fig_albuns = px.pie(
        df_albuns_artista,
        values='Quantidade',
        names='Album',
        title=f'Distribuição de Músicas por Álbum - {artista_selecionado}',
        hole=0.4
    )

    st.plotly_chart(fig_albuns, use_container_width=True)

    # =============================================
    # GRÁFICO 4: LINHA DO TEMPO DE LANÇAMENTOS
    # =============================================

    st.subheader('📅 Linha do Tempo de Lançamentos')

    # Extrair ano e ordenar
    df_artista['release_year'] = df_artista['album_release_date'].dt.year
    df_timeline = df_artista.sort_values('album_release_date')

    fig_timeline = px.scatter(
        df_timeline,
        x='album_release_date',
        y='track_popularity',
        size='track_duration_min',
        color='album_name',
        title=f'Evolução da Popularidade - {artista_selecionado}',
        labels={
            'album_release_date': 'Data de Lançamento',
            'track_popularity': 'Popularidade',
            'album_name': 'Álbum',
            'track_duration_min': 'Duração'
        },
        hover_data=['track_name']
    )

    fig_timeline.update_layout(
        xaxis_title_text='Data de Lançamento',
        yaxis_title_text='Popularidade da Música',
        height=400
    )
    st.plotly_chart(fig_timeline, use_container_width=True)

    # =============================================
    # TABELA DETALHADA
    # =============================================

    st.subheader('📋 Detalhes das Músicas')

    # Colunas para exibir
    colunas_detalhes = {
        'track_name': 'Música',
        'album_name': 'Álbum',
        'track_popularity': 'Popularidade',
        'track_duration_min': 'Duração (min)',
        'explicit': 'Explícito',
        'album_release_date': 'Data Lançamento'
    }

    df_detalhes = df_artista[list(colunas_detalhes.keys())].rename(columns=colunas_detalhes)
    df_detalhes['Data Lançamento'] = df_detalhes['Data Lançamento'].dt.strftime('%d/%m/%Y')
    
    st.dataframe(df_detalhes, use_container_width=True)

else:
    st.warning('Nenhum dado encontrado para o artista selecionado.')

# =============================================
# COMPARAÇÃO ENTRE ARTISTAS
# =============================================

st.markdown('---')
st.header('🎭 Comparação entre Artistas')

col1, col2 = st.columns(2)

with col1:
    artista_1 = st.selectbox('Artista 1:', artistas_ordenados, key='artista1')
    
with col2:
    # Remove o artista 1 da lista do artista 2
    artistas_restantes = [a for a in artistas_ordenados if a != artista_1]
    artista_2 = st.selectbox('Artista 2:', artistas_restantes, key='artista2')

if artista_1 and artista_2:
    df_comp1 = df[df['artist_name'] == artista_1]
    df_comp2 = df[df['artist_name'] == artista_2]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(f"Popularidade Média - {artista_1}", 
                 f"{df_comp1['track_popularity'].mean():.1f}",
                 f"{df_comp1['track_popularity'].mean() - df_comp2['track_popularity'].mean():.1f}")
    
    with col2:
        st.metric(f"Popularidade Média - {artista_2}", 
                 f"{df_comp2['track_popularity'].mean():.1f}",
                 f"{df_comp2['track_popularity'].mean() - df_comp1['track_popularity'].mean():.1f}")
    
    with col3:
        st.metric(f"Duração Média - {artista_1}", 
                 f"{df_comp1['track_duration_min'].mean():.1f} min")
    
    with col4:
        st.metric(f"Duração Média - {artista_2}", 
                 f"{df_comp2['track_duration_min'].mean():.1f} min")

st.caption('🎵 Análise por Artista - Dashboard Spotify')