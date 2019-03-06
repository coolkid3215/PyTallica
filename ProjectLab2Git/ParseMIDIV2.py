#Author: Isaac Morales
#Notes: first off, let me just apologize to whoever is seeing this. I am still
#learning python so this is a very rudamentary and ugly way of parsing through
# a text file that used to be a midi file and extracting the note_off, note_ on,
#and note= information and putting it into another file containing only that
#info in a list under the format "note_on note="
#From there we remove the elements from this list containing the word note_off,
#we do this by replacing them with spaces in the list, we then create a new
#array containing only the 'note_on note=' thing, since we didnt do that earlier
# then we do some cute shit, we read thru this array and remove the parts of the
# element containing 'note_on note=' yes i know this is hardcoding, step off!
# Finally we create, you guessed it! another array, this one of integers,
#containing the what is now just numbers in the previous array

import array
import time

# import RPi.GPIO as GPIO
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(29,GPIO.OUT) #Thick E2 string 0
# GPIO.setup(31,GPIO.OUT) #A string 1
# GPIO.setup(33,GPIO.OUT) #D string 2
# GPIO.setup(35,GPIO.OUT) #G string 3
# GPIO.setup(37,GPIO.OUT) #B string 4
# GPIO.setup(40,GPIO.OUT) # thin E4 string 5
# GPIO.output(29,False)
# GPIO.output(31,False)
# GPIO.output(33,False)
# GPIO.output(35,False)
# GPIO.output(37,False)
# GPIO.output(40,False)

    #create two lists, one for note status, one for note value
def ReadIt(fname, term0, term1, term2):
    paper = open(fname + '.txt', 'r')
    myArray = []
    secArr= []
    if paper.mode == 'r':
            message = paper.read()
            words = message.split()
            for i in words:
                # print(i)
                if term0 in i :
                    myArray.append(i)
                elif term1 in i :
                    myArray.append(i)
                elif term2 in i:
                    secArr.append(i)
    ArrayPrinter(myArray, secArr)
    paper.close()

def ReadTime(fname):
    paper = open(fname + '.txt', 'r')
    timeStatus = []
    timeLen = []
    if paper.mode == 'r':
        message = paper.read()
        words  = message.split()
        for i in words:
            if term0 in i:
                timeStatus.append(i)
            elif term1 in i:
                timeStatus.append(i)
            elif 'time=' in i:
                timeLen.append(i)
            else:
                continue
        for i in range(len(timeStatus)):
            if timeStatus[i] == term0:
                timeDelay.append(timeLen[i])
            else:
                continue
        for i in range(len(timeDelay)):
            timeDelay[i]= timeDelay[i].split('time=',2)[1]

    #create another list, this one with the note status as the first part of
    #an element and the note as the second part of an element
def ArrayPrinter(myArray, secArr):
    size = len(secArr)
    size1 = len(myArray)
    Notes = []
    for i in range(size):
        Notes.append(myArray[i] +' '+ secArr[i])
    # print(Notes)
    OnlyOn(Notes)

    #now we write this new 2D list into a text file, it's a surprise tool that
    #wil help us later ;)
def OnlyOn(Notes):
    OnArray=fname+'onArr.txt'
    paper = open(OnArray, 'w+')
    for i in range(len(Notes)):
        if term1 in Notes[i]:
            Notes[i] = ' '
        else:
            continue
    on =[]
    for i in range(len(Notes)):
        if Notes[i] != ' ':
            on.append(Notes[i])
        else:
            continue
    for i in range(len(on)):
        paper.write(on[i] + '\n')
    paper.close()
    TakeNums(OnArray,Notes)

    #FINALLY(for now anyways) we extract the numbers corresponding to notes from
     #the list and put them into an integer aray to use later..
def TakeNums(OnArray, Notes):
    Numbers=[]
    for i in range(len(Notes)):
        if Notes[i] != ' ':
            Numbers.append(Notes[i])

    Numbers=[i.split('note_on note=',2)[1] for i in Numbers]
    # print(Numbers)
    # print(len(Numbers))
    NoteNums = array.array('i',(0 for i in range(0,len(Numbers))))
    for x in range(len(NoteNums)):
        NoteNums[x] = int(Numbers[x])
        # print(NoteNums[x])
    GimmeString(NoteNums)



def GimmeString(NoteNums):
    for i in range(len(NoteNums)):
        if NoteNums[i] <=88 and NoteNums[i] >= 64:   #E4
            NoteNums[i] = 64
        elif NoteNums[i] <= 63 and NoteNums[i] >= 59:    #B3
            NoteNums[i] = 59
        elif NoteNums[i] <= 58 and NoteNums[i] >=55: #G3
            NoteNums[i] = 55
        elif NoteNums[i] <= 54 and NoteNums[i] >= 50:    #D2
            NoteNums[i] = 50
        elif NoteNums[i] <= 49 and NoteNums[i] >=45: #A2
            NoteNums[i] =45
        elif NoteNums[i] <=44 and NoteNums[i] >=40:  #E2
            NoteNums[i] = 40
        else:
            continue
    LetsPlayOpen(NoteNums)

# OpenStrings = []
# OpenStrings.append([40,'e2',29])
def LetsPlayOpen(NoteNums): #eventually this will take in sleep time
    OpenStrings = [[40,'E2',29],[45,'A2',31],[50,'D2',33],[55,'G3',35],[59,'B3',37],[64,'E4',40]]
    signal = array.array('B',(False for i in range(0,len(OpenStrings))))
    for i in range(len(NoteNums)):
        for n in range(len(OpenStrings)):
            if NoteNums[i] is OpenStrings[n][0]:
                if signal[n] == False:
                    signal[n] = True
                elif signal[n] == True:
                    signal[n] = False
                else:
                    continue
                print('play ' +OpenStrings[n][1], signal[n])
                # GPIO.output(OpenStrings[n][2],signal[n])
                print(timeDelay[i])
                time.sleep(float(timeDelay[i]))

            # else:
            #     continue
    # print(OpenStrings)
#This is for JT's part
notes_dict = {}
def Dictionary():
    fname1 ='noteSteps'
    paper = open(fname1 + '.txt','r')
    if paper.mode == 'r':
        Notes = paper.readlines()
        Notes = [i.split('\n',2)[0]for i in Notes]
        NoteVals = [i.split('\t',2)[0]for i in Notes]
        StepPos = [i.split('\t',2)[1]for i in Notes]
        for x,y in zip(NoteVals, StepPos):
            notes_dict[x] = y
        # for x,y in notes_dict.items():
        #     print(x,y)
        paper.close()

fname = input('what file are you looking for? \t')
# fname = Nothing
term0 = 'note_on'
term1 = 'note_off'
term2 = 'note='
timeDelay =[]
Dictionary()
ReadTime(fname)
ReadIt(fname,term0, term1, term2)
