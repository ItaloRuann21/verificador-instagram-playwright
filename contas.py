

def contas_ativas(usuario, senha):
    with open('contas_ativas.txt', 'a+') as arquivo:
        conteudo = arquivo.readlines()

        if len(conteudo) > 0:
            conteudo.append('\n'+ usuario + ' ' + senha)
        else:
            conteudo.append(usuario + ' ' + senha + '\n')
        arquivo.seek(0)
        arquivo.writelines(conteudo)

def contas_inativas(usuario, senha):
    with open('contas_inativas.txt', 'a+') as arquivo:
        conteudo = arquivo.readlines()
  
        if len(conteudo) > 0:
            conteudo.append('\n'+ usuario + ' ' + senha)
        else:
            conteudo.append(usuario + ' ' + senha + '\n')
        arquivo.seek(0)
        arquivo.writelines(conteudo)

def nao_fez_login(usuario, senha):
    with open('nao_fez_login.txt', 'a+') as arquivo:
        conteudo = arquivo.readlines()
  
        if len(conteudo) > 0:
            conteudo.append('\n'+ usuario + ' ' + senha)
        else:
            conteudo.append(usuario + ' ' + senha + '\n')
        arquivo.seek(0)
        arquivo.writelines(conteudo)
        
def quantidade_ativas(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:  # Abre o arquivo em modo de leitura ('r')
        quant_contas_ativas = sum(1 for linha in arquivo)  # Conta o número de linhas no arquivo
    return quant_contas_ativas  # Retorna o número de linhas contadas 


def quantidade_inativas(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:  # Abre o arquivo em modo de leitura ('r')
        quant_contas_inativas = sum(1 for linha in arquivo)  # Conta o número de linhas no arquivo
    return quant_contas_inativas  # Retorna o número de linhas contadas
    
