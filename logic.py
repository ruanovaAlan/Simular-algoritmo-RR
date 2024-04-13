""" El algoritmo a implementar para la cola de listos es el 
Round Robin con un quantum de 5 """

import time
import random
import copy
from tkinter import *
from tkinter import ttk

no_all_procesos = 0 #Variable para el número total de procesos
start_time = None #Variable para el reloj
tiempo_transcurrido_proceso = 0 #Variable para el tiempo transcurrido
clock_running = True #Variable para validar si el reloj esta corriendo
lote = [] #Array de lote
procesos_para_txt = [] #Array de procesos para el archivo de texto
lote_terminados = [] #Array de lote terminados
num_lote = 1 #Variable para el número de lote para los procesos terminados
end_lote = False #Variable para validar si el lote actual termino
cont_procesos = 0 #Variable para contar los procesos terminados
tiempo_en_espera = 0 #Variable para el tiempo en espera
tiempo_fin_proceso = None #Variable para el tiempo final del proceso
proceso_asignar_tiempo_inicio = 6 #Variable para asignar el tiempo de inicio a los procesos
program_running = True #Variable para validar si el programa esta corriendo
pause_time = None #Variable para el tiempo de pausa
procesos_en_espera = [] #Array de procesos en espera
nuevos_procesos = [] #Array de nuevos procesos
procesos_bloqueados = [] #Array de procesos bloqueados




#Función que actualiza el reloj
def update_clock(relojGlobal_label, root): 
    global start_time, program_running
    if start_time is None:
        start_time = time.time()
    if clock_running:
        elapsed_time = time.time() - start_time
        relojGlobal_label.config(text=f"Reloj: {int(elapsed_time)} segundos")
    root.after(1000, update_clock, relojGlobal_label, root)  # Actualiza el reloj cada 1000 milisegundos

#Funcion para detener el reloj
def stop_clock():
    global clock_running
    clock_running = False

#Funcion que retorna un numero aleatorio para el tiempo maximo estimado de un proceso
def getTiempoMaxEstimado():
    return random.randint(6, 12)

#Funcion para generar una operacion aleatoria
def getOperacion():
    operadores = ['+','-','*','/']
    operador = random.choice(operadores)
    datos = (random.randint(0,10), random.randint(0,10))
    while operador == '/' and datos[1] == 0:
        datos = (random.randint(0,10), random.randint(0,10))    
    operacion = f"{str(datos[0])} {operador} {str(datos[1])}"
    return operacion



#Funcion para generar lote de procesos con datos aleatorios
def crear_procesos(n):
    nombre_programadores = ['Alan', 'Juan', 'Jenny', 'Luis', 'Maria', 'Pedro', 'Sofia', 'Tom', 'Valeria', 'Ximena']
    num_programa = 1
    global lote, nuevos_procesos, procesos_para_txt
    #lote = []
    tiempo_llegada = 0
    for i in range(n):
        tiempo_maximo = getTiempoMaxEstimado()
        proceso = {
            'nombre': random.choice(nombre_programadores),
            'operacion': getOperacion(),
            'tiempo_maximo': tiempo_maximo,
            'tiempo_restante': tiempo_maximo,
            'numero_programa': num_programa,
            'interrumpido': False,
            'error': False,
            'tiempo_inicio': None,
            'tiempo_llegada': tiempo_llegada, #Hora en la que el proceso entra al sistema.
            'tiempo_finalizacion': 0, #Hora en la que el proceso termino.
            'tiempo_retorno': 0, #Tiempo total desde que el proceso llega hasta que termina.
            'tiempo_espera': 0, #Tiempo que el proceso ha estado esperando para usar el procesador.
            'tiempo_servicio': 0, #Tiempo que el proceso ha estado dentro del procesador.
            'tiempo_respuesta': 0, # Tiempo transcurrido desde que llega hasta que es atendido por primera vez.
            'tiempo_bloqueado': 3, #Tiempo que el proceso estara bloqueado
            'bloqueado': False, #Variable para validar si el proceso esta bloqueado
            'ha_sido_bloqueado': False #Variable para validar si el proceso ha sido bloqueado
        }
        
        procesos_para_txt.append(proceso)
        if num_programa < 6:
            lote.append(proceso)
        else:
            nuevos_procesos.append(proceso)
        
        num_programa += 1





#Funcion para escribir lote a un archivo
def procesos_a_txt():
    global procesos_para_txt
    if procesos_para_txt != []:
        with open('datos.txt', 'w') as file:
            # for i, lote in enumerate(lote, start=1):
            #     file.write(f'Lote {i}:\n')
            #     file.write('\n')
            for proceso in procesos_para_txt:
                file.write(f"{proceso['numero_programa']}. {proceso['nombre']}\n")
                file.write(f"{proceso['operacion']}\n")
                file.write(f"TME: {proceso['tiempo_maximo']}\n")
                file.write('\n')
                file.write('\n')
            file.write('\n')


def tabla_calculos_tiempos(calculos, file):
    file.write('\n')
    file.write('Calculos:\n')
    file.write('------------------------------------------------------------------------------------------------')
    file.write('\n: Proceso : T. Llegada : T. Espera : T. Respuesta : T. Servicio : T. Retorno : T. Finalizacion :\n')
    file.write('------------------------------------------------------------------------------------------------\n')
    
    for proceso in calculos:
        #tabla = f": {proceso['numero_programa']}{" "*(8-len(str(proceso['numero_programa'])))}: {proceso['tiempo_llegada']}{" "*(11-len(str(proceso['tiempo_llegada'])))}: {proceso['tiempo_espera']}{" "*(10-len(str(proceso['tiempo_espera'])))}: {proceso['tiempo_respuesta']}{" "*(13-len(str(proceso['tiempo_respuesta'])))}: {proceso['tiempo_servicio']}{" "*(12-len(str(proceso['tiempo_servicio'])))}: {proceso['tiempo_retorno']}{" "*(11-len(str(proceso['tiempo_retorno'])))}: {proceso['tiempo_finalizacion']}{" "*(16-len(str(proceso['tiempo_finalizacion'])))}:"
        tabla = ": {:<8}: {:<11}: {:<10}: {:<13}: {:<12}: {:<11}: {:<16}:"
        tabla = tabla.format(proceso['numero_programa'], proceso['tiempo_llegada'], proceso['tiempo_espera'], proceso['tiempo_respuesta'], proceso['tiempo_servicio'], proceso['tiempo_retorno'], proceso['tiempo_finalizacion'])

        file.write(f"{tabla}\n")

#Funcion para escribir resultados a un archivo
def resultados_a_txt():
    global lote_terminados 
    calculos = []
    with open('Resultados.txt', 'w') as file:            
        for proceso in lote_terminados: #Muestra los procesos terminados
            # if type(proceso) == str:
            #     file.write(f"{proceso}\n\n")
            # else:
            calculos.append(proceso)
            if proceso['error']:
                file.write(f"{proceso['numero_programa']}. {proceso['nombre']}\n{proceso['operacion']}\n\n")
            else:
                resultado = round(eval(proceso['operacion']), 4)
                file.write(f"{proceso['numero_programa']}. {proceso['nombre']}\n{proceso['operacion']} = {resultado}\n\n")
        tabla_calculos_tiempos(calculos, file)


def en_espera(lote, procesosEnEspera_text):
    global end_lote, tiempo_en_espera, procesos_en_espera, tiempo_fin_proceso
    all_process = lote
        
    procesos_en_espera = all_process[1:5]  # Toma los procesos en espera
    tiempo_en_espera += 1

    procesosEnEspera_text.delete('1.0', END)  
    for proceso in procesos_en_espera:
        if proceso['interrumpido']:  #Si el proceso fue interrumpido
            procesosEnEspera_text.insert(END, f"{proceso['numero_programa']}. {proceso['nombre']}\n{proceso['operacion']}\nTME: {proceso['tiempo_maximo']}\nTiempo restante: {round(proceso['tiempo_restante'])}\n\n")
        else:
            procesosEnEspera_text.insert(END, f"{proceso['numero_programa']}. {proceso['nombre']}\n{proceso['operacion']}\nTME: {proceso['tiempo_maximo']}\n\n")
        
        proceso['tiempo_espera'] = tiempo_en_espera - proceso['tiempo_llegada'] # Asigna el tiempo de espera


def en_ejecucion(lote, ejecucion_text, bloqueado_text, tiempo_inicio_proceso):
    global tiempo_transcurrido_proceso, procesos_bloqueados 
    
    all_process = lote  # Toma el primer lote
    procesoEnEjecucion = all_process[0]  # Toma el primer proceso en espera
    
    if tiempo_inicio_proceso is None:  # Si es la primera vez que se llama a la función para este proceso
        tiempo_inicio_proceso = time.time() - start_time
        tiempo_transcurrido_proceso = 0
    
    if procesoEnEjecucion['tiempo_inicio'] is None:
        procesoEnEjecucion['tiempo_inicio'] = round(time.time() - start_time)
        procesoEnEjecucion['tiempo_respuesta'] = procesoEnEjecucion['tiempo_inicio']  # Asigna el tiempo de respuesta (tiempo transcurrido desde que llega hasta que es atendido por primera vez
        
    tiempo_transcurrido_proceso += 1
    if tiempo_transcurrido_proceso == 5:
        interrumpir_por_rr_q5()
        
    tiempo_transcurrido = tiempo_transcurrido_proceso
    
    procesoEnEjecucion['tiempo_servicio'] += 1  # Asigna el tiempo de servicio
    
    if procesoEnEjecucion['error']:  # If the process has an error
        tiempo_restante = 0
    elif procesoEnEjecucion['interrumpido'] or procesoEnEjecucion['ha_sido_bloqueado']:  # If the process was interrupted
        tiempo_restante = procesoEnEjecucion['tiempo_restante'] - tiempo_transcurrido
    else:
        tiempo_restante = procesoEnEjecucion['tiempo_maximo'] - tiempo_transcurrido
    
    ejecucion_text.delete('1.0', END) 
    
    if all_process: #Muestra el proceso en ejecución
        if procesoEnEjecucion['interrumpido'] or procesoEnEjecucion['ha_sido_bloqueado']:
            ejecucion_text.insert(END, f"{procesoEnEjecucion['numero_programa']}. {procesoEnEjecucion['nombre']}\n{procesoEnEjecucion['operacion']}\nTiempo ejecutado:{procesoEnEjecucion['tiempo_maximo'] - procesoEnEjecucion['tiempo_restante']}\nTME: {round(tiempo_restante) if tiempo_restante > 0 else 0}")
        else:
            ejecucion_text.insert(END, f"{procesoEnEjecucion['numero_programa']}. {procesoEnEjecucion['nombre']}\n{procesoEnEjecucion['operacion']}\nTME: {round(tiempo_restante) if tiempo_restante > 0 else 0}")
            if procesos_bloqueados:
                gestionar_procesos_bloqueados(bloqueado_text)
    return tiempo_restante, tiempo_inicio_proceso


def terminados(lote, terminados_text, procesos_terminados, tiempo_restante, tiempo_inicio_proceso, ejecucion_text, obtenerResultadosBtn):
    all_process = lote
    global cont_procesos, lote_terminados, end_lote, tiempo_fin_proceso, nuevos_procesos, procesos_en_espera
    
    if tiempo_restante <= 0: 
        proceso_terminado = all_process.pop(0)        
        procesos_terminados.append(proceso_terminado)  # Elimina el proceso de la lista de procesos en espera y lo añade a la lista de procesos terminados
                
        procesos_terminados[-1]['tiempo_finalizacion'] = round(time.time() - start_time + 1)   # Asigna el tiempo de finalización
        procesos_terminados[-1]['tiempo_retorno'] = procesos_terminados[-1]['tiempo_finalizacion'] - procesos_terminados[-1]['tiempo_llegada'] # Calcula el tiempo de retorno
        tiempo_fin_proceso = procesos_terminados[-1]['tiempo_finalizacion']
        if nuevos_procesos and tiempo_fin_proceso is not None:
            no_arrive_tme_process = nuevos_procesos.pop(0)
            no_arrive_tme_process['tiempo_llegada'] = tiempo_fin_proceso
            lote.append(no_arrive_tme_process)
        # proceso_asignar_tiempo_inicio += 1

        end_lote = False
        #cont_procesos += 1
        tiempo_inicio_proceso = None  # Resetea el tiempo de inicio para el próximo proceso
        if not all_process:  # Si el lote actual está vacío
            # lote.pop(0)  # Elimina el lote de la lista de lote
            ejecucion_text.delete('1.0', END)
            
    terminados_text.delete('1.0', END)
    
    for proceso in procesos_terminados: #Muestra los procesos terminados
        if type(proceso) == str:
            terminados_text.insert(END, f"{proceso}\n\n")
        else:
            if proceso['error']:
                terminados_text.insert(END, f"{proceso['numero_programa']}. {proceso['nombre']}\n{proceso['operacion']}\n\n")
            else:
                resultado = round(eval(proceso['operacion']), 4)
                terminados_text.insert(END, f"{proceso['numero_programa']}. {proceso['nombre']}\n{proceso['operacion']} = {resultado}\n\n")
    
    # Si todos los lote están vacíos, habilita el botón obtenerResultadosBtn
    if not lote:
        lote_terminados = copy.deepcopy(procesos_terminados)
        for proceso in lote_terminados:
            if proceso['tiempo_espera'] < (proceso['tiempo_respuesta'] - proceso['tiempo_llegada']):
                proceso['tiempo_espera'] += 1
        obtenerResultadosBtn.config(state='normal')
        stop_clock() #Detiene el reloj si no hay más procesos
    
    return tiempo_inicio_proceso


def ejecutar_proceso(lote, noLotesPendientes_label, ejecucion_text, root, procesosEnEspera_text, terminados_text, obtenerResultadosBtn, bloqueado_text, procesos_terminados=[], tiempo_inicio_proceso=None):
    global nuevos_procesos
    if program_running and lote:  
        #Funcion para mostrar el proceso en ejecución
        tiempo_restante, tiempo_inicio_proceso = en_ejecucion(lote, ejecucion_text, bloqueado_text, tiempo_inicio_proceso)
        en_espera(lote, procesosEnEspera_text) #Funcion para mostrar los procesos en espera
        #Funcion para mostrar los procesos terminados
        tiempo_inicio_proceso = terminados(lote, terminados_text, procesos_terminados, tiempo_restante, tiempo_inicio_proceso, ejecucion_text, obtenerResultadosBtn)
        total_procesos = len(nuevos_procesos)
        cantidad_procesos = total_procesos
        # Actualiza el número de lote pendientes
        noLotesPendientes_label.config(text=f"# De procesos pendientes: {cantidad_procesos}")
    
    # Llama a la función de nuevo después de 1 segundo
    root.after(1000, ejecutar_proceso, lote, noLotesPendientes_label, ejecucion_text, root, procesosEnEspera_text, terminados_text, obtenerResultadosBtn, bloqueado_text, procesos_terminados, tiempo_inicio_proceso)

#Funcion para generar procesos y ejecutarlos
def generar_procesos(noProcesos_entry, ejecucion_text, noLotesPendientes_label, root, procesosEnEspera_text, terminados_text, obtenerResultadosBtn, relojGlobal_label, bloqueado_text):
    global lote, no_all_procesos
    n = int(noProcesos_entry.get())
    no_all_procesos = n
    crear_procesos(n)
    procesos_a_txt()
    update_clock(relojGlobal_label, root)  # Inicia el reloj 
    ejecutar_proceso(lote, noLotesPendientes_label, ejecucion_text, root, procesosEnEspera_text, terminados_text, obtenerResultadosBtn, bloqueado_text)  # Inicia el "bucle"

# Función para interrumpir el proceso actual
def interrumpir_proceso():
    global tiempo_transcurrido_proceso, end_lote, procesos_bloqueados 
    if lote:  # Si hay lote
        all_process = lote  # Toma el primer lote
        if all_process and end_lote == False:  # Si hay procesos en el lote
            proceso = all_process.pop(0)  # Toma y elimina el primer proceso
            proceso['tiempo_restante'] -= tiempo_transcurrido_proceso  # Actualiza el tiempo restante
            proceso['bloqueado'] = True  # Marca el proceso como bloqueado
            proceso['ha_sido_bloqueado'] = True  # Marca el proceso como que por lo menos ha sido bloqueado 1 vez
            procesos_bloqueados.append(proceso)  # Mueve el proceso a la lista de procesos bloqueados
            tiempo_transcurrido_proceso = 0  # Resetea el tiempo transcurrido

# Función para gestionar los procesos bloqueados
def gestionar_procesos_bloqueados(bloqueado_text):
    global procesos_bloqueados, lote
    procesos_a_reintegrar = []  # Lista para almacenar los procesos que deben reintegrarse al lote actual

    for proceso in list(procesos_bloqueados):  # Itera sobre una copia de la lista
        proceso['tiempo_bloqueado'] -= 1  # Decrementa el tiempo de bloqueo
        if proceso['tiempo_bloqueado'] <= 0:  # Si el tiempo de bloqueo ha terminado
            proceso['bloqueado'] = False  # Marca el proceso como no bloqueado
            proceso['tiempo_bloqueado'] = 3  # Restablece el tiempo de bloqueo predeterminado
            procesos_a_reintegrar.append(proceso)  # Agrega el proceso a la lista de procesos a reintegrar
            procesos_bloqueados.remove(proceso)  # Elimina el proceso de la lista de procesos bloqueados
            
    # Reintegra los procesos bloqueados al lote actual
    for proceso in procesos_a_reintegrar:
        lote.append(proceso)  # Agrega los procesos a reintegrar al final del lote actual
        
    # Actualiza el widget bloqueado_text para reflejar los cambios
    bloqueado_text.delete('1.0', END)
    for proceso in procesos_bloqueados:
        bloqueado_text.insert(END, f"{proceso['numero_programa']}. {proceso['nombre']}\n{proceso['operacion']}\nTB: {round(proceso['tiempo_bloqueado'])}\n")

# Función para terminar el proceso actual
def terminar_proceso():
    global tiempo_transcurrido_proceso
    if lote:  # Si hay lote
        all_process = lote  # Toma el primer lote
        if all_process:  # Si hay procesos en el lote
            proceso = all_process[0]  # Toma el primer proceso
            proceso['error'] = True  # Marca el proceso como interrumpido
            proceso['operacion'] += ' = ERROR'  # Asigna ERROR a la operación
            tiempo_transcurrido_proceso = 0  # Resetea el tiempo transcurrido

# Función para pausar el programa
def pausar_programa():
    global program_running, clock_running, pause_time
    program_running = False
    clock_running = False
    pause_time = time.time()  # Registra el momento en que se pausa el reloj

def continuar_programa():
    global program_running, clock_running, start_time, pause_time
    program_running = True
    clock_running = True
    if pause_time is not None:
        start_time += time.time() - pause_time  # Ajusta start_time por la cantidad de tiempo que el reloj estuvo en pausa
        pause_time = None

def interrumpir_por_rr_q5():
    global tiempo_transcurrido_proceso, end_lote
    if lote:  # Si hay lote
        all_process = lote  # Toma el primer lote
        if all_process and end_lote == False:  # Si hay procesos en el lote
            proceso = all_process.pop(0)  # Toma y elimina el primer proceso
            proceso['tiempo_restante'] -= tiempo_transcurrido_proceso  # Actualiza el tiempo restante
            proceso['interrumpido'] = True  # Marca el proceso como interrumpido
            all_process.append(proceso)  # Mueve el proceso al final de la cola de espera
            tiempo_transcurrido_proceso = 0  # Resetea el tiempo transcurrido
