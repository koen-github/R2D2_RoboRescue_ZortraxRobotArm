import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import threading
import matplotlib.animation as animation
import pylab
import time

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# x = angle of highest axis
# y = angle of lowest axis
# z = angle of yaw axis
motor = {'x': 0, 'y': 0, 'z': 0}

#the coordinated of the axes
baseW = {'x': 0, 'y': 0, 'z': 0}    # aka tip of the robot arm
baseY = {'x': 0, 'y': 0, 'z': 0}    # the coordinated of the base.
baseX = {'x': 0, 'y': 0, 'z': 0}

#distance between axles
lenXY = 15.5
lenXW = 18+22

def printPos():
    print('pos', sorted( baseW.items( ) ) )

def printMotor():
    print('motor',sorted(motor.items()))

def printBaseX():
    print('baseX',sorted(baseX.items()))

def printBaseY():
    print('baseY',sorted(baseY.items()))

def motor2pos():
    radZ = math.radians( motor['z'] )

    #calculated pos for baseX
    radY = math.radians( motor['y'] )
    baseX['z'] = math.cos( radY ) * lenXY
    radiusX = math.sin( radY) * lenXY
    baseX['x']= (math.cos( radZ ) * radiusX)
    baseX['y']= (math.sin( radZ ) * radiusX)

    #calculated pos for baswW (aka pos)(exept motor z as)
    radX = radY+math.radians( motor['x'] )
    baseW['z'] = (math.cos( radX ) * lenXW) + baseX['z']
    radiusW = (math.sin( radX ) * lenXW)+radiusX
    baseW['x']= (math.cos( radZ ) * radiusW)
    baseW['y']= (math.sin( radZ ) * radiusW)

def pos2motor(baseW):
    motor = {'x': 0, 'y': 0, 'z': 0}

    if baseW['x'] !=0:
        motor['z'] = math.degrees(math.atan(abs(baseW['y'])/abs(baseW['x'])))
    elif baseW['y']!=0:
        motor['z']=90
    if baseW['x']<0:
        motor['z']=180-motor['z']
    if baseW['y']<0:
        motor['z']=360-motor['z']

    topViewDistance = math.sqrt((baseW['x']**2)+(baseW['y']**2))#pytagoras
    realDist = math.sqrt((topViewDistance**2)+(baseW['z']**2))#pytagoras
    motor['x'] =180- math.degrees(math.acos(((lenXW**2)+(lenXY**2)-(realDist**2))/(2*lenXW*lenXY)))
    if topViewDistance != 0:
        motor['y'] = ((180-motor['x'])/2)-math.degrees(math.atan(baseW['z']/topViewDistance))
    else:
        motor['y']=0-(motor['x']/2)
    return motor



def animate(i):
    #updateGraph==true
    ax.clear()
    ax.axis([-20, 20, -20, 20])#this scales the hight properly
    ax.plot([0,0], [0,0],[-20,20], '-', label='line 1', linewidth=0)#sneaky manier om de hoogte in te stellen
    ax.plot([baseY['x'],baseX['x'],baseW['x']], [baseY['y'],baseX['y'],baseW['y']],[baseY['z'],baseX['z'],baseW['z']], 'o-', label='line 1', linewidth=10)

def showArm():
    ani = animation.FuncAnimation(fig, animate, interval=10)
    pylab.show()

# just a gimmick function to slowly move the arm in the graph
def goto(x,y,z):
    target = pos2motor({'x': x, 'y': y, 'z': z})
    target['x']=round(target['x'])
    target['y']=round(target['y'])
    target['z']=round(target['z'])
    target=shorterPath(target)
    while(target != motor):
        if target['x'] < motor['x']:
            motor['x']-=1
        elif target['x'] > motor['x']:
            motor['x']+=1
        if target['y'] < motor['y']:
            motor['y']-=1
        elif target['y'] > motor['y']:
            motor['y']+=1
        if target['z'] < motor['z']:
            motor['z']-=1
        elif target['z'] > motor['z']:
            motor['z']+=1
        motor2pos()
        time.sleep(0.1)

def shorterPath(angles):
    if angles['x']>180:
        angles['x']=angles['x']-360
    if angles['y']>180:
        angles['y']=angles['y']-360
    if angles['z']>180:
        angles['z']=angles['z']-360
    return angles


def tmp():
    motor['y']=0
    motor['x']=0
    motor['z']=0
    motor2pos()
    goto(10,5,24)
    printPos()
    printMotor()
    goto(10,10,24)
    printPos()
    printMotor()
    goto(10,10,29)
    printPos()
    printMotor()
    goto(10,10,29)
    printPos()
    printMotor()
    goto(10,5,24)
    printPos()
    printMotor()

def poop_GCode(x,y,z):
    tmp = pos2motor({'x': x, 'y': y, 'z': z})
    print("G1 X{0} Y{1} Z{2}".format(round(tmp['x']*-1,1),round(tmp['y']*-1,1),round(tmp['z'],1)))


#X:87.00 Y:0.00 Z:4.20 E:0.00 Count X: 87.01 Y:0.00 Z:4.20
#X:-129.90 Y:-24.30 Z:0.00 E:0.00 Count X: -129.90 Y:-24.30 Z:0.00
motor = {'x': -129.90, 'y': -24.30, 'z': 0}
motor2pos()
printPos()
tempX = baseW['x']
tempY = baseW['y']
tempZ = baseW['z']
print(tempX)
#target['x']=round(target['x'])
print('G21')
print('G90')

for x in range(0,50):
    poop_GCode(tempX+x*0.1,tempY+x*0.1,tempZ)


#for x in range(0,5):
#    poop_GCode(10,0,30)
#    poop_GCode(10,0,15)
#print('G1 X0 Y0 Z0')

#t = threading.Thread(target=tmp)
#t.daemon = True
#t.start()
#showArm()
#t.join()


#X:70.00 Y:4.60 Z:0.00 E:0.00 Count X: 70.00 Y:4.60 Z:0.00





