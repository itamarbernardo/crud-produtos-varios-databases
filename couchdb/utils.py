import socket
import couchdb

def conectar():
    """
    Função para conectar ao servidor
    """
    user = "admin"
    password = "1234"
    
    conexao = couchdb.Server(f'http://{user}:{password}@localhost:5984')
    
    banco = 'python_couch'
    
    if banco in conexao:
        #Caso o banco exista na conexao
        db = conexao[banco]
        
        return db
    else:
        try:
            #Vou criar o banco
            db = conexao.create(banco)
            
            return db
        except socket.gaierror as e:
            #O CouchDB faz uso de Sockets na conexão
            print(f'Erro na conexao: {e}')
        except couchdb.http.Unauthorized as f:
            #Usuario ou Senha errada 
            print(f'Você não tem permissão de acesso: {f}')
        except ConnectionRefusedError as c:
            print(f'Não foi possíve conectar ao servidor: {c}')

def desconectar():
    """ 
    Função para desconectar do servidor.
    """
    #O próprio CouchDB já faz a desconexao automaticamente
    print('Desconectando do servidor...')


def listar():
    """
    Função para listar os produtos
    """
    db = conectar()
    
    if db:
        if db.info()['doc_count'] > 0:
            print('Listando produtos....')
            print('--------------------')
            for doc in db:
                print(f"ID: {db[doc]['_id']}")
                print(f"Revisao (Rev): {db[doc]['_rev']}")
                print(f"Nome: {db[doc]['nome']}")
                print(f"Preço: {db[doc]['preco']}")
                print(f"Estoque: {db[doc]['estoque']}")
                print('---------------')
        else:
            print('Não existem produtos cadastrados')
    else:
        print('Não foi possível conectar ao servidor')

def inserir():
    """
    Função para inserir um produto
    """  
    db = conectar()
    
    if db:
        nome = input('Informe o nome do produto: ')
        preco = float(input('Informe o preço do produto: '))
        estoque = int(input('Informe o estoque do produto: '))
        
        produto = {"nome": nome, "preco": preco, "estoque": estoque}
        
        resultado = db.save(produto)
        
        if resultado:
            print(f'O produto {nome} foi inserido com sucesso')
        else:
            print('Não foi possível inserir o produto')
    else:
        print('Não foi possível conectar ao servidor')

def atualizar():
    """
    Função para atualizar um produto
    """
    db = conectar()
    
    if db:
        
        chave = input('Informe o ID do produto: ')

        try:
            doc = db[chave] #Se ele nao encontrar, já vai para o except
                        
            nome = input('Informe o nome do produto: ')
            preco = float(input('Informe o preço do produto: '))
            estoque = int(input('Informe o estoque do produto: '))

            doc['nome'] = nome
            doc['preco'] = preco
            doc['estoque'] = estoque
            
            db[doc.id] = doc
            print(f'O produto {nome} foi atualizado com sucesso')
        except couchdb.http.ResourceNotFound as e:
            print(f'Produto não encontrado: {e}')
                    
    else:
        print('Não foi possível conectar ao servidor')

def deletar():
    """
    Função para deletar um produto
    """  
    db = conectar()
    
    if db:
        chave = input('Informe o ID do produto: ')
        try:
            db.delete(db[chave])
            
            print('Produto deletado com sucesso')
        except couchdb.http.ResourceNotFound as e:
            print(f'Erro ao deletar o produto: {e}')
    else:
        print('Não foi possível conectar ao servidor')


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
