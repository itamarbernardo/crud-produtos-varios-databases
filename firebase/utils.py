import pyrebase

def conectar():
    """
    Função para conectar ao servidor
    """
    config = {
        "apiKey": "LKUaSuA18u5M9aD9txSpy25R-rcEDvlDL04uG2k",
        "authDomain": "https://python-firebase-6709a-default-rtdb.firebaseio.com/",
        "databaseURL": "https://python-firebase-6709a-default-rtdb.firebaseio.com/",
        "storageBucket": "python-firebase-6709a.appspot.com/"        
    }
    
    conexao = pyrebase.initialize_app(config=config)
    
    db = conexao.database()

    return db

def desconectar():
    """ 
    Função para desconectar do servidor.
    """
    #O firebase faz automatico


def listar():
    """
    Função para listar os produtos
    """
    db = conectar()
    
    produtos = db.child("produtos").get()
    
    if produtos.val():
        print('Listando produtos....')
        print('---------------------')
        for produto in produtos.each():
            print(f'ID: {produto.key()}')
            print(f"Nome: {produto.val()['nome']}")
            print(f"Preço: {produto.val()['preco']}")
            print(f"Estoque: {produto.val()['estoque']}")
            print('-------------------')
    else:
        print('Não existem produtos cadastrados')
        

def inserir():
    """
    Função para inserir um produto
    """  
    db = conectar()
    
    nome = input('Digite o nome do produto: ')
    preco = float(input('Digite o preço do produto: '))
    estoque =  int(input('Digite o estoque do produto: '))
    
    produto = {"nome": nome, "preco": preco, "estoque": estoque}
    
    resultado = db.child('produtos').push(produto)
    
    if 'name' in resultado: #Se der tudo certo, ele retorna uma chave da colecao -> Essa chave ele chama de 'name' 
        print(f'O produto {nome} inserido com sucesso!')
    else:
        print('Não foi possível inserir o produto')

def atualizar():
    """
    Função para atualizar um produto
    """
    
    db = conectar()
    
    _id = input('Digite o ID do produto: ')
    
    produto = db.child('produtos').child(_id).get()
    
    if produto.val():
        #O produto existe    
        nome = input('Digite o nome do produto: ')
        preco = float(input('Digite o preço do produto: '))
        estoque =  int(input('Digite o estoque do produto: '))

        novo_produto = {"nome": nome, "preco": preco, "estoque": estoque}
        
        # Esse metodo não retorna nada
        db.child('produtos').child(_id).update(novo_produto)
            
        print(f'O produto {nome} foi atualizado com sucesso')
    else:
        print('Não existe produto com esse ID')
        
def deletar():
    """
    Função para deletar um produto
    """  
    db = conectar()
    
    _id = input('Digite o ID do produto: ')
    
    produto = db.child('produtos').child(_id).get()
    
    if produto.val():
        # Esse metodo não retorna nada
        db.child('produtos').child(_id).remove()
        
        print('O produto foi deletado com sucesso')
    else:
        print('Não existe produto com o ID informado')

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
