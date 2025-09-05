import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import io

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Análise de Desligamentos",
    page_icon="📊",
    layout="wide"
)

def check_login():
    """Verifica se o usuário está logado"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    return st.session_state.logged_in

def login_page():
    """Página de login"""
    st.title("🔐 Login - Dashboard de Análise de Desligamentos")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Acesso ao Sistema")
        
        with st.form("login_form"):
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            submit_button = st.form_submit_button("Entrar")
            
            if submit_button:
                if username == "clamed@" and password == "clamed@2025#":
                    st.session_state.logged_in = True
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos!")
        
        # st.markdown("---")
        # st.info("**Credenciais de acesso:**\n\nUsuário: admin\n\nSenha: admin123@")

def logout():
    """Função para logout"""
    st.session_state.logged_in = False
    st.rerun()

def calculate_tenure_group(tenure_days):
    """Calcula o grupo de tempo de permanência"""
    years = tenure_days / 365.25
    if years < 1:
        return "< 1 ano"
    elif years < 2:
        return "1-2 anos"
    elif years < 5:
        return "2-5 anos"
    elif years < 10:
        return "5-10 anos"
    else:
        return "> 10 anos"

def calculate_age_group(age):
    """Calcula o grupo etário"""
    if age < 25:
        return "0-25 anos"
    elif age < 35:
        return "25-34 anos"
    elif age < 45:
        return "35-44 anos"
    elif age < 55:
        return "45-54 anos"
    else:
        return "≥ 55 anos"

def process_data(df):
    """Processa os dados da planilha"""
    # Converter datas
    df['Data Admissão'] = pd.to_datetime(df['Data Admissão'], errors='coerce')
    df['Data Desligamento'] = pd.to_datetime(df['Data Desligamento'], errors='coerce')
    df['Nascimento'] = pd.to_datetime(df['Nascimento'], errors='coerce')
    
    # Calcular tempo de permanência
    df['Tempo Permanencia (dias)'] = (df['Data Desligamento'] - df['Data Admissão']).dt.days
    df['Grupo Tempo Permanencia'] = df['Tempo Permanencia (dias)'].apply(calculate_tenure_group)
    
    # Calcular idade no desligamento
    df['Idade Desligamento'] = ((df['Data Desligamento'] - df['Nascimento']).dt.days / 365.25).round(0)
    df['Grupo Etario'] = df['Idade Desligamento'].apply(calculate_age_group)
    
    # Calcular tempo médio de empresa em anos
    df['Tempo Empresa (anos)'] = df['Tempo Permanencia (dias)'] / 365.25
    
    return df

def create_overview_metrics(df):
    """Cria métricas da visão geral"""
    
    cutoff_date = datetime.now() - timedelta(days=365)
    df_12m = df[df['Data Desligamento'] >= cutoff_date]
    
    total_desligados_12m = len(df_12m)
    
    total_quadro_estimado = 640  
    percentual = (total_desligados_12m / total_quadro_estimado) * 100
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Desligados (12 meses)", total_desligados_12m)
    
    with col2:
        st.metric("Total de gerentes ativos", total_quadro_estimado)
    
    with col3:
        st.metric("Turnover (Percentual)", f"{percentual:.1f}%")

def create_monthly_timeline(df):
    """Cria gráfico de linha temporal mensal"""
    df['Mes_Ano'] = df['Data Desligamento'].dt.to_period('M')
    monthly_data = df.groupby(['Mes_Ano', 'Iniciativa Desligamento']).size().reset_index(name='Quantidade')
    monthly_data['Mes_Ano_str'] = monthly_data['Mes_Ano'].astype(str)
    
    fig = px.line(monthly_data, 
                  x='Mes_Ano_str', 
                  y='Quantidade', 
                  color='Iniciativa Desligamento',
                  title='Distribuição Mensal de Desligamentos por Iniciativa',
                  markers=True)
    
    fig.update_layout(
        xaxis_title="Mês/Ano",
        yaxis_title="Quantidade de Desligamentos",
        legend_title="Iniciativa"
    )
    
    fig.update_xaxes(tickangle=45)
    
    return fig

def create_risk_matrix(df, filter_iniciativa=None):
    """Cria matriz de risco"""
    if filter_iniciativa:
        df_filtered = df[df['Iniciativa Desligamento'] == filter_iniciativa]
    else:
        df_filtered = df
    
    # Criar matriz de risco
    risk_data = df_filtered.groupby(['Grupo Tempo Permanencia', 'Motivo Desligamento']).agg({
        'Tempo Empresa (anos)': 'mean',
        'Idade Desligamento': 'mean',
        'Matrícula': 'count'
    }).reset_index()
    
    risk_data.columns = ['Tempo_Cargo', 'Motivo', 'Tempo_Medio_Empresa', 'Idade_Media', 'Quantidade']
    
    # Criar pivot para heatmap
    pivot_quantidade = risk_data.pivot(index='Tempo_Cargo', columns='Motivo', values='Quantidade').fillna(0)
    pivot_tempo = risk_data.pivot(index='Tempo_Cargo', columns='Motivo', values='Tempo_Medio_Empresa').fillna(0)
    pivot_idade = risk_data.pivot(index='Tempo_Cargo', columns='Motivo', values='Idade_Media').fillna(0)
    
    # Criar texto para hover
    hover_text = []
    for i in range(len(pivot_quantidade.index)):
        hover_row = []
        for j in range(len(pivot_quantidade.columns)):
            quantidade = pivot_quantidade.iloc[i, j]
            tempo_medio = pivot_tempo.iloc[i, j]
            idade_media = pivot_idade.iloc[i, j]
            
            text = f"Quantidade: {quantidade}<br>"
            text += f"Tempo Médio Empresa: {tempo_medio:.1f} anos<br>"
            text += f"Idade Média: {idade_media:.0f} anos"
            hover_row.append(text)
        hover_text.append(hover_row)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_quantidade.values,
        x=pivot_quantidade.columns,
        y=pivot_quantidade.index,
        text=hover_text,
        hovertemplate='%{text}<extra></extra>',
        colorscale=[[0, 'green'], [0.5, 'yellow'], [1, 'red']],
        colorbar=dict(title="Quantidade de Desligamentos")
    ))
    
    title = "Matriz de Risco - Tempo no Cargo vs Motivo de Desligamento"
    if filter_iniciativa:
        title += f" ({filter_iniciativa})"
    
    fig.update_layout(
        title=title,
        xaxis_title="Motivo do Desligamento",
        yaxis_title="Tempo no Cargo"
    )
    
    return fig

def create_age_analysis(df):
    """Cria análise por grupo etário"""
    age_data = df.groupby(['Grupo Etario', 'Iniciativa Desligamento']).size().reset_index(name='Quantidade')
    
    fig = px.bar(age_data, 
                 x='Grupo Etario', 
                 y='Quantidade', 
                 color='Iniciativa Desligamento',
                 title='Desligamentos por Grupo Etário e Iniciativa',
                 text='Quantidade')
    
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(xaxis_title="Grupo Etário", yaxis_title="Quantidade de Desligamentos")
    
    return fig

def main():
    if not check_login():
        login_page()
        return
    
    with st.sidebar:
        st.markdown("---")
        if st.button("🚪 Sair", type="secondary"):
            logout()
        # st.markdown(f"👤 Logado como: **admin**")
        # st.markdown("---")
    
    st.title("📊 Dashboard de Análise de Desligamentos")
    st.markdown("---")
    
    # Upload do arquivo
    uploaded_file = st.file_uploader("Faça upload da planilha de dados", type=['xlsx', 'xls', 'csv'])
    
    if uploaded_file is not None:
        try:
            # Ler arquivo
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file, sheet_name='Base')
            
            # Processar dados
            df = process_data(df)
            
            st.success(f"Arquivo carregado com sucesso! {len(df)} registros encontrados.")
            
            # Sidebar com filtros
            st.sidebar.header("Filtros")
            
            # Filtros
            regionais = ['Todos'] + sorted(df['Regional'].dropna().unique().tolist())
            regional_selected = st.sidebar.selectbox("Regional", regionais)
            
            supervisores = ['Todos'] + sorted(df['Supervisor'].dropna().unique().tolist())
            supervisor_selected = st.sidebar.selectbox("Supervisor", supervisores)
            
            bandeiras = ['Todos'] + sorted(df['Bandeira'].dropna().unique().tolist())
            bandeira_selected = st.sidebar.selectbox("Bandeira", bandeiras)
            
            iniciativas = ['Todos'] + sorted(df['Iniciativa Desligamento'].dropna().unique().tolist())
            iniciativa_selected = st.sidebar.selectbox("Iniciativa Desligamento", iniciativas)
            
            motivos = ['Todos'] + sorted(df['Motivo Desligamento'].dropna().unique().tolist())
            motivo_selected = st.sidebar.selectbox("Motivo Desligamento", motivos)
            
            # Aplicar filtros
            df_filtered = df.copy()
            
            if regional_selected != 'Todos':
                df_filtered = df_filtered[df_filtered['Regional'] == regional_selected]
            
            if supervisor_selected != 'Todos':
                df_filtered = df_filtered[df_filtered['Supervisor'] == supervisor_selected]
            
            if bandeira_selected != 'Todos':
                df_filtered = df_filtered[df_filtered['Bandeira'] == bandeira_selected]
            
            if iniciativa_selected != 'Todos':
                df_filtered = df_filtered[df_filtered['Iniciativa Desligamento'] == iniciativa_selected]
            
            if motivo_selected != 'Todos':
                df_filtered = df_filtered[df_filtered['Motivo Desligamento'] == motivo_selected]
            
            # Visão Geral
            st.header("📈 Visão Geral")
            create_overview_metrics(df_filtered)
            
            # Timeline mensal
            st.header("📅 Distribuição Mensal")
            fig_timeline = create_monthly_timeline(df_filtered)
            st.plotly_chart(fig_timeline, use_container_width=True)
            
            # Matriz de Risco
            st.header("🎯 Matriz de Risco")

            # Função para gerar eixo X formatado (Mês/Ano)
            def get_mes_ano_str(df):
                return df['Data Desligamento'].dt.strftime('%m/%Y')

            # Agrupa os dados por mês/ano e iniciativa
            pedido_grouped = (
                df_filtered[df_filtered['Iniciativa Desligamento'] == 'Inic. Empregado']
                .groupby(df_filtered['Data Desligamento'].dt.to_period('M'))
                .size()
                .reset_index(name='Quantidade')
            )
            demissao_grouped = (
                df_filtered[df_filtered['Iniciativa Desligamento'] == 'Inic. Empresa']
                .groupby(df_filtered['Data Desligamento'].dt.to_period('M'))
                .size()
                .reset_index(name='Quantidade')
            )

            # Converte período para string MM/YYYY
            pedido_grouped['Mes_Ano_str'] = pedido_grouped['Data Desligamento'].dt.strftime('%m/%Y')
            demissao_grouped['Mes_Ano_str'] = demissao_grouped['Data Desligamento'].dt.strftime('%m/%Y')

            # Verifica se há dados
            if not pedido_grouped.empty or not demissao_grouped.empty:
                fig = go.Figure()

                if not pedido_grouped.empty:
                    fig.add_trace(go.Bar(
                        x=pedido_grouped['Mes_Ano_str'],
                        y=pedido_grouped['Quantidade'],
                        name='Pedido de Demissão',
                        marker_color='#4A90E2'
                    ))

                if not demissao_grouped.empty:
                    fig.add_trace(go.Bar(
                        x=demissao_grouped['Mes_Ano_str'],
                        y=demissao_grouped['Quantidade'],
                        name='Demissão',
                        marker_color='#50E3C2'
                    ))

                fig.update_layout(
                    title="Matriz de Risco - Desligamentos",
                    xaxis_title="Mês/Ano",
                    yaxis_title="Quantidade",
                    barmode='group',
                    height=600,
                    legend_title="Tipo de Desligamento"
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Não há dados de desligamento para exibir")
            
            # Matriz geral
            st.subheader("Matriz Geral (Todas as Iniciativas)")
            fig_risk_geral = create_risk_matrix(df_filtered)
            st.plotly_chart(fig_risk_geral, use_container_width=True)
            
            # Análise por idade
            st.header("👥 Análise por Grupo Etário")
            fig_age = create_age_analysis(df_filtered)
            st.plotly_chart(fig_age, use_container_width=True)
            
            # Legenda explicativa
            # st.header("🎨 Legenda das Cores")
            # col1, col2, col3 = st.columns(3)
            
            # with col1:
            #     st.markdown("🟢 **Verde**: Menor quantidade de desligamentos")
            
            # with col2:
            #     st.markdown("🟡 **Amarelo**: Quantidade média de desligamentos")
            
            # with col3:
            #     st.markdown("🔴 **Vermelho**: Maior quantidade de desligamentos")
            
            # Dados filtrados
            if st.checkbox("Mostrar tabela com dados filtrados"):
                st.dataframe(df_filtered)
            
        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {str(e)}")
            st.info("Verifique se o arquivo contém as colunas necessárias: Regional, Supervisor, Bandeira, Matrícula, Nome do Colaborador, Nascimento, Cargo do Colaborador, Data Admissão, Data Desligamento, Iniciativa Desligamento, Motivo Desligamento")
    
    else:
        st.info("👆 Faça upload de uma planilha para começar a análise")
        
        # Mostrar exemplo de estrutura esperada
        st.subheader("📋 Estrutura esperada da planilha:")
        exemplo_df = pd.DataFrame({
            'Regional': ['Nome Regional 1', 'Nome Regional 2'],
            'Supervisor': ['Nome Supervisor 1', 'Nome Supervisor 2'],
            'Cód. Rubi': ['001', '215'],
            'Cód. Fil': ['100', '534'],
            'Nome Filial': ['Filial X', 'Filial Y'],
            'Bandeira': ['FPP', 'DC'],
            'Local': ['Local X', 'Local Y'],
            'Matrícula': ['12345', '67890'],
            'Nome do Colaborador': ['Nome do Colaborador 1', 'Nome do Colaborador 2'],
            'Nascimento': ['15/05/1985', '16/05/1986'],
            'Cargo do Colaborador': ['Gerente', 'Supervisor'],
            'Data Admissão': ['15/01/2020', '15/01/2021'],
            'Data Desligamento': ['15/01/2021', '15/01/2022'],
            'Iniciativa Desligamento': ['Inic. Empresa', 'Inic. Empregado'],
            'Motivo Desligamento': ['Motivo Desligamento X', 'Motivo Desligamento Y']
        })
        st.dataframe(exemplo_df)

if __name__ == "__main__":
    main()
