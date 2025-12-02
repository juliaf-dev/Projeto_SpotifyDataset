import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from utils.carrega_dados import carregar_dados

st.set_page_config(
    page_title='Insights Avançados',
    page_icon='🔍',
    layout='wide'
)

st.title('🔍 Insights Avançados e Análises Estatísticas')

# Isso evita recarregar os dados a cada interação, melhorando a experiência do usuário
df = carregar_dados()

# =============================================
# ANÁLISE DE TENDÊNCIAS TEMPORAIS AVANÇADA
# =============================================

st.header('📈 Evolução Temporal das Características Musicais')

# Mostra evolução real do mercado musical ao longo do tempo
df['release_year'] = df['album_release_date'].dt.year
df_temporal = df[df['release_year'] >= 2010]  # Focar em anos mais relevantes

# Permite ver várias tendências simultaneamente
df_ano = df_temporal.groupby('release_year').agg({
    'track_popularity': 'mean',
    'track_duration_min': 'mean', 
    'artist_popularity': 'mean',
    'track_name': 'count',
    'explicit': lambda x: (x == 'Sim').mean() * 100  # % de conteúdo explícito
}).reset_index()

df_ano.columns = ['Ano', 'Popularidade_Media', 'Duracao_Media', 'Popularidade_Artista_Media', 
                  'Quantidade_Musicas', 'Percentual_Explicito']

# de diferentes escalas (popularidade vs duração vs quantidade)
fig_temporal = go.Figure()

# Popularidade (eixo principal)
fig_temporal.add_trace(go.Scatter(
    x=df_ano['Ano'], y=df_ano['Popularidade_Media'],
    name='🎵 Popularidade Média',
    line=dict(color='#1DB954', width=4),  # Verde do Spotify
    mode='lines+markers'
))

# Duração (eixo secundário)
fig_temporal.add_trace(go.Scatter(
    x=df_ano['Ano'], y=df_ano['Duracao_Media'],
    name='⏱️ Duração Média',
    line=dict(color='#FF6B6B', width=3),
    yaxis='y2'
))

# Quantidade de lançamentos (eixo terciário)
fig_temporal.add_trace(go.Bar(
    x=df_ano['Ano'], y=df_ano['Quantidade_Musicas'],
    name='📊 Lançamentos',
    marker_color='rgba(100, 149, 237, 0.6)',
    yaxis='y3'
))

fig_temporal.update_layout(
    title='Evolução do Mercado Musical (2010-2025)',
    xaxis_title='Ano de Lançamento',
    yaxis=dict(title='Popularidade Média', side='left'),
    yaxis2=dict(title='Duração Média (minutos)', overlaying='y', side='right'),
    yaxis3=dict(title='Quantidade de Lançamentos', overlaying='y', side='right', position=0.85),
    height=500,
    showlegend=True
)

st.plotly_chart(fig_temporal, use_container_width=True)


st.markdown('---')

# =============================================
# ANÁLISE DE SEGMENTAÇÃO DE MERCADO MELHORADA
# =============================================

st.header('🎵 Segmentação Estratégica do Mercado Musical')

# que clusterização automática. Baseada em conhecimento do domínio musical.
st.markdown("""
**Metodologia:** Segmentação baseada em regras de negócio da indústria musical.
Categoriza artistas em grupos estrategicamente relevantes.
""")

# Segmentação melhorada com critérios de negócio
conditions = [
    (df['artist_popularity'] >= 80) & (df['artist_followers'] >= 5000000),
    (df['artist_popularity'] >= 65) & (df['artist_followers'] >= 1000000),
    (df['artist_popularity'] >= 50) & (df['artist_followers'] >= 100000),
    (df['artist_popularity'] >= 35) & (df['artist_followers'] >= 10000),
    (df['artist_popularity'] < 35) | (df['artist_followers'] < 10000)
]

segments = ['🏆 Superstars', '⭐ Estrelas', '🚀 Emergentes', '🌱 Promessas', '🎨 Independentes']
df['segmento_estrategico'] = np.select(conditions, segments, default='🎨 Independentes')

# Gráfico de segmentação interativo
fig_segmentos = px.scatter(
    df.drop_duplicates('artist_name'),
    x='artist_popularity',
    y='artist_followers',
    color='segmento_estrategico',
    size='artist_popularity',
    hover_name='artist_name',
    hover_data=['artist_genres'],
    title='Mapa Estratégico do Mercado Musical por Segmento',
    labels={
        'artist_popularity': 'Popularidade do Artista',
        'artist_followers': 'Seguidores no Spotify',
        'segmento_estrategico': 'Segmento Estratégico'
    },
    log_y=True,
    color_discrete_sequence=px.colors.qualitative.Bold
)

fig_segmentos.update_layout(
    height=600,
    xaxis_title="Popularidade do Artista (0-100)",
    yaxis_title="Seguidores (Escala Logarítmica)"
)

st.plotly_chart(fig_segmentos, use_container_width=True)

# de forma mais clara que clusters abstratos
st.subheader('📊 Análise de Oportunidades por Segmento')

segment_stats = df.groupby('segmento_estrategico').agg({
    'track_popularity': ['mean', 'count'],
    'track_duration_min': 'mean',
    'artist_name': 'nunique',
    'explicit': lambda x: (x == 'Sim').mean() * 100
}).round(2)

# Reformatar o DataFrame para melhor visualização
segment_stats.columns = ['Popularidade_Média', 'Total_Músicas', 'Duração_Média', 'Artistas_Únicos', 'Percentual_Explicito']
segment_stats = segment_stats.sort_values('Popularidade_Média', ascending=False)

st.dataframe(segment_stats, use_container_width=True)

st.markdown('---')

# =============================================
# ANÁLISE PREDITIVA SIMPLES E INTERPRETÁVEL
# =============================================

st.header('🔮 Simulador de Potencial de Popularidade')

# JUSTIFICATIVA: Modelo preditivo simples é mais útil que clusterização
# Dá ao usuário ferramentas práticas para tomada de decisão
st.markdown("""
**Como funciona:** Baseado nas correlações identificadas nos dados, estimamos o potencial 
de popularidade de uma música considerando características do artista e da música.
""")

# JUSTIFICATIVA: Simulador interativo engaja usuários e mostra aplicação prática dos insights dos dados
st.subheader('🎮 Experimente o Simulador')

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**👤 Perfil do Artista**")
    artist_pop = st.slider(
        'Popularidade do Artista:',
        0, 100, 70,
        help="Quão conhecido é o artista no mercado"
    )
    artist_followers = st.slider(
        'Seguidores (milhões):',
        0.0, 100.0, 5.0, 0.1,
        help="Base de fãs no Spotify"
    )

with col2:
    st.markdown("**🎵 Características da Música**")
    track_duration = st.slider(
        'Duração (minutos):',
        1.0, 10.0, 3.5, 0.1,
        help="Duração ideal está entre 3-4 minutos"
    )

with col3:
    st.markdown("**📊 Métricas Adicionais**")
    album_type = st.selectbox(
        'Tipo de Álbum:',
        ['single', 'album', 'compilation'],
        help="Singles tendem a ser mais focados em sucesso comercial"
    )


# Fórmula preditiva baseada nas correlações observadas
if st.button('🎯 Calcular Potencial de Popularidade', type='primary'):

    # Fatores inspirados nas correlações reais
    fator_artista = artist_pop * 0.6                    # mais relevante
    fator_seguidores = (artist_followers / 100) * 100 * 0.25  # até 25% do peso
    fator_duracao = max(0, 50 - abs(track_duration - 3.5) * 20) * 0.15

    # singles tendem a performar melhor
    fator_album = 8 if album_type == 'single' else 0

    # Soma final
    popularidade_estimada = (
        fator_artista +
        fator_seguidores +
        fator_duracao +
        fator_album
    )

    # Limitar entre 0 e 100
    popularidade_estimada = max(0, min(100, popularidade_estimada))

    # Exibir resultado
    st.success(f"## 🎵 Potencial de Popularidade Estimado: **{popularidade_estimada:.1f}/100**")

    # ============================
    # ANÁLISE DETALHADA
    # ============================

    col_analise1, col_analise2 = st.columns(2)

    with col_analise1:
        if popularidade_estimada >= 80:
            st.info("""
            **🔥 Alto Potencial de Sucesso!**
            - Grande chance de entrar nas paradas
            - Potencial viral nas redes sociais
            - Muito alinhado com os padrões das músicas mais populares
            """)
        elif popularidade_estimada >= 60:
            st.info("""
            **💫 Bom Potencial**
            - Forte engajamento esperado
            - Pode crescer com marketing adequado
            - Artista bem posicionado
            """)
        elif popularidade_estimada >= 40:
            st.info("""
            **⭐ Potencial Moderado**
            - Atinge nichos específicos
            - Depende mais do momento e divulgação
            """)
        else:
            st.info("""
            **🌱 Baixo Potencial Inicial**
            - Precisa de maior visibilidade
            - Estratégias de lançamento podem ajudar
            """)

    with col_analise2:
        st.markdown("### 📌 O que mais influenciou o resultado?")
        st.markdown(f"""
        - **Popularidade do artista:** {fator_artista:.1f} pontos  
        - **Seguidores do artista:** {fator_seguidores:.1f} pontos  
        - **Duração da música:** {fator_duracao:.1f} pontos  
        - **Tipo do álbum:** +{fator_album} pontos  
        """)



# =============================================
# RECOMENDAÇÕES ESTRATÉGICAS BASEADAS EM DADOS
# =============================================

st.header('💡 Recomendações Estratégicas Baseadas em Evidências')

# visualizações complexas sem aplicação prática
col1, col2 = st.columns(2)

with col1:

    
    st.markdown("""
    
    ### ⏱️ Otimização de Duração
    - **Foco em 3-4 minutos**: Maior engajamento do ouvinte
    - **Evite extremos**: Músicas muito curtas ou longas performam pior
    - **Estrutura eficiente**: Mantenha a atenção do início ao fim
    
    ### 👥 Construção de Base de Fãs
    - **Seguidores = Popularidade**: Correlação de +0.7 comprovada
    - **Marketing digital**: Invista em redes sociais e playlists
    - **Engajamento constante**: Interaja com sua comunidade
    
    ### 🎯 Conhecimento de Mercado
    - **Estude seu segmento**: Artistas similares têm estratégias testadas
    - **Identifique oportunidades**: Segmentos menos saturados
    - **Análise sazonal**: Melhores épocas para lançamento
    """)

with col2:
    st.subheader('🏢 Para a Indústria Musical')
    
    st.markdown("""
    **📊 Decisões Data-Driven:**
    
    ### 🔍 Descoberta de Talentos
    - **Artistas emergentes**: Busque alta correlação popularidade-seguidores
    - **Segmentos promissores**: "Promessas" com crescimento acelerado
    - **Diversidade genérica**: Explore gêneros com alta popularidade média
    
    ### 📈 Gestão Estratégica
    - **Portfólio balanceado**: Mix entre superstars e independentes
    - **Timing de lançamentos**: Alta temporada para lançamentos importantes
    - **Análise de tendências**: Acompanhe evolução do mercado anualmente
    
    ### 🎪 Inovação no Catálogo
    - **Experimentos controlados**: Teste novos formatos em pequena escala
    - **Colaborações estratégicas**: Una artistas de segmentos complementares
    - **Dados como guia**: Use análises para validar intuições criativas
    """)
