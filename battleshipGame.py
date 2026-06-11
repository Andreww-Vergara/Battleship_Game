import numpy as np
import random
import time
import os

class jugador():
    def __init__(self, name,poder):
        self.name=name#nombre de jugador
        self.barco=1#ID del barco a colocar
        self.matriz=None#mapa real del jugador
        self.muestra=None#mapa de vista del oponente
        self.tiro=(0,0)#coordenadas del tiro
        self.golpes=0#impactos recibidos
        self.rest=0#barcos restantes
        self.poder=poder#contador para poder especial, reescrito por cada clase hija

    def creamatrices(self,x,y):#crea las matrices del juego
        self.matriz=np.zeros((x,y), dtype=int)
        self.muestra=np.full((x,y),"*")
        self.matriz[0]=np.arange(0,y)
        self.muestra[0]=np.arange(0,y)
        for i in range(x):
            self.matriz[i,0]=i
            self.muestra[i,0]=i
        return self.matriz,self.muestra
    
class player(jugador):
    def botes(self,mapa,cantidad,tamaño):#coloca los barcos del jugador
        num=cantidad
        while num>0:
            os.system('cls')#limpia la pantalla
            print(("Posiciona tus barcos:"))
            print(f"tienes {num} barco(s) restantes de {tamaño} espacios.")
            print("Coloca tu barco No. ",self.barco)
            if tamaño!=1:
                print("Elige su dirección: ")
                print("1. vertical")
                print("2. horizontal")
                dir=rango(val(),1,2)
            else:
                dir=1
            print("Posición:")
            tito=True
            if dir==1:#vertical
                while tito:
                    print(self.matriz)
                    print("Fila:")
                    posx=rango(val(),1,mapa.shape[0]-1)
                    print("Columna:")
                    posy=rango(val(),1,mapa.shape[1]-1)
                    gordo=True
                    if tamaño+posx<=mapa.shape[0]:
                        for i in range(0,tamaño):
                            if mapa[posx+i][posy]!=0:
                                print("No cabe, menso")
                                gordo=False
                                break
                        if gordo:
                            for j in range(0,tamaño):
                                mapa[posx+j][posy]=self.barco
                            self.barco=self.barco+1
                            tito=False
                    else:
                        print("No cabe, burro")

            elif dir==2:#horizontal
                while tito:
                    print(self.matriz)
                    print("Fila:")
                    posx=rango(val(),1,mapa.shape[0]-1)
                    print("Columna:")
                    posy=rango(val(),1,mapa.shape[1]-1)
                    gordo=True
                    if tamaño+posy<=mapa.shape[1]:
                        for i in range(0,tamaño):
                            if mapa[posx][posy+i]!=0:
                                print("No cabe, tonto")
                                gordo=False
                                break
                        if gordo:
                            for j in range(0,tamaño):
                                mapa[posx][posy+j]=self.barco
                            self.barco=self.barco+1
                            tito=False
                    else:
                        print("No cabe, burro")
            num=num-1
            print(f"Barco colocado en [{posx}],[{posy}].")
            print(mapa)
            input("Continue...")
        return mapa

    def disparo(self,rival):
        for i in range(3):
            os.system('cls')#limpia la pantalla
            print(f"Turno No. {i+1} de {self.name}")
            print("Barcos restantes del enemigo: ",rival.rest)
            print(rival.muestra)
            while 1:
                print("\nEscoge tu ataque: ")
                print("1. Disparo")
                if self.golpes>=self.poder:
                    print("2. Disparo especial")
                ataque=val()
                if ataque==1 or (self.golpes>=self.poder and ataque==2):
                    break
                else:
                    print("Antes la gente sabía leer. Elige bien, asno")
            while True:#while para no repetir ataque
                os.system('cls')#limpia la pantalla
                print("Mapa del enemigo: ")
                print(rival.muestra)
                print("Posiciona tu ataque: ")
                if ataque==2:self.llamado()
                print("Fila:")
                posx=rango(val(),1,rival.matriz.shape[0]-1)
                print("Columna:")
                posy=rango(val(),1,rival.matriz.shape[1]-1)
                self.tiro=(posx,posy)
                if rival.muestra[posx][posy] in ["*", "B"]:
                    break
                else:
                    print("Ya atacaste ahí, burro.")
                    input("Continue...")
            if ataque==2:
                self.especial(posx,posy,rival)
                continue
            if ataque==1:
                time.sleep(2)
                x=rival.matriz[posx][posy]#su matriz, mi tiro
                if x > 0 :#impacto en barco
                    print(f"{self.name} ha impactado en {self.tiro}!")
                    rival.matriz[self.tiro],rival.muestra[self.tiro] = -x,"X"
                    self.golpes=self.golpes+1
                    print(rival.muestra)
                    input("Continue...")
                    if not np.any(rival.matriz[1:,1:] == x):
                        print(f"Barco No. {x} hundido!")#si no hay más partes del barco, se hunde
                        rival.rest=rival.rest-1
                        input("Continue...")
                    if not np.any(rival.matriz[1:,1:] > 0):#si no hay más barcos
                        print(f"¡{rival.name} se ha quedado sin barcos!")
                        input("Continue...")
                        os.system('cls')
                        time.sleep(1)
                        print(f"{self.name} HA GANADO LA PARTIDA!!")
                        input("Presiona ENTER para cerrar.")
                        exit()
                elif rival.matriz[posx][posy] == 0:
                    print(f"{self.name} ha fallado.")
                    rival.muestra[posx][posy] = "O"
                    print(rival.muestra)
                    input("Continue...")           

class bot(jugador):
    def botes(self,mapa,cantidad,tamaño):#coloca los botes si es bot
        num=cantidad
        while num>0:
            dir=random.randint(1,2)
            tito=True
            if dir==1:#vertical
                while tito:
                    posx=random.randint(1, mapa.shape[0]-tamaño)
                    posy=random.randint(1, mapa.shape[1]-1)
                    gordo=True
                    for i in range(0,tamaño):
                        if mapa[posx+i][posy]!=0:
                            gordo=False
                            break
                    if gordo:
                        for j in range(0,tamaño):
                            mapa[posx+j][posy]=self.barco
                        self.barco=self.barco+1
                        tito=False
            elif dir==2:#horizontal
                while tito:
                    posx=random.randint(1, mapa.shape[0]-1)
                    posy=random.randint(1, mapa.shape[1]-tamaño)
                    gordo=True
                    for i in range(0,tamaño):
                        if mapa[posx][posy+i]!=0:
                            gordo=False
                            break
                    if gordo:
                        for j in range(0,tamaño):
                            mapa[posx][posy+j]=self.barco
                        self.barco=self.barco+1
                        tito=False
            num=num-1
        return mapa

    def disparo(self,rival):
        for i in range(3):
            os.system('cls')#limpia la pantalla
            print(f"Turno No. {i+1} de {self.name}")
            while True:#evita repetir ataque
                posx=random.randint(1, rival.matriz.shape[0]-1)
                posy=random.randint(1, rival.matriz.shape[1]-1)
                self.tiro=(posx,posy)
                if rival.muestra[posx][posy]=="*":
                    break
                if rival.muestra[posx][posy]!="X" and rival.muestra[posx][posy]!="O":
                    break
            if self.golpes>=self.poder:
                self.especial(posx,posy,rival)
                continue
            x=rival.matriz[self.tiro]
            time.sleep(2)
            if x > 0:#impacto en barco
                print(f"{self.name} ha impactado en {self.tiro}!")
                rival.matriz[posx][posy],rival.muestra[posx][posy] = -x,"X"
                self.golpes=self.golpes+1
                print(rival.muestra)
                input("Continue...")
                if not np.any(rival.matriz[1:,1:] == x):
                    print(f"Barco No. {x} hundido!")#si no hay más partes del barco, se hunde
                    rival.rest=rival.rest-1
                if not np.any(rival.matriz[1:,1:] > 0):#si no hay más barcos
                    print(f"¡{rival.name} se ha quedado sin barcos!")
                    input("Continue...")
                    os.system('cls')
                    time.sleep(1)
                    print(f"{self.name} HA GANADO LA PARTIDA!!")
                    input("Presiona ENTER para cerrar.")
                    exit()

            elif rival.matriz[posx][posy] == 0:
                print(f"{self.name} ha fallado.")
                rival.muestra[posx][posy] = "O"
                print(rival.muestra)
                input("Continue...")

class espia(player):#su especial es observar area del oponente
    def llamado(self):
        print("Escoge sabiamente...la habilidad muestra los espacios alrededor de tu disparo.")
    
    def especial(self,a,b,rival):
        self.golpes = 0
        rowmin = a-1
        rowmax = a+2
        colmin = b-1
        colmax = b+2
        if rowmin<1:rowmin=1
        if rowmax>rival.matriz.shape[0]:rowmax=rival.matriz.shape[0]
        if colmin<1:colmin=1
        if colmax>rival.matriz.shape[1]:colmax=rival.matriz.shape[1]
        area = rival.matriz[rowmin:rowmax, colmin:colmax]# Convertimos a string para que encaje en la matriz de muestra
        filtro = np.where(area < 0, "X", np.where(area > 0, "B", "O"))        
        rival.muestra[rowmin:rowmax, colmin:colmax] = filtro            
        print(f"¡Radar activado! Área revelada de [{a}],[{b}]...")
        input("Continue...")

class espiabot(bot):
    def especial(self,a,b,rival):
        self.golpes = 0
        rowmin = a-1
        rowmax = a+2
        colmin = b-1
        colmax = b+2
        if rowmin<1:rowmin=1
        if rowmax>rival.matriz.shape[0]:rowmax=rival.matriz.shape[0]
        if colmin<1:colmin=1
        if colmax>rival.matriz.shape[1]:colmax=rival.matriz.shape[1]
        area = rival.matriz[rowmin:rowmax, colmin:colmax]# Convertimos a string para que encaje en la matriz de muestra
        filtro = np.where(area < 0, "X", np.where(area > 0, "B", "*"))#astype convierte el tipo de dato
        rival.muestra[rowmin:rowmax, colmin:colmax] = filtro            
        print(f"¡Radar activado! Área revelada de [{a}],[{b}]...")

class piloto(player):#su especial es ataque aereo
    def llamado(self):   
        print("Ataque aéreo: dispara 3 espacios en horizontal, uno antes, otro después.")

    def especial(self,a,b,rival):
        self.golpes=0
        colmin = b-1
        colmax = b+2
        if colmin < 1:colmin = 1
        if colmax > rival.matriz.shape[1]:colmax = rival.matriz.shape[1]
        fila = a
        print(f"Ataque aéreo de {colmin} a {colmax-1}")
        for col in range(colmin, colmax):
            x = rival.matriz[fila][col]
            if x > 0:
                print(f"Impacto en [{fila},{col}]!")
                rival.matriz[fila][col] = -x
                rival.muestra[fila][col] = "X"
                self.golpes += 1
                if not np.any(rival.matriz[1:,1:] == x):
                    print(f"Barco No. {x} hundido!")
                    rival.rest -= 1
            elif x == 0:
                rival.muestra[fila][col] = "O"
        print(rival.muestra)
        if not np.any(rival.matriz[1:,1:] > 0):
            print(f"¡{rival.name} se ha quedado sin barcos!")
            input("Continue...")
            os.system('cls')
            print(f"{self.name} HA GANADO LA PARTIDA!!")
            input("Presiona ENTER para cerrar.")
            exit()

class pilotobot(bot):
    def especial(self,a,b,rival):
        self.golpes=0
        colmin = b-1
        colmax = b+2
        if colmin < 1:colmin = 1
        if colmax > rival.matriz.shape[1]:colmax = rival.matriz.shape[1]
        fila = a
        print(f"Ataque aéreo de {colmin} a {colmax-1}")
        for col in range(colmin, colmax):
            x = rival.matriz[fila][col]
            if x > 0:
                print(f"Impacto en [{fila},{col}]!")
                rival.matriz[fila][col] = -x
                rival.muestra[fila][col] = "X"
                self.golpes += 1
                if not np.any(rival.matriz[1:,1:] == x):
                    print(f"Barco No. {x} hundido!")
                    rival.rest -= 1
            elif x == 0:
                rival.muestra[fila][col] = "O"
        print(rival.muestra)
        if not np.any(rival.matriz[1:,1:] > 0):
            print(f"¡{rival.name} se ha quedado sin barcos!")
            input("Continue...")
            os.system('cls')
            print(f"{self.name} HA GANADO LA PARTIDA!!")
            input("Presiona ENTER para cerrar.")
            exit()
        
class bombardero(player):#Bombardea toda un área
    def llamado(self):   
        print("Escoge sabiamente...la habilidad bombardea alrededor de tu disparo.")

    def especial(self,a,b,rival):#bombardea toda un área
        self.golpes = 0
        rowmin = a-1
        rowmax = a+2
        colmin = b-1
        colmax = b+2
        if rowmin<1:rowmin=1
        if rowmax>rival.matriz.shape[0]:rowmax=rival.matriz.shape[0]
        if colmin<1:colmin=1
        if colmax>rival.matriz.shape[1]:colmax=rival.matriz.shape[1]
        areaReal = rival.matriz[rowmin:rowmax, colmin:colmax]#sobre la matriz
        areaVista = rival.muestra[rowmin:rowmax, colmin:colmax]#sobre la muestra
        self.golpes=self.golpes+np.count_nonzero(areaReal>0)
        ids=np.unique(areaReal[areaReal>0])
        
        areaVista[areaReal > 0] = "X" #marca barcos impactados
        areaVista[areaReal == 0] = "O" #marca el agua
        areaReal[areaReal > 0] *= -1 #el ID impactado se multiplica para negativo
        print(f"¡Bombardeo ejecutado en el área alrededor de [{a}], [{b}]!")
        for num in ids:
            if not np.any(rival.matriz[1:, 1:] == num):
                print(f"Barco No. {num} destruido.")
                rival.rest -= 1
        if not np.any(rival.matriz[1:,1:] > 0):
            print(f"¡{rival.name} se ha quedado sin barcos!")
            input("Continue...")
            os.system('cls')
            print(f"{self.name} HA GANADO LA PARTIDA!!")
            input("Presiona ENTER para cerrar.")
            exit()

class bombarderobot(bot):
    def especial(self,a,b,rival):
        self.golpes = 0
        rowmin = a-1
        rowmax = a+2
        colmin = b-1
        colmax = b+2
        if rowmin<1:rowmin=1
        if rowmax>rival.matriz.shape[0]:rowmax=rival.matriz.shape[0]
        if colmin<1:colmin=1
        if colmax>rival.matriz.shape[1]:colmax=rival.matriz.shape[1]
        areaReal = rival.matriz[rowmin:rowmax, colmin:colmax]#sobre la matriz
        areaVista = rival.muestra[rowmin:rowmax, colmin:colmax]#sobre la muestra
        areaVista[areaReal > 0] = "X" #marca barcos impactados
        areaVista[areaReal == 0] = "O" #marca el agua
        areaReal[areaReal > 0] *= -1 #el ID impactado se multiplica para negativo
        print(f"¡Bombardeo ejecutado en el área alrededor de [{a}], [{b}]!")

def val():#valida integers
    try:
        local=int(input("..."))
        return local
    except:
        print("Fijate bien lo que te pido, tonto.")
        return val()
    
def rango(local, min, max):#valida rangos
    while True:
        if min<=local<=max:
            return local
        print("No sabes escoger o qué, wey.")
        local=val()

def seleccion():
    print("Selecciona tu jugador:")
    print (f"--1. Brandon, el espía")
    print("Ataque especial: Revela un área del oponente al acertar 3 ataques")
    print (f"--2. Aaron, el piloto")
    print("Ataque especial: Disparo múltiple al oponente al acertar 5 ataques")
    print (f"--3. Dwight, el bombardero")
    print("Ataque especial: bombardea un área del oponente al acertar 7 ataques")
    a=rango(val(),1,3)
    if a==1:
        print("Selecciona tu rival:")
        print (f"--1. Aaron, el piloto")
        print (f"--2. Dwight, el bombardero")
        b=rango(val(),1,2)
        if b==1:
            perros=(1,2)
        elif b==2:
            perros=(1,3)
    elif a==2:
        print("Selecciona tu rival:")
        print (f"--1. Brandon, el espía")
        print (f"--2. Dwight, el bombardero")
        b=rango(val(),1,2)
        if b==1:
            perros=(2,1)
        elif b==2:
            perros=(2,3)
    elif a==3:
        print("Selecciona tu rival:")
        print (f"--1. Brandon, el espía")
        print (f"--2. Aaron, el piloto")
        b=rango(val(),1,2)
        if b==1:
            perros=(3,1)
        elif b==2:
            perros=(3,2)
    return perros

def inicio(j1,j2):
        os.system('cls')#limpia la pantalla
        ancho,largo=7,8
        nb2,nb3,nb4,nb5=2,2,1,1
        tb2,tb3,tb4,tb5=2,3,4,5#truco aprendido a fallo y error
        j1.rest=nb2+nb3+nb4+nb5
        j2.rest=nb2+nb3+nb4+nb5
        j1.matriz,j1.muestra=j1.creamatrices(ancho,largo)
        j2.matriz,j2.muestra=j2.creamatrices(ancho,largo)
        print(f"{j1.name} vs {j2.name}")
        print((f"-- Mapa de {ancho-1}x{largo-1} --"))
        print(("Cada uno tendrá"))
        print((f"-- {nb5} barco(s) de {tb5} espacios --"))
        print((f"-- {nb4} barco(s) de {tb4} espacios --"))
        print((f"-- {nb3} barco(s) de {tb3} espacios --"))
        print((f"-- {nb2} barco(s) de {tb2} espacios --"))
        input("Continue...")

        os.system('cls')#limpia la pantalla
        time.sleep(1)#dramatismo
        j1.matriz=j1.botes(j1.matriz,nb5,tb5)
        j1.matriz=j1.botes(j1.matriz,nb4,tb4)
        j1.matriz=j1.botes(j1.matriz,nb3,tb3)
        j1.matriz=j1.botes(j1.matriz,nb2,tb2)
        os.system('cls')#limpia la pantalla
        print("Es turno del oponente...")
        input("Continue...")  
        os.system('cls')#limpia la pantalla
        time.sleep(1)#dramatismo
        input("Continue...")
        j2.matriz=j2.botes(j2.matriz,nb5,tb5)
        j2.matriz=j2.botes(j2.matriz,nb4,tb4)
        j2.matriz=j2.botes(j2.matriz,nb3,tb3)
        j2.matriz=j2.botes(j2.matriz,nb2,tb2)
        return j1,j2

def pelea(j1,j2):
    while True:
        print(f"Es turno del jugador 1, {j1.name}. ")
        print(f"Has acertado {j1.golpes} impacto(s).")
        print(f"Tu especial se activa al alcanzar {j1.poder} impactos")
        input("Continue...")
        os.system('cls')
        j1.disparo(j2)
        os.system('cls')
        print(f"Es turno del jugador 2, {j2.name}. ")
        print(f"Has acertado {j2.golpes} impacto(s).")
        print(f"Tu especial se activa al alcanzar {j2.poder} impactos")
        input("Continue...")
        os.system('cls')
        j2.disparo(j1)
        os.system('cls')

juego=True
while juego:###juego
    print ("\n<<<<<<<BATTLESHIP>>>>>>>\n")
    print("-- Destruye la flota enemiga --")
    print ("Elige una opción:")
    print ("--1. Player vs Bot")
    print ("--2. Player vs Player")
    print ("--3. Salir")
    numero=rango(val(),1,3)
    if numero==1:##player vs bot
        print("Jugador contra PC")
        os.system('cls')#limpia la pantalla
        players=seleccion()
        if players==(1,2):
            wey1,wey2=inicio(espia("Brandon",3), pilotobot("Aaron",5))
        elif players==(1,3):
            wey1,wey2=inicio(espia("Brandon",3), bombarderobot("Dwight",7))
        elif players==(2,1):
            wey1,wey2=inicio(piloto("Aaron",5), espiabot("Brandon",3))
        elif players==(2,3):
            wey1,wey2=inicio(piloto("Aaron",5), bombarderobot("Dwight",7))
        elif players==(3,1):
            wey1,wey2=inicio(bombardero("Dwight",7), espiabot("Brandon",3))
        elif players==(3,2):
            wey1,wey2=inicio(bombardero("Dwight",7), pilotobot("Aaron",5))
        os.system('cls')
        print("<<<<<<<<<<<<<Empieza la batalla>>>>>>>>>>>>>>>\n")
        print("Destruye todos los barcos enemigos para ganar.")
        input("Continue...")
        pelea(wey1,wey2)
    elif numero==2:##player vs player
        os.system('cls')#limpia la pantalla
        print("Jugador contra Jugador")
        players=seleccion()
        if players==(1,2):
            wey1,wey2=inicio(espia("Brandon",3), piloto("Aaron",5))
        elif players==(1,3):
            wey1,wey2=inicio(espia("Brandon",3), bombardero("Dwight",7))
        elif players==(2,1):
            wey1,wey2=inicio(piloto("Aaron",5), espia("Brandon",3))
        elif players==(2,3):
            wey1,wey2=inicio(piloto("Aaron",5), bombardero("Dwight",7))
        elif players==(3,1):
            wey1,wey2=inicio(bombardero("Dwight",7), espia("Brandon",3))
        elif players==(3,2):
            wey1,wey2=inicio(bombardero("Dwight",7), piloto("Aaron",5))
        os.system('cls')
        print("<<<<<Empieza la batalla>>>>>")        
        pelea(wey1,wey2)
    elif numero==3:
            exit()
