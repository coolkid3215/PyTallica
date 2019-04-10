import time
#import RPi.GPIO as gpio
#!/usr/bin/env python
# from IOPi import IOPi
class Stepper:
        def __init__(driver,info):
            driver.info = info
            driver.BUS = info[0]
            driver.enable = info[1]
            driver.steps = info[2]
            driver.direction = info[3]
            # if driver.BUS == 2:
            #     driver.bus = IOPi(0x21)  #Different bus? hopefully...
            #     driver.bus.set_port_direction(1, 0x00)   # pins 9-16 are outputs
            #     driver.bus.write_port(1, 0x00)   #currently all False
            # else:
            #     driver.bus = IOPi(0x20)  #Different bus? hopefully...
            #     driver.bus.set_port_direction(0, 0x00)   # pins 1-8 are outputs
            #     driver.bus.write_port(0, 0x00)   #currently all False
            #       #Different bus? hopefully...
            #     driver.bus.set_port_direction(1, 0x00)   # pins 1-8 are outputs
            #     driver.bus.write_port(1, 0x00)   #currently all False
            #     #set enable to high, power isn't going to motor for now
            # driver.bus.write_pin(driver.enable,True)

            print('Bus:', driver.BUS)
            print('Enable is tied to pin', driver.enable)
            print('steps is tied to pin ', driver.steps)
            print('direction is tied to pin ',driver.direction)

        # def cleanUP(driver):
        #     driver.bus.write_port(0, 0x00)   #currently all False

        #step the motor
    # steps = number of steps to take
    # dir = direction stepper will move
    # speed = defines the denominator in the waitTime equation: waitTime = 0.000001/speed. As "speed" is increased, the waitTime between steps is lowered
    # stayOn = defines whether or not stepper should stay "on" or not. If stepper will need to receive a new step command immediately, this should be set to "True." Otherwise, it should remain at "False."

        def step(driver,takeSteps,dir,speed =1, stayON=False):
            # driver.bus.write_pin(driver.enable,False)
           # turn = True
            statement = 'down Fret'
            if dir == 2:    #up fret
                turn = False
                statement = 'up Fret'
            elif dir == 1:  #down fret
                turn = True
                statement = 'down Fret'
            # driver.bus.write_pin(driver.direction,turn)
            count = 0
            delay = 0.0025/speed
            for count in range(takeSteps):
                # driver.bus.write_pin(driver.steps,True)
                # driver.bus.write_pin(driver.steps,False)
                # print('step: ',count)
                #print(driver.steps,True)
                #print(driver.steps,False)
                time.sleep(delay)

            if stayON == False:
                # driver.bus.write_pin(driver.enable,True)
                print('power is no longer going to the motor')
            print('The stepper should have turned ',takeSteps, 'steps ',statement)
            return 1
