#!/usr/bin/env python

import pyxhook
import time
import subprocess
import sys


#Define a function called at every keypress
def kbevent_down(event):
    global nome_terminale
    if event.Ascii == tasto_ascii:
        subprocess.call(['amixer', '-q', 'set', 'Capture', 'cap'])
    elif event.Ascii == 113 and event.WindowName == nome_terminale:
        global running
        running = False


def kbevent_up(event):
    if event.Ascii == tasto_ascii:
        subprocess.call(['amixer', '-q', 'set', 'Capture', 'nocap'])


id_linea = subprocess.check_output(['xprop', '-root', '_NET_ACTIVE_WINDOW']).strip()
id_parti = id_linea.split()
id = id_parti[-1]
nome_linea = subprocess.check_output(['xprop', '-id', id, 'WM_NAME']).strip()
nome_parti = nome_linea.split()
nome_parti_utili = nome_parti[2:]
nome_parti_utili_unite = ' '.join(nome_parti_utili)
nome_terminale = nome_parti_utili_unite[1:-1]
#To make sure the Capture interface is up
subprocess.call(['amixer', '-q', 'set', 'Capture', 'cap'])
#Set the push-to-talk button
tasto = raw_input('Seleziona il tasto per spegnere/accendere il microfono (NO Q, ctrl, alt, shift, cose strane)\n')
tasto_ascii = ord(tasto)
print('Settaggio completato, lo script e\' ora in funzione\n'
      'Il microfono e\' disattivato, tenere premuto \"' + tasto.upper() + '\" per attivarlo\n'
      'Per disattivare lo scrip premere \"Q\" in questa finestra. Fly safe!')
subprocess.call(['amixer', '-q', 'set', 'Capture', 'nocap'])
subprocess.call(['notify-send', '-t', '1000', 'mic_toggle e\' ora in funzione'])
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
subprocess.call(['amixer', '-q', 'set', 'Capture', 'cap'])
print('\nScript terminato. Grazie per aver utilizzato python_mic_toggle!')
subprocess.call(['notify-send', '-t', '1000', 'mic_toggle e\' stato disattivato'])
#Close the listener when we are done
hookman.cancel()
