from mensagens.mensagens_coloridas import (mensagem_erro, mensagem_fim,
                                           mensagem_sucesso)


def verificacao_contas(pagina, usuario):
    try:
        
        link_conta = f'https://www.instagram.com/{usuario}/'
        
        # Iniciando verificação das contas
        pagina.goto(link_conta)
        
        # Espera até que a página esteja carregada
        pagina.wait_for_load_state()
        
        # Verifica se a conta está ativa, se estiver, anota as contas na função contas_ativas
        try:
            pagina.wait_for_selector('.x78zum5.x1q0g3np.xieb3on', timeout=5000)
            mensagem_sucesso(f'O perfil {usuario} está ativo!')
            return 1

        except:
            try:
                pagina.reload()
                pagina.wait_for_selector('[class="x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye x133cpev x1s688f x5n08af x2b8uid x4zkp8e x41vudc x10wh9bi x1wdrske x8viiok x18hxmgj"]', timeout=5000)
                mensagem_erro(f'O perfil {usuario} não está ativo!')
                return 2
            
            except:
                pagina.wait_for_selector('[class="x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w x972fbf xcfux6l x1qhh985 xm0m39n xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x18d9i69 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x9bdzbf x1ypdohk x78zum5 x1f6kntn xwhw2v2 xl56j7k x17ydfre x1n2onr6 x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye xn3w4p2 x5ib6vp xc73u3c x1tu34mt xzloghq"]', timeout=5000)
                mensagem_fim(f'perfil sofreu restrição de página.')
                return False
        
    except Exception as e:
        mensagem_erro(f'Não foi possível verificar a conta {usuario}. Erro: {e}')

        return 3