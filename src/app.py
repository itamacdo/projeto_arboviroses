import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Monitor de Arboviroses - Insights", layout="wide")

st.title("Inteligência de Dados: Arboviroses em Barbalha")
st.markdown("Monitoramento comparativo com geração automática de insights.")

@st.cache_data
def carregar_e_consolidar():
    doencas = ['dengue', 'zika', 'chikungunya']
    dfs = []
    for d in doencas:
        temp_df = pd.read_csv(f'data/{d}_2301901.csv')
        col_data = 'data_iniSE' if 'data_iniSE' in temp_df.columns else 'data_ini_se'
        temp_df['data'] = pd.to_datetime(temp_df[col_data])
        temp_df['doenca'] = d.capitalize()
        dfs.append(temp_df[['data', 'casos', 'doenca', 'tempmed']])
    return pd.concat(dfs).sort_values('data')

try:
    df_completo = carregar_e_consolidar()

    # --- SEÇÃO DE INSIGHTS AUTOMÁTICOS ---
    st.subheader("Insights Automáticos (Últimos 30 dias)")
    
    # Cálculo de variação
    ultima_data = df_completo['data'].max()
    mes_anterior = ultima_data - pd.Timedelta(days=30)
    
    dados_recentes = df_completo[df_completo['data'] > mes_anterior]
    resumo_recente = dados_recentes.groupby('doenca')['casos'].sum()
    
    if not resumo_recente.empty:
        doenca_lider = resumo_recente.idxmax()
        total_lider = resumo_recente.max()
        
        col_ins1, col_ins2 = st.columns(2)
        with col_ins1:
            st.info(f"A doença com maior incidência recente é **{doenca_lider}**, com **{int(total_lider)}** novos casos registrados nos últimos 30 dias.")
        with col_ins2:
            temp_media = dados_recentes['tempmed'].mean()
            st.warning(f"A temperatura média no período foi de **{temp_media:.1f}°C**. Lembre-se: temperaturas acima de 25°C aceleram o ciclo do mosquito.")

    # --- GRÁFICOS ---
    st.divider()
    col_esq, col_dir = st.columns([2, 1])

    with col_esq:
        st.subheader("Tendência Temporal")
        fig_comp = px.line(df_completo, x='data', y='casos', color='doenca',
                           line_shape='spline',
                           color_discrete_map={'Dengue': '#e74c3c', 'Zika': '#2ecc71', 'Chikungunya': '#f1c40f'})
        st.plotly_chart(fig_comp, use_container_width=True)

    with col_dir:
        st.subheader("Distribuição Total")
        fig_pie = px.pie(df_completo, values='casos', names='doenca', hole=0.5,
                         color='doenca', color_discrete_map={'Dengue': '#e74c3c', 'Zika': '#2ecc71', 'Chikungunya': '#f1c40f'})
        st.plotly_chart(fig_pie, use_container_width=True)

except Exception as e:
    st.error(f"Erro: {e}")
    st.info("Rode 'python src/coleta_dados.py' para baixar os dados.")
