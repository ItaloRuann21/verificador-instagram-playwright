from PyQt5.QtWidgets import QMessageBox


def mensagem_atualização(self):
    # Exibe uma janela popup com o tempo restante em dias
    QMessageBox.information(self, 'Atualização 6.1', f'<font color="yellow"><center><h1>Atualizações no Verificador<br>6.0 para 6.1!</h1></center></font><br><font color="white"><h2>O que mudou:</h2><p>1 - Agora as verificações estão mais rápidas e eficientes!</p><p>2 - Se algum perfil sofrer restrição de página, entra no segundo perfil da lista sucessivamente.</p><p>3 - Se sua internet estiver lenta e não conseguir verificar alguma conta, será salva em um arquivo txt todas as contas que ocorreram erros na verificação.</p><p>4 - Agora, após fazer o login, suas credenciais já estarão salvas automaticamente.</p><p>5 - Removemos o terminal. As quantidades de perfis serão atualizados em tempo real na interface!</font>')
    
