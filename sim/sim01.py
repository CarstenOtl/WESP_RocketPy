## Imports
# from logging import root
# from tkinter import Widget
# import matplotlib as plt
from rocketpy import Environment, SolidMotor, Rocket, Flight 

# %matplotlib Widget

## Setting up the Simulation

#some definitions
class launchRail():
    railLength=6.5     #m
    railOrientation=88   #º with respect to ground

# Create an Environment (e.g. MUNICH)
Env = Environment(
    railLength=launchRail.railLength, 
    latitude=32.99, 
    longitude=50, 
    elevation=5
    )
# #get weather data 
# import datetime

# tomorrow = datetime.date.today() + datetime.timedelta(days=1)
# Env.setDate((tomorrow.year, tomorrow.month, tomorrow.day, 12)) #Hours given in UTC time 

# #Tell Env to use forcasted weather to get atmosphereic conditions for flight 
# Env.setAtmosphericModel(type="Forecoasst", file="GFS")
# #see weather info 
# Env.info()

## Create a Motor 

# solid motor class requires thurst curve from .eng or .csv file and other param. 
J180T = SolidMotor(
    thrustSource="../motors/AeroTech_J180T.csv",
    burnOut=4.5,
    grainNumber=5,
    grainSeparation=5/1000, 
    grainDensity=1815, 
    grainOuterRadius=33/1000,
    grainInitialInnerRadius=15/1000, 
    grainInitialHeight=120/1000, 
    nozzleRadius=33/1000,
    throatRadius=11/1000, 
    interpolationMethod="linear" #other interpolation methods dont work
)

# J180T.info()

## Create a Rocket
WESP = Rocket(
    motor=J180T, 
    mass = 20, #(kg)
    radius= 0.1, #(m)
    inertiaI=6, #TOB from structures 
    inertiaZ=0.05, #TOB from structures 
    distanceRocketNozzle=1, 
    distanceRocketPropellant=-1, 
    powerOffDrag=[(0, 0, 0), (0.5, 0.5, 0.1),(0.7, 0.7, 0.4), (1, 1, 0.5)], #'../data/rocket/powerOffDragCurve.csv', #TBD 
    powerOnDrag= [(0, 0, 0), (0.5, 0.5, 0.1),(0.7, 0.7, 0.4), (1, 1, 0.5)] #'../data/rocket/powerOnDragCurve.csv', #TBD
)

## Adding Aerodynamic Surfaces 

NoseCone =WESP.addNose(length=0.7, kind="vonKarman", distanceToCM=1.68)

FinSet = WESP.addTrapezoidalFins(
    n= 4,
    span= 0.27,
    rootChord= 0.35, 
    tipChord= 0.08, 
    distanceToCM= -0.86,
    cantAngle= 0, 
    radius= None, 
    airfoil= None,
)

# Tail = Rocket.addTail(
#     topRadius=, bottomRadius=, length=, distanceToCM=
# )

WESP.allInfo()

## Add Parachutes 

def drogueTrigger(p,y):
    # p = pressure
    # y = [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
    # activate drogue when vz < 0 m/s.
    return True if y[5] < 0 else False

def mainTrigger(p,y):
    # p = pressure
    # y = [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
    # activate main when vz < 0 m/s and z < 800 + 1400 m (+1400 due to surface elevation).
    return True if y[5] < 0 and y[2] < 800 + 1400 else False

mainChute =WESP.addParachute(
    "Main", 
    CdS=10.0,
    trigger=mainTrigger, 
    samplingRate=105, 
    lag=1.5, 
    noise=(0,8.3, 0.5)
)

DrogueChute =WESP.addParachute(
    "Drogue", 
    CdS=10.0,
    trigger=mainTrigger, 
    samplingRate=105, 
    lag=1.5, 
    noise=(0,8.3, 0.5)
)

## Simating Flight 

Flight = Flight(
    rocket=WESP, 
    environment=Env,
    inclination=launchRail.railOrientation, 
    heading=0 
)

Flight.allInfo()