# repo_app.py (VERSÃO REVESTIMENTO FINAL)
import streamlit as st
import pandas as pd
import os

# --- Configuração da Página ---
st.set_page_config(page_title="Repositório z1p0l0ck", page_icon="🔗", layout="wide")

# --- INJEÇÃO DO CSS E DA FONTE ---
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)
try:
    with open("streamlit_assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass # Ignora se o arquivo de estilo não for encontrado

# --- Carregamento de Dados ---
FILE_PATH = "links_repo.csv"
@st.cache_data
def load_data():
    if not os.path.exists(FILE_PATH):
        pd.DataFrame(columns=['category', 'title', 'url', 'description']).to_csv(FILE_PATH, index=False)
    return pd.read_csv(FILE_PATH)

df_links = load_data()

# --- Gerenciamento de Estado ---
if 'admin_auth' not in st.session_state:
    st.session_state.admin_auth = False

# --- Interface ---
st.title("🔗 Repositório de Inteligência z1p0l0ck")

with st.sidebar:
    st.header("Filtros")
    categorias = ["Todas"] + sorted(df_links['category'].unique()) if not df_links.empty else ["Todas"]
    cat_selecionada = st.selectbox("Filtrar por Categoria:", categorias)
    termo_busca = st.text_input("Buscar no Repositório:")
    st.divider()
    st.header("Área do Admin")
    
    # --- SENHA REVELADA ---
    st.info("Senha: `z1p0l0ck_admin_pass`")
    
    password = st.text_input("Senha de Acesso:", type="password", key="password_input")
    if st.button("Autenticar"):
        if password == "z1p0l0ck_admin_pass": 
            st.session_state.admin_auth = True
            st.rerun() 
        else:
            st.error("Senha incorreta.")
    if st.session_state.admin_auth:
        with st.expander("Adicionar Novo Link", expanded=False):
            with st.form("new_link_form", clear_on_submit=True):
                new_cat = st.text_input("Categoria")
                new_title = st.text_input("Título")
                new_url = st.text_input("URL")
                new_desc = st.text_area("Descrição")
                submitted = st.form_submit_button("Adicionar")
                if submitted:
                    if all([new_cat, new_title, new_url, new_desc]):
                        new_data = pd.DataFrame([[new_cat, new_title, new_url, new_desc]], columns=df_links.columns)
                        new_data.to_csv(FILE_PATH, mode='a', header=False, index=False)
                        st.cache_data.clear()
                        st.success("Link adicionado!")
                        st.rerun()
                    else:
                        st.warning("Todos os campos são obrigatórios.")

# Em repo_app.py, SUBSTITUA a seção "Lógica de Exibição"

# --- LÓGICA DE EXIBIÇÃO CUSTOMIZADA ---
df_filtrado = df_links.copy()
if cat_selecionada != "Todas": 
    df_filtrado = df_filtrado[df_filtrado['category'] == cat_selecionada]
if termo_busca:
    termo_busca = termo_busca.lower()
    df_filtrado = df_filtrado[
        df_filtrado['title'].str.lower().str.contains(termo_busca) | 
        df_filtrado['description'].str.lower().str.contains(termo_busca)
    ]

st.subheader(f"Encontrados {len(df_filtrado)} registros de inteligência.")

if df_filtrado.empty:
    st.warning("Nenhum registro corresponde aos filtros atuais.")
else:
    # Loop para renderizar cada link como um bloco customizado
    for index, row in df_filtrado.iterrows():
        with st.container(border=True):
            # Título com a categoria
            st.subheader(f"[{row['category']}] {row['title']}")
            
            # Descrição, procurando por comandos entre crases
            description = str(row['description'])
            if '`' in description:
                # Separa a descrição em partes normais e comandos
                parts = description.split('`')
                # Recria a descrição com a sintaxe de bloco de código do markdown
                formatted_description = ""
                for i, part in enumerate(parts):
                    if i % 2 == 1: # Ímpar, ou seja, dentro das crases
                        formatted_description += f"```{part}```"
                    else:
                        formatted_description += part
                st.markdown(formatted_description, unsafe_allow_html=True)
            else:
                st.markdown(f"_{description}_")

            # Link de acesso
            st.markdown(f"**URL:** <a href='{row['url']}' target='_blank'>{row['url']}</a>", unsafe_allow_html=True)
