from instagram.acessar_perfil_instagram import acessar_perfil_instagram
from mensagens import mensagem_erro, mensagem_sucesso


def logado(pagina, navegador, usuario, senha):
    try:
        # Obtendo todos os cookies
        identificador_erro = pagina.wait_for_selector('text="Ocorreu um problema e não foi possível carregar a página."', timeout=5000)
        
        if identificador_erro:
            navegador.close()
            acessar_perfil_instagram(usuario, senha)
            return True
        
        return True
    except Exception as a:
        mensagem_erro(f'Erro na função logado: {a}')
        return False