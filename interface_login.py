import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit, QMessageBox,
                             QPushButton, QVBoxLayout, QWidget)

from db.banco_de_dados import verificar_login
from interface_verificador import MainWindow
from mensagens.mensagens_att import mensagem_atualização
from storage.config.credenciais import carregar_credenciais, salvar_credenciais


def interface_login(app):
    window = QWidget()
    window.setWindowTitle('IR Automações')
    window.resize(350, 600)  # Definindo o tamanho da janela
    

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

    # Carregar as credenciais salvas
    saved_email, saved_password = carregar_credenciais()
    email_input.setText(saved_email)  # Preenche o campo de email com o email salvo
    password_input.setText(saved_password)  # Preenche o campo de senha com a senha salva

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
                salvar_credenciais(email, password)
                mensagem_atualização(window)
                main_window = MainWindow()
                main_window.show()
                window.close()

    login_button.clicked.connect(handle_login)

    # Altera o cursor para o ícone de mão ao passar sobre o botão "Iniciar"
    login_button.setCursor(Qt.PointingHandCursor)

    window.setLayout(layout)
    window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    interface_login(app)
    sys.exit(app.exec_())
