from contas import contas_ativas, nao_fez_login
from mensagens.mensagens_coloridas import (mensagem_erro, mensagem_normal,
                                           mensagem_sucesso)


def acessar_perfil_instagram(pagina, usuario, senha):
    try:
        mensagem_normal(f'{usuario} - Fazendo login no Instagram')

        # Site instagram
        pagina.goto('https://www.instagram.com/')

        # Definindo usuário e senha do instagram
        pagina.wait_for_selector('[name="username"]')
        pagina.fill('[name="username"]', usuario)
        pagina.wait_for_timeout(2000)
        pagina.wait_for_selector('[name="password"]')
        pagina.fill('[name="password"]', senha)

        # Confirmando credenciais
        pagina.wait_for_selector('text="Entrar"')
        pagina.wait_for_timeout(2000)
        pagina.click('text="Entrar"')

        # Esperando o seletor do span página inicial aparecer
        pagina.wait_for_selector(
            'span:has-text("Página inicial")', timeout=60000)

        contas_ativas(usuario, senha)

        return True
    except Exception as e:
        mensagem_erro(f'Erro ao fazer login: {str(e)}')
        nao_fez_login(usuario, senha)

        # Gravando o erro em um arquivo de log
        with open('./logs/instagram_error.txt', 'a+') as arquivo:
            arquivo.write(
                f'Erro na arquivo acessar_perfil_instagram.py. Código: {str(e)}\n\n')

        return False
