import hashlib
import platform
from datetime import datetime

import ntplib
import pymongo
from PyQt5.QtWidgets import QMessageBox
from pytz import timezone


# Função para obter a data e hora atual no fuso horário brasileiro
def obter_data_hora_atual_ntp():
    try:
        cliente_ntp = ntplib.NTPClient()
        resposta = cliente_ntp.request('pool.ntp.org')
        if resposta:
            tempo_unix = resposta.tx_time
            tz_brasil = timezone('America/Sao_Paulo')
            return datetime.fromtimestamp(tempo_unix, tz=tz_brasil)
    except Exception as e:
        print(f"Erro ao obter tempo do NTP: {e}")
        
        # Gravando o erro em um arquivo de log
        with open('./logs/banco_de_dados_error.txt', 'a+') as arquivo:
            arquivo.write(f'Erro ao obter tempo do NTP. Código: {str(e)}\n\n')
    return None

# Função para verificar o status do plano semanal
def verificar_plano_semanal(expiracao):
    agora = obter_data_hora_atual_ntp()

    # Verifica se a data atual é válida (não é None)
    if agora:
        return agora < expiracao
    else:
        # Se a data atual não for obtida, considera o plano expirado
        return False

# Função para obter um identificador exclusivo do dispositivo
def get_device_unique_id():
    # Obtém o endereço MAC da máquina
    mac_address = ":".join(hex(i)[2:].zfill(2) for i in platform.node().encode('utf-8'))
    # Pode ser necessário ajustar a formatação do endereço MAC de acordo com suas necessidades

    # Hash do endereço MAC para armazenamento seguro como identificador exclusivo
    return hashlib.sha256(mac_address.encode()).hexdigest()

def verificar_login(email, password, window, app):
    try:
        conexao = pymongo.MongoClient("mongodb+srv://italorvt:32578079@python-montador.exgtqsa.mongodb.net/?retryWrites=true&w=majority")
        db = conexao.get_database('verificador-db')
        colecao = db.get_collection('clientes')
        usuario = colecao.find_one({"email": email, "password": password})

        if usuario:
            expiracao_plano = usuario.get("expiracao", None)

            if expiracao_plano:
                # Obtém o identificador exclusivo do dispositivo
                device_unique_id = get_device_unique_id()

                # Verifica se já há um identificador registrado para o usuário
                stored_device_id = usuario.get("device_unique_id")
                if stored_device_id:  # Se já há um identificador registrado
                    if stored_device_id != device_unique_id:  # Se o identificador atual não corresponde ao registrado
                        QMessageBox.information(window, 'IR Automações', f'<font color="red">Login bloqueado! Proibido uso de login em máquinas diferentes.</font>')
                        return False
                else:  # Se não há um identificador registrado, armazena o identificador atual
                    colecao.update_one({"email": email}, {"$set": {"device_unique_id": device_unique_id}})

                # Adiciona a informação de fuso horário a expiracao_plano
                tz_brasil = timezone('America/Sao_Paulo')
                expiracao_plano = expiracao_plano.replace(tzinfo=tz_brasil)

                if verificar_plano_semanal(expiracao_plano):

                    # Calcula quanto tempo falta para o plano expirar
                    tempo_falta = expiracao_plano - obter_data_hora_atual_ntp()

                    # Calcula o número de dias restantes
                    dias_restantes = round(tempo_falta.total_seconds() / (24 * 3600))

                    # Exibe uma janela popup com o tempo restante em dias
                    QMessageBox.information(window, 'IR Automações', f'<font color="Lime">Login realizado com sucesso!</font>')
                    

                    # Exibe uma janela popup com o tempo restante em dias
                    QMessageBox.information(window, 'Tempo restante', f'<font color="yellow">Seu plano expira em:</font> {dias_restantes} dias')

                    # Fechando janela de login após o OK
                    window.close()

                    # Retorna True para indicar sucesso no login
                    return True
                else:
                    # Exibe uma janela popup com o tempo restante em dias
                    QMessageBox.information(window, 'IR Automações', f'<font color="Yellow">Seu plano expirou. Entre em contato com o desenvolvedor e renove sua licença! (79) 99134-3217</font>')
                    return False
        else:
            # Exibe uma janela popup com o tempo restante em dias
            QMessageBox.information(window, 'Login incorreto!', f'<font color="red">Por favor, verifique seu email e senha novamente!</font>')
            return False
    except pymongo.errors.ConnectionFailure:
        window.setText('Erro! Mude para DNS da Google')
        
        return False