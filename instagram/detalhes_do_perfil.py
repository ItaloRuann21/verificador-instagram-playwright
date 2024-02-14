def publicacoes(pagina):
    try:
        # Obter o texto do conteúdo da classe 'li>._ac2a'
        quantidade_fotos_texto = pagina.evaluate("""
            const quantidade_fotos_elemento = document.querySelector('li>._ac2a');
            quantidade_fotos_elemento ? quantidade_fotos_elemento.textContent : '';
        """)

        # Converter o texto para um número inteiro
        quantidade_fotos = int(quantidade_fotos_texto)

        return quantidade_fotos
    except Exception as e:
        print(f"Ocorreu um erro ao obter as publicações: {e}")
        # Gravando o erro em um arquivo de log
        with open('./logs/publicacoes_error.txt', 'a+') as arquivo:
            arquivo.write(f'Ocorreu um erro ao obter as publicações no arquivo detalhes_do_perfil.py Código: {str(e)}\n\n')
        return None
