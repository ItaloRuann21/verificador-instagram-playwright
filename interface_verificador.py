import json
import sys
from threading import Thread

from playwright.sync_api import sync_playwright
from PyQt5.QtCore import QObject, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QComboBox, QDesktopWidget,
                             QHBoxLayout, QLabel, QPushButton, QTextEdit,
                             QVBoxLayout, QWidget)

from main import run
from styles.css_verificador import estilo_verificador


class Contadores(QObject):
    contador_ativas_atualizado = pyqtSignal(int)
    contador_inativas_atualizado = pyqtSignal(int)
    contador_bug_atualizado = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.contador_ativas = 0
        self.contador_inativas = 0
        self.contador_bug = 0

    def atualizar_contadores(self, contador_ativas, contador_inativas, contador_bug):
        self.contador_ativas = contador_ativas
        self.contador_inativas = contador_inativas
        self.contador_bug = contador_bug
        self.contador_ativas_atualizado.emit(self.contador_ativas)
        self.contador_inativas_atualizado.emit(self.contador_inativas)
        self.contador_bug_atualizado.emit(self.contador_bug)

class MainWindow(QWidget):
    fechar_sinal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle('IR Automações')
        
        self.resize(350, 600)  # Definindo o tamanho da janela

        # Centraliza a janela na tela
        screen_geometry = QDesktopWidget().screenGeometry()
        width = screen_geometry.width()
        height = screen_geometry.height()
        window_width = self.width()
        window_height = self.height()
        x = (width - window_width) // 2
        y = (height - window_height) // 8
        self.move(x, y)

        # Definindo icone da interface
        icon = QIcon('./storage/img/irvtbot.png')
        self.setWindowIcon(icon)

        # Definindo a logo da interface
        logo = './storage/img/verificador.png'
        icone_logo = QIcon(logo)

        # Define um layout principal vertical
        layout = QVBoxLayout()

        # Título centralizado
        label_icone = QLabel()
        icone_logo = QIcon('./storage/img/verificador.png')
        label_icone.setPixmap(icone_logo.pixmap(250, 250))
        label_icone.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_icone)

        # Formulário
        label_perfis = QLabel('Digite os perfis do Instagram:')
        label_perfis.setAlignment(Qt.AlignCenter)
        self.lista_de_perfis = QTextEdit()
        # Adicionando o placeholder
        self.lista_de_perfis.setPlaceholderText("usuario senha\nusuario senha\nusuario senha\nusuario senha\nusuario senha\nusuario senha")  
        label_modo = QLabel('Navegador Visível')
        label_modo.setAlignment(Qt.AlignCenter)
        self.modo = QComboBox()  # Removido o modo local para que possa ser acessado globalmente
        self.modo.addItems(['Sim', 'Não'])
        label_navegador = QLabel('Navegador padrão')
        label_navegador.setAlignment(Qt.AlignCenter)
        self.navegador = QComboBox()  # Removido o navegador local para que possa ser acessado globalmente
        self.navegador.addItems(['Brave', 'Google Chrome', 'Edge'])

        layout.addWidget(label_perfis)
        layout.addWidget(self.lista_de_perfis)
        layout.addWidget(label_modo)
        layout.addWidget(self.modo)
        layout.addWidget(label_navegador)
        layout.addWidget(self.navegador)

        # Botão Iniciar
        btn_iniciar = QPushButton('Iniciar')
        # Altera o cursor para o ícone de mão ao passar sobre o botão "Iniciar"
        btn_iniciar.setCursor(Qt.PointingHandCursor)
        btn_iniciar.clicked.connect(lambda: self.iniciar_em_thread(
            self.lista_de_perfis.toPlainText().strip(), self.modo.currentText(), self.navegador.currentText()))
        layout.addWidget(btn_iniciar)

        # Layout para os contadores
        layout_horizontal = QHBoxLayout()

        # Contadores
        for icon_path in ['./storage/img/check.png', './storage/img/trash.png', './storage/img/complain.png']:
            label = QLabel()
            label.setPixmap(QIcon(icon_path).pixmap(100, 100))
            layout_horizontal.addWidget(label)
            mensagem = QLabel()
            layout_horizontal.addWidget(mensagem)
            if icon_path == './storage/img/check.png':
                self.mensagem_ativa = mensagem
            elif icon_path == './storage/img/trash.png':
                self.mensagem_inativa = mensagem
            elif icon_path == './storage/img/complain.png':
                self.mensagem_bug = mensagem

        layout.addLayout(layout_horizontal)

        # Aplica o layout à janela principal
        self.setLayout(layout)

        # Carrega o estilo CSS
        estilo = estilo_verificador()
        self.setStyleSheet(estilo)

        # Conecta o sinal fechar_sinal ao método closeEvent
        self.fechar_sinal.connect(self.closeEvent)

        # QTimer para atualizar a interface a cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_interface)
        self.timer.start(1000)  # 1000 ms = 1 segundo

        # Instância global da classe Contadores
        self.contadores = Contadores()

        # Carregar conteúdo do arquivo JSON ao iniciar
        self.carregar_conteudo()

        # Conectar sinais de alteração nos ComboBoxes aos slots correspondentes
        self.modo.currentIndexChanged.connect(self.atualizar_conteudo)
        self.navegador.currentIndexChanged.connect(self.atualizar_conteudo)

    def iniciar_em_thread(self, perfis, modo, navegadores):
        thread = Thread(target=self.iniciar, args=(perfis, modo, navegadores))
        thread.start()

    def iniciar(self, perfis, modo, navegadores):
        def callback(contador_ativas, contador_inativas, contador_bug):
            self.contadores.atualizar_contadores(
                contador_ativas, contador_inativas, contador_bug)

        playwright = sync_playwright().start()
        run(playwright, modo, navegadores, perfis, callback)
        playwright.stop()

    def closeEvent(self, event):
        self.salvar_conteudo()  # Salva o conteúdo antes de fechar
        self.fechar_sinal.emit()
        event.accept()

    def atualizar_interface(self):
        # Atualiza a interface com os valores atuais dos contadores
        self.mensagem_ativa.setText(str(self.contadores.contador_ativas))
        self.mensagem_inativa.setText(str(self.contadores.contador_inativas))
        self.mensagem_bug.setText(str(self.contadores.contador_bug))

    def carregar_conteudo(self):
        try:
            with open('./storage/config/localStorage.json', 'r') as file:
                data = json.load(file)
                conteudo_salvo = data.get('configs', '')
                self.lista_de_perfis.setPlainText(conteudo_salvo)
                # Carrega as escolhas anteriores dos ComboBoxes
                modo_salvo = data.get('modo', '')
                if modo_salvo:
                    self.modo.setCurrentIndex(self.modo.findText(modo_salvo))
                navegador_salvo = data.get('navegador', '')
                if navegador_salvo:
                    self.navegador.setCurrentIndex(self.navegador.findText(navegador_salvo))
        except FileNotFoundError:
            pass

    def salvar_conteudo(self):
        conteudo = self.lista_de_perfis.toPlainText()
        with open('./storage/config/localStorage.json', 'w') as file:
            data = {'configs': conteudo,
                    'modo': self.modo.currentText(),
                    'navegador': self.navegador.currentText()}
            json.dump(data, file)

    def atualizar_conteudo(self):
        self.salvar_conteudo()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()
