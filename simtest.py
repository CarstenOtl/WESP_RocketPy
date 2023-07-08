from rocketpy import Environment, Rocket, SolidMotor, Flight
# help(Flight)

# Launch-related functions:
class launchDay():
    date=(2023,7,4,15) #yyyymmdd+UTC
    

class launchSite():
    launchSiteName = "Straubing"
    latitude = 48.8777  #º
    longitude = 12.5802 #º
    elevation = 322     #m
    date = launchDay.date
    timeZone = 'UTC'

class launchRail():
    railLength=6.5     #m
    railOrientation=88   #º with respect to ground


# Engine-related functions:
class engineSelection():
    thrustSource="../data/motors/Aerotech_J180T.eng", # Change to J180T eng file
    burnOut=4.5,
    grainNumber=5,
    grainSeparation=5/1000,
    grainDensity=1815,
    grainOuterRadius=33/1000,
    grainInitialInnerRadius=15/1000,
    grainInitialHeight=120/1000,
    nozzleRadius=33/1000,
    throatRadius=11/1000,
    interpolationMethod='linear'

# Rocket dimensional functions:
class rocketDimensions():
    mass=20     #kg
    radius=0.1   #m
    inertiaI=6      #TBO from Structures?
    inertiaZ=0.05   #TBO from Structures?
    distanceRocketNozzle=-1 #TBO from Structures?
    distanceRocketPropellant=-1 #TBO from Structures?
    powerOffDrag='../data/calisto/powerOffDragCurve.csv' #TBD
    powerOnfDrag='../data/calisto/powerOnDragCurve.csv' #TBD

# Rocket component functions:
class nosecone():
    length=0.7
    kind="vonKarman"
    distanceToCM=1.68

class fins():
    finNumber=4
    finSpan=0.27
    rootChord=0.35
    tipChord=0.08
    distanceToCM=-0.86  # -ve bcoz is behind

# Recovery system functions:
def drogueTrigger(p, y):
    return True if y[5] < 0 else False

def mainTrigger(p, y):
    return True if y[5] < 0 and y[2] < 800 else False
 

def main():
    print("Welcome to WESP's first rocket simulation:")

    # 1. Define Environment variables:
    Env = Environment(
        railLength=launchRail.railLength,
        date=launchDay.date,
        latitude=launchSite.latitude,
        longitude=launchSite.longitude,
        elevation=launchSite.elevation,
        timeZone=launchSite.timeZone
    )
    # Initialize environment
    Env.setAtmosphericModel(type='Forecast',file='GFS')

    # 2. Create a sample solid Engine:
    J180T = SolidMotor(
        thrustSource=engineSelection.thrustSource,
        burnOut=engineSelection.burnOut,
        grainNumber=engineSelection.grainNumber,
        grainSeparation=engineSelection.grainSeparation,
        grainDensity=engineSelection.grainDensity,
        grainOuterRadius=engineSelection.grainOuterRadius,
        grainInitialInnerRadius=engineSelection.grainInitialInnerRadius,
        grainInitialHeight=engineSelection.grainInitialHeight,
        nozzleRadius=engineSelection.nozzleRadius,
        throatRadius=engineSelection.throatRadius,
        interpolationMethod=engineSelection.interpolationMethod)
    
    # 3. Define the rocket structure and components:
        # 3.1. Rocket Body
    WESP = Rocket(
        mass=rocketDimensions.mass,
        radius=rocketDimensions.radius,
        inertiaI=rocketDimensions.inertiaI,
        inertiaZ=rocketDimensions.inertiaZ,
        distanceRocketNozzle=rocketDimensions.distanceRocketNozzle,
        distanceRocketPropellant=rocketDimensions.distanceRocketPropellant,
        powerOffDrag=rocketDimensions.powerOffDrag,
        powerOnfDrag=rocketDimensions.powerOnDrag
    )    
        # 3.2. Set Rail Buttons
    WESP.setRailButtons([0.2,-0.5]) #TBO from GSE
        # 3.3 Set NoseCone Shape
    NoseCone = WESP.addNose(
        length=nosecone.length,
        kind=nosecone.kind,
        distanceToCM=nosecone.distanceToCM
    )
        # 3.4 Set Fins
    FinSet = WESP.addTrapezoidalFins(
        finNumber=fins.finNumber,
        finSpan=fins.finSpan,
        rootChord=fins.rootChord,
        tipChord=fins.tipChord,
        distanceToCM=fins.distanceToCM
    )

    # 4. Address the Recovery system:
    MainParachute = WESP.addParachute('Main',
                                CdS=10.0,
                                trigger=mainTrigger, 
                                samplingRate=105,
                                lag=1.5,
                                noise=(0, 8.3, 0.5))

    DrogueParachute = WESP.addParachute('Drogue',
                                CdS=1.0,
                                trigger=drogueTrigger, 
                                samplingRate=105,
                                lag=1.5,
                                noise=(0, 8.3, 0.5))

    # 5. Create a Flight object to simulate trajectory:
    TestFlight = Flight(
        rocket=WESP,
        environment=Env,
        inclination=launchRail.railOrientation,
        heading=0
    )

    # Print all data from simulation:
    TestFlight.allInfo()

if __name__ == "__main__":
    main()