from mensagens import mensagem_erro, mensagem_sucesso


def logado(pagina):
    
    try:
        # Obtendo todos os cookies
        cookies = pagina.cookies()
        
        # Variável para verificar se perfil está logado
        perfil_logado = False
        
        # Iterar sobre os cookies para verificar o cookie "sessionid"
        for cookie in cookies:
            if cookie['name'] == 'sessionid':
                mensagem_sucesso('Perfil logado com sucesso!')
                perfil_logado = True
                break

        if not perfil_logado:
            mensagem_erro('O perfil foi deslogado. Refazendo o login...')
            return False
        return True
    except:
        mensagem_erro('Não foi possível relogar no perfil!')
        return False