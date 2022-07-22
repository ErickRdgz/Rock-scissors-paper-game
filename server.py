# from fileinput import close
#from curses.ascii import NUL
#from pickletools import read_uint1
# from _theread import*
import socket
import threading
#import time
import select

clients=[]

waitingFlag=False
closeWait=threading.Event()

#Inicialización del servidor
def initServer():

    s=socket.socket()
    host="localhost"
    port=8081

    s.bind((host,port))
    print("Server started")
    print("Host",host)
    print("Port",port)
    print("waiting for connection.....")

    #Espera 2 conexiones
    s.listen(5)
    clientCounter=0
    
    while True:
        #Acepta al primer jugador
        conn, addr=s.accept()
        clientCounter+=1
        clients.append(conn)

        #Manda señal de conexión
        print("Got Connection form",addr)
        

        global waitingFlag
        global player1
        global wthread

        if waitingFlag:
            waitingFlag=False
            #Manda señal de conexión de jugador 2
            print("Pareja formada")
            ###conn.send(1) #Esperando respuesta de jugador 2
            closeWait.set()
            wthread.join()
            t=threading.Thread(target=game,args=(player1,conn))
            t.start()
        else:
            waitingFlag=True
            player1=conn
            t=threading.Thread(target=waitThread,args=(conn,))
            t.start()
            wthread=t
    s.close()

#Esperando a jugador 2
def waitThread(client):
    client.send('Jugador2Desconectado'.encode('utf-8')) #Esperando conexión de jugador 2
    print("Señal jugador 2 desconectado enviada")
    client.setblocking(0)
    while True:
        # print('.')
        if closeWait.is_set():
            print ("fin de espera")
            break
        try:
            
            buffer = select.select([client],[],[],1)
            # print(buffer)
            # print(error)
            if buffer[0]:
                print(".")
                data=client.recv(20).decode('utf-8')
                if data=='@Ready':
                    print("A jugar!")

        except:
            client.close()



def game(player1,player2):
    print("A jugar!")

    #Jugador 2 conectado, esperando respuesta!
    player1.send('2JugadoresConectados'.encode('utf-8'))
    player2.send('2JugadoresConectados'.encode('utf-8'))
    print("Señal 2 jugadores conectados enviada a ambos jugadores")
    

    player1.setblocking(0)
    player2.setblocking(0)


    player1Flag=False
    shot1 = 'Nada'
    player2Flag=False
    shot2 = 'Nada'

    while True:

        buffer=tuple() 
        if player1Flag==False:
            buffer = select.select([player1],[],[],0.1)
            if buffer[0]:
                shot1=player1.recv(20).decode('utf-8')
                print("P1:",shot1)
                if shot1=='Piedra':
                    player2.send('Piedra'.encode('utf-8'))
                    print("P1 seleccionó PIEDRA enviado a P2")
                    player1Flag=True
                if shot1=='Papel':
                    player2.send('Papel'.encode('utf-8'))
                    print("P1 seleccionó PAPEL enviado a P2")
                    player1Flag=True
                if shot1=='Tijeras':
                    player2.send('Tijeras'.encode('utf-8'))
                    print("P1 seleccionó TIJERAS enviado a P2")
                    player1Flag=True  
                elif shot1=='Abandonar':
                    break

    
        buffer=tuple()
        if player2Flag==False:
            buffer = select.select([player2],[],[],0.1)
            if buffer[0]:
                shot2=player2.recv(20).decode('utf-8')
                print("P2:",shot2)
                if shot2=='Piedra':
                    player1.send('Piedra'.encode('utf-8'))
                    print("P2 seleccionó PIEDRA enviado a P1")
                    player2Flag=True
                if shot2=='Papel':
                    player1.send('Papel'.encode('utf-8'))
                    print("P2 seleccionó PAPEL enviado a P1")
                    player2Flag=True
                if shot2=='Tijeras':
                    player1.send('Tijeras'.encode('utf-8'))
                    print("P2 seleccionó TIJERAS enviado a P1")
                    player2Flag=True  
                elif shot2=='Abandonar':
                    break




    print("Fin del hilo de juego")
    player1.send('3'.encode('utf-8'))
    player2.send('3'.encode('utf-8'))
    player1.close()
    player2.close()



if __name__=='__main__':
    initServer()
