import psycopg2

def conectar():
    """
    Função para conectar ao servidor
    """
    
    try:
        conexao = psycopg2.connect(database="python_postgre", host="localhost", user="geek", password="1234")
        return conexao
    except psycopg2.Erro as e:
        print(f'Erro na conexão ao PostgreSQL: {e}')
        
def desconectar(conexao):
    """ 
    Função para desconectar do servidor.
    """
    if conexao:
        conexao.close()

def listar():
    """
    Função para listar os produtos
    """
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    
    if len(produtos) > 0:
        print('Listando produtos....')
        print('----------------------')
        for produto in produtos:
            print(f'ID: {produto[0]}')
            print(f'Nome: {produto[1]}')
            print(f'Preço: {produto[2]}')
            print(f'Estoque: {produto[3]}')
            print('------------------------')
    else:
        print('Não há produtos cadastrados!') 
    desconectar(conexao=conexao)
       
def inserir():
    """
    Função para inserir um produto
    """  
    conexao = conectar()
    cursor = conexao.cursor()
    
    nome = input('Informe o nome do produto: ')
    preco = float(input('Informe o preço do produto: '))
    estoque = int(input('Informe o estoque do produto: '))
    
    cursor.execute(f"INSERT INTO produtos (nome, preco, estoque) VALUES ('{nome}', {preco}, {estoque})")
    
    conexao.commit()
    
    if cursor.rowcount == 1:
        print(f'Produto {nome} inserido com sucesso!')
    else:
        print('Erro ao inserir produto')
    desconectar(conexao=conexao)
    
def atualizar():
    """
    Função para atualizar um produto
    """
    conexao = conectar()
    cursor = conexao.cursor()
    
    codigo = int(input('Informe o ID do produto: '))    
    nome = input('Informe o novo nome do produto: ')
    preco = float(input('Informe o novo preço do produto: '))
    estoque = int(input('Informe o novo estoque do produto: '))

    cursor.execute(f"UPDATE produtos SET nome='{nome}', preco={preco}, estoque={estoque} WHERE id={codigo}")
    conexao.commit()
    
    # se ele conseguir atualizar, retornamos 1, se não retorna zero -> Por isso não precisa fazer uma busca pra ver se o produto existe
    if cursor.rowcount == 1:
        print(f'Produto {nome} atualizado com sucesso!')
    else:
        print('Erro ao atualizar produto')
    desconectar(conexao=conexao)
    
    
def deletar():
    """
    Função para deletar um produto
    """  
    conexao = conectar()
    cursor = conexao.cursor()
    
    codigo = int(input('Digite o código do produto para excluir: '))

    cursor.execute(f'DELETE FROM produtos WHERE id={codigo}')
    conexao.commit()
    
    
    if cursor.rowcount == 1:
        print('Produto excluído com sucesso')
    elif cursor.rowcount > 1:
        print('Exclusão de mais de um produto')
    else:
        print('Erro ao excluir o produto')
    desconectar(conexao)
    
def menu():
    """
    Função para gerar o menu inicial
    """
    print('=========Gerenciamento de Produtos==============')
    print('Selecione uma opção: ')
    print('1 - Listar produtos.')
    print('2 - Inserir produtos.')
    print('3 - Atualizar produto.')
    print('4 - Deletar produto.')
    opcao = int(input())
    if opcao in [1, 2, 3, 4]:
        if opcao == 1:
            listar()
        elif opcao == 2:
            inserir()
        elif opcao == 3:
            atualizar()
        elif opcao == 4:
            deletar()
        else:
            print('Opção inválida')
    else:
        print('Opção inválida')
