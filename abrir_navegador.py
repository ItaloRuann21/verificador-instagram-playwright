

from mensagens.mensagens_coloridas import mensagem_erro
from useragent import user_agent_aleatorio


def abrir_navegador(playwright, modo, navegadores):
   
   try:
        
        if modo == 'Sim':
            modo = False
        else:
            modo = True
            
        if navegadores == 'Brave':
            navegadores = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
        elif navegadores == 'Google Chrome':
            navegadores = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        elif navegadores == 'Edge':
            navegadores = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
        
        # instanciando user agent
        useragent = user_agent_aleatorio()
        
        # construtor do navegador
        navegador = playwright.chromium.launch(
            headless=modo, executable_path=navegadores,
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
        pagina.set_viewport_size({"width": 800, "height": 600})

        
        return navegador, pagina
    
   except Exception as error:
       mensagem_erro(f'Erro no navegador! {error}')
       with open('./logs/navegador_error.txt', 'a+') as arquivo:
            arquivo.write(f'Erro na função do navegador. Código: {str(error)}\n\n')