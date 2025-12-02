import streamlit as st
import pandas as pd
import plotly.express as px
import re
from utils.carrega_dados import carregar_dados

# =====================================================
# FUNÇÃO PARA PADRONIZAR NOMES DE ARTISTAS
# =====================================================
def limpar_artista(nome):
    if not isinstance(nome, str):
        return None

    nome = nome.strip()

    # Remove símbolos no início e no fim, mas preserva símbolos internos
    nome = re.sub(r'^[^a-zA-Z0-9]+', '', nome)
    nome = re.sub(r'[^a-zA-Z0-9]+$', '', nome)

    if nome.strip() == "":
        return None

    # Mantém siglas como NSYNC em caixa alta
    if nome.isupper():
        return nome

    return nome.title()


# Função para gerar a lista de artistas já limpa
def obter_artistas(df):
    artistas = df["artist_name"].apply(limpar_artista)
    artistas = artistas.dropna().unique().tolist()
    artistas.sort()
    return artistas


# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================
st.set_page_config(
    page_title='Análise por Artista',
    page_icon='🎵',
    layout='wide'
)

# =====================================================
# CARREGAR DADOS
# =====================================================
df = carregar_dados()

# Criar coluna limpa
df["artist_clean"] = df["artist_name"].apply(limpar_artista)

st.title("🎤 Análise por Artista")

st.markdown("""
Nesta página, você pode selecionar um artista e visualizar análises **específicas** sobre:
- Popularidade das músicas  
- Evolução da carreira  
- Álbuns mais relevantes  
- Distribuição de durações  
""")

# =====================================================
# SELEÇÃO DO ARTISTA
# =====================================================

st.header("🔍 Selecione o Artista")

lista_artistas = obter_artistas(df)   # Agora tratada corretamente

artista_selecionado = st.selectbox(
    "Escolha um artista para analisar:",
    lista_artistas,
    index=0,
    placeholder="Selecione..."
)

# Filtrar dados do artista com coluna limpa
df_artista = df[df["artist_clean"] == artista_selecionado]

if df_artista.empty:
    st.warning("Nenhum dado encontrado para este artista.")
    st.stop()

st.markdown(f"### 🎧 Analisando **{artista_selecionado}**")

# =====================================================
# MÉTRICAS DO ARTISTA
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:
    seguidores = df_artista["artist_followers"].max()
    st.metric("👥 Seguidores", f"{seguidores:,.0f}")

with col2:
    pop_artista = df_artista["artist_popularity"].max()
    st.metric("🔥 Popularidade do Artista", f"{pop_artista}")

with col3:
    qtd_musicas = df_artista.shape[0]
    st.metric("🎵 Músicas no Dataset", qtd_musicas)

st.divider()

# =====================================================
# GRÁFICO 1 — Popularidade das músicas
# =====================================================
st.subheader("📈 Popularidade das Músicas do Artista")

fig_pop = px.bar(
    df_artista.sort_values(by="track_popularity", ascending=False),
    x="track_name",
    y="track_popularity",
    title=f"Popularidade das Músicas de {artista_selecionado}",
    labels={"track_name": "Música", "track_popularity": "Popularidade"},
)

fig_pop.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_pop, use_container_width=True)

# =====================================================
# GRÁFICO 2 — Evolução Temporal
# =====================================================

st.subheader("📅 Evolução dos Lançamentos ao Longo dos Anos")

df_artista["release_year"] = df_artista["album_release_date"].dt.year

df_ano = df_artista["release_year"].value_counts().sort_index().reset_index()
df_ano.columns = ["Ano", "Quantidade"]

fig_ano = px.line(
    df_ano,
    x="Ano",
    y="Quantidade",
    markers=True,
    title=f"Linha do Tempo de Lançamentos — {artista_selecionado}",
    labels={"Quantidade": "Número de Músicas", "Ano": "Ano"},
)

st.plotly_chart(fig_ano, use_container_width=True)

# =====================================================
# GRÁFICO 3 — Popularidade por Álbum
# =====================================================

st.subheader("💿 Popularidade Média por Álbum")

df_album = df_artista.groupby("album_name")["track_popularity"].mean().reset_index()

fig_album = px.bar(
    df_album.sort_values("track_popularity", ascending=False),
    x="album_name",
    y="track_popularity",
    title=f"Popularidade Média dos Álbuns — {artista_selecionado}",
    labels={"album_name": "Álbum", "track_popularity": "Popularidade Média"},
)

fig_album.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_album, use_container_width=True)

# =====================================================
# GRÁFICO 4 — Distribuição da Duração
# =====================================================

st.subheader("⏱️ Distribuição da Duração das Músicas")

fig_dur = px.histogram(
    df_artista,
    x="track_duration_min",
    nbins=20,
    title=f"Duração das Músicas — {artista_selecionado}",
    labels={"track_duration_min": "Duração (min)"},
)

st.plotly_chart(fig_dur, use_container_width=True)

# =====================================================
# INTERPRETAÇÃO AUTOMÁTICA
# =====================================================

st.header("🧠 Interpretação Automática do Artista")

musica_top = df_artista.sort_values(by="track_popularity", ascending=False).iloc[0]
nome_top = musica_top["track_name"]
pop_top = musica_top["track_popularity"]

album_top = df_album.sort_values("track_popularity", ascending=False).iloc[0]
nome_album_top = album_top["album_name"]
pop_album_top = album_top["track_popularity"]

st.markdown(f"""
### 📌 Principais insights sobre **{artista_selecionado}**

- 🎵 **Música mais popular:** *{nome_top}* (popularidade {pop_top})
- 💿 **Álbum mais forte:** *{nome_album_top}* (popularidade média {pop_album_top:.1f})
- 📅 Lançamentos variam de **{df_ano['Ano'].min()}** a **{df_ano['Ano'].max()}**
- 📈 A carreira apresenta **{ "crescimento" if df_ano['Quantidade'].iloc[-1] > df_ano['Quantidade'].iloc[0] else "queda" }** no volume de lançamentos ao longo dos anos
""")
