# Importa as funções necessárias de diferentes módulos
from abrir_navegador import abrir_navegador
from contas import (contas_ativas, contas_inativas, contas_vazias,
                    erro_ao_verificar, nao_fez_login)
from instagram.acessar_perfil_instagram import acessar_perfil_instagram
from instagram.detalhes_do_perfil import publicacoes
from instagram.verificar_contas import verificacao_contas
from mensagens.mensagens_coloridas import mensagem_fim, mensagem_titulo


# Define a função principal
def run(playwright, modo, navegadores, perfis, callback):
    try:
        # Exibe uma mensagem de título
        mensagem_titulo('Iniciando Verificação')
        
        # Obtém a lista de perfis dividindo a string pelos caracteres de quebra de linha
        lista_perfis = perfis.split('\n')
        
        # Instancia o navegador e a página
        navegador, pagina =  abrir_navegador(playwright, modo, navegadores)
        
        # Inicializa contadores para contas ativas, inativas e erros
        contador_ativas = 0
        contador_inativas = 0
        contador_bug = 0
    
        # Itera sobre cada perfil na lista de perfis
        for perfil in lista_perfis:
            
            # Divide o perfil em usuário e senha
            values = perfil.split()
            if len(values) != 2:
                continue

            usuario_instagram, senha_instagram = values

            # Acessa o perfil do Instagram com o usuário e senha fornecidos
            res = acessar_perfil_instagram(pagina, usuario_instagram, senha_instagram)

            # Se a função de acesso retornar False, fecha o navegador e continua para o próximo perfil
            if res == False:
                contador_bug += 1
                callback(contador_ativas, contador_inativas, contador_bug)  # Chamada do callback
                nao_fez_login(usuario_instagram, senha_instagram)
                navegador.close()
                navegador, pagina = abrir_navegador(playwright, modo, navegadores)
                continue
            else:
                # Se o login foi efetuado com sucesso, sai do loop
                contador_ativas += 1
                callback(contador_ativas, contador_inativas, contador_bug)  # Chamada do callback
                break

        indice_perfil = 1

        for perfil in lista_perfis:
            # Separando os valores do perfil atual
            valores = perfil.split()

            # Coletando usuario e senha da lista_perfis
            usuario_instagram = valores[0].strip()
            senha_instagram = valores[1].strip()

            # Realizando a verificação da conta
            res = verificacao_contas(pagina, usuario_instagram)
            
            # Verificando pela quantidade de publicações se a conta está vazia ou não
            quantidade_fotos = publicacoes(pagina)

            # Verifica se o número de publicações é igual a 0
            if quantidade_fotos == 0:
                contas_vazias(usuario_instagram, senha_instagram)
            elif quantidade_fotos is None:
                # Trata explicitamente o caso em que a quantidade de fotos é None
                # Neste caso, optamos por não fazer nada (passar)
                pass
            
            # Atualiza os contadores e chama o callback com base no resultado da verificação
            if res == 1:
                contador_ativas += 1
                callback(contador_ativas, contador_inativas, contador_bug)  # Chamada do callback
                contas_ativas(usuario_instagram, senha_instagram)
            elif res == 2:
                contador_inativas += 1
                callback(contador_ativas, contador_inativas, contador_bug)  # Chamada do callback
                contas_inativas(usuario_instagram, senha_instagram)
            elif res == 3:
                contador_bug += 1
                callback(contador_ativas, contador_inativas, contador_bug)  # Chamada do callback
                erro_ao_verificar(usuario_instagram, senha_instagram)

            # Se a verificação falhou, fecha o navegador, abre um novo e continua para o próximo perfil
            elif res == False:
                contador_bug += 1
                erro_ao_verificar(usuario_instagram, senha_instagram)
                navegador.close()
                navegador, pagina = abrir_navegador(playwright, modo, navegadores)
                
                try:
                    outros_perfis = lista_perfis[indice_perfil]
                    novo_usuario, nova_senha = outros_perfis.split()
                except Exception as abre:
                    print(abre)
                
                res = acessar_perfil_instagram(pagina, novo_usuario, nova_senha)
                
                if res == False:
                    navegador.close()
                    navegador, pagina = abrir_navegador(playwright, modo, navegadores)
                    acessar_perfil_instagram(pagina, novo_usuario, nova_senha)
                else:
                    pass
                
                indice_perfil += 1
                
                continue
                    
                

        # Exibe uma mensagem de fim após a verificação de todas as contas
        mensagem_fim('TODAS AS CONTAS JÁ FORAM VERIFICADAS!')
        return contador_ativas, contador_inativas, contador_bug


    except Exception as e:
        # Exibe uma mensagem de erro se ocorrer uma exceção
        print(f"Ocorreu um erro: {e}")
        with open('./logs/error_main.txt', 'a+') as arquivo:
            arquivo.write(f'Ocorreu um erro na no arquivo main.py. Código: {str(e)}\n\n')
