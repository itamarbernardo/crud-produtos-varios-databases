import redis

def conectar():
    """
    Função para conectar ao servidor
    """
    conexao = redis.Redis(host="localhost", port=6379)
    
    return conexao

def desconectar(conexao):
    """ 
    Função para desconectar do servidor.
    """    
    conexao.connection_pool.disconnect()


def listar():
    """
    Função para listar os produtos
    """
    conexao = conectar()
    
    try:
        #vamos buscar todas as chaves com esse formato
        #Nós definimos o formato de chave -> o que ficar mais facil para identificar os hashs
        dados = conexao.keys(pattern='produtos:*')
        
        if len(dados) > 0:
            print('Listando Produtos.....')
            print('-----------------------')
            for chave in dados:
                produto = conexao.hgetall(chave)
                print(f"ID: {str(chave, 'UTF-8', 'ignore')}")
                #Os dados vem no formato de String binaria -> Por isso estamos convertendo e por isso o 'b' abaixo
                print(f"Nome: {str(produto[b'nome'], 'UTF-8', 'ignore')}")
                print(f"Preço: {str(produto[b'preco'], 'UTF-8', 'ignore')}")
                print(f"Estoque: {str(produto[b'estoque'], 'UTF-8', 'ignore')}")
                print('-----------------------')
        else:
            print('Não existem produtos cadastrados')
    except redis.exceptions.ConnectionError as e:
        print(f'Erro ao listar produtos: {e}')
    desconectar(conexao=conexao)

def inserir():
    """
    Função para inserir um produto
    """  
    conexao = conectar()
    
    nome = input('Informe o nome do produto:')
    preco = float(input('Informe o preço do produto: '))
    estoque = int(input('Informe o estoque do produto: '))

    produto = {"nome": nome, "preco": preco, "estoque": estoque}
    chave = f'produtos:{gerar_id()}'
    
    try:
        #Colocamos multiplos sets de uma vez
        resultado = conexao.hmset(chave, produto)
        if resultado:
            print(f'Produto {nome} inserido com sucesso!')
        else:
            print('Não foi possível inserir o produto')
    except redis.exceptions.ConnectionError as e:
            print(f'Erro ao inserir produto: {e}')
    desconectar(conexao)
    
def gerar_id():
    try:
        conexao = conectar()
        chave = conexao.get('chave')
        
        #Se a chave já existir, eh porque eu já tenho algum produto cadastrado
        #Vou incrementa-la para gerar a nova chave
        if chave:
            chave = conexao.incr('chave')
            return chave
        else:
            #Se não existir, vamos setar uma chave
            conexao.set('chave', 1)
            return 1
    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possivel gerar a chave: {e}')
    desconectar(conexao=conexao)    
    
def atualizar():
    """
    Função para atualizar um produto
    """
    conexao = conectar()
    
    chave = input('Informe a chave do produto: ')    
    nome = input('Informe o nome do produto:')
    preco = float(input('Informe o preço do produto: '))
    estoque = int(input('Informe o estoque do produto: '))

    produto = {"nome": nome, "preco": preco, "estoque": estoque}
    
    try:
        chave = conexao.get(chave)
 
        #Se a chave já existir, eh porque eu já tenho algum produto cadastrado
        #Então, permito a atualizacao
        if chave:        
            resultado = conexao.hmset(chave, produto) #Vamos sobrescrever os dados na chave -> Se a chave não existir, vai inserir nessa nova chave
            
            if resultado:
                print(f'O produto {nome} foi atualizado com sucesso')
        else:
            print(f'Não existe produto com a chave: {chave}')
    except redis.exceptions.ConnectionError as e:
            print(f'Erro ao atualizar produto: {e}')
    desconectar(conexao)
    
def deletar():
    """
    Função para deletar um produto
    """  
    conexao = conectar()
    chave = input('Informe a chave do produto: ')
    
    try:
        resultado = conexao.delete(chave)
        
        if resultado == 1:
            print('Produto deletado com sucesso!')
        else:
            print('Não existe produto com a chave informada')
    except redis.exceptions.ConnectionError as e:
        print(f'Erro ao deletar produto: {e}')
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
