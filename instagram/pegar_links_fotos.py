import instaloader


def pegar_link_perfis(usuario):
    try:
        # Criar uma instância do Instaloader
        loader = instaloader.Instaloader()

        # Carregar o perfil do usuário
        perfil = instaloader.Profile.from_username(loader.context, usuario)

        # Abrir o arquivo de saída em modo de adição
        with open('./relatorios/link_posts.txt', 'a+') as arquivo:
            # Escrever o nome de usuário uma vez
            arquivo.write(usuario + ':\n')

            # Contador para acompanhar o número de fotos coletadas
            contador = 0

            # Iterar sobre os posts do perfil
            for post in perfil.get_posts():
                if post.typename == "GraphImage":  # Verificar se o post é uma imagem
                    link_post = f"https://www.instagram.com/p/{post.shortcode}/"
                    arquivo.write(link_post + '\n')  # Salvar o link da página do post no arquivo
                    
                    contador += 1
                    if contador >= 6:  # Parar após coletar as 6 primeiras fotos
                        break
            
            # Adicionar uma linha em branco após cada bloco de links do usuário
            arquivo.write('\n')
            
        return True
    except Exception as erro:
        # Gravando o erro em um arquivo de log
        with open('./logs/erro_link_fotos.txt', 'a+') as arquivo:
            arquivo.write(f'Erro ao pegar link de cada post no perfil. Código: {str(erro)}\n\n')
        
        return False
