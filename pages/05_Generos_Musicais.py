import streamlit as st
import plotly.express as px
import pandas as pd
from utils.carrega_dados import carregar_dados

st.set_page_config(
    page_title='Gêneros Musicais',
    page_icon='🎼',
    layout='wide'
)

st.title('🎼 Análise de Gêneros Musicais')

# Carrega os dados
df = carregar_dados()

# =============================================
# PROCESSAMENTO DOS GÊNEROS
# =============================================

st.sidebar.header('🎛️ Filtros de Gênero')

@st.cache_data
def processar_generos(df):
    """Processa e extrai todos os gêneros musicais do dataset"""
    todos_generos = []
    
    for genero_str in df['artist_genres'].dropna():
        if genero_str != 'N/A':
            # Divide os gêneros separados por vírgula
            generos = [g.strip() for g in genero_str.split(',')]
            todos_generos.extend(generos)
    
    # Remove duplicatas e retorna lista ordenada
    return sorted(list(set(todos_generos)))

# Obter lista de gêneros
lista_generos = processar_generos(df)

# Filtro por gênero
genero_selecionado = st.sidebar.selectbox(
    'Selecione um Gênero para Análise:',
    ['Todos'] + lista_generos
)

# =============================================
# VISÃO GERAL DOS GÊNEROS
# =============================================

st.header('🌍 Panorama dos Gêneros Musicais')

# Contar frequência de cada gênero
@st.cache_data
def contar_generos(df):
    contagem_generos = {}
    
    for genero_str in df['artist_genres'].dropna():
        if genero_str != 'N/A':
            generos = [g.strip() for g in genero_str.split(',')]
            for genero in generos:
                contagem_generos[genero] = contagem_generos.get(genero, 0) + 1
    
    return pd.DataFrame({
        'Genero': list(contagem_generos.keys()),
        'Quantidade': list(contagem_generos.values())
    }).sort_values('Quantidade', ascending=False)

df_contagem_generos = contar_generos(df)

col1, col2 = st.columns(2)

with col1:
    st.subheader('🎯 Top 10 Gêneros Mais Comuns')
    
    fig_top_generos = px.bar(
        df_contagem_generos.head(10),
        x='Quantidade',
        y='Genero',
        orientation='h',
        title='Top 10 Gêneros Musicais',
        color='Quantidade',
        color_continuous_scale='purples'
    )
    
    fig_top_generos.update_layout(height=400)
    st.plotly_chart(fig_top_generos, use_container_width=True)

with col2:
    st.subheader('📊 Distribuição dos Gêneros')
    
    fig_pizza_generos = px.pie(
        df_contagem_generos.head(15),
        values='Quantidade',
        names='Genero',
        title='Distribuição dos 15 Gêneros Principais',
        hole=0.4
    )
    
    fig_pizza_generos.update_layout(height=400)
    st.plotly_chart(fig_pizza_generos, use_container_width=True)

st.markdown('---')

# =============================================
# ANÁLISE ESPECÍFICA POR GÊNERO
# =============================================

if genero_selecionado != 'Todos':
    st.header(f'🎵 Análise Detalhada: {genero_selecionado}')
    
    # Filtrar artistas do gênero selecionado
    def filtrar_por_genero(df, genero_alvo):
        artistas_do_genero = []
        
        for idx, row in df.iterrows():
            if pd.notna(row['artist_genres']) and row['artist_genres'] != 'N/A':
                generos_artista = [g.strip() for g in row['artist_genres'].split(',')]
                if genero_alvo in generos_artista:
                    artistas_do_genero.append(row['artist_name'])
        
        return df[df['artist_name'].isin(artistas_do_genero)]
    
    df_genero = filtrar_por_genero(df, genero_selecionado)
    
    if not df_genero.empty:
        # Métricas do gênero
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            artistas_unicos = df_genero['artist_name'].nunique()
            st.metric("Artistas Únicos", artistas_unicos)
        
        with col2:
            musicas_total = len(df_genero)
            st.metric("Total de Músicas", musicas_total)
        
        with col3:
            popularidade_media = df_genero['track_popularity'].mean()
            st.metric("Popularidade Média", f"{popularidade_media:.1f}")
        
        with col4:
            duracao_media = df_genero['track_duration_min'].mean()
            st.metric("Duração Média", f"{duracao_media:.1f} min")
        
        # =============================================
        # TOP ARTISTAS DO GÊNERO
        # =============================================
        
        st.subheader(f'👑 Top Artistas do {genero_selecionado}')
        
        # Agrupar por artista e calcular métricas
        df_artistas_genero = df_genero.groupby('artist_name').agg({
            'track_popularity': 'mean',
            'artist_popularity': 'first',
            'artist_followers': 'first',
            'track_name': 'count'
        }).round(2).reset_index()
        
        df_artistas_genero.columns = ['Artista', 'Popularidade_Média', 'Popularidade_Artista', 'Seguidores', 'Quantidade_Musicas']
        df_artistas_genero = df_artistas_genero.sort_values('Popularidade_Média', ascending=False)
        
        fig_artistas_genero = px.bar(
            df_artistas_genero.head(10),
            x='Popularidade_Média',
            y='Artista',
            orientation='h',
            title=f'Top 10 Artistas do {genero_selecionado} por Popularidade Média',
            color='Popularidade_Média',
            color_continuous_scale='greens'
        )
        
        fig_artistas_genero.update_layout(height=400)
        st.plotly_chart(fig_artistas_genero, use_container_width=True)
        
        # =============================================
        # DISTRIBUIÇÃO DE POPULARIDADE
        # =============================================
        
        st.subheader(f'📈 Distribuição de Popularidade no {genero_selecionado}')
        
        fig_distribuicao = px.histogram(
            df_genero,
            x='track_popularity',
            nbins=20,
            title=f'Distribuição de Popularidade - {genero_selecionado}',
            labels={'track_popularity': 'Popularidade'},
            color_discrete_sequence=['lightblue']
        )
        
        fig_distribuicao.update_layout(height=400)
        st.plotly_chart(fig_distribuicao, use_container_width=True)
        
        # =============================================
        # COMPARAÇÃO ENTRE GÊNEROS
        # =============================================
        
        st.subheader('🆚 Comparação com Outros Gêneros')
        
        # Selecionar alguns gêneros para comparação
        generos_comparacao = st.multiselect(
            'Selecione gêneros para comparar:',
            lista_generos,
            default=[genero_selecionado] + list(df_contagem_generos['Genero'].head(3))
        )
        
        if generos_comparacao:
            dados_comparacao = []
            
            for genero in generos_comparacao:
                df_gen = filtrar_por_genero(df, genero)
                if not df_gen.empty:
                    dados_comparacao.append({
                        'Genero': genero,
                        'Popularidade_Media': df_gen['track_popularity'].mean(),
                        'Duracao_Media': df_gen['track_duration_min'].mean(),
                        'Quantidade_Musicas': len(df_gen),
                        'Artistas_Unicos': df_gen['artist_name'].nunique()
                    })
            
            if dados_comparacao:
                df_comparacao = pd.DataFrame(dados_comparacao)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_comp_popularidade = px.bar(
                        df_comparacao,
                        x='Genero',
                        y='Popularidade_Media',
                        title='Comparação de Popularidade Média',
                        color='Popularidade_Media',
                        color_continuous_scale='reds'
                    )
                    st.plotly_chart(fig_comp_popularidade, use_container_width=True)
                
                with col2:
                    fig_comp_duracao = px.bar(
                        df_comparacao,
                        x='Genero',
                        y='Duracao_Media',
                        title='Comparação de Duração Média',
                        color='Duracao_Media',
                        color_continuous_scale='blues'
                    )
                    st.plotly_chart(fig_comp_duracao, use_container_width=True)
    
    else:
        st.warning(f'Nenhum artista encontrado para o gênero "{genero_selecionado}"')

else:
    st.info('🎯 Selecione um gênero específico na barra lateral para ver análises detalhadas.')

# =============================================
# MAPA DE GÊNEROS E SUBGÊNEROS
# =============================================

st.markdown('---')
st.header('🗺️ Mapa de Relações entre Gêneros')

# Análise de co-ocorrência de gêneros
@st.cache_data
def analisar_coocorrencia(df):
    coocorrencias = {}
    
    for genero_str in df['artist_genres'].dropna():
        if genero_str != 'N/A':
            generos = [g.strip() for g in genero_str.split(',')]
            
            # Para cada par de gêneros no mesmo artista
            for i in range(len(generos)):
                for j in range(i + 1, len(generos)):
                    par = tuple(sorted([generos[i], generos[j]]))
                    coocorrencias[par] = coocorrencias.get(par, 0) + 1
    
    # Converter para DataFrame
    pares_coocorrencia = []
    for par, count in coocorrencias.items():
        if count >= 5:  # Só mostrar pares com pelo menos 5 ocorrências
            pares_coocorrencia.append({
                'Genero1': par[0],
                'Genero2': par[1],
                'Coocorrencias': count
            })
    
    return pd.DataFrame(pares_coocorrencia).sort_values('Coocorrencias', ascending=False)

df_coocorrencia = analisar_coocorrencia(df)

if not df_coocorrencia.empty:
    st.subheader('🔗 Gêneros que Frequentemente Aparecem Juntos')
    
    # Mostrar top pares
    st.dataframe(df_coocorrencia.head(15), use_container_width=True)
    
    st.info("""
    **💡 Insight:** Estes são gêneros que frequentemente são associados aos mesmos artistas, 
    mostrando possíveis fusões ou influências mútuas entre estilos musicais.
    """)

st.caption('🎼 Análise de Gêneros Musicais - Dashboard Spotify')