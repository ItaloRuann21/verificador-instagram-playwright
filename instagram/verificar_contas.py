from contas import contas_ativas, contas_inativas
from mensagens import mensagem_erro, mensagem_normal, mensagem_sucesso


def verificacao_contas(pagina, usuario, senha):
    try:
        link_conta = f'https://www.instagram.com/{usuario}/'
        
        # Iniciando verificação das contas
        pagina.goto(link_conta)
        
        # Espera o seletor estar presente na página
        perfil_ativo = pagina.wait_for_selector('.x78zum5.x1q0g3np.xieb3on', timeout=8000)
        
        if perfil_ativo:
            mensagem_sucesso(f'O perfil {usuario} está ativo!')
            contas_ativas(usuario, senha)
            return True
        else:
            mensagem_erro(f'O perfil {usuario} não está ativo!')
            contas_inativas(usuario, senha)
            return False
    except Exception as e:
        mensagem_erro(f'Ocorreu um erro ao verificar contas: {e}')
        return False
