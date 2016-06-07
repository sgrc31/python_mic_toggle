#!/usr/bin/env python

import pyxhook
import time
import subprocess
import sys


#Define a function called at every keypress
def kbevent_down(event):
    if event.Ascii == tasto_ascii:
        subprocess.call('amixer -q set Capture cap', shell=True)
    elif event.Ascii == 113 and event.WindowName[-7:] == 'toggler':
        global running
        running = False

        
def kbevent_up(event):
    if event.Ascii == tasto_ascii:
        subprocess.call('amixer -q set Capture nocap', shell=True)


#Pre flight checks
lista_output = ['amixer get Capture | grep "\[on\]" | head -1 | cut -d " " -f 7',
                'amixer get Capture | grep "\[on\]" | head -1 | cut -d " " -f 8',
                'amixer get Capture | grep "\[on\]" | head -1 | cut -d " " -f 9']

#To make sure the Capture interface is up
subprocess.call('amixer -q set Capture cap', shell=True)

#Select right amixer command
avanzamento = 0
for papabile in lista_output:
    output = subprocess.check_output(papabile, shell=True).strip().decode('ascii')
    print(str(avanzamento) + ' > ' + output)
    avanzamento += 1

verifica_stato = ''

while verifica_stato == '':
    output_selezionato = raw_input('Seleziona il numero di riga dove e\' comparso \"[on]\"\n')
    if output_selezionato == '0':
        verifica_stato = lista_output[0]
    elif output_selezionato == '1':
        verifica_stato = lista_output[1]
    elif output_selezionato == '2':
        verifica_stato = lista_output[2]
    else:
        print('selezione non valida, riprova')

#Set the push-to-talk button
tasto = raw_input('Ora seleziona il tasto per spegnere/accendere il microfono (NO Q, ctrl, alt, shift, cose strane)\n')
tasto_ascii = ord(tasto)

print('Settaggio completato, lo script e\' ora in funzione\n'
      'Il microfono e\' disattivato, tenere premuto \"' + tasto.upper() + '\" per attivarlo\n'
      'Per disattivare lo scrip premere \"Q\" in questa finestra. Fly safe!')
subprocess.call('amixer -q set Capture nocap', shell=True)

#Create hookmanager
hookman = pyxhook.HookManager()
#Define our callback to fire when a key is pressed down/up
hookman.KeyDown = kbevent_down
hookman.KeyUp = kbevent_up
#Hook the keyboard
hookman.HookKeyboard()
#Start our listener
hookman.start()
    
#Let's start this thing
running = True
while running:
    time.sleep(0.1)

#Put the Capture interface back up
subprocess.call('amixer -q set Capture cap', shell=True)
print('Grazie per aver utilizzato python_mic_toggle!')

#Close the listener when we are done
hookman.cancel()
