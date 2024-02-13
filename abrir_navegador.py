

from mensagens.mensagens_coloridas import mensagem_erro
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
            headless=modo, executable_path='C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe',
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
        
        
        # Definindo o tamanho da tela
        pagina.set_viewport_size({"width": 600, "height": 600})

        
        return navegador, pagina
    
   except Exception as error:
       mensagem_erro(f'Erro no navegador! {error}')