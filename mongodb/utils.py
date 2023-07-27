from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from bson import errors as beerros

def conectar():
    """
    Função para conectar ao servidor
    """
    conexao = MongoClient('localhost', 27017)
    
    return conexao

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
    db = conexao.python_mongo #selecionamos o banco que foi criado
    
    #Ele não dá exceção no conectar e desconectar
    try:
        if db.produtos.count_documents({}) > 0:
            produtos = db.produtos.find()
            print('Listando produtos......')
            print('-----------------------')
            for produto in produtos:
                print(f"ID: {produto['_id']}")
                print(f"Nome: {produto['nome']}")
                print(f"Preço: {produto['preco']}")
                print(f"Estoque: {produto['estoque']}")
                print('---------------------')
        else:
            print('Não existem produtos cadastrados')
    except errors.PyMongoError as e:
        print(f'Erro ao acessar banco de dados: {e}')
    desconectar(conexao)
            
def inserir():
    """
    Função para inserir um produto
    """  
    conexao = conectar()
    db = conexao.python_mongo #Selecionamos o banco de dados pra conexão
    
    nome = input('Informe o nome do produto: ')
    preco = float(input('Informe o preço do produto: '))
    estoque = int(input('Informe o estoque do produto: '))
    
    try:
        db.produtos.insert_one( #Se não tiver a coleção com o nome produtos, vai criar uma nova
            {
                "nome": nome,
                "preco": preco,
                "estoque": estoque
            }
        )
        print(f'O produto {nome} foi inserido com sucesso!')
    except errors.PyMongoError as e:
        print('Erro ao inserir produto')
    desconectar(conexao)
    
def atualizar():
    """
    Função para atualizar um produto
    """
    conexao = conectar()
    db = conexao.python_mongo
    
    # id no python é uma função -> Criamos a variavel _id com o '_' para não dar conflito
    _id = input('Informe o ID do produto: ')
    nome = input('Informe o nome do produto: ')
    preco = float(input('Informe o preço do produto: '))
    estoque = int(input('Informe o estoque do produto: '))
    
    try:
        if db.produtos.count_documents({}) > 0:
            
            # o primeiro dado é o filtro, o segundo é o que será alterado
            resultado = db.produtos.update_one(
                {'_id': ObjectId(_id)}, #não é apenas uma string, é um ObjectId
                {
                    "$set": {
                        "nome": nome,
                        "preco": preco,
                        "estoque": estoque
                    }
                }
            )
            if resultado.modified_count == 1:
                print(f'O produto {nome} foi atualizado com sucesso')
            else:
                print('Não foi possível atualizar o produto')
        else:
            print('Não há produtos para serem atualizados')
    except errors.PyMongoError as e:
        print('Erro ao atualizar produto')
    except beerros.InvalidId as f:
        print(f'Object ID inválido: {f}')
    desconectar(conexao)

def deletar():
    """
    Função para deletar um produto
    """  
    conexao = conectar()
    db = conexao.python_mongo
    
    _id = input('Informe o ID do produto: ')
    
    try:
        if db.produtos.count_documents({}) > 0:
            resultado = db.produtos.delete_one(
                {"_id": ObjectId(_id)}
            ) 
            if resultado.deleted_count > 0:
                print('Produto deletado com sucesso')
            else:
                print('Não foi possível deletar o produto')
        else:
            print('Não existem produtos a serem deletados')
    except errors.PyMongoError as e:
        print(f'Erro ao acessar banco de dados: {e}')
    except beerros.InvalidId as f:
        print(f'Object ID inválido: {f}')
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
