from contas import contas_ativas, nao_fez_login
from mensagens.mensagens_coloridas import (mensagem_erro, mensagem_normal,
                                           mensagem_sucesso)


def acessar_perfil_instagram(pagina, usuario, senha):
    try:
        
        mensagem_normal('Fazendo login no Instagram')
        
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
        pagina.wait_for_selector('span:has-text("Página inicial")')
        
        contas_ativas(usuario, senha)
        
        return True
    except:
        mensagem_erro('Erro ao fazer login. Tentando outra conta!')
        nao_fez_login(usuario, senha)
        return False
    