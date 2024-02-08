import hashlib
import platform
from datetime import datetime

import ntplib
import pymongo
import PySimpleGUI as sg
from pytz import timezone

from interface import main


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

# Função para autenticar o usuário
def verificar_login(email, password, window):
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
                        window['mensagem'].update('Login bloqueado! Proibido uso de login em máquinas diferentes!', text_color='#FF0000')
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

                    window['mensagem'].update(f'Login realizado com sucesso!', text_color='#00CC00')

                    # Exibe uma janela popup com o tempo restante em dias
                    sg.popup(f'Tempo restante para o plano expirar: {dias_restantes} dias')
                    
                    # Fechando janela de login após o OK
                    window.close()

                    return True
                else:
                    window['mensagem'].update('Plano expirado. Você não pode fazer login.', text_color='#FFFF00')
                    return False
        else:
            window['mensagem'].update('Email ou senha incorretos!', text_color='#FF0000')
            return False
    except pymongo.errors.ConnectionFailure:
        window['mensagem'].update('Erro ao fazer conexão com o banco mongodb', text_color='#FF0000')
        return False

# Definindo o tema
sg.theme('Python')

# Configurando as opções
sg.SetOptions(
    text_color="#FFF",
    font='poppins 11',
    input_elements_background_color='#1B1B1E',
    sbar_background_color='#222',
    input_text_color='#FFF',
    scrollbar_color='#1B1B1E',
    text_element_background_color='#1B1B1E',
    sbar_arrow_color='#fff',
    background_color='#1B1B1E',
    button_color=('#FFF', '#4863F7'),
)

interface_login_sistema = [
    [sg.Text('Email')],
    [sg.Input(key='email_usuario')],
    [sg.Text('Senha')],
    [sg.Input(key='password_usuario', password_char='*')],
    [sg.Button('Login')],
    [sg.Text('', key='mensagem')]
]

def interface_login():
    window = sg.Window('Italo Automações - Verificador', interface_login_sistema)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            return False

        if event == 'Login':
            if values['email_usuario'] == '':
                window['mensagem'].update('Preencha o email!', text_color='#FF0000')
            elif values['password_usuario'] == '':
                window['mensagem'].update('Preencha a senha!', text_color='#FF0000')
            else:
                email_usuario = values['email_usuario']
                password_usuario = values['password_usuario']

                if verificar_login(email_usuario, password_usuario, window):
                    return True

if __name__ == "__main__":
    if interface_login():
        main()
