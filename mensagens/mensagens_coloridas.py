from termcolor import colored


def mensagem_titulo(mensagem):
    print(colored(mensagem, 'blue'))

def mensagem_normal(mensagem):
    print(mensagem)

def mensagem_sucesso(mensagem):
    print(colored(mensagem, 'green'))

def mensagem_erro(mensagem):
    print(colored(mensagem, 'red'))
    
def mensagem_fim(mensagem):
    print(colored(mensagem, 'yellow'))