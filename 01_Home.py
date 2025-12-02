import streamlit as st
from utils.carrega_dados import carregar_dados

st.set_page_config(
    page_title="Análise de Músicas do Spotify",
    page_icon="🎵",
    layout="wide"
)

st.title("Análise de Dados Musicais do Spotify")

# Carrega os dados usando a função cacheada
df = carregar_dados()

st.markdown(f"""
Bem-vindo(a) ao **Dashboard de Análise de Dados Musicais do Spotify**!

Este aplicativo interativo foi desenvolvido para explorar e visualizar as principais percepções sobre músicas, artistas e álbuns disponíveis no Spotify. Através de dados detalhados, buscamos responder a perguntas como:

* **Quais artistas têm maior popularidade e seguidores?**
* **Como diferentes fatores se relacionam com sua popularidade?**
* **Quais gêneros musicais são mais predominantes?**

Nosso objetivo é fornecer uma ferramenta clara e intuitiva para que **fãs de música, artistas, produtores e pesquisadores** possam compreender melhor as características do cenário musical atual.

---

### 🎯 Como Navegar:

Utilize o menu de navegação na **barra lateral (esquerda)** para explorar as diferentes seções do aplicativo:

* **📊 Visão Geral:** Explore a distribuição de artistas, álbuns e métricas principais.
* **🎵 Análise por Artista:** Análises específicas por artista.
* **📈 Popularidade** Análise de fatores para popularidade.
* **🎼 Gêneros Musicais:** Analise de detalhes sobre cada gênero musical e comparações.
* **🔍 Insights Avançados:** Análises aprofundadas para uso comercial

---

### 📋 Sobre o Dataset:

O seu conjunto de dados tem as seguintes dimensões:
- **Total de Músicas (Linhas):** 🎵 `{df.shape[0]:,}` 
- **Variáveis Analisadas (Colunas):** 📈 `{df.shape[1]}` 
- **Artistas Únicos:** 👩‍🎤​ `{df['artist_name'].nunique()}` diferentes
- **Álbuns Únicos:** 💿​ `{df['album_name'].nunique()}` álbuns
- **Tipos de Álbum:** ​💽​ `{df['album_type'].nunique()}` categorias

**Principais métricas analisadas:**
- **Popularidade** de artistas e músicas
- **Número de seguidores** dos artistas
- **Duração** das músicas
- **Gêneros musicais**
- **Data de lançamento**


""")

# Métricas rápidas
st.header("📈 Métricas Rápidas")

#Criando colunas para as métricas
col1, col2, col3 = st.columns(3) 

with col1:
    # Encontra o nome do artista com maior valor na coluna artist_popularity
    artista_mais_popular = df.loc[df['artist_popularity'].idxmax(), 'artist_name'] 
    st.metric("Artista Mais Popular", artista_mais_popular)

with col2:
    # Calcula a média da popularidade das músicas
    avg_popularity = df['track_popularity'].mean()
    st.metric("Popularidade Média", f"{avg_popularity:.1f}")

with col3:
    # Duração média das músicas
    avg_duration = df['track_duration_min'].mean()
    st.metric("Duração Média", f"{avg_duration:.1f} min")

st.header("👀 Prévia dos Dados")
st.info(f"Abaixo uma amostra das primeiras 10 músicas de um total de {df.shape[0]:,} linhas no dataset.")

# Mapeia nomes das colunas originais para nomes mais amigáveis ao usuário
colunas_para_exibir = {
    'track_name': 'Nome da Música',
    'artist_name': 'Artista',
    'album_name': 'Álbum',
    'track_popularity': 'Popularidade',
    'artist_popularity': 'Popularidade do Artista',
    'track_duration_min': 'Duração (min)',
    'explicit': 'Explícito'
}
  
# Criar DataFrame apenas com as colunas que queremos exibir
df_display = df[list(colunas_para_exibir.keys())].rename(columns=colunas_para_exibir)
st.dataframe(df_display.head(10), use_container_width=True)

# Informação adicional sobre o tamanho do dataset
st.caption(f"📊 Dataset completo possui **{df.shape[0]:,} linhas** e **{df.shape[1]} colunas**")

#barra lateralde navegação
st.sidebar.header("Navegação")
st.sidebar.success("Tudo pronto! Selecione uma página acima para explorar!")
