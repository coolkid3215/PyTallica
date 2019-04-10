#Author: Isaac Morales
# This is a prettier version of my original code for playing the guitar using
#the raspberry pi. Uncomment the GPIO stuff to play :)

import array as ar
import time
import mido
from mido import MidiFile
# import RPi.GPIO as GPIO
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(29,GPIO.OUT) #Thick E2 string 0
# GPIO.setup(31,GPIO.OUT) #A string 1
# GPIO.setup(33,GPIO.OUT) #D string 2
# GPIO.setup(35,GPIO.OUT) #G string 3
# GPIO.setup(37,GPIO.OUT) #B string 4
# GPIO.setup(40,GPIO.OUT) # thin E4 string 5

def menu():
    print('Welcome! please select where to start')
    print('1. Start from MIDI file ')
    print('2. Start from text file')
    choice = input(':)\n')
    return int(choice)

    #This function turns the MIDI file into a text file
def MIDItoTxt(fname):
    paper = open(fname + ".txt", "w+")
    for message in MidiFile(fname +'.mid').play():
        # time.sleep(message.time)
        if not message.is_meta:
            oof = str(message)
            paper.write(oof + '\n')
        else:
            continue
    paper.close()
    return True

#Read new text file
def ReadIt(fname):
    paper = open(fname + '.txt',)
    term0 = 'note_on'
    term1 = 'note_off'
    term2 = 'note='
    term3 = 'time='
    noteStatus = []
    note = []
    timeDelay = []
    if paper.mode == 'r':
        message = paper.read()
        words = message.split()
        for i in words:
            if term0 in i:  #note_on
                noteStatus.append(i)
            elif term1 in i:    #note_off
                noteStatus.append(i)
            elif term2 in i:    #note=
                note.append(i)
            elif term3 in i:    #time=
                timeDelay.append(i)
            else:
                continue
            noteCount = len(note)
            timeCount = len(timeDelay)
            if timeCount > noteCount:
                del timeDelay[timeCount-1]
            else:
                continue
        paper.close()
        # combine both arrays for the Midi values when on
        MidiNotes = []
        count = 0
        # print(len(timeDelay)) #number of time delays
        # print(len(note))  #number of notes
        for i in range(len(timeDelay)):
            if term0 in noteStatus[i]:
                temp = note[i].split(term2,2)[1]
                temp2 = timeDelay[i].split(term3,2)[1]
                MidiNotes.append([int(temp),float(temp2)]) #We kinda snapped with this sis
                count +=1
            else:
                continue
        # print(count)
        print('Midi notes and their time delays no modifications:\n',MidiNotes)
    return MidiNotes

def Open(MidiNotes,notePos,strings):

    StringE4 = []
    StringB3 = []
    StringG3 = []
    StringD2 = []
    StringA2 = []
    StringE2 = []
    for i in range(len(MidiNotes)):

        if MidiNotes[i][0] <=88 and MidiNotes[i][0] >= 64:   #E4
            StringE4.append([i,MidiNotes[i][0]])
            MidiNotes[i][0] = 64
        elif MidiNotes[i][0] <= 63 and MidiNotes[i][0] >= 59:    #B3
            StringB3.append([i,MidiNotes[i][0]])
            MidiNotes[i][0] = 59
        elif MidiNotes[i][0] <= 58 and MidiNotes[i][0] >= 55: #G3
            StringG3.append([i,MidiNotes[i][0]])
            MidiNotes[i][0] = 55
        elif MidiNotes[i][0] <= 54 and MidiNotes[i][0] >= 50:    #D2
            StringD2.append([i,MidiNotes[i][0]])
            MidiNotes[i][0] = 50
        elif MidiNotes[i][0] <= 49 and MidiNotes[i][0] >=45: #A2
            StringA2.append([i,MidiNotes[i][0]])
            MidiNotes[i][0] =45
        elif MidiNotes[i][0] <=44 and MidiNotes[i][0] >=40:  #E2
            StringE2.append([i,MidiNotes[i][0]])
            MidiNotes[i][0] = 40
        else:
            continue
        # print(MidiNotes)

    strings.append(StringE4)    #string 0
    strings.append(StringB3)    #string 1
    strings.append(StringG3)    #string 2
    strings.append(StringD2)    #string 3
    strings.append(StringA2)    #string 4
    strings.append(StringE2)    #string 5
    print('all 6 strings and the list of notes on each one ft. their index: \n',strings)
    # print(strings[0][0][0]) #[open string][index of info in list][member of 2D info] //0 = index , 1 =  Note
    # print(len(strings[1]))

    return (MidiNotes,strings)

def Dictionary(notePos):
   #Dictionary full of steps and notes
    fname1 ='noteSteps'
    paper = open(fname1 + '.txt','r')
    if paper.mode == 'r':
        Notes = paper.readlines()
        Notes = [i.split('\n',2)[0]for i in Notes]
        NoteVals = [i.split('\t',2)[0]for i in Notes]
        StepPos = [i.split('\t',2)[1]for i in Notes]
        for x,y in zip(NoteVals, StepPos):
            notePos[x] = y
        # for x,y in notePos.items():
        #     print(x,y)

        paper.close()
    return notePos



def LetsPlay(MidiNotes,strings,notePos):
    # OpenStrings =[]
    OpenStrings = [[64,'E4',40],[59,'B3',37],[55,'G3',35],[50,'D2',33],[45,'A2',31],[40,'E2',29]]
    pluck = ar.array('B',(False for v in range(0,len(OpenStrings))))
    for i in range(len(MidiNotes)):
        for string in range(len(strings)):
            for n in range(len(strings[string])):
                if int(strings[string][n][0]) == i:
                    # print(strings[string][n][0])
                    if n>0:
                        print('--------------------------------------------------------------------------')
                        print(i,' note: ',strings[string][n][1] )
                        print('index of previous note on this string: ',strings[string][n-1][0])
                        print('steps from the end: ',notePos[str(strings[string][n-1][1])])
                        print('index of current note on this string: ',strings[string][n][0])
                        print('steps from the end: ',notePos[str(strings[string][n][1])])
                        #difference between notes on the same string
                        difference = int(notePos[str(strings[string][n-1][1])]) - int(notePos[str(strings[string][n][1])])
                        print('move Stepper on string ',string,' aka ',OpenStrings[string][1],difference,' steps')
                        for x in range(len(OpenStrings)):
                            if MidiNotes[i][0] is OpenStrings[x][0]:
                                if pluck[x] == False:
                                    pluck[x] = True
                                elif pluck[x] == True:
                                    pluck[x] = False
                                else:
                                    continue
                                print('play ' + OpenStrings[x][1], pluck[x])

                                # GPIO.output(OpenStrings[n][2],pluck[n])
                                print('time delay: ',MidiNotes[i][1])
                                time.sleep(MidiNotes[i][1])

                    else:
                        print('--------------------------------------------------------------------------')
                        print('since this is the first note played on this string, move to its distance') #will def be changing considering we might start with open notes
                        print(i,' note: ',strings[string][n][1] )
                        difference = int(notePos[str(strings[string][n][1])])   #move to note we need
                        print('move Stepper on string ',string,' aka ',OpenStrings[string][1],'\t',difference,' steps')
                        for x in range(len(OpenStrings)):
                            if MidiNotes[i][0] is OpenStrings[x][0]:
                                if pluck[x] == False:
                                    pluck[x] = True
                                elif pluck[x] == True:
                                    pluck[x] = False
                                else:
                                    continue
                                print('play ' + OpenStrings[x][1], pluck[x])

                                # GPIO.output(OpenStrings[n][2],pluck[n])
                                print('time delay: ',MidiNotes[i][1])
                                time.sleep(MidiNotes[i][1])


def main():
    #Start here
    # GPIO.output(29,False)
    # GPIO.output(31,False)
    # GPIO.output(33,False)
    # GPIO.output(35,False)
    # GPIO.output(37,False)
    # GPIO.output(40,False)
    notePos={}  #declare an empty dictionary
    strings = []
    notePos = Dictionary(notePos) #Fill said dictionary w/ nots and pos
    print('Dictionary for referrence \n ', notePos)
    choice = menu() #start with a midi file or with a text file
    if int(choice == 1):    #Midi
        fname = input('Give me a file name please\n')
        Written = MIDItoTxt(fname)  #Convert to text
        if Written:
            MidiNotes = ReadIt(fname)   #parse thru text file
    elif int(choice == 2):  #text
        fname = input('Give me a file name please\n')
        MidiNotes = ReadIt(fname)   #parse thru text file

    (MidiNotes,strings) = Open(MidiNotes, notePos ,strings) #For Strumming, convert to open notes and

    print('Open string Midi Notes \n', MidiNotes)
    print('strings\n ', strings)


    LetsPlay(MidiNotes,strings, notePos)


if __name__ == '__main__':
    main()
