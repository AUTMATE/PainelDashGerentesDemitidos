# 🤖 Dashboard de Análise de Desligamentos

## 📄 Descrição Geral
Um dashboard interativo para análise de desligamentos de colaboradores, incluindo login, upload de dados e visualizações gráficas. O sistema permite que os usuários visualizem métricas e gráficos relacionados a desligamentos, facilitando a análise de dados e a tomada de decisões.

## 🔧 Tecnologia e Linguagem
- **Linguagem Principal:** Python
- **Tipo de Aplicação:** Web App
- **Arquitetura:** MVC

## 🎯 Objetivo e Finalidade
Criar um dashboard interativo para análise de desligamentos de colaboradores com visualizações gráficas e métricas. O sistema visa facilitar a compreensão dos dados de desligamento e auxiliar na identificação de padrões e tendências.

## 📚 Descrição Técnica
O projeto utiliza a biblioteca Streamlit para a criação de interfaces web interativas, Pandas para manipulação e análise de dados, e Plotly para a criação de gráficos expressivos. O sistema é estruturado em um padrão MVC, onde a lógica de negócios é separada da apresentação, permitindo uma melhor manutenção e escalabilidade.

## 🔄 Funcionalidades Principais

### Visão Geral do Sistema
O sistema possui funcionalidades que incluem autenticação de usuários, upload de arquivos, processamento de dados, e geração de gráficos e métricas. Cada funcionalidade é projetada para ser intuitiva e interativa, permitindo que os usuários explorem os dados de desligamento de forma eficiente.

### Detalhamento das Funcionalidades

#### 🔹 Login
- **Objetivo:** Permite que usuários façam login no sistema para acessar o dashboard.
- **Categoria:** Authentication
- **Criticidade:** Alto

**Fluxo de Execução:**
1. Verifica se o usuário está logado usando a função `check_login`.
2. Exibe a página de login através da função `login_page`.

- **Tecnologias Envolvidas:** Streamlit
- **Dependências:** session_state
- **Tratamento de Erros:** Redireciona para a página de login se não estiver logado.
- **Tempo Estimado:** 1 segundo

#### 🔹 Processamento de Dados
- **Objetivo:** Processa os dados da planilha de desligamentos para análise.
- **Categoria:** Business Logic
- **Criticidade:** Médio

**Fluxo de Execução:**
1. Lê e processa o arquivo de dados utilizando a função `process_data`.

- **Tecnologias Envolvidas:** Pandas
- **Dependências:** Pandas, datetime
- **Tratamento de Erros:** Exibe mensagem de erro se o arquivo não puder ser processado.
- **Tempo Estimado:** 2-5 segundos

#### 🔹 Visualização de Métricas
- **Objetivo:** Cria e exibe métricas gerais sobre desligamentos.
- **Categoria:** Business Logic
- **Criticidade:** Médio

**Fluxo de Execução:**
1. Calcula e exibe métricas de desligamento utilizando a função `create_overview_metrics`.

- **Tecnologias Envolvidas:** Streamlit
- **Dependências:** Streamlit
- **Tratamento de Erros:** Exibe mensagem de erro se não houver dados.
- **Tempo Estimado:** 1-2 segundos

#### 🔹 Gráficos de Desligamento
- **Objetivo:** Gera gráficos para visualização de dados de desligamento.
- **Categoria:** Business Logic
- **Criticidade:** Médio

**Fluxo de Execução:**
1. Cria gráficos de linha e barra para análise utilizando as funções `create_monthly_timeline`, `create_risk_matrix`, e `create_age_analysis`.

- **Tecnologias Envolvidas:** Plotly, Streamlit
- **Dependências:** Plotly, Streamlit
- **Tratamento de Erros:** Exibe mensagem de erro se não houver dados para plotar.
- **Tempo Estimado:** 2-4 segundos

## 🚀 Fluxo de Execução Completo

### 1. Inicialização do Sistema
O sistema inicia configurando a página e verificando o estado de login do usuário. As configurações incluem o título da página, ícone e layout. É feita uma validação para verificar se o usuário está logado.

### 2. Processamento Principal
O fluxo principal envolve o login do usuário, upload do arquivo, processamento dos dados e geração de visualizações. O sistema itera sobre os dados do DataFrame e verifica se o arquivo foi carregado e se o usuário está logado.

### 3. Finalização e Limpeza
O sistema finaliza exibindo os resultados e permitindo que o usuário faça logout. Durante a finalização, o estado da sessão é limpo ao fazer logout, e logs de atividades do usuário são gerados.

## 🔗 Integrações com Sistemas Externos
Não foram identificadas integrações com sistemas externos.

## 🔒 Aspectos de Segurança
- **Autenticação:** Verificação de credenciais de login.
- **Autorização:** Controle de acesso baseado no estado de login.
- **Criptografia:** Não aplicável (não há armazenamento de dados sensíveis).
- **Validações:** Sanitização de entradas do usuário.
- **Auditoria:** Logs de tentativas de login e erros.

## ⚠️ Pontos Críticos e Tratamento de Erros
1. **Login do usuário**
   - **Impacto:** Se falhar, o usuário não poderá acessar o dashboard.
   - **Mitigação:** Exibir mensagem de erro e permitir nova tentativa.
   - **Monitoramento:** Logs de tentativas de login.

2. **Processamento de dados**
   - **Impacto:** Se falhar, não será possível gerar visualizações.
   - **Mitigação:** Exibir mensagem de erro e solicitar novo upload.
   - **Monitoramento:** Logs de erros durante o processamento.

## 🧩 Arquitetura e Estrutura

### Classes/Estruturas Principais
Não foram identificadas classes ou estruturas definidas.

### Padrões de Design Utilizados
Não foram identificados padrões de design utilizados.

## 📦 Dependências e Requisitos

### Bibliotecas/Frameworks
- Streamlit
- Pandas
- Plotly

### Variáveis de Ambiente
Não foram identificadas variáveis de ambiente.

### Configurações
Não foram identificadas configurações específicas.

## 📁 Arquivos e Diretórios
- **Caminho:** `uploaded_file`
  - **Tipo:** arquivo
  - **Operação:** leitura
  - **Formato:** xlsx/csv

## 🌐 APIs e WebServices
Não foram identificadas APIs ou web services.

## ⚙️ Documentação Completa das Funções/Métodos

### 🔧 `check_login`
- **Parâmetros:** `[]`
- **Retorno:** `bool`
- **Visibilidade:** public
- **Estático:** false
- **Assíncrono:** false
- **Complexidade:** baixa
- **Descrição:** Verifica se o usuário está logado e atualiza o estado de login.

### 🔧 `login_page`
- **Parâmetros:** `[]`
- **Retorno:** `None`
- **Visibilidade:** public
- **Estático:** false
- **Assíncrono:** false
- **Complexidade:** média
- **Descrição:** Exibe a página de login e processa a autenticação do usuário.

### 🔧 `logout`
- **Parâmetros:** `[]`
- **Retorno:** `None`
- **Visibilidade:** public
- **Estático:** false
- **Assíncrono:** false
- **Complexidade:** baixa
- **Descrição:** Realiza o logout do usuário.

### 🔧 `calculate_tenure_group`
- **Parâmetros:** `tenure_days: int`
- **Retorno:** `str`
- **Visibilidade:** public
- **Estático:** false
- **Assíncrono:** false
- **Complexidade:** baixa
- **Descrição:** Calcula o grupo de tempo de permanência baseado em dias.

### 🔧 `calculate_age_group`
- **Parâmetros:** `age: int`
- **Retorno:** `str`
- **Visibilidade:** public
- **Estático:** false
- **Assíncrono:** false
- **Complexidade:** baixa
- **Descrição:** Calcula o grupo etário baseado na idade.

### 🔧 `process_data`
- **Parâmetros:** `df: DataFrame`
- **Retorno:** `DataFrame`
- **Visibilidade:** public
- **Estático:** false
- **Assíncrono:** false
- **Complexidade:** média
- **Descrição:** Processa os dados da planilha, convertendo datas e calculando métricas.

### 🔧 `create_overview_metrics`
- **Parâmetros:** `df: DataFrame`
- **Retorno:** `None`
- **Visibilidade:** public
- **Estático:** false
- **Assíncrono:** false
- **Complexidade:** média
- **Descrição:** Cria e exibe métricas da visão geral a partir dos dados filtrados.

### 🔧 `create_monthly_timeline`
- **Parâmetros:** `df: DataFrame`
- **Retorno:** `Figure`
- **Visibilidade:** public
- **Estático:** false
- **Assíncrono:** false
- **Complexidade:** média
- **Descrição:** Cria um gráfico de linha temporal mensal dos desligamentos.

### 🔧 `create_risk_matrix`
- **Parâmetros:** `df: DataFrame`, `filter_iniciativa: str`
- **Retorno:** `Figure`
- **Visibilidade:** public
- **Estático:** false
- **Assíncrono:** false
- **Complexidade:** alta
- **Descrição:** Cria uma matriz de risco com base nos dados filtrados.

### 🔧 `create_age_analysis`
- **Parâmetros:** `df: DataFrame`
- **Retorno:** `Figure`
- **Visibilidade:** public
- **Estático:** false
- **Assíncrono:** false
- **Complexidade:** média
- **Descrição:** Cria uma análise gráfica por grupo etário.

### 🔧 `main`
- **Parâmetros:** `[]`
- **Retorno:** `None`
- **Visibilidade:** public
- **Estático:** false
- **Assíncrono:** false
- **Complexidade:** alta
- **Descrição:** Função principal que controla o fluxo do aplicativo.

### 🔧 `get_mes_ano_str`
- **Parâmetros:** `df: DataFrame`
- **Retorno:** `Series`
- **Visibilidade:** private
- **Estático:** false
- **Assíncrono:** false
- **Complexidade:** baixa
- **Descrição:** Gera uma string formatada para o eixo X (Mês/Ano) a partir dos dados.

## 🛠️ Configurações e Constantes
Não foram identificadas configurações ou constantes específicas.

---