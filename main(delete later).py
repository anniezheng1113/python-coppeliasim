try:
    import sim
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')

import sys
import time                #used to keep track of time
import math
import numpy as np         #array library

#initialization
PI=math.pi  #pi=3.14..., constant

#establish connection
sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
print ("client id:",clientID)   #checking message, delete later

if clientID!=-1:
    print ('Connected to remote API server')
else:
    print ('Connection failed')
    sys.exit('Could not connect!')

#left motor handle
errorCode,left_motor_handle = sim.simxGetObjectHandle(clientID,'./leftMotor',sim.simx_opmode_oneshot_wait)
#print ("errorCode:",errorCode)  #checking message, delete later
#print("left moter handle:",left_motor_handle)   #checking message, delete later

#right motor handle
errorCode,right_motor_handle = sim.simxGetObjectHandle(clientID,'./rightMotor',sim.simx_opmode_oneshot_wait)
#print ("errorCode:",errorCode)  #checking message, delete later
#print("left moter handle:",right_motor_handle)  #checking message, delete later

#set robot joint velocity
#errorCode = sim.simxSetJointTargetVelocity(clientID,left_motor_handle,0.2,sim.simx_opmode_streaming)    #set the target velovity to 0.2
#errorCode = sim.simxSetJointTargetVelocity(clientID,right_motor_handle,0.2,sim.simx_opmode_streaming)    #set the target velovity to 0.2

#set sensor 1
# errorCode,sensor1 = sim.simxGetObjectHandle(clientID,'./ultrasonicSensor[1]',sim.simx_opmode_oneshot_wait)
#print ("errorCode:",errorCode)  #checking message, delete later
#print("sensor 1:",sensor1)   #checking message, delete later

#errorCode, detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector = sim.simxReadProximitySensor(clientID,sensor1,sim.simx_opmode_streaming)
#errorCode,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=sim.simxReadProximitySensor(clientID,sensor1,sim.simx_opmode_streaming)        
# errorCode, detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector = sim.simxReadProximitySensor(clientID,sensor1,sim.simx_opmode_buffer)
# print ("errorCode:",errorCode)  #checking message, delete later
# print("detectionState:",detectionState)   #checking message, delete later
# print("detectedPoint",detectedPoint)   #checking message, delete later
# print ("detectedObjectHandle:",detectedObjectHandle)  #checking message, delete later
# print("detectedSutfaceNormalVector:",detectedSurfaceNormalVector)   #checking message, delete later


sensor_h=[] #empty list for handles
sensor_val=np.array([]) #empty array for sensor measurements

#orientation of all the sensors: 
sensor_loc=np.array([-PI/2, -50/180.0*PI,-30/180.0*PI,-10/180.0*PI,10/180.0*PI,30/180.0*PI,50/180.0*PI,PI/2,PI/2,130/180.0*PI,150/180.0*PI,170/180.0*PI,-170/180.0*PI,-150/180.0*PI,-130/180.0*PI,-PI/2]) 

#for loop to retrieve sensor arrays and initiate sensors
for x in range(1,16+1):
        errorCode,sensor_handle=sim.simxGetObjectHandle(clientID,'./ultrasonicSensor[1]'+str(x),sim.simx_opmode_oneshot_wait)
        sensor_h.append(sensor_handle) #keep list of handles        
        errorCode,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=sim.simxReadProximitySensor(clientID,sensor_handle,sim.simx_opmode_streaming)                
        sensor_val=np.append(sensor_val,np.linalg.norm(detectedPoint)) #get list of values (take 3 dimensional num to 1 dimensional num)
        

t = time.time()

while (time.time()-t)<60:      #script run for 60s
    #Loop Execution
    sensor_val=np.array([])    
    for x in range(1,16+1):
        errorCode,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=sim.simxReadProximitySensor(clientID,sensor_h[x-1],sim.simx_opmode_buffer)                
        sensor_val=np.append(sensor_val,np.linalg.norm(detectedPoint)) #get list of values

    
    #controller specific
    sensor_sq=sensor_val[0:8]*sensor_val[0:8] #square the values of front-facing sensors 1-8
        
    min_ind=np.where(sensor_sq==np.min(sensor_sq))
    min_ind=min_ind[0][0]
    
    if sensor_sq[min_ind]<0.2:
        steer=-1/sensor_loc[min_ind]
    else:
        steer=0
            
    
    v=1	#forward velocity
    kp=0.5	#steering gain
    vl=v+kp*steer
    vr=v-kp*steer
    print ("V_l =",vl)
    print ("V_r =",vr)

    errorCode=sim.simxSetJointTargetVelocity(clientID,left_motor_handle,vl, sim.simx_opmode_streaming)
    errorCode=sim.simxSetJointTargetVelocity(clientID,right_motor_handle,vr, sim.simx_opmode_streaming)


    time.sleep(0.2) #loop executes once every 0.2 seconds (= 5 Hz)

#Post ALlocation
errorCode=sim.simxSetJointTargetVelocity(clientID,left_motor_handle,0, sim.simx_opmode_streaming)
errorCode=sim.simxSetJointTargetVelocity(clientID,right_motor_handle,0, sim.simx_opmode_streaming)
