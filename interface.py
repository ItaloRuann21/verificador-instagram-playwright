import sys
from threading import Thread
from playwright.sync_api import sync_playwright
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QComboBox, QLabel, QPushButton,
                             QTextEdit, QVBoxLayout, QWidget)

from main import run

class MainWindow(QWidget):
    # Sinal personalizado para fechar o aplicativo
    fechar_sinal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Projeto Verificador XCTRL')
        self.setGeometry(100, 100, 500, 300)

        layout = QVBoxLayout()

        label_perfis = QLabel('Digite os perfis do Instagram')
        label_perfis.setAlignment(Qt.AlignCenter)
        text_edit_perfis = QTextEdit()
        label_modo = QLabel('Você quer ver acontecendo?')
        label_modo.setAlignment(Qt.AlignCenter)
        combo_modo = QComboBox()
        combo_modo.addItems(['Sim', 'Não'])

        btn_iniciar = QPushButton('Iniciar')
        btn_iniciar.clicked.connect(lambda: self.iniciar_em_thread(text_edit_perfis.toPlainText(), combo_modo.currentText()))

        layout.addWidget(label_perfis)
        layout.addWidget(text_edit_perfis)
        layout.addWidget(label_modo)
        layout.addWidget(combo_modo)
        layout.addWidget(btn_iniciar)

        self.setLayout(layout)

        estilo = """
            QWidget {
                background-color: #F0F0F0;
                font-family: Arial, sans-serif;
            }
            
            QLabel {
                font-size: 14px;
                margin-bottom: 5px;
            }
            
            QTextEdit {
                min-height: 100px;
                font-size: 12px;
            }
            
            QComboBox, QPushButton {
                font-size: 14px;
                padding: 5px;
                margin-top: 5px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 3px;
            }
            
            QPushButton:hover {
                background-color: #45a049;
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
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
