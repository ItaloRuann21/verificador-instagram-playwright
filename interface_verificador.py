import json
import sys
from threading import Thread

from playwright.sync_api import sync_playwright
from PyQt5.QtCore import QObject, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QComboBox, QDesktopWidget, QFrame,
                             QHBoxLayout, QLabel, QPushButton, QScrollArea,
                             QTextEdit, QVBoxLayout, QWidget)

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
        layout_principal = QVBoxLayout(self)

        # Cria um widget de área de rolagem
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout_principal.addWidget(scroll_area)

        # Cria um widget central para conter todos os widgets do layout rolável
        central_widget = QWidget()
        scroll_area.setWidget(central_widget)

        # Define um layout principal vertical para o widget central
        layout_central = QVBoxLayout(central_widget)

        # Título centralizado
        label_icone = QLabel()
        label_icone.setPixmap(icone_logo.pixmap(250, 250))
        label_icone.setAlignment(Qt.AlignCenter)
        layout_central.addWidget(label_icone)

        # Formulário
        label_perfis = QLabel('Digite os perfis do Instagram:')
        label_perfis.setAlignment(Qt.AlignCenter)
        layout_central.addWidget(label_perfis)
        self.lista_de_perfis = QTextEdit()
        self.lista_de_perfis.setPlaceholderText("usuario senha\nusuario senha\nusuario senha\nusuario senha\nusuario senha\nusuario senha")
        layout_central.addWidget(self.lista_de_perfis)
        label_modo = QLabel('Navegador Visível')
        label_modo.setAlignment(Qt.AlignCenter)
        layout_central.addWidget(label_modo)
        self.modo = QComboBox()
        self.modo.addItems(['Sim', 'Não'])
        layout_central.addWidget(self.modo)
        label_navegador = QLabel('Navegador padrão')
        label_navegador.setAlignment(Qt.AlignCenter)
        layout_central.addWidget(label_navegador)
        self.navegador = QComboBox()
        self.navegador.addItems(['Brave', 'Google Chrome', 'Edge'])
        layout_central.addWidget(self.navegador)
        label_link_posts = QLabel('Salvar link de fotos de cada perfil\nObs: A verificação ficará lenta.')
        label_link_posts.setAlignment(Qt.AlignCenter)
        layout_central.addWidget(label_link_posts)
        self.link_posts = QComboBox()
        self.link_posts.addItems(['Sim', 'Não'])
        layout_central.addWidget(self.link_posts)


        # Adiciona um espaço flexível para empurrar os widgets para cima
        layout_central.addStretch()

        # Layout secundário para os widgets fixos na parte inferior
        layout_fixo = QVBoxLayout()

        # Botão Iniciar
        btn_iniciar = QPushButton('Iniciar')
        btn_iniciar.setCursor(Qt.PointingHandCursor)
        btn_iniciar.clicked.connect(lambda: self.iniciar_em_thread(
            self.lista_de_perfis.toPlainText().strip(), self.modo.currentText(), self.navegador.currentText(), self.link_posts.currentText()))
        layout_fixo.addWidget(btn_iniciar)

        # Layout para os contadores
        layout_horizontal_contadores = QHBoxLayout()

        # Contadores
        for icon_path in ['./storage/img/check.png', './storage/img/trash.png', './storage/img/complain.png']:
            label = QLabel()
            label.setPixmap(QIcon(icon_path).pixmap(100, 100))
            layout_horizontal_contadores.addWidget(label)
            mensagem = QLabel()
            layout_horizontal_contadores.addWidget(mensagem)
            if icon_path == './storage/img/check.png':
                self.mensagem_ativa = mensagem
            elif icon_path == './storage/img/trash.png':
                self.mensagem_inativa = mensagem
            elif icon_path == './storage/img/complain.png':
                self.mensagem_bug = mensagem

        layout_fixo.addLayout(layout_horizontal_contadores)

        # Adiciona o layout fixo na parte inferior ao layout principal
        layout_principal.addLayout(layout_fixo)

        # Carrega o estilo CSS
        estilo = estilo_verificador()
        self.setStyleSheet(estilo)

        # Conecta o sinal fechar_sinal ao método closeEvent
        self.fechar_sinal.connect(self.closeEvent)

        # QTimer para atualizar a interface a cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_interface)
        self.timer.start()

        # Instância global da classe Contadores
        self.contadores = Contadores()

        # Carregar conteúdo do arquivo JSON ao iniciar
        self.carregar_conteudo()

        # Conectar sinais de alteração nos ComboBoxes aos slots correspondentes
        self.modo.currentIndexChanged.connect(self.atualizar_conteudo)
        self.navegador.currentIndexChanged.connect(self.atualizar_conteudo)

    def iniciar_em_thread(self, perfis, modo, navegadores, link_fotos):
        thread = Thread(target=self.iniciar, args=(perfis, modo, navegadores, link_fotos))
        thread.start()

    def iniciar(self, perfis, modo, navegadores, link_fotos):
        def callback(contador_ativas, contador_inativas, contador_bug):
            self.contadores.atualizar_contadores(
                contador_ativas, contador_inativas, contador_bug)

        playwright = sync_playwright().start()
        run(playwright, modo, navegadores, perfis, callback, link_fotos)
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
                link_fotos_salvo = data.get('modo_link_fotos', '')
                if link_fotos_salvo:
                    self.link_posts.setCurrentIndex(self.link_posts.findText(link_fotos_salvo))
        except FileNotFoundError:
            pass

    def salvar_conteudo(self):
        conteudo = self.lista_de_perfis.toPlainText()
        with open('./storage/config/localStorage.json', 'w') as file:
            data = {'configs': conteudo,
                    'modo': self.modo.currentText(),
                    'navegador': self.navegador.currentText(),
                    'modo_link_fotos': self.link_posts.currentText()
                    }
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
