 #Importa biblioteca do sistema para comandos do command line 
import picamera          
import time, math
import RPi.GPIO as GPIO
from Fusion import EulerAngles
from Functions import ARMAZENA_ROT
from Functions import *
import lsm303d


#Importando Funcoes camera = picamera.PiCamera()
camera = picamera.PiCamera()


#Definindo Variaveis
count=0
n=0
ROT_STR=[]
TRA_STR=[]
(x,y,z)=(0,0,0)

#Dados para MTX de Rotacao
Euler=[]
ROT=[]
Euler_STR=0

#Dados para MTX de Translacao
POS=[]
POS_ATUAL=[0,0,0]


#Setando GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Definindo acionamento de captura por meio do botoao (GPIO 18)
while True:  
    input_state = GPIO.input(18)
    desliga = GPIO.input(20)
    POS_ATUAL=POSICAO(0,0,0,0,0,0,0,0,0,0,0,0,POS_ATUAL,POS)
    
    if input_state == False:

        n=1
        count=count+n

        #For principal - Minimu9 + Picamera
        for i in range (0, n):

            #Identifica e chama func. que captura a imagem em .PNG
            print ('IMAGEM %d' % count)
            CAPTURA_IMG(count, camera)
            
            #Chama Func que armazena os Angulos de Euler em .TXT
            Euler=EulerAngles(count)
            ARMAZENA_EULER(Euler_STR, Euler, count)
            print ('')
            print (Euler_STR)

            #Chama Func. que constroi matriz de Rotacao
            print('MATRIZ DE ROTAÇÃO %s:' % count)
            ROT=MTX_ROT(Euler)
            print (ROT)
    
            #Captura ACeleracao

            
            #Gera Matriz de Translacao
            print('\nMATRIZ DE TRANSLACAO %s:' % count)
            TRANSLACAO=MAT_TRA(POS_ATUAL[0],POS_ATUAL[1],POS_ATUAL[2])            
            
            #Chama Func. que armazena matriz de rotacao em .TXT
            ARMAZENA_ROT(ROT_STR, Euler, count)
            ARMAZENA_TRA(POS_ATUAL[0],POS_ATUAL[1],POS_ATUAL[2], count, TRANSLACAO)
            
            print ('')
    elif desliga == False:
        break
