import sys
import socket
from time import sleep, time
from Prueba2 import Ui_MainWindow
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QTimer
from PySide2 import QtCore
import select
import time
import threading

class QtWindow(QMainWindow):
    enviar=False
    consulta=True
    PC ='Nada seleccionado'
    usuario ='Nada seleccionado'
    vidas1 = 3
    vidas2 = 3
    conectados=2
    respuesta_jugador1=False
    respuesta_jugador2=False
    seleccion_jugador2='Nada'

    # #Timer
    # timer = QTimer()
    # timer.setInterval(10) 
    # timer.start()

    s=socket.socket()
    server_host='192.168.1.79'
    server_port=8081
    s.connect((server_host,server_port))
    nombre='Jugador2'
    # message='hola servidor'
    counter=0
    # s.send(message.encode('utf-8'))
    msg='nada'
    
    
    def hilo(self,a):
        while True:
            print(a)
            time.sleep(1)

    def reader(server):
        msg=server.recv(20).decode('utf-8')
        print(msg)

    def __init__(self):
        super(QtWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        
        #Push buttons 
        self.ui.pushButton_Enviar.clicked.connect(self.boton_enviar_presionado)
        self.ui.pushButton_NuevaPartida.clicked.connect(self.boton_nueva_partida_presionado)

        #Boton abandonar, auxiliar por el momento
        self.ui.pushButton_Abandonar.clicked.connect(self.boton_abandonar_partida_presionado)
        
        #Actualizar selección de usuario
        self.ui.radioButton_piedra.toggled.connect(self.user_choice)
        self.ui.radioButton_papel.toggled.connect(self.user_choice)
        self.ui.radioButton_tijeras.toggled.connect(self.user_choice)
        
        #Recoge mensajes
        # self.timer.timeout.connect(self.lee_mensaje)
        # self.timer.timeout.connect(print('timeout'))

        print('antes th')
        # t=threading.Thread(target=self.hilo,args=("hola",))
        t=threading.Thread(target=self.lee_mensaje,args=("hola",))
        t.start()
        print('despues th')



        

    def lee_mensaje(self,a):
        #Lee mensaje
        print('Entra a funcion lee_mensaje')
        
        # buffer = select.select([self.s],[],[],0.1)
        while True:
        # if buffer[0]:
            self.msg=self.s.recv(20).decode('utf-8')
            print(self.msg)
            if self.msg=='Jugador2Desconectado':
                self.ui.stackedWidget_mensaje_jugador2.setCurrentWidget(self.ui.page_jugador_desconectado)
                print("Jugador 2 Desconectado")
            if self.msg=='2JugadoresConectados':
                self.ui.stackedWidget_mensaje_jugador2.setCurrentWidget(self.ui.page_esperando_respuesta)
                print("Jugador 2 conectado!")
                self.conectados=2
            if self.msg=='Piedra':
                print("Jugador ha respondido piedra!")
                self.ui.stackedWidget_mensaje_jugador2.setCurrentWidget(self.ui.page_jugador_ha_respondido)
                self.respuesta_jugador2=True
                self.seleccion_jugador2='Piedra'
            if self.msg=='Papel':
                self.respuesta_jugador2=True
                self.ui.stackedWidget_mensaje_jugador2.setCurrentWidget(self.ui.page_jugador_ha_respondido)
                print("Jugador ha respondido papel!")
                self.seleccion_jugador2='Papel'
            if self.msg=='Tijeras':
                self.respuesta_jugador2=True
                self.ui.stackedWidget_mensaje_jugador2.setCurrentWidget(self.ui.page_jugador_ha_respondido)
                print("Jugador ha respondido tijeras!")
                self.seleccion_jugador2='Tijeras'

            #Actualiza resultado
            if self.respuesta_jugador1 and self.respuesta_jugador2:
                self.resultado()

            #Reinicia timer
            # self.timer.start()


    def resultado(self):
        #Borra manos laterales jugador 2     
        self.ui.stackedWidget_piedra2.setCurrentWidget(self.ui.page_SPiedra_2)
        self.ui.stackedWidget_tijeras2.setCurrentWidget(self.ui.page_STijeras_2)
        #Actualiza la mano central del jugador 2
        if self.seleccion_jugador2 == 'Piedra': 
            self.ui.stackedWidget_p_papel_t2.setCurrentWidget(self.ui.page_MPiedra_2)
        elif self.PC == 'Tijeras':
            self.ui.stackedWidget_p_papel_t2.setCurrentWidget(self.ui.page_MTijeras_2)
        #Auxiliares
        print(f'Usuario: {self.usuario}')
        print(f'Jugador 2: {self.seleccion_jugador2}')

        #Resultado
        if self.usuario == 'Piedra':
            if self.seleccion_jugador2 == 'Papel':
                self.vidas1-=1
            elif self.seleccion_jugador2 == 'Tijeras':
                self.vidas2-=1
        elif self.usuario == 'Papel':
            if self.seleccion_jugador2 == 'Piedra':
                self.vidas2-=1
            elif self.seleccion_jugador2 == 'Tijeras':
                self.vidas1-=1
        elif self.usuario == 'Tijera':
            if self.seleccion_jugador2 == 'Papel':
                self.vidas2-=1
            elif self.seleccion_jugador2 == 'Piedra':
                self.vidas1-=1
        #Vidas (corazones) del Jugador 1
        if self.vidas1 < 3:
            self.ui.stackedWidget_corazon13.setCurrentWidget(self.ui.page_SC_1_3)   
        if self.vidas1 < 2:
            self.ui.stackedWidget_corazon12.setCurrentWidget(self.ui.page_SC_1_2) 
        if self.vidas1 < 1:
            self.ui.stackedWidget_corazon11.setCurrentWidget(self.ui.page_SC_1_1)
            self.ui.stackedWidget_resultado.setCurrentWidget(self.ui.page_perdiste)
            #Termina la partida
            self.s.send('Abandonar'.encode('utf-8'))
            self.s.close()
            self.consulta=False
            self.ui.stackedWidget_partida_en_curso.setCurrentWidget(self.ui.page_STexto_pec)
            #Restablecer corazones jugador 1
            self.ui.stackedWidget_corazon11.setCurrentWidget(self.ui.page_CC_1_1)
            self.ui.stackedWidget_corazon12.setCurrentWidget(self.ui.page_CC_1_2)
            self.ui.stackedWidget_corazon13.setCurrentWidget(self.ui.page_CC_1_3)
            #Restablecer corazones jugador 2
            self.ui.stackedWidget_corazon21.setCurrentWidget(self.ui.page_CC_2_1)
            self.ui.stackedWidget_corazon22.setCurrentWidget(self.ui.page_CC_2_2)
            self.ui.stackedWidget_corazon23.setCurrentWidget(self.ui.page_CC_2_3)
            self.ui.stackedWidget_KO.setCurrentWidget(self.ui.page_CKO)
            self.vidas1=3
            self.vidas2=3
        #Vidas (corazones) del Jugador 2
        if self.vidas2 < 3:
            self.ui.stackedWidget_corazon23.setCurrentWidget(self.ui.page_SC_2_3)   
        if self.vidas2 < 2:
            self.ui.stackedWidget_corazon22.setCurrentWidget(self.ui.page_SC_2_2) 
        if self.vidas2 < 1:
            self.ui.stackedWidget_corazon21.setCurrentWidget(self.ui.page_SC_2_1)
            self.ui.stackedWidget_resultado.setCurrentWidget(self.ui.page_ganaste)
            #Termina la partida
            self.s.send('Abandonar'.encode('utf-8'))
            self.s.close()
            self.consulta=False
            self.ui.stackedWidget_partida_en_curso.setCurrentWidget(self.ui.page_STexto_pec)
            #Restablecer corazones jugador 1
            self.ui.stackedWidget_corazon11.setCurrentWidget(self.ui.page_CC_1_1)
            self.ui.stackedWidget_corazon12.setCurrentWidget(self.ui.page_CC_1_2)
            self.ui.stackedWidget_corazon13.setCurrentWidget(self.ui.page_CC_1_3)
            #Restablecer corazones jugador 2
            self.ui.stackedWidget_corazon21.setCurrentWidget(self.ui.page_CC_2_1)
            self.ui.stackedWidget_corazon22.setCurrentWidget(self.ui.page_CC_2_2)
            self.ui.stackedWidget_corazon23.setCurrentWidget(self.ui.page_CC_2_3)
            self.ui.stackedWidget_KO.setCurrentWidget(self.ui.page_CKO)
            self.vidas1=3
            self.vidas2=3


    #Botón enviar
    def boton_enviar_presionado(self):
        print('Boton enviar presionado')
        #Si hay una partida en curso y se presiona enviar..
        if self.consulta and self.conectados==2:
            self.respuesta_jugador1=True
            #Borra manos laterales jugador 1
            self.ui.stackedWidget_piedra1.setCurrentWidget(self.ui.page_SPiedra_1)
            self.ui.stackedWidget_tijeras1.setCurrentWidget(self.ui.page_STijeras1)
            #Actualiza la mano central del usuario por la selección
            self.s.send(self.usuario.encode('utf-8'))
            if self.usuario == 'Piedra':
                self.ui.stackedWidget_p_papel_t1.setCurrentWidget(self.ui.page_MPiedra_1)
            elif self.usuario == 'Tijeras':
                self.ui.stackedWidget_p_papel_t1.setCurrentWidget(self.ui.page_MTijeras_1)
            
                

    def boton_nueva_partida_presionado(self):
        print('Boton iniciar partida presionado')
        #Si no hay una partida en curso, la inicia
        if not self.consulta:
            
            #Borrar mensaje de KO
            self.ui.stackedWidget_KO.setCurrentWidget(self.ui.page_SKO)
            #Borrar el resultado
            self.ui.stackedWidget_resultado.setCurrentWidget(self.ui.page_sin_resultado)
            print(f'Partida iniciada wuu')
            #Partida en curso
            self.ui.stackedWidget_partida_en_curso.setCurrentWidget(self.ui.page_CTexto_pec)
            #Esperando a jugador 2!
            self.ui.stackedWidget_mensaje_jugador2.setCurrentWidget(self.ui.page_jugador_desconectado)
            #Indicador de partida activa encendido
            self.consulta=True
            #Envía señal
            self.s.send('Jugador conectado'.encode('utf-8'))
            #Recibe condición del servidor
            
            


    def boton_abandonar_partida_presionado(self):
        print('Boton abandonar partida presionado')
        self.s.send('Abandonar'.encode('utf-8'))
        self.s.close()
        self.consulta=False
        #Restablecer corazones jugador 1
        self.ui.stackedWidget_corazon11.setCurrentWidget(self.ui.page_CC_1_1)
        self.ui.stackedWidget_corazon12.setCurrentWidget(self.ui.page_CC_1_2)
        self.ui.stackedWidget_corazon13.setCurrentWidget(self.ui.page_CC_1_3)
        #Restablecer corazones jugador 2
        self.ui.stackedWidget_corazon21.setCurrentWidget(self.ui.page_CC_2_1)
        self.ui.stackedWidget_corazon22.setCurrentWidget(self.ui.page_CC_2_2)
        self.ui.stackedWidget_corazon23.setCurrentWidget(self.ui.page_CC_2_3)
        #Restablecer manos jugador 1
        self.ui.stackedWidget_piedra1.setCurrentWidget(self.ui.page_CPiedra_1)
        self.ui.stackedWidget_p_papel_t1.setCurrentWidget(self.ui.page_MPapel_1)
        self.ui.stackedWidget_tijeras1.setCurrentWidget(self.ui.page_CTijeras_1)
        #Restablecer manos jugador 2
        self.ui.stackedWidget_piedra2.setCurrentWidget(self.ui.page_CPiedra_2)
        self.ui.stackedWidget_p_papel_t2.setCurrentWidget(self.ui.page_MPapel_2)
        self.ui.stackedWidget_tijeras2.setCurrentWidget(self.ui.page_CTijeras_2)
        #Resetea vidas
        self.vidas1=3
        self.vidas2=3

        self.ui.stackedWidget_KO.setCurrentWidget(self.ui.page_SKO)
        self.ui.stackedWidget_resultado.setCurrentWidget(self.ui.page_sin_resultado)
        self.ui.stackedWidget_partida_en_curso.setCurrentWidget(self.ui.page_STexto_pec)

    def user_choice(self):
        self.ui.stackedWidget_piedra1.setCurrentWidget(self.ui.page_CPiedra_1)
        self.ui.stackedWidget_p_papel_t1.setCurrentWidget(self.ui.page_MPapel_1)
        self.ui.stackedWidget_tijeras1.setCurrentWidget(self.ui.page_CTijeras_1)
        self.ui.stackedWidget_piedra2.setCurrentWidget(self.ui.page_CPiedra_2)
        self.ui.stackedWidget_p_papel_t2.setCurrentWidget(self.ui.page_MPapel_2)
        self.ui.stackedWidget_tijeras2.setCurrentWidget(self.ui.page_CTijeras_2)
        if self.ui.radioButton_piedra.isChecked():
            self.usuario ='Piedra'
        if self.ui.radioButton_papel.isChecked():
            self.usuario ='Papel'
        if self.ui.radioButton_tijeras.isChecked():
            self.usuario ='Tijeras'





if __name__ == '__main__':
    app = QApplication()
    window = QtWindow()
    window.show()
    sys.exit(app.exec_())
