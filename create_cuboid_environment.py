#Import Libraries:
import sim                  #V-rep library
import sys
import time                #used to keep track of time
import numpy as np         #array library
import math
import matplotlib as mpl   #used for image plotting

#Pre-Allocation

PI=math.pi  #pi=3.14..., constant

#connection
sim.simxFinish(-1) # just in case, close all opened connections

clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5)


if clientID!=-1:  #check if client connection successful
    print ('Connected to remote API server')
    sim.simxFinish(clientID)  
    # Create a cuboid
    length = 1
    width = 1
    height = 1
    mass = 1.0
    # options = [sim.simulationparameter_show_lines, 1]
    # Set the options for the cuboid
    #options = [sim.sim_boolparam_static, sim.sim_objcollider_non_convex]
    # Create the cuboid shape
    #res, cuboid_handle = sim.simxCreatePureShape(clientID, sim.sim_shape_type_cuboid, [length, width, height], mass, options, sim.simx_opmode_blocking)

    options = [sim.simulationparam_bullet_use_ccd, sim.sim_boolparam_shape_dynamic_approximation]
    res, cuboid_handle = sim.simxCreatePureShape(clientID, sim.sim_shape_type_cuboid, [length, width, height], mass, options, sim.simx_opmode_blocking)
    
    # #res, cuboid_handle = sim.simxCreatePureShape(clientID, sim.sim_shape_type_cuboid , [length, width, height], mass, options, sim.simx_opmode_blocking)

# Check if the cuboid was

    # Check if the cuboid was created successfully
    if res == sim.simx_return_ok:
        print("Cuboid created successfully!")
    else:
        print("Failed to create cuboid.")
else:
    print ('Connection not successful')
    sys.exit('Could not connect')



