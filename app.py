import streamlit as st
import sqlite3

# Conexão com o banco de dados
conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

# Define o modo wide
st.set_page_config(layout="wide")

# Função para inserir um novo produto
def add_produto(descricao, unidade, numero_lote, localizacao, quantidade, validade, dias_para_vencer, situacao,
                preco_custo, preco_venda):
    cursor.execute(
        'INSERT INTO produtos (descricao, unidade, numero_lote, localizacao, quantidade, validade, dias_para_vencer, situacao, preco_custo, preco_venda) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (descricao, unidade, numero_lote, localizacao, quantidade, validade, dias_para_vencer, situacao,
         preco_custo, preco_venda)
    )
    conn.commit()
    return cursor.lastrowid  # Retorna o ID do produto inserido


# Função para atualizar um produto
def update_produto(id, descricao, unidade, numero_lote, localizacao, quantidade, validade, dias_para_vencer, situacao,
                   preco_custo, preco_venda):
    cursor.execute(
        'UPDATE produtos SET descricao = ?, unidade = ?, numero_lote = ?, localizacao = ?, quantidade = ?, validade = ?, dias_para_vencer = ?, situacao = ?, preco_custo = ?, preco_venda = ? WHERE id = ?',
        (descricao, unidade, numero_lote, localizacao, quantidade, validade, dias_para_vencer, situacao, preco_custo,
         preco_venda, id)
    )
    conn.commit()


# Função para deletar um produto
def delete_produto(id):
    cursor.execute('DELETE FROM produtos WHERE id = ?', (id,))
    conn.commit()


# Título da aplicação
st.title("Gerenciamento de Estoque")

# Abas
tabs = st.tabs(["Visualizar", "Adicionar", "Atualizar", "Deletar"])

# Aba Visualizar
with tabs[0]:
    st.header("Visualizar Produtos")
    st.markdown("---")  # Separador horizontal

    # Filtro
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            filtro_coluna = st.selectbox("Filtrar por:",
                                         ['id', 'descricao', 'unidade', 'numero_lote', 'localizacao', 'quantidade',
                                          'validade', 'dias_para_vencer', 'situacao', 'preco_custo', 'preco_venda'])
        with col2:
            filtro_valor = st.text_input("Valor do Filtro")

    if filtro_valor:
        produtos = cursor.execute(
            f'SELECT * FROM produtos WHERE {filtro_coluna} LIKE "%{filtro_valor}%"'
        ).fetchall()
    else:
        produtos = cursor.execute(
            f'SELECT * FROM produtos'
        ).fetchall()

    # Exibe a tabela com os dados (sem os nomes das colunas)
    st.table(produtos)

# Aba Adicionar
with tabs[1]:
    st.header("Adicionar Produto")
    st.markdown("---")  # Separador horizontal

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            descricao = st.text_input("Descrição")
            unidade = st.text_input("Unidade")
            numero_lote = st.text_input("Número do Lote")
            localizacao = st.text_input("Localização")
        with col2:
            quantidade = st.number_input("Quantidade", min_value=0)
            validade = st.date_input("Validade")
            dias_para_vencer = st.number_input("Dias para Vencer", min_value=0)
            situacao = st.text_input("Situação")

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            preco_custo = st.number_input("Preço Custo")
        with col2:
            preco_venda = st.number_input("Preço Venda")

    if st.button("Salvar"):
        produto_id = add_produto(descricao, unidade, numero_lote, localizacao, quantidade, validade, dias_para_vencer,
                    situacao, preco_custo, preco_venda)
        st.success(f"Produto adicionado com sucesso! ID: {produto_id}")

# Aba Atualizar
with tabs[2]:
    st.header("Atualizar Produto")
    st.markdown("---")  # Separador horizontal

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            id = st.text_input("ID do Produto", key="id_input")
            if id:
                produto = cursor.execute('SELECT * FROM produtos WHERE id = ?', (id,)).fetchone()
                if produto:
                    st.write(f"ID do Produto: {produto['id']}")  # Exibe o ID do banco de dados
                    descricao = st.text_input("Descrição", value=produto['descricao'])
                    unidade = st.text_input("Unidade", value=produto['unidade'])
                    numero_lote = st.text_input("Número do Lote", value=produto['numero_lote'])
                    localizacao = st.text_input("Localização", value=produto['localizacao'])
                else:
                    st.error("Produto não encontrado.")

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            if id and produto:
                quantidade = st.number_input("Quantidade", min_value=0, value=produto['quantidade'])
                validade = st.date_input("Validade", value=produto['validade'])
                dias_para_vencer = st.number_input("Dias para Vencer", min_value=0, value=produto['dias_para_vencer'])
                situacao = st.text_input("Situação", value=produto['situacao'])
        with col2:
            if id and produto:
                preco_custo = st.number_input("Preço Custo", value=produto['preco_custo'])
                preco_venda = st.number_input("Preço Venda", value=produto['preco_venda'])

    if st.button("Atualizar") and id and produto:
        update_produto(id, descricao, unidade, numero_lote, localizacao, quantidade, validade, dias_para_vencer,
                        situacao, preco_custo, preco_venda)
        st.success("Produto atualizado com sucesso!")

# Aba Deletar
with tabs[3]:
    st.header("Deletar Produto")
    st.markdown("---")  # Separador horizontal

    id = st.text_input("ID do Produto", key="delete_id_input")  # Adiciona a chave 'delete_id_input'
    if st.button("Deletar"):
        delete_produto(id)
        st.success("Produto deletado com sucesso!")

# Fecha a conexão com o banco de dados
conn.close()
