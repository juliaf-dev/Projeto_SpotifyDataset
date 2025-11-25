import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils.carrega_dados import carregar_dados

st.set_page_config(
    page_title='Popularidade & Duração',
    page_icon='📈',
    layout='wide'
)

st.title('📈 Relação entre Popularidade e Duração')

# Carrega os dados
df = carregar_dados()

# =============================================
# ANÁLISE DE CORRELAÇÃO
# =============================================

st.header('🔗 Correlação entre Variáveis')

# Calcular matriz de correlação
variaveis_numericas = ['track_popularity', 'artist_popularity', 'track_duration_min', 'artist_followers']
df_corr = df[variaveis_numericas].corr()

# Gráfico de heatmap de correlação
fig_corr = px.imshow(
    df_corr,
    text_auto=True,
    aspect='auto',
    color_continuous_scale='RdBu_r',
    title='Matriz de Correlação entre Variáveis Musicais'
)

fig_corr.update_layout(height=500)
st.plotly_chart(fig_corr, use_container_width=True)

st.markdown("""
**📝 Interpretação:**
- **Valores próximos de 1:** Correlação positiva forte (quando uma aumenta, a outra também)
- **Valores próximos de -1:** Correlação negativa forte (quando uma aumenta, a outra diminui)  
- **Valores próximos de 0:** Pouca ou nenhuma correlação
""")

st.markdown('---')

# =============================================
# GRÁFICO 1: SCATTER PLOT AVANÇADO
# =============================================

st.header('🎯 Popularidade vs Duração - Análise Detalhada')

col1, col2 = st.columns([3, 1])

with col1:
    # Scatter plot interativo
    fig_scatter = px.scatter(
        df,
        x='track_duration_min',
        y='track_popularity',
        color='artist_popularity',
        size='artist_followers',
        hover_name='track_name',
        hover_data=['artist_name', 'album_name', 'explicit'],
        title='Relação entre Duração e Popularidade das Músicas',
        labels={
            'track_duration_min': 'Duração (minutos)',
            'track_popularity': 'Popularidade da Música',
            'artist_popularity': 'Popularidade do Artista',
            'artist_followers': 'Seguidores do Artista'
        },
        color_continuous_scale='viridis'
    )
    
    fig_scatter.update_layout(height=600)
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    st.subheader('📊 Estatísticas')
    
    correlacao = df['track_duration_min'].corr(df['track_popularity'])
    st.metric("Correlação Duração-Popularidade", f"{correlacao:.3f}")
    
    st.markdown("**Distribuição por Duração:**")
    
    # Estatísticas por faixa de duração
    df['faixa_duracao'] = pd.cut(df['track_duration_min'], 
                                bins=[0, 2, 3, 4, 5, 10, 20],
                                labels=['0-2min', '2-3min', '3-4min', '4-5min', '5-10min', '10+min'])
    
    stats_duracao = df.groupby('faixa_duracao')['track_popularity'].agg(['mean', 'count']).round(2)
    st.dataframe(stats_duracao)

st.markdown('---')

# =============================================
# GRÁFICO 2: DENSIDADE 2D
# =============================================

st.header('📊 Densidade da Relação Popularidade-Duração')

# Gráfico de densidade 2D
fig_density = px.density_heatmap(
    df,
    x='track_duration_min',
    y='track_popularity',
    nbinsx=30,
    nbinsy=20,
    title='Densidade de Músicas por Duração e Popularidade',
    labels={
        'track_duration_min': 'Duração (minutos)',
        'track_popularity': 'Popularidade'
    },
    color_continuous_scale='viridis'
)

fig_density.update_layout(height=500)
st.plotly_chart(fig_density, use_container_width=True)

st.markdown('---')

# =============================================
# GRÁFICO 3: ANÁLISE POR FAIXAS
# =============================================

st.header('📋 Análise por Faixas de Duração')

# Criar faixas de duração
df['faixa_duracao'] = pd.cut(df['track_duration_min'], 
                            bins=[0, 2, 3, 4, 5, 10, 20],
                            labels=['0-2min', '2-3min', '3-4min', '4-5min', '5-10min', '10+min'])

# Boxplot por faixa de duração
fig_box_faixas = px.box(
    df,
    x='faixa_duracao',
    y='track_popularity',
    title='Distribuição de Popularidade por Faixa de Duração',
    labels={
        'faixa_duracao': 'Faixa de Duração',
        'track_popularity': 'Popularidade'
    },
    color='faixa_duracao'
)

fig_box_faixas.update_layout(height=500)
st.plotly_chart(fig_box_faixas, use_container_width=True)

# =============================================
# ANÁLISE DE OUTLIERS
# =============================================

st.markdown('---')
st.header('🔍 Análise de Valores Extremos')

col1, col2 = st.columns(2)

with col1:
    st.subheader('🎵 Músicas Mais Curtas e Populares')
    
    # Músicas curtas e populares
    df_curtas_populares = df.nsmallest(10, 'track_duration_min').nlargest(5, 'track_popularity')
    for idx, row in df_curtas_populares.iterrows():
        st.write(f"**{row['track_name']}** - {row['artist_name']}")
        st.write(f"⏱️ {row['track_duration_min']:.1f}min | ⭐ {row['track_popularity']}/100")
        st.write('---')

with col2:
    st.subheader('🎵 Músicas Mais Longas e Populares')
    
    # Músicas longas e populares
    df_longas_populares = df.nlargest(10, 'track_duration_min').nlargest(5, 'track_popularity')
    for idx, row in df_longas_populares.iterrows():
        st.write(f"**{row['track_name']}** - {row['artist_name']}")
        st.write(f"⏱️ {row['track_duration_min']:.1f}min | ⭐ {row['track_popularity']}/100")
        st.write('---')

# =============================================
# RECOMENDAÇÕES BASEADAS EM DADOS
# =============================================

st.markdown('---')
st.header('💡 Insights Práticos')

col1, col2 = st.columns(2)

with col1:
    st.subheader('🎯 Duração Ideal')
    
    # Encontrar a duração com maior popularidade média
    popularidade_por_duracao = df.groupby('faixa_duracao')['track_popularity'].mean()
    duracao_ideal = popularidade_por_duracao.idxmax()
    popularidade_max = popularidade_por_duracao.max()
    
    st.metric("Faixa de Duração Mais Popular", duracao_ideal, f"{popularidade_max:.1f} de popularidade média")
    
    st.info("""
    **Insight:** Músicas entre 3-4 minutos tendem a ter a melhor relação 
    entre engajamento do ouvinte e potencial de popularidade.
    """)

with col2:
    st.subheader('📊 Estatísticas Globais')
    
    duracao_media_geral = df['track_duration_min'].mean()
    popularidade_media_geral = df['track_popularity'].mean()
    
    st.metric("Duração Média Global", f"{duracao_media_geral:.1f} min")
    st.metric("Popularidade Média Global", f"{popularidade_media_geral:.1f}/100")
    
    # Correlação
    correlacao = df['track_duration_min'].corr(df['track_popularity'])
    st.metric("Correlação Geral", f"{correlacao:.3f}")

st.caption('📈 Análise de Popularidade & Duração - Dashboard Spotify')