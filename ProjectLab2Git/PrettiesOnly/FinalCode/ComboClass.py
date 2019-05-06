import time
import array as ar
#!/usr/bin/env python
from IOPi import IOPi

class guitar:
    def __init__(self,info):
        self.info = info
        if len(self.info) == 1:
            # self.pluck = []
            self.B = info[0]

        elif len(self.info) == 5:
            # self.info = info
            self.B = info[0]
            self.enable = info[1]
            self.steps = info[2]
            self.direction = info[3]
            self.stepper = info[4]

        else:
            print('boi ya goofed')

        if self.B == 1:
            self.bus = IOPi(0x20)  #Bus 1 adress
            print('Bus 1 initialized')
            # self.bus.set_port_direction(0, 0x00)   # pins 1-8 are outputs

            # self.bus.set_port_direction(1, 0x00)   # pins 9-16 are outputs

        elif self.B == 2:
            self.bus = IOPi(0x21)   #Bus 2 address
            print('Bus 2 initialized')
            if len(self.info) == 1:
                self.bus.set_port_direction(0, 0x00)   # pins 1-8 are outputs
#                print('Bus 2 port 0 initialized')
            elif len(self.info) == 5:
                self.bus.set_port_direction(1, 0x00)   # pins 1-8 are outputs
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
#            print(takeSteps)
            if int(takeSteps) > 0:
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
            else:
                return 1

    def Plucking(self,desiredPin,position):
        self.bus.write_pin(desiredPin,position)
        print('played pick on pin ',desiredPin, 'it is', position)
        return 1


    def multi(self,strings,string,MidiNotes,notePos):
        OpenStrings = [[0,'E4',1,64],[1,'B3',2,59],[2,'G3',3,55],[3,'D2',4,50],[4,'A2',5,45],[5,'E2',6,40]]
        pluck = ar.array('B',(False for v in range(0,len(OpenStrings))))
        # delay = 0
        for index in range(len(MidiNotes)):

            if len(strings[string]) > 0:    #as long as its not an empty string
                for note in range(len(strings[string])):
                    if note > 0 and strings[string][note][0]==index:
                        print('thread ',string)
                        print(index)
                        prevPos = int(strings[string][note-1][1])-int(OpenStrings[string][3])
                        currPos = int(strings[string][note][1])-int(OpenStrings[string][3])
                        # print(currPos,'-',prevPos)
                        # the difference...........................please brain can i have ONE thing i-
                        difference = int(notePos[str(currPos)])- int(notePos[str(prevPos)])
                        direction = 2 if difference > 0 else 1
                        difference = abs(difference)

                        done = self.step(difference,direction)
                        if done and strings[string][note][0]==index:
                            if  strings[string][note][4] is OpenStrings[string][0]:
                                if pluck[string] == False:
                                    pluck[string] = True
                                elif pluck[string] == True:
                                    pluck[string] = False
                                self.pick = guitar([2])
                                wait = self.pick.Plucking(OpenStrings[string][2],pluck[string])
                                if wait:
                                    # index += 1
                                    #delay = float(strings[string][note][5])
                                    delay = float(strings[string][note][5]) - float(strings[string][note-1][5])         #honestly a stretch
                                    #so when we add up the delays we might still need to subtract prev same string note delay from curr note delays

                                    time.sleep(float(delay))

                    elif note == 0 and strings[string][note][0]==index:
                        print('first note on this string')
                        print('thread ',string)
                        print(index)
                        difference = int(strings[string][note][1]) - int(OpenStrings[string][3])
                        direction = 1 if difference > 0 else 2
                        difference = abs(difference)

                        difference = int(notePos[str(difference)])

                        done = self.step(difference,direction)
                        if done and strings[string][note][0]==index:

                            # for x in range(len(OpenStrings)):
                            #     if len(strings[x])> 0:
                            if  strings[string][note][4] is OpenStrings[string][0]:
                                if pluck[string] == False:
                                    pluck[string] = True
                                elif pluck[string] == True:
                                    pluck[string] = False
                                self.pick = guitar([2])
                                wait = self.pick.Plucking(OpenStrings[string][2],pluck[string])
                                if wait:
                                    time.sleep(float(strings[string][note][5]))
