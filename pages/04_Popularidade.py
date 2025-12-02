import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils.carrega_dados import carregar_dados

# =============================================
# CONFIGURAÇÃO
# =============================================

st.set_page_config(
    page_title='Popularidade',
    page_icon='📈',
    layout='wide'
)

st.title('📈 Análise de Popularidade Musical')


# =============================================
# CARREGAR DADOS
# =============================================

df = carregar_dados()


# =============================================
# ANÁLISE DE CORRELAÇÃO
# =============================================

st.header('🔗 Correlação entre Variáveis')

variaveis_numericas = [
    'track_popularity',
    'artist_popularity',
    'track_duration_min',
    'artist_followers'
]

df_corr = df[variaveis_numericas].corr()

mapeamento_nomes = {
    'track_popularity': 'Popularidade da Música',
    'artist_popularity': 'Popularidade do Artista',
    'track_duration_min': 'Duração da Música (min)',
    'artist_followers': 'Seguidores do Artista'
}

df_corr_pt = df_corr.rename(index=mapeamento_nomes, columns=mapeamento_nomes)

# Heatmap
fig_corr = px.imshow(
    df_corr_pt,
    text_auto=True,
    aspect='auto',
    color_continuous_scale='RdBu_r',
    title='Matriz de Correlação entre Variáveis Musicais'
)
st.plotly_chart(fig_corr, use_container_width=True)


# =============================================
# INTERPRETAÇÃO AUTOMÁTICA DA CORRELAÇÃO
# =============================================

st.subheader("🧠 Interpretação Automática da Correlação")

df_long = df_corr_pt.stack().reset_index()
df_long.columns = ["Variável 1", "Variável 2", "Correlação"]
df_long = df_long[df_long["Variável 1"] < df_long["Variável 2"]]

analises = []

for _, row in df_long.iterrows():
    v1, v2, corr = row["Variável 1"], row["Variável 2"], row["Correlação"]

    if abs(corr) >= 0.7:
        intensidade = "forte"
    elif abs(corr) >= 0.4:
        intensidade = "moderada"
    else:
        intensidade = "fraca"

    tipo = "positiva" if corr > 0 else "negativa"

    analises.append(f"- **{v1} × {v2}** → correlação **{tipo} {intensidade}** ({corr:.2f})")

st.markdown("\n".join(analises))


# =============================================
# GRÁFICOS DE RELAÇÃO COM POPULARIDADE
# =============================================

st.header("📊 Gráficos de Relação com Popularidade da Música")

# Função para gerar regressão sem statsmodels
def linha_tendencia(x, y):
    coef = np.polyfit(x, y, 1)
    poly = np.poly1d(coef)
    return poly(x), coef


# -------------------------------------------------
# 1) Popularidade da Música × Popularidade do Artista
# -------------------------------------------------

st.subheader("🎤 Popularidade da Música × Popularidade do Artista")

fig1 = px.scatter(
    df,
    x="artist_popularity",
    y="track_popularity",
    title="Popularidade da Música vs Popularidade do Artista",
    labels={"artist_popularity": "Popularidade do Artista", "track_popularity": "Popularidade da Música"}
)

# linha de tendência
y_pred, coef = linha_tendencia(df["artist_popularity"], df["track_popularity"])
fig1.add_trace(go.Scatter(x=df["artist_popularity"], y=y_pred, mode="lines", name="Tendência"))

st.plotly_chart(fig1, use_container_width=True)

st.markdown(f"""
📌 **Análise Automática:**  
Quando o valor da popularidade do artista aumenta, a popularidade da música tende a **aumentar** também.  
A inclinação da linha de tendência é **{coef[0]:.2f}**, indicando relação **positiva**.
""")


# -------------------------------------------------
# 2) Popularidade da Música × Seguidores do Artista
# -------------------------------------------------

st.subheader("👥 Popularidade da Música × Seguidores do Artista")

fig2 = px.scatter(
    df,
    x="artist_followers",
    y="track_popularity",
    title="Popularidade da Música vs Seguidores do Artista",
    labels={"artist_followers": "Seguidores do Artista", "track_popularity": "Popularidade da Música"}
)

y_pred, coef = linha_tendencia(df["artist_followers"], df["track_popularity"])
fig2.add_trace(go.Scatter(x=df["artist_followers"], y=y_pred, mode="lines", name="Tendência"))

st.plotly_chart(fig2, use_container_width=True)

st.markdown(f"""
📌 **Análise Automática:**  
A popularidade da música tende a aumentar levemente conforme o número de seguidores do artista cresce.  
Inclinação da tendência: **{coef[0]:.4f}**.
""")


# -------------------------------------------------
# 3) Popularidade da Música × Duração da Música
# -------------------------------------------------

st.subheader("⏱️ Popularidade da Música × Duração (min)")

fig3 = px.scatter(
    df,
    x="track_duration_min",
    y="track_popularity",
    title="Popularidade da Música vs Duração",
    labels={"track_duration_min": "Duração (min)", "track_popularity": "Popularidade da Música"}
)

y_pred, coef = linha_tendencia(df["track_duration_min"], df["track_popularity"])
fig3.add_trace(go.Scatter(x=df["track_duration_min"], y=y_pred, mode="lines", name="Tendência"))

st.plotly_chart(fig3, use_container_width=True)

st.markdown(f"""
📌 **Análise Automática:**  
A duração da música tem impacto **{ 'positivo' if coef[0] > 0 else 'negativo' }** porém **fraco** sobre a popularidade.  
Inclinação: **{coef[0]:.4f}**.
""")

