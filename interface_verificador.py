import sys
from threading import Thread

from playwright.sync_api import sync_playwright
from PyQt5.QtCore import QObject, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
                             QPushButton, QTextEdit, QVBoxLayout, QWidget)

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
        self.contador_ativas += contador_ativas
        self.contador_inativas += contador_inativas
        self.contador_bug += contador_bug
        self.contador_ativas_atualizado.emit(self.contador_ativas)
        self.contador_inativas_atualizado.emit(self.contador_inativas)
        self.contador_bug_atualizado.emit(self.contador_bug)


class MainWindow(QWidget):
    fechar_sinal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle('IR Automações')
        self.resize(500, 300)

        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 8
        self.move(x, y)

        icon = QIcon('./storage/img/irvtbot.png')
        self.setWindowIcon(icon)

        logo = './storage/img/verificador.png'
        icone_logo = QIcon(logo)
        label_icone = QLabel()
        pixmap = icone_logo.pixmap(250, 250)
        label_icone.setPixmap(pixmap)
        label_icone.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()

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

        layout_horizontal = QHBoxLayout()

        layoult_ativa = QHBoxLayout()
        layoult_inativa = QHBoxLayout()
        layoult_bug = QHBoxLayout()

        icone_ativa = QIcon('./storage/img/check.png')
        label_ativa = QLabel()
        pixmap = icone_ativa.pixmap(100, 100)
        label_ativa.setPixmap(pixmap)

        icone_desativada = QIcon('./storage/img/trash.png')
        label_desativada = QLabel()
        pixmap = icone_desativada.pixmap(100, 100)
        label_desativada.setPixmap(pixmap)

        icone_bug = QIcon('./storage/img/complain.png')
        label_bug = QLabel()
        pixmap = icone_bug.pixmap(100, 100)
        label_bug.setPixmap(pixmap)

        layoult_ativa.setAlignment(Qt.AlignCenter)
        layoult_inativa.setAlignment(Qt.AlignCenter)
        layoult_bug.setAlignment(Qt.AlignCenter)

        self.mensagem_ativa = QLabel()
        self.mensagem_inativa = QLabel()
        self.mensagem_bug = QLabel()

        layoult_ativa.addWidget(label_ativa)
        layoult_ativa.addWidget(self.mensagem_ativa)
        layoult_inativa.addWidget(label_desativada)
        layoult_inativa.addWidget(self.mensagem_inativa)
        layoult_bug.addWidget(label_bug)
        layoult_bug.addWidget(self.mensagem_bug)

        layout_horizontal.addLayout(layoult_ativa)
        layout_horizontal.addLayout(layoult_inativa)
        layout_horizontal.addLayout(layoult_bug)

        layout.addWidget(label_icone)
        layout.addWidget(quebra_linha)
        layout.addWidget(label_perfis)
        layout.addWidget(self.text_edit_perfis)
        layout.addWidget(quebra_linha)
        layout.addWidget(label_modo)
        layout.addWidget(combo_modo)
        layout.addWidget(quebra_linha)
        layout.addWidget(btn_iniciar)
        layout.addLayout(layout_horizontal)

        self.setLayout(layout)

        estilo = estilo_verificador()
        self.setStyleSheet(estilo)

        self.fechar_sinal.connect(self.closeEvent)

        # QTimer para atualizar a interface a cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_interface)
        self.timer.start(1000)  # 1000 ms = 1 segundo

        # Instância global da classe Contadores
        self.contadores = Contadores()

    def iniciar_em_thread(self, perfis, modo):
        thread = Thread(target=self.iniciar, args=(perfis, modo))
        thread.start()

    def iniciar(self, perfis, modo):
        playwright = sync_playwright().start()
        contador_ativas, contador_inativas, contador_bug = run(playwright, modo, perfis)
        self.contadores.atualizar_contadores(contador_ativas, contador_inativas, contador_bug)
        playwright.stop()

    def closeEvent(self, event):
        self.fechar_sinal.emit()
        event.accept()

    def atualizar_interface(self):
        # Atualiza a interface com os valores atuais dos contadores
        self.mensagem_ativa.setText(str(self.contadores.contador_ativas))
        self.mensagem_inativa.setText(str(self.contadores.contador_inativas))
        self.mensagem_bug.setText(str(self.contadores.contador_bug))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


# if __name__ == "__main__":
#     main()
