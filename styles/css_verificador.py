def estilo_verificador():
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
    return estilo