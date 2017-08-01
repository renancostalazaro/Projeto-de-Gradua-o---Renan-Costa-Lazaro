import sys, getopt
import time
sys.path.append('.')
import RTIMU
import os.path
import math

def EulerAngles(count):
  EULER=[]
  SETTINGS_FILE = "RTIMULib"

  
  #print("Using settings file " + SETTINGS_FILE + ".ini")
  if not os.path.exists(SETTINGS_FILE + ".ini"):
    print("Settings file does not exist, will be created")

  s = RTIMU.Settings(SETTINGS_FILE)
  imu = RTIMU.RTIMU(s)

  #print("IMU Name: " + imu.IMUName())
  print ('...')   #NAO REMOVER: CORRIGE ERRO DE TEMPO DE PROCESSAMENTO
  if (not imu.IMUInit()):
      print("IMU Init Failed")
      sys.exit(1)
  else:()
    #  print("IMU Init Succeeded")

# this is a good time to set any fusion parameters
  print ('') #NAO REMOVER: CORRIGE ERRO DE TEMPO DE PROCESSAMENTO
  imu.setSlerpPower(0.01)
  print ('') #NAO REMOVER: CORRIGE ERRO DE TEMPO DE PROCESSAMENTO
  imu.setGyroEnable(True)
  #print ('5')
  imu.setAccelEnable(True)
  #print ('4')
  imu.setCompassEnable(True)
  #print ('3')
  
  poll_interval = imu.IMUGetPollInterval()
  print("Angulos de Euler %d:" % count) # %dmS\n" % poll_interval)


  #while x==1:
  if imu.IMURead():
    data = imu.getIMUData()
    fusionPose = data["fusionPose"]
    print("r: %f p: %f y: %f" % (math.degrees(fusionPose[0]), math.degrees(fusionPose[1]), math.degrees(fusionPose[2])))
    EULER=[math.degrees(fusionPose[0]),math.degrees(fusionPose[1]), math.degrees(fusionPose[2])]
  return EULER
  
