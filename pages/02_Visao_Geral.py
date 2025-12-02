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

# Criar categorias agrupando por duração para melhor visualização
df['duration_category'] = pd.cut(df['track_duration_min'], 
                               bins=[0, 2, 4, 6, 10, 20], 
                               labels=['0-2min', '2-4min', '4-6min', '6-10min', '10+min'])

# Converter para string para evitar problemas de serialização
df['duration_category_str'] = df['duration_category'].astype(str)

#CRIANDO GRAFICO BOXPLOT
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
- **Popularidade:** Escala de 0-100, onde 100 é mais popular
- **Duração:** Categorizada em intervalos de minutos
""")
# =============================================
# INTERPRETAÇÃO AUTOMÁTICA DO GRÁFICO
# =============================================

# 1. Encontrar qual categoria tem MAIS músicas
categoria_mais_comum = (
    df['duration_category_str']
    .value_counts()
    .idxmax()
)

# 2. Encontrar qual categoria tem MAIOR POPULARIDADE MÉDIA
categoria_mais_popular = (
    df.groupby('duration_category_str')['track_popularity']
    .mean()
    .idxmax()
)

# 3. Mediana por categoria para interpretar distribuição
medianas = df.groupby('duration_category_str')['track_popularity'].median()

# 4. Determinar categoria com MENOR popularidade mediana
categoria_menos_popular = medianas.idxmin()

# 5. Número de outliers (pontos fora do padrão) por categoria
outliers_info = {}
for cat in df['duration_category_str'].unique():
    grupo = df[df['duration_category_str'] == cat]['track_popularity']
    q1, q3 = grupo.quantile([0.25, 0.75])
    iqr = q3 - q1
    limite_superior = q3 + 1.5 * iqr
    outliers = grupo[grupo > limite_superior]
    outliers_info[cat] = len(outliers)

categoria_mais_outliers = max(outliers_info, key=outliers_info.get)


st.markdown(f"""
### 🧠 Interpretação Automática do Gráfico

- A maior densidade de músicas está na categoria **{categoria_mais_comum}**, indicando ser a duração mais comum do dataset.
- As músicas **mais populares**, em média, pertencem à categoria **{categoria_mais_popular}**.
- A categoria menos popular, analisando a mediana, é **{categoria_menos_popular}**.
- A categoria que apresenta **mais outliers de popularidade** (músicas muito mais populares que o restante do grupo) é **{categoria_mais_outliers}**.
- Isso sugere que músicas de duração **moderada** tendem a ter desempenho mais consistente, enquanto músicas muito curtas ou muito longas apresentam grande variabilidade.
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

st.markdown("""
**📝 Interpretação:** Analisa que músicas de albuns possuem maior populares.
""")

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

st.markdown("""
**📝 Interpretação:** Analisa que a artista mais popular é a Taylor Swift.
""")
st.markdown("---")


# =============================================
# GRÁFICO 6: EVOLUÇÃO TEMPORAL (LANÇAMENTOS)
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
# =============================================
# INTERPRETAÇÃO AUTOMÁTICA DO GRÁFICO TEMPORAL
# =============================================

# Encontrar ano com mais lançamentos
ano_max = df_anos.loc[df_anos['Quantidade'].idxmax(), 'Ano']
qtd_max = df_anos['Quantidade'].max()

# Encontrar ano com menos lançamentos
ano_min = df_anos.loc[df_anos['Quantidade'].idxmin(), 'Ano']
qtd_min = df_anos['Quantidade'].min()

# Tendência geral ao longo dos anos (aumento, queda ou estabilidade)
import numpy as np
coef = np.polyfit(df_anos['Ano'], df_anos['Quantidade'], 1)[0]

if coef > 0:
    tendencia = "uma **tendência geral de aumento** no número de lançamentos ao longo dos anos"
elif coef < 0:
    tendencia = "uma **tendência geral de queda** no número de lançamentos ao longo dos anos"
else:
    tendencia = "um **comportamento estável**, sem tendência clara de crescimento ou queda"

# Montar texto final
interpretacao_temporal = f"""
### 🧠 Interpretação Automática do Gráfico — Lançamentos ao Longo do Tempo

- O ano com **maior número de lançamentos** foi **{ano_max}**, com aproximadamente **{qtd_max} músicas**.
- O ano com **menor número de lançamentos** foi **{ano_min}**, com cerca de **{qtd_min} músicas**.
- A análise da linha temporal indica **{tendencia}**.
"""

st.markdown(interpretacao_temporal)

st.markdown("---")

# =============================================
# MÉTRICAS RÁPIDAS NO FINAL
# =============================================

st.subheader('📋 Resumo Estatístico')


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

