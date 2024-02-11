import sys
from threading import Thread

from playwright.sync_api import sync_playwright
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QComboBox, QLabel, QPushButton,
                             QTextEdit, QVBoxLayout, QWidget)

from main import run


class MainWindow(QWidget):
    # Sinal personalizado para fechar o aplicativo
    fechar_sinal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle('IR Automações')
        self.resize(500, 300)  # Definindo o tamanho da janela
        
        # Centralizando a janela na tela
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 8
        self.move(x, y)
        
        # Icone da interface
        icon = QIcon('./storage/img/irvtbot.png')
        self.setWindowIcon(icon)
        
        # icone da logo principal
        logo = './storage/img/verificador.png'
        icone_logo = QIcon(logo)
        label_icone = QLabel()
        pixmap = icone_logo.pixmap(250, 250)
        label_icone.setPixmap(pixmap)
        label_icone.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        
        # Criando qlabel para quebra de linha
        quebra_linha = QLabel('')

        label_perfis = QLabel('Digite os perfis do Instagram')
        label_perfis.setAlignment(Qt.AlignCenter)
        self.text_edit_perfis = QTextEdit()
        label_modo = QLabel('Navegador Visível')
        label_modo.setAlignment(Qt.AlignCenter)
        combo_modo = QComboBox()
        combo_modo.addItems(['Sim', 'Não'])

        btn_iniciar = QPushButton('Iniciar')
        btn_iniciar.clicked.connect(lambda: self.iniciar_em_thread(self.text_edit_perfis.toPlainText().strip(), combo_modo.currentText()))

        layout.addWidget(label_icone)
        layout.addWidget(quebra_linha)
        layout.addWidget(label_perfis)
        layout.addWidget(self.text_edit_perfis)
        layout.addWidget(quebra_linha)
        layout.addWidget(label_modo)
        layout.addWidget(combo_modo)
        layout.addWidget(quebra_linha)
        layout.addWidget(btn_iniciar)

        self.setLayout(layout)

        estilo = """
            QWidget {
                background-color: #363636;
                font-family: poppins, sans-serif;
            }

            QLabel {
                font-size: 14px;
                margin-bottom: 5px;
                color: #FFF;
            }

            QTextEdit {
                min-height: 100px;
                font-size: 12px;
                background-color: #1B1B1E;
                color: #FFF;
            }
            
            

            QPushButton {
                font-size: 14px;
                padding: 5px;
                margin-top: 5px;
                background-color: #4863F7;
                color: white;
                border: none;
                border-radius: 3px;
            }
            
            QComboBox {
                font-size: 14px;
                padding: 5px;
                margin-top: 5px;
                background-color: #1B1B1E;
                color: white;
                border: none;
                border-radius: 3px;
            }

            QPushButton:hover {
                background-color: #3A4FF5;
            }

            QLineEdit {
                border: 1px solid #1B1B1E;
                border-radius: 3px;
                padding: 5px;
                background-color: #1B1B1E;
                color: #FFF;
                selection-background-color: #4863F7;
            }
            
            QLineEdit:focus {
                border: 1px solid #4863F7;
            }
        """

        self.setStyleSheet(estilo)

        # Conecta o sinal fechar_sinal ao método closeEvent
        self.fechar_sinal.connect(self.closeEvent)

    def iniciar_em_thread(self, perfis, modo):
        thread = Thread(target=self.iniciar, args=(perfis, modo))
        thread.start()

    def iniciar(self, perfis, modo):
        with sync_playwright() as playwright:
            run(playwright, modo, perfis)
        
    def closeEvent(self, event):
        # Emitir o sinal fechar_sinal quando a janela está prestes a ser fechada
        self.fechar_sinal.emit()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app  # Retorna a instância de QApplication