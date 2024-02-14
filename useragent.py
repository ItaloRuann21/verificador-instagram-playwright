from random import choice


def user_agent_aleatorio():
    
    try:
        # Ler o arquivo user agent :D
        userAgent = open('./storage/config/useragents.txt', 'r')
        
        # retornando todas as linhas já sorteada do userAgent
        return choice(userAgent.readlines()).strip()
    except Exception as e:
        with open('./logs/error_useragents.txt', 'a+') as arquivo:
            arquivo.write(f'Erro no arquivo useragent.py. Código: {str(e)}\n\n')