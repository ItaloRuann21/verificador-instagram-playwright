import hashlib
import platform
import sys
from datetime import datetime

import ntplib
import pymongo
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit, QMessageBox,
                             QPushButton, QVBoxLayout, QWidget)
from pytz import timezone

from interface import MainWindow  # Importando a outra interface


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
                        window.setText('<font color="red">Login bloqueado! Proibido uso de login em máquinas diferentes!</font>')
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

                    window.setText('<font color="green">Login realizado com sucesso!</font>')

                    # Exibe uma janela popup com o tempo restante em dias
                    QMessageBox.information(window, 'Tempo restante', f'<font color="yellow">Seu plano expira em:</font> {dias_restantes} dias')

                    # Fechando janela de login após o OK
                    window.close()

                    # Retorna True para indicar sucesso no login
                    return True
                else:
                    window.setText('<font color="yellow">Plano expirado. Renove sua licença!</font>')
                    return False
        else:
            window.setText('<font color="red">Login incorreto!</font')
            return False
    except pymongo.errors.ConnectionFailure:
        window.setText('Erro! Mude para DNS da Google')
        return False


def interface_login(app):
    window = QWidget()
    window.setWindowTitle('IR Automações')
    window.resize(500, 300)  # Definindo o tamanho da janela

    # Centralizando a janela na tela
    screen_geometry = app.desktop().screenGeometry()
    x = int((screen_geometry.width() - window.width()) / 2)
    y = int((screen_geometry.height() - window.height()) / 5)
    window.move(x, y)

    layout = QVBoxLayout()
    window.setLayout(layout)
    window.show()
    
    # Icone da interface
    icon = QIcon('./storage/img/irvtbot.png')
    window.setWindowIcon(icon)
    
    # icone da logo principal
    logo = './storage/img/principal.png'
    icone_logo = QIcon(logo)
    label_icone = QLabel()
    pixmap = icone_logo.pixmap(250, 250)
    label_icone.setPixmap(pixmap)
    label_icone.setAlignment(Qt.AlignCenter)
    
    
    quebra_linha = QLabel('')
    email_label = QLabel('Email')
    email_input = QLineEdit()
    email_label.setAlignment(Qt.AlignCenter)
    
    password_label = QLabel('Senha')
    password_input = QLineEdit()
    password_label.setAlignment(Qt.AlignCenter)
    password_input.setEchoMode(QLineEdit.Password)

    login_button = QPushButton('Iniciar')
    mensagem_label = QLabel('')
    mensagem_label.setAlignment(Qt.AlignCenter)

    # Aplicando estilos do PySimpleGUI
    email_label.setStyleSheet("color: #FFF;")
    password_label.setStyleSheet("color: #FFF;")
    mensagem_label.setStyleSheet("color: #FFF;")
    # Aplicando estilos do PySimpleGUI
    window.setStyleSheet("""
        background-color: #363636;
        font-family: poppins, sans-serif;
    """)

    email_label.setStyleSheet("""
        color: rgb(255, 255, 255);
        font-family: poppins;
        font-size: 14px;
    """)
    password_label.setStyleSheet("""
        color: rgb(255, 255, 255);
        font-family: poppins;
        font-size: 14px;
    """)
    mensagem_label.setStyleSheet("""
        color: rgb(255, 255, 255);
        font-family: poppins;
        font-size: 14px;
    """)

    email_input.setStyleSheet("""
        background-color: #1B1B1E;
        color: rgb(255, 255, 255);
        font-family: poppins;
        border: 1px solid rgb(58, 58, 58);
        border-radius: 9px;
        padding: 5px;
        border-color: #8B8682;
        font-size: 14px;
    """)
    password_input.setStyleSheet("""
        background-color: #1B1B1E;
        color: rgb(255, 255, 255);
        font-family: poppins;
        border: 1px solid rgb(58, 58, 58);
        border-radius: 9px;
        padding: 5px;
        border-color: #8B8682;
        font-size: 14px;
    """)

    login_button.setStyleSheet("""
        background-color: rgb(72, 99, 247);
        color: rgb(255, 255, 255);
        font-family: poppins;
        font-size: 14px;
        border: 1px solid rgb(58, 58, 58);
        border-radius: 9px;
        padding: 5px 10px;
    """)


    layout.addWidget(label_icone)
    layout.addWidget(quebra_linha)
    layout.addWidget(email_label)
    layout.addWidget(email_input)
    layout.addWidget(quebra_linha)
    layout.addWidget(password_label)
    layout.addWidget(password_input)
    layout.addWidget(quebra_linha)
    layout.addWidget(login_button)
    layout.addWidget(mensagem_label)
    

    def handle_login():
        email = email_input.text()
        password = password_input.text()

        if email == '':
            mensagem_label.setText('Preencha o email!')
        elif password == '':
            mensagem_label.setText('Preencha a senha!')
        else:
            if verificar_login(email, password, mensagem_label, app):
                # Se o login for bem-sucedido, cria e exibe a outra interface
                main_window = MainWindow()
                main_window.show()
                window.close()

    login_button.clicked.connect(handle_login)

    window.setLayout(layout)
    window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    interface_login(app)
    sys.exit(app.exec_())
