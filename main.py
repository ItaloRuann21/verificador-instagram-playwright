from abrir_navegador import abrir_navegador
from instagram.acessar_perfil_instagram import acessar_perfil_instagram
from instagram.verificar_contas import verificacao_contas
from logado import logado
from mensagens import mensagem_erro, mensagem_normal, mensagem_titulo


def run(playwright, modo, perfis):
    try:
        mensagem_titulo('Iniciando Verificação')
        
        # Obtendo a lista de perfis
        lista_perfis = perfis.split('\n')
        
        # Instancia dp navegador e pagina
        navegador, pagina =  abrir_navegador(playwright, modo)
        
        # iterando para cada perfil, obter o usuario e senha
        for perfil in lista_perfis:
            
            # Coletando usuario e senha da lista de perfis
            usuario_instagram, senha_instagram = perfil.split()

            # Acessar o perfil do Instagram
            res =  acessar_perfil_instagram(pagina, usuario_instagram, senha_instagram)

            # Se a resposta da função for falsa, fecha navegador e continua o loop for para avançar na próxima conta.
            if res == False:
                navegador.close()
                continue
            else:
                # Se o login foi efetuado com sucesso, para o loop for
                break
            
        # Iniciando verificação das contas
        for perfil in lista_perfis:
            usuario_instagram, senha_instagram = perfil.split()
            res_verificacao = verificacao_contas(pagina, usuario_instagram, senha_instagram)
            
            if res_verificacao == False:
                mensagem_erro(f"Não foi possível verificar o perfil: {usuario_instagram}")
                break  # Encerra o loop se a verificação falhar
                        

        # Fechar o navegador após terminar as operações
        navegador.close()

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
