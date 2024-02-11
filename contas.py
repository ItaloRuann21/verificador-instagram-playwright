

def contas_ativas(usuario, senha):
    try:
        with open('contas_ativas.txt', 'r') as arquivo:
            conteudo = arquivo.readlines()
    except FileNotFoundError:
        conteudo = []

    with open('contas_ativas.txt', 'a+') as arquivo:
        usuarios_senha = [linha.strip().split() for linha in conteudo]
        if [usuario, senha] not in usuarios_senha:
            arquivo.write(usuario + ' ' + senha + '\n')


def contas_inativas(usuario, senha):
    try:
        with open('contas_inativas.txt', 'r') as arquivo:
            conteudo = arquivo.readlines()
    except FileNotFoundError:
        conteudo = []

    with open('contas_inativas.txt', 'a+') as arquivo:
        usuarios_senha = [linha.strip().split() for linha in conteudo]
        if [usuario, senha] not in usuarios_senha:
            arquivo.write(usuario + ' ' + senha + '\n')

def nao_fez_login(usuario, senha):
    try:
        with open('nao_fez_login.txt', 'r') as arquivo:
            conteudo = arquivo.readlines()
    except FileNotFoundError:
        conteudo = []

    with open('nao_fez_login.txt', 'a+') as arquivo:
        usuarios_senha = [linha.strip().split() for linha in conteudo]
        if [usuario, senha] not in usuarios_senha:
            arquivo.write(usuario + ' ' + senha + '\n')

def erro_ao_verificar(usuario, senha):
    try:
        with open('erro_ao_verificar.txt', 'r') as arquivo:
            conteudo = arquivo.readlines()
    except FileNotFoundError:
        conteudo = []

    with open('erro_ao_verificar.txt', 'a+') as arquivo:
        usuarios_senha = [linha.strip().split() for linha in conteudo]
        if [usuario, senha] not in usuarios_senha:
            arquivo.write(usuario + ' ' + senha + '\n')