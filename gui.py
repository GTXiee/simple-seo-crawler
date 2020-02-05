import PySimpleGUI as sg
from process import process_crawl, validate_start_url

sg.theme('DarkAmber')
# Inside the window
layout = [
    [sg.Text('Start URL:', key='start-url'), sg.InputText(tooltip='https://example.com')],
    [sg.Text('Output:'), sg.InputText(), sg.FolderBrowse()],
    [sg.Button('Start')]
]

# Create the window
window = sg.Window('SEO Spider', layout)

# Event Loop
while True:
    event, values = window.read()
    start_url = values[0]
    output_location = values[1]
    if event == 'Start':
        if validate_start_url(start_url):
            process_crawl(start_url, output_location)
        else:  # Throws error if http protocol not included
            sg.Popup('Please include the http protocol', title='Error')

