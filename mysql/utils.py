import MySQLdb


def conectar():
    """
    Função para conectar ao servidor
    """
    try:
        conexao = MySQLdb.connect(db='python_mysql', host='localhost', user='geek', passwd='1234')
        return conexao
    except MySQLdb.Error as e:
        print('Erro na conexão com o MySQL Server {e}')

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
    cursor.execute('SELECT * FROM produtos') #Faz a consulta no banco de dados
    produtos = cursor.fetchall() #Pega o resultado e transforma em uma tupla (tuplas são imutáveis)
    
    if len(produtos) > 0:
        print('Listando produtos....')
        print('-----------------------')
        for produto in produtos:
            print(f'ID: {produto[0]}') #Estamos pegando os indices na mesma ordem que a tabela foi criada
            print(f'Nome: {produto[1]}')
            print(f'Preço: {produto[2]}')
            print(f'Estoque: {produto[3]}')
            print('-----------------------')
    else:
        print('Não há produtos cadastrados')
        
    desconectar(conexao)        
            
def inserir():
    """
    Função para inserir um produto
    """  
    conexao = conectar()
    cursor = conexao.cursor()
    
    nome = input('Informe o nome do produto: ')
    preco = float(input('Informe o preço do produto: '))
    estoque = int(input("Informe a quantidade em estoque: "))
    
    cursor.execute(f"INSERT INTO produtos (nome, preco, estoque) VALUES ('{nome}', {preco}, {estoque})") #Faz a consulta no banco de dados
    conexao.commit()
    
    #print(dir(cursor)) #Vai mostrar todos os métodos que eu posso fazer com o cursor
    if cursor.rowcount == 1:
        print(f'O produto {nome} foi inserido com sucesso!')
    else:
        print('Erro ao inserir o produto')
        
    desconectar(conexao)
    
def atualizar():
    """
    Função para atualizar um produto
    """
    conexao = conectar()
    cursor = conexao.cursor()
    
    codigo = int(input('Informe o código do produto: '))
    nome = input('Informe o novo nome do produto: ')
    preco = float(input('Informe o novo preço do produto: '))
    estoque = int(input("Informe a nova quantidade em estoque: "))
    
    cursor.execute(f"UPDATE produtos SET nome='{nome}', preco={preco}, estoque={estoque} WHERE id={codigo}") 
    conexao.commit()

    if cursor.rowcount == 1:
        print(f'O produto {nome} foi atualizado com sucesso')
    else:
        print('Erro ao atualizar produto')

    desconectar(conexao)

def deletar():
    """
    Função para deletar um produto
    """  
    conexao = conectar()
    cursor = conexao.cursor()
    
    codigo = int(input('Informe o código do produto: '))
    
    cursor.execute(f"DELETE FROM produtos WHERE id={codigo}") #Faz a consulta no banco de dados
    conexao.commit()

    if cursor.rowcount == 1:
        print('Produto Deletado com sucesso')
    else:
        print(f'Erro ao Excluir produto com id {codigo}')

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
