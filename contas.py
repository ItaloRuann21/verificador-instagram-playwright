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