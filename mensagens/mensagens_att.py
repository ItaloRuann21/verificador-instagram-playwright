from PyQt5.QtWidgets import QMessageBox


def mensagem_atualização(self):
    # Exibe uma janela popup com o tempo restante em dias
    
    mensagem_1 = 'Novidades:'
    
    logs_erros = '1 - Logs de erros adicionado. Se o sistema falhar, logs serão geradas para detectar o problema.'
    
    contas_vazias = '2 - Se na hora da verificação existir contas vazias, será gerado em relatórios.'
    
    contador = '3 - O bug do contador foi corrigido. Agora, será possível observar em tempo real.'
    
    navegadores = '4 - Agora é possível escolher qual navegador deseja utilizar no Verificador.'
    
    QMessageBox.information(self, 'Atualização 6.2', f'<font color="yellow"><h1>{mensagem_1}</h1></font><font color="white"><h3>{logs_erros}</h3><h3>{contas_vazias}</h3><h3>{contador}</h3><h3>{navegadores}</h3></font>')
    
