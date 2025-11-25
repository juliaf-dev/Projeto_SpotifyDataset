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

Este aplicativo interativo foi desenvolvido para explorar e visualizar os principais insights sobre músicas, artistas e álbuns disponíveis no Spotify. Através de dados detalhados, buscamos responder a perguntas cruciais como:

* **Quais artistas têm maior popularidade e seguidores?**
* **Como a duração das músicas se relaciona com sua popularidade?**
* **Quais gêneros musicais são mais predominantes?**
* **Como a data de lançamento afeta o desempenho das músicas?**

Nosso objetivo é fornecer uma ferramenta clara e intuitiva para que **fãs de música, artistas, produtores e pesquisadores** possam compreender melhor as características do cenário musical atual.

---

### 🎯 Como Navegar:

Utilize o menu de navegação na **barra lateral (esquerda)** para explorar as diferentes seções do aplicativo:

* **📊 Visão Geral:** Explore a distribuição de artistas, álbuns e métricas principais.
* **🎵 Análise por Artista:** Mergulhe em análises específicas por artista.
* **📈 Popularidade & Duração:** Entenda a relação entre duração musical e popularidade.
* **🎼 Gêneros Musicais:** Explore a diversidade de gêneros no dataset.
* **🔍 Insights Avançados:** Acesse padrões mais profundos nos dados.

---

### 📋 Sobre o Dataset:

O seu conjunto de dados tem as seguintes dimensões:
- **Total de Músicas (Linhas):** `{df.shape[0]:,}` 🎵
- **Variáveis Analisadas (Colunas):** `{df.shape[1]}` 📈
- **Artistas Únicos:** `{df['artist_name'].nunique()}` diferentes
- **Álbuns Únicos:** `{df['album_name'].nunique()}` álbuns
- **Tipos de Álbum:** `{df['album_type'].nunique()}` categorias

**Principais métricas analisadas:**
- **Popularidade** de artistas e músicas
- **Número de seguidores** dos artistas
- **Duração** das músicas
- **Gêneros musicais**
- **Data de lançamento**
- **Conteúdo explícito**

Agradecemos a sua visita e esperamos que encontre informações valiosas para sua apreciação musical!
""")

# Métricas rápidas
st.header("📈 Métricas Rápidas")

col1, col2, col3, col4 = st.columns(4)

with col1:
    # Artista mais popular
    artista_mais_popular = df.loc[df['artist_popularity'].idxmax(), 'artist_name']
    st.metric("Artista Mais Popular", artista_mais_popular)

with col2:
    # Popularidade média
    avg_popularity = df['track_popularity'].mean()
    st.metric("Popularidade Média", f"{avg_popularity:.1f}")

with col3:
    # Duração média das músicas
    avg_duration = df['track_duration_min'].mean()
    st.metric("Duração Média", f"{avg_duration:.1f} min")

with col4:
    # Porcentagem de conteúdo explícito
    explicit_count = len(df[df['explicit'] == 'Sim'])
    percent_explicit = (explicit_count / len(df)) * 100
    st.metric("Conteúdo Explícito", f"{percent_explicit:.1f}%")

st.header("👀 Prévia dos Dados")
st.info(f"Abaixo uma amostra das primeiras 10 músicas de um total de {df.shape[0]:,} linhas no dataset.")

# Mapeamento de colunas para exibição
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

st.sidebar.header("Navegação")
st.sidebar.success("🎵 **Selecione uma página acima para começar a explorar!**")
st.sidebar.markdown(f"""
**🎵 Sobre o Dataset:**
- **{df.shape[0]:,} músicas** analisadas
- **{df['artist_name'].nunique()} artistas** únicos
- **{df['album_name'].nunique()} álbuns** diferentes
- Dados musicais do **Spotify**

**🎯 Público-Alvo:**
- Fãs de música e curiosos
- Artistas e produtores musicais
- Pesquisadores da indústria musical
- Desenvolvedores de aplicações musicais
""")