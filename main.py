from termcolor import colored

from abrir_navegador import abrir_navegador
from contas import quantidade_ativas, quantidade_inativas
from instagram.acessar_perfil_instagram import acessar_perfil_instagram
from instagram.verificar_contas import verificacao_contas
from mensagens import (mensagem_erro, mensagem_fim, mensagem_normal,
                       mensagem_sucesso, mensagem_titulo)


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
            
        # Iniciando verificação das contas
        for perfil in lista_perfis:
            values = perfil.split()
            if len(values) != 2:
                continue

            usuario_instagram, senha_instagram = values
            
            res = verificacao_contas(pagina, usuario_instagram, senha_instagram)

            # Verificar se o instagram está com bloqueio. Se estiver, retorna outra conta
            if res == False:
                navegador.close()
                navegador, pagina = abrir_navegador(playwright, modo)
                acessar_perfil_instagram(pagina, usuario_instagram, senha_instagram)
                continue
                
        
        # Instanciando a quantidade de contas ativas
        quantidade_ativa = quantidade_ativas('contas_ativas.txt')
        
        # Instanciando a quantidade de contas inativas
        quantidade_inativa = quantidade_inativas('contas_inativas.txt')
        
        print('')
        mensagem_fim('TODAS AS CONTAS FORAM VERIFICADAS!')
        
        print(f'Contas ativas: {colored(quantidade_ativa, 'green')}')
        print(f'Contas inativas: {colored(quantidade_inativa, 'red')}')
            
    except Exception as e:
        print(f"Ocorreu um erro: {e}")