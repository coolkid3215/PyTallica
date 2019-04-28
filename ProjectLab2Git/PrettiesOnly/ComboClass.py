import time
#!/usr/bin/env python
from IOPi import IOPi

class guitar:
    def __init__(self,info):
        self.info = info
        if len(self.info) == 1:
            # self.pluck = []
            self.B = info[0]


#            print('we are doing plucking stuff on bus ', self.B)
            # print('Bus', self.B)
            # print('strings', self.pluck)

        elif len(self.info) == 5:
            # self.info = info
            self.B = info[0]
            self.enable = info[1]
            self.steps = info[2]
            self.direction = info[3]
            self.stepper = info[4]
#            print('Bus:', self.B)
#            print('Enable is tied to pin', self.enable)
#            print('steps is tied to pin ', self.steps)
#            print('direction is tied to pin ',self.direction)
        else:
            print('boi ya goofed')


        if self.B == 1:
            self.bus = IOPi(0x20)  #Bus 1 adress
#            print('Bus 1 initialized')

            self.bus.set_port_direction(0, 0x00)   # pins 1-8 are outputs
            self.bus.write_port(0, 0x00)   #currently all False
#            print('Bus 1 port 0 initialized')

            self.bus.set_port_direction(1, 0x00)   # pins 9-16 are outputs
            self.bus.write_port(1, 0x00)   #currently all False
#            print('Bus 1 port 1 initialized')
        elif self.B == 2:
            self.bus = IOPi(0x21)   #Bus 2 address
#            print('Bus 2 initialized')
            if len(self.info) == 1:
                self.bus.set_port_direction(0, 0x00)   # pins 1-8 are outputs
#                self.bus.write_port(0, 0x00)   #currently all False
#                print('Bus 2 port 0 initialized')

            elif len(self.info) == 5:
                self.bus.set_port_direction(1, 0x00)   # pins 1-8 are outputs
                self.bus.write_port(1, 0x00)   #currently all False
#                print('Bus 2 port 0 initialized')

    def step(self,takeSteps,dir,speed = 1,stayON=False):
            self.bus.write_pin(self.enable,False)
           # turn = True
            statement = 'down Fret'
            if self.stepper <= 2:
                if dir == 2:
                    turn = False
                    statement = 'down Fret'
                elif dir == 1:
                    turn = True
                    statement = 'up Fret'
            elif self.stepper > 2: #handles upside down steppers
                if dir == 1:
                    turn = False
                    statement = 'down Fret'
                elif dir == 2:  #down fret
                    turn = True
                    statement = 'up Fret'
            self.bus.write_pin(self.direction,turn)
            count = 0
            delay = 0.0025/speed
            for count in range(takeSteps):
                self.bus.write_pin(self.steps,True)
                self.bus.write_pin(self.steps,False)
                # print('step: ',count)
                #print(self.steps,True)
                #print(self.steps,False)
                time.sleep(delay)

            if stayON == False:
                self.bus.write_pin(self.enable,True)
                print('power is no longer going to the motor')
            print('The stepper should have turned ',takeSteps, 'steps ',statement)
            return 1

    def Plucking(self,desiredPin,position):
        self.bus.write_pin(desiredPin,position)
#        print('played pick on pin ',desiredPin, 'it is', position)
        return 1
