# Importação das bibliotecas e funções
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.carrega_dados import carregar_dados

st.set_page_config(
    page_title='Visão Geral',
    page_icon='📈',
    layout='wide'
)

st.title('Visão Geral dos Dados Musicais do Spotify')

# Carrega os dados usando a função cacheada
df = carregar_dados()

# =============================================
# GRÁFICO 1: BOXPLOT - POPULARIDADE POR DURAÇÃO
# =============================================

st.subheader('📊 Distribuição da Popularidade por Duração da Música')

# Criar categorias de duração para melhor visualização
df['duration_category'] = pd.cut(df['track_duration_min'], 
                               bins=[0, 2, 4, 6, 10, 20], 
                               labels=['0-2min', '2-4min', '4-6min', '6-10min', '10+min'])

# Converter para string para evitar problemas de serialização
df['duration_category_str'] = df['duration_category'].astype(str)

fig = px.box(df,
    x='duration_category_str',
    y='track_popularity',
    points='all',
    title='Distribuição da Popularidade por Duração da Música',
    labels={'track_popularity':'Popularidade', 'duration_category_str':'Duração (minutos)'},
    color='duration_category_str',
    color_discrete_sequence=px.colors.qualitative.Set3
)

fig.update_layout(
    xaxis_title_text='Duração da Música',
    yaxis_title_text='Popularidade',
    title_x=0.5,
    margin=dict(t=80)
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
**📝 Interpretação:** Este gráfico mostra como a popularidade das músicas se distribui entre diferentes durações.
- **Popularidade:** Escala de 0-100, onde 100 é mais popular
- **Duração:** Categorizada em intervalos de minutos
""")

st.markdown("---")

# =============================================
# GRÁFICO 2: BOXPLOT - POPULARIDADE DO ARTISTA VS MÚSICA
# =============================================

st.subheader('📊 Popularidade do Artista vs Popularidade da Música')

# Criar categorias para popularidade do artista
df['artist_popularity_cat'] = pd.cut(df['artist_popularity'], 
                                   bins=5, 
                                   labels=['Muito Baixa', 'Baixa', 'Média', 'Alta', 'Muito Alta'])

# Converter para string
df['artist_popularity_cat_str'] = df['artist_popularity_cat'].astype(str)

fig = px.box(df,
    x='artist_popularity_cat_str',
    y='track_popularity',
    points='all',
    title='Relação entre Popularidade do Artista e Popularidade da Música',
    labels={'track_popularity':'Popularidade da Música', 'artist_popularity_cat_str':'Popularidade do Artista'},
    color_discrete_sequence=['lightblue']
)

fig.update_layout(
    xaxis_title_text='Popularidade do Artista',
    yaxis_title_text='Popularidade da Música',
    title_x=0.5,
    margin=dict(t=80),
    xaxis_tickangle=-45
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
**📝 Interpretação:** Analisa se artistas mais populares tendem a ter músicas mais populares.
""")

st.markdown("---")

# =============================================
# GRÁFICO 3: DISTRIBUIÇÃO POR TIPO DE ÁLBUM
# =============================================

st.subheader('🎯 Distribuição de Músicas por Tipo de Álbum')

# Contagem por tipo de álbum
df_albuns = df['album_type'].value_counts().reset_index()
df_albuns.columns = ['Tipo_Album', 'Quantidade']

fig_barras = px.bar(
    df_albuns,
    x='Tipo_Album',
    y='Quantidade',
    title='Quantidade de Músicas por Tipo de Álbum',
    labels={'Quantidade': 'Número de Músicas', 'Tipo_Album': 'Tipo de Álbum'},
    color='Quantidade',
    color_continuous_scale='blues'
)

fig_barras.update_layout(
    xaxis_title_text='Tipo de Álbum',
    yaxis_title_text='Quantidade de Músicas',
    title_x=0.5,
    margin=dict(t=80)
)
st.plotly_chart(fig_barras, use_container_width=True)

st.markdown("---")


# =============================================
# GRÁFICO 5: TOP ARTISTAS MAIS POPULARES
# =============================================

st.subheader('👑 Top Artistas Mais Populares')

# Top 10 artistas por popularidade média
df_artistas = df.groupby('artist_name')['artist_popularity'].mean().nlargest(10).reset_index()
df_artistas.columns = ['Artista', 'Popularidade_Média']

fig_barras_h = px.bar(
    df_artistas,
    y='Artista',
    x='Popularidade_Média',
    orientation='h',
    title='Top 10 Artistas por Popularidade Média',
    labels={'Popularidade_Média': 'Popularidade Média', 'Artista': 'Artista'},
    color='Popularidade_Média',
    color_continuous_scale='viridis'
)

fig_barras_h.update_layout(
    yaxis_title_text='Artista',
    xaxis_title_text='Popularidade Média',
    title_x=0.5,
    margin=dict(t=80)
)
st.plotly_chart(fig_barras_h, use_container_width=True)

st.markdown("---")

# =============================================
# GRÁFICO 6: SCATTER PLOT - DURAÇÃO VS POPULARIDADE
# =============================================

st.subheader('📈 Relação entre Duração e Popularidade das Músicas')

fig_scatter = px.scatter(
    df,
    x='track_duration_min',
    y='track_popularity',
    color='explicit',
    size='artist_popularity',
    title='Relação entre Duração e Popularidade das Músicas',
    labels={
        'track_duration_min': 'Duração (minutos)',
        'track_popularity': 'Popularidade da Música',
        'explicit': 'Conteúdo Explícito',
        'artist_popularity': 'Popularidade do Artista'
    },
    color_discrete_map={'Sim': 'red', 'Não': 'green'},
    hover_data=['artist_name', 'album_name']
)

fig_scatter.update_layout(
    xaxis_title_text='Duração da Música (minutos)',
    yaxis_title_text='Popularidade da Música',
    title_x=0.5,
    margin=dict(t=80)
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("""
**📝 Interpretação:** Este gráfico de dispersão permite visualizar a relação entre a duração das músicas e sua popularidade.
- **Cores:** Indicam se a música tem conteúdo explícito
- **Tamanho dos pontos:** Representa a popularidade do artista
""")

# =============================================
# GRÁFICO 7: EVOLUÇÃO TEMPORAL (LANÇAMENTOS)
# =============================================

st.subheader('📅 Distribuição de Lançamentos por Ano')

# Extrair ano da data de lançamento
df['release_year'] = df['album_release_date'].dt.year

# Contar lançamentos por ano
df_anos = df['release_year'].value_counts().sort_index().reset_index()
df_anos.columns = ['Ano', 'Quantidade']

fig_temporal = px.line(
    df_anos,
    x='Ano',
    y='Quantidade',
    title='Distribuição de Lançamentos de Músicas por Ano',
    labels={'Quantidade': 'Número de Músicas', 'Ano': 'Ano de Lançamento'}
)

fig_temporal.update_layout(
    xaxis_title_text='Ano de Lançamento',
    yaxis_title_text='Quantidade de Músicas',
    title_x=0.5,
    margin=dict(t=80)
)
st.plotly_chart(fig_temporal, use_container_width=True)

st.markdown("---")

# =============================================
# MÉTRICAS RÁPIDAS NO FINAL
# =============================================

st.markdown("---")
st.subheader('📋 Resumo Estatístico')

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Músicas", f"{len(df):,}")
    
with col2:
    media_duracao = df['track_duration_min'].mean()
    st.metric("Duração Média", f"{media_duracao:.1f} min")
    
with col3:
    popularidade_media = df['track_popularity'].mean()
    st.metric("Popularidade Média", f"{popularidade_media:.1f}")
    
with col4:
    musicas_explicit = len(df[df['explicit'] == 'Sim'])
    st.metric("Músicas Explícitas", f"{musicas_explicit}")

# Métricas adicionais
col5, col6, col7, col8 = st.columns(4)

with col5:
    artistas_unicos = df['artist_name'].nunique()
    st.metric("Artistas Únicos", f"{artistas_unicos}")
    
with col6:
    albuns_unicos = df['album_name'].nunique()
    st.metric("Álbuns Únicos", f"{albuns_unicos}")
    
with col7:
    max_popularity = df['track_popularity'].max()
    st.metric("Popularidade Máxima", f"{max_popularity}")
    
with col8:
    min_year = df['release_year'].min()
    max_year = df['release_year'].max()
    st.metric("Período Analisado", f"{min_year}-{max_year}")

st.caption("🎵 Dashboard de Análise de Dados Musicais - Desenvolvido para Projeto Streamlit")