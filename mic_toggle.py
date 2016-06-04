#!/usr/bin/env python

import pyxhook
import time
import subprocess
import sys




#Define a function called at every keypress
""" First try, discarded 'cause checking againt a variable doesn't
    work if an external software changes mic status 
"""
#mic_attivo = True
#def kbevent(event):
#    global mic_attivo
#    notifica_disattivazione = 'notify-send -u normal -t 1 "microfono disattivato"'
#    notifica_attivazione = 'notify-send -u normal -t 1 "microfono attivato"'
#    if  event.Ascii == tasto and mic_attivo:
#        subprocess.call('amixer set Capture toggle', shell=True)
#        subprocess.call(notifica_disattivazione, shell=True)
#        mic_attivo = False
#    elif event.Ascii == tasto and not mic_attivo:
#        subprocess.call('amixer set Capture toggle', shell=True)
#        subprocess.call(notifica_attivazione, shell=True)
#        mic_attivo = True

def kbevent(event):
    notifica_disattivazione = 'notify-send -u normal -t 1 "microfono disattivato"'
    notifica_attivazione = 'notify-send -u normal -t 1 "microfono attivato"'
    if event.Ascii == tasto_ascii:
        subprocess.call('amixer set Capture toggle', shell=True)
        check_mic_status = subprocess.check_output(verifica_stato, shell=True).strip().decode('ascii')
        if check_mic_status == '[on]':
            subprocess.call(notifica_attivazione, shell=True)
        else:
            subprocess.call(notifica_disattivazione, shell=True)


lista_output = ['amixer get Capture | grep "\[on\]" | head -1 | cut -d " " -f 8', 'amixer get Capture | grep "\[on\]" | head -1 | cut -d " " -f 9', 'amixer get Capture | grep "\[on\]" | head -1 | cut -d " " -f 10']

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

#Trovo Ascii del tasto utilizzato per mutare il microfono
tasto = raw_input('Ora seleziona il tasto per spegnere/accendere il microfono (NO ctrl, alt, shift, cose strane)\n')
tasto_ascii = ord(tasto)

print('Settaggio completato, lo script e\' ora in funzione')
#Create hookmanager
hookman = pyxhook.HookManager()
#Define our callback to fire when a key is pressed down
hookman.KeyDown = kbevent
#Hook the keyboard
hookman.HookKeyboard()
#Start our listener
hookman.start()
    
#Let's start this thing
while True:
    time.sleep(0.1)

#Close the listener when we are done
hookman.cancel()
