import sys, getopt
sys.path.append('.')
import RTIMU
import os.path
import lsm303d
import math, time

def CAPTURA_IMG(count, camera):
  IMG = 'IMG/imagem_%d.jpg' % count
  camera.capture(IMG)
  return

def ARMAZENA_EULER(Euler_STR, Euler, count ):
  Euler_STR = [str(x) for x in [Euler]]
  arq=open("EXTRINSECOS/EULER_%d (r,p,y).txt" % count, "w")
  arq.write(Euler_STR[0])
  arq.write('\n')
  arq.close()
  return

def MTX_ROT(RPY_GRAUS):

  x=math.pi*RPY_GRAUS[0]/180
  y=math.pi*RPY_GRAUS[1]/180
  z=math.pi*RPY_GRAUS[2]/180

  RPY=[x,y,z]

  # Matriz de Euler - Roll
  Rx = [[1,0,0],[0,math.cos(RPY[0]),-math.sin(RPY[0])],[0,math.sin(RPY[0]),math.cos(RPY[0])]]

  # Matriz de Euler - Pitch
  Ry = [[math.cos(RPY[1]),0,math.sin(RPY[1])],[0,1,0],[-math.sin(RPY[1]),0,math.cos(RPY[1])]]

  # Matriz de Euler - yaw
  Rz = [[math.cos(RPY[2]),-math.sin(RPY[2]),0],[math.sin(RPY[2]),math.cos(RPY[2]),0],[0,0,1]]

  # result is 3x4
  aux = [[0,0,0],[0,0,0],[0,0,0]]
  MTX_ROT = [[0,0,0],[0,0,0],[0,0,0]]

  # iterate through rows of X
  for i in range(len(Rz)):
     # iterate through columns of Y
     for j in range(len(Ry[0])):
         # iterate through rows of Y
         for k in range(len(Ry)):
             aux[i][j] += Rz[i][k] * Ry[k][j]

  # iterate through rows of X
  for i in range(len(aux)):
     # iterate through columns of Y
     for j in range(len(Rx[0])):
         # iterate through rows of Y
         for k in range(len(Rx)):
             MTX_ROT[i][j] += aux[i][k] * Rx[k][j]






  #a11=math.cos(RPY[2])*math.cos(RPY[0])-math.cos(RPY[1])*math.sin(RPY[0])*math.sin(RPY[2])
  #a12=math.cos(RPY[2])*math.sin(RPY[0])+math.cos(RPY[1])*math.cos(RPY[0])*math.sin(RPY[2])
  #a13=math.sin(RPY[2])*math.sin(RPY[1])
  #a21=-math.sin(RPY[2])*math.cos(RPY[0])-math.cos(RPY[1])*math.sin(RPY[0])*math.cos(RPY[2])
  #a22=-math.sin(RPY[2])*math.sin(RPY[0])+math.cos(RPY[1])*math.cos(RPY[0])*math.cos(RPY[2])
  #a23=math.cos(RPY[2])*math.sin(RPY[1])
  #a31=math.sin(RPY[1])*math.sin(RPY[0])
  #a32=-math.sin(RPY[1])*math.cos(RPY[0])
  #a33=math.cos(RPY[1])
  #MTX_ROT=[[a11,a12,a13],[a21,a22,a23],[a31,a32,a33]]
  return MTX_ROT

def ARMAZENA_ROT(ROT_STR, Euler, count):
  
  ROT_STR[:] = [str(x) for x in (MTX_ROT(Euler))]

  arq=open("EXTRINSECOS/ROT_%d.txt" % count, "w")
  for i in range (0,3):
    arq.write(ROT_STR[i])
    arq.write('\n')
  arq.close()
  return

def ACC():
  acc_mag=lsm303d.lsm303d()
  try:
    ACC=acc_mag.getRealAccel()
  except IOError:
    print("Unable to read from accelerometer, check the sensor and try again")
  HEADING=acc_mag.getHeading()
  return ACC, HEADING

def POSICAO(Vx,Vy,Vz,Vix,Viy,Viz,Sx,Sy,Sz,Six,Siy,Siz, POS_ATUAL, POS):
  T=0.1
  #print (POS_ATUAL)
  (ACEL, HEADING)=ACC()
  #print ('HEEEEADING')
  #print (HEADING)
  
  #Converte Aceleracao para Velocidade
  time.sleep(T)
  Vx=Vix+ACEL[0]*T
  Vy=Viy+ACEL[1]*T
  Vz=Viz+ACEL[2]*T
  (Vix,Viy,Viz)=(Vx,Vy,Vz)
  VEL=[Vx,Vy,Vz]

  #Converte Aceleracao para Velocidade
  Sx=Six+VEL[0]*T
  Sy=Siy+VEL[1]*T
  Sz=Siz+VEL[2]*T
  (Six,Siy,Siz)=(Sx,Sy,Sz)
  POS=[Sx,Sy,Sz]
  for i in range (0,3):
    POS_ATUAL[i]=POS_ATUAL[i]+POS[i]
  return POS_ATUAL

#Armazena Matrizes no TXT
def MAT_TRA(tx, ty, tz):
  MTX_TRA=[]
  MTX_TRA=[[1,0,0,tx],[0,1,0,ty],[0,0,1,tz],[0, 0, 0, 1]]
  print (MTX_TRA)
  return MTX_TRA

def ARMAZENA_TRA(tx, ty, tz, count, MTX_TRA):
  TRA_STR=[]
  TRA_STR[:] = [str(x) for x in (MTX_TRA)]

  arq=open("EXTRINSECOS/TRANSL_%d.txt" % count, "w")
  for i in range (0,4):
    arq.write(TRA_STR[i])
    arq.write('\n')
  arq.close()
  return

