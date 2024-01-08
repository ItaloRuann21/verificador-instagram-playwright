import PySimpleGUI as sg
from playwright.sync_api import sync_playwright

from main import run

# Definindo o tema
sg.theme('Python')


layout = [
    [sg.Text('Digite os perfis do Instagram')],
    [sg.Multiline(size=(50, 12), key='perfis')],
    [sg.Text('Você quer ver acontecendo?')],
    [sg.Combo(['Sim', 'Não'], default_value='Sim', size=(50, 1), key='modo', button_background_color='#1B1B1E', visible=True)],
    [sg.Button('Iniciar', size=(46, 2), visible=True)],
]

window = sg.Window('Projeto Verificador XCTRL', layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break

    if event == 'Iniciar':

        perfis = values['perfis']
        modo = values['modo']

        with sync_playwright() as playwright:
            run(playwright, modo, perfis)


window.close()
