import pyautogui
import pyperclip
import webbrowser
from time import sleep

def enviar_email():
    # Abre o navegador com o link do Google Forms
    webbrowser.open('https://mail.google.com/mail/u/0/#inbox')
    sleep(10)  # Aguarda o carregamento da página

    # Preenche o formulário
    pyautogui.click(x=500, y=500)  # Clica no campo de texto
    pyperclip.copy('Seu Nome')  # Copia o nome para a área de transferência
    pyautogui.hotkey('ctrl', 'v')  # Cola o nome no campo de texto
    pyautogui.press('tab')  # Move para o próximo campo

    pyperclip.copy('Seu Email')  # Copia o email para a área de transferência
    pyautogui.hotkey('ctrl', 'v')  # Cola o email no campo de texto
    pyautogui.press('tab')  # Move para o próximo campo

    pyperclip.copy('Sua Mensagem')  # Copia a mensagem para a área de transferência
    pyautogui.hotkey('ctrl', 'v')  # Cola a mensagem no campo de texto

    sleep(2)  # Aguarda um pouco antes de enviar

    pyautogui.press('enter')  # Envia o formulário