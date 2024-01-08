from pyautogui import size

from mensagens import mensagem_erro
from useragent import user_agent_aleatorio


def abrir_navegador(playwright, modo):
   
   try:
        
        if modo == 'Sim':
            modo = False
        else:
            modo = True
        
        # instanciando user agent
        useragent = user_agent_aleatorio()
        
        # construtor do navegador
        navegador = playwright.chromium.launch(
            headless=modo,
            args=[
                '--no-sandbox',
                '--ignore-certificate-errors',
                '--user-agent=' + useragent
            ]
        )
        
        # Criando um contexto anônimo
        contexto_anônimo = navegador.new_context()

        # Abrindo uma janela em modo anônimo
        pagina = contexto_anônimo.new_page()

        # Configurando a linguagem da página para português
        pagina.set_extra_http_headers({'Accept-Language': 'pt-br'})
        
        largura, altura = size()
        
        # Definindo o tamanho da tela
        pagina.set_viewport_size({"width": largura, "height": altura})

        
        return navegador, pagina
    
   except:
       mensagem_erro('Erro no navegador!')