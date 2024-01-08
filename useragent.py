from random import choice


def user_agent_aleatorio():
    
    # Ler o arquivo user agent :D
    userAgent = open('useragents.txt', 'r')
    
    # retornando todas as linhas já sorteada do userAgent
    return choice(userAgent.readlines()).strip()
