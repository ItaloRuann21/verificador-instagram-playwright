import sys
from threading import Thread

from playwright.sync_api import sync_playwright
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QComboBox, QLabel, QPushButton,
                             QTextEdit, QVBoxLayout, QWidget)

from main import run


# Função que inicia a execução com base nos perfis e modo selecionados
def iniciar(perfis, modo):
    with sync_playwright() as playwright:
        run(playwright, modo, perfis)

# Função que executa a função iniciar em uma thread separada
def iniciar_em_thread(perfis, modo):
    thread = Thread(target=iniciar, args=(perfis, modo))
    thread.start()

# Função principal que configura a interface gráfica usando PyQt5
def main():
    # Inicializa a aplicação PyQt
    app = QApplication(sys.argv)
    
    # Cria uma janela principal
    window = QWidget()
    window.setWindowTitle('Projeto Verificador XCTRL')
    window.setGeometry(100, 100, 500, 300)

    # Cria um layout vertical para organizar os widgets
    layout = QVBoxLayout()

    # Cria rótulos, caixas de texto e botões necessários
    label_perfis = QLabel('Digite os perfis do Instagram')
    label_perfis.setAlignment(Qt.AlignCenter)
    text_edit_perfis = QTextEdit()
    label_modo = QLabel('Você quer ver acontecendo?')
    label_modo.setAlignment(Qt.AlignCenter)
    combo_modo = QComboBox()
    combo_modo.addItems(['Sim', 'Não'])

    # Cria um botão 'Iniciar' e conecta a função iniciar_em_thread ao evento de clique
    btn_iniciar = QPushButton('Iniciar')
    btn_iniciar.clicked.connect(lambda: iniciar_em_thread(text_edit_perfis.toPlainText(), combo_modo.currentText()))

    # Adiciona os widgets ao layout
    layout.addWidget(label_perfis)
    layout.addWidget(text_edit_perfis)
    layout.addWidget(label_modo)
    layout.addWidget(combo_modo)
    layout.addWidget(btn_iniciar)

    # Define o layout da janela principal
    window.setLayout(layout)

    # Estilo básico para melhorar a aparência
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

    # Aplica o estilo à janela principal
    window.setStyleSheet(estilo)

    # Exibe a janela
    window.show()

    # Executa o loop de eventos da aplicação
    sys.exit(app.exec_())

# Verifica se o script está sendo executado diretamente
if __name__ == '__main__':
    main()
