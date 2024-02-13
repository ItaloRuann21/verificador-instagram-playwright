from abrir_navegador import abrir_navegador
from contas import (contas_ativas, contas_inativas, erro_ao_verificar,
                    nao_fez_login)
from instagram.acessar_perfil_instagram import acessar_perfil_instagram
from instagram.verificar_contas import verificacao_contas
from mensagens.mensagens_coloridas import (mensagem_erro, mensagem_fim,
                                           mensagem_normal, mensagem_titulo)


def run(playwright, modo, perfis, callback):
    try:
        mensagem_titulo('Iniciando Verificação')
        
        # Obtendo a lista de perfis
        lista_perfis = perfis.split('\n')
        
        # Instancia dp navegador e pagina
        navegador, pagina =  abrir_navegador(playwright, modo)
        
        # contadores
        contador_ativas = 0
        contador_inativas = 0
        contador_bug = 0
    
        # iterando para cada perfil, obter o usuario e senha
        for perfil in lista_perfis:
            
            # Coletando usuario e senha da lista de perfis
            values = perfil.split()
            if len(values) != 2:
                continue

            usuario_instagram, senha_instagram = values

            # Acessar o perfil do Instagram
            res = acessar_perfil_instagram(pagina, usuario_instagram, senha_instagram)

            # Se a resposta da função for falsa, fecha o navegador, recria a página e continua o loop for para avançar na próxima conta.
            if res == False:
                navegador.close()
                navegador, pagina = abrir_navegador(playwright, modo)
                continue
            else:
                # Se o login foi efetuado com sucesso, para o loop for
                break

        # Verificação das contas
        posicao_conta = 0
        while posicao_conta < len(lista_perfis):
            perfil = lista_perfis[posicao_conta]
            values = perfil.split()
            if len(values) != 2:
                posicao_conta += 1
                continue

            usuario_instagram, senha_instagram = values

            res = verificacao_contas(pagina, usuario_instagram, senha_instagram)
            
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

            # Verificar se a verificação falhou
            if res == False:
                contador_bug += 1
                erro_ao_verificar(usuario_instagram, senha_instagram)
                navegador.close()
                navegador, pagina = abrir_navegador(playwright, modo)
                
                # Escolher a segunda conta da lista na posição atual
                segunda_conta = lista_perfis[posicao_conta + 1].split()
                segundo_usuario_instagram, segundo_senha_instagram = segunda_conta[0], segunda_conta[1]

                acessar_perfil_instagram(pagina, segundo_usuario_instagram, segundo_senha_instagram)

                # Incrementar a posição para pular a próxima conta
                posicao_conta += 2
                continue
            
            posicao_conta += 1
            
        mensagem_fim('TODAS AS CONTAS JÁ FORAM VERIFICADAS!')
        return contador_ativas, contador_inativas, contador_bug       

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
