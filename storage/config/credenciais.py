import configparser


def salvar_credenciais(email, senha):
    
    try:
        # Cria uma instância do ConfigParser
        config = configparser.ConfigParser()

        # Abre o arquivo de configuração (ou cria se não existir)
        config.read('./storage/config/config.ini')

        # Adiciona as informações de email e senha ao arquivo de configuração
        config['Credenciais'] = {'email': email, 'senha': senha}

        # Salva as alterações no arquivo de configuração
        with open('./storage/config/config.ini', 'w') as config_file:
            config.write(config_file)
    except Exception as e:
        
        with open('./logs/error.txt', 'a+') as arquivo:
            arquivo.write(f'Erro ao pegar credenciais no arquivo credenciais.py. Código: {str(e)}\n\n')

def carregar_credenciais():
    # Cria uma instância do ConfigParser
    config = configparser.ConfigParser()

    # Abre o arquivo de configuração (se existir)
    config.read('./storage/config/config.ini')

    # Verifica se existem credenciais armazenadas no arquivo de configuração
    if 'Credenciais' in config:
        return config['Credenciais']['email'], config['Credenciais']['senha']
    else:
        return '', ''  # Retorna strings vazias se não houver credenciais armazenadas