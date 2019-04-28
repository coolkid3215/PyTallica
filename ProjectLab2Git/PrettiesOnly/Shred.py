#Author: Isaac Morales
# This is a prettier version of my original code for playing the guitar using
#the raspberry pi.
#!/usr/bin/env python

import array as ar
import time
import mido
from mido import MidiFile
from ComboClass import guitar

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
        for j in range(len(timeDelay)):
            print( noteStatus[j],timeDelay[j])

        sel = input('on or off? \n')

        for i in range(len(timeDelay)):
            if sel == 'on':
                if term0 in noteStatus[i]:
                    temp = note[i].split(term2,2)[1]
                    temp2 = timeDelay[i].split(term3,2)[1]
                    MidiNotes.append([int(temp),float(temp2)]) #We kinda snapped with this sis
                    count +=1
                else:
                    continue
            elif sel == 'off':
                if term1 in noteStatus[i]:
                    temp = note[i].split(term2,2)[1]
                    temp2 = timeDelay[i].split(term3,2)[1]
                    MidiNotes.append([int(temp),float(temp2)]) #We kinda snapped with this sis
                    count +=1
                else:
                    continue

        # print(count)
        print('Midi notes and their time delays for this song no modifications:\n',MidiNotes)
    return MidiNotes

def Open(MidiNotes,notePos,strings):
    StringE4 = []
    StringB3 = []
    StringG3 = []
    StringD2 = []
    StringA2 = []
    StringE2 = []
    for i in range(len(MidiNotes)):
        if MidiNotes[i][0] <=71 and MidiNotes[i][0] >= 66:   #E4
    # index, note, string as string, finger flag, string as number, time delay of note
            StringE4.append([i,MidiNotes[i][0],'StringE4',0,0,MidiNotes[i][1]])
            MidiNotes[i][0] = 64
            # StringE4.append(64)
        elif MidiNotes[i][0] <= 65 and MidiNotes[i][0] >= 60:    #B3
            StringB3.append([i,MidiNotes[i][0],'StringB3',0,1,MidiNotes[i][1]])
            MidiNotes[i][0] = 59
            # StringB3.append(59)
        elif MidiNotes[i][0] <= 59 and MidiNotes[i][0] >= 55: #G3
            StringG3.append([i,MidiNotes[i][0],'StringG3',0,2,MidiNotes[i][1]])
            MidiNotes[i][0] = 55
            # StringG3.append(55)
        elif MidiNotes[i][0] <= 54 and MidiNotes[i][0] >= 50:    #D2
            StringD2.append([i,MidiNotes[i][0],'StringD2',0,3,MidiNotes[i][1]])
            MidiNotes[i][0] = 50
            # StringD2.append(50)
        elif MidiNotes[i][0] <= 49 and MidiNotes[i][0] >=45: #A2
            StringA2.append([i,MidiNotes[i][0],'StringA2',0,4,MidiNotes[i][1]])
            MidiNotes[i][0] =45
            # StringA2.append(45)
        elif MidiNotes[i][0] <=44 and MidiNotes[i][0] >=40:  #E2
            StringE2.append([i,MidiNotes[i][0],'StringE2',0,5,MidiNotes[i][1]])   #index,note,string, flag
            MidiNotes[i][0] = 40
            # StringE2.append(40)
        else:
            continue
        # print(MidiNotes)
    strings.append(StringE4)    #string 0
    strings.append(StringB3)    #string 1
    strings.append(StringG3)    #string 2
    strings.append(StringD2)    #string 3
    strings.append(StringA2)    #string 4
    strings.append(StringE2)    #string 5
    # print('all 6 strings and the list of notes on each one ft. their index: \n',strings)
    print('-----------------------------------------')
    print('String 0 ranged 66 to 71: \n ',StringE4)
    print('-----------------------------------------')
    print('String 1 ranged 60 to 65: \n ',StringB3)
    print('-----------------------------------------')
    print('String 2 ranged 55 to 59: \n ',StringG3)
    print('-----------------------------------------')
    print('String 3 ranged 50 to 54: \n ',StringD2)
    print('-----------------------------------------')
    print('String 4 ranged 45 to 49: \n ',StringA2)
    print('-----------------------------------------')
    print('String 5 ranged 40 to 44: \n ',StringE2)
    print('-----------------------------------------')
    # print(strings[0][0][0]) #[open string][index of info in list][member of 2D info] //0 = index , 1 =  Note
    # print(len(strings[1]))
    # print(strings[2][1][2])
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

def Preview(MidiNotes,strings,notePos,pls):
    OpenStrings = [[0,'E4',1,64],[1,'B3',2,59],[2,'G3',3,55],[3,'D2',4,50],[4,'A2',5,45],[5,'E2',6,40]]
    pluck = ar.array('B',(False for v in range(0,len(OpenStrings))))     #since the picks are backwards now this may flop but idk
    if pls < len(MidiNotes):
        i = pls
        for i in range(len(MidiNotes)): #for evey note in the song
            for string in range(len(strings)):  #on ever string
                stringLen = len(strings[string])
                for n in range(stringLen):  #for every note on that string
                    if strings[string][n][0] == i:  #index of the notes have been spread thru out strings
                        if n>0: #not the first note on the string
                            print('--------------------------------------------------------------------------')
                            print(i,' note: ',strings[string][n][1] )
                            print('index of previous note on this string: ',strings[string][n-1][0])
                            # print('steps from the end: ',notePos[str(strings[string][n-1][1])])
                            print('index of current note on this string: ',strings[string][n][0])
                            # print('steps from the end: ',notePos[str(strings[string][n][1])])
                            difference = int(strings[string][n-1][1])- int(strings[string][n][1])   #distance b/w curent note on string and prev note on string
                            direction = 2 if difference > 0 else 1  #if pos: move fwd, neg: back
                            difference = abs(difference)

                            strings[string][n][3] = 1   #flag indicating current pos of finger

                            for b in range(len(strings)):  #check each string
                                changeLen = len(strings[b])
                                for note in range(changeLen): #check every note that is on that string
                                    if int(strings[b][note][3]) == 1  and b < string:  #explain this sis... #index,note,string, flag,string
                                        # print(strings[b][note][1],'-',strings[string][n][1])
                                        check =  int(strings[b][note][1]) - int(strings[string][n][1])   #EX: i,MidiNotes[i][0],'StringA2',0,4
                                        print(check)    #difference b/w current pos of stepper on a lower string and current note
                                        # print(b, 'out of ', string)
                                        print('index of note on string: ',note)
                                        print('Difference in question: ', difference)
                                        print('what we could change it to: ',check)
                                        if check < (difference-1) and check >=0:    #that -1 is a bandaid that idk what to replace with
                                            # print('in change loop: ',strings[b][note][3])
                                            # print(i,strings[b][note][2])
                                            print('Original: index: ',strings[string][n][0],' note: ',strings[string][n][1],'string:',
                                            strings[string][n][2],' finger pos: ',strings[string][n][3],'string:',strings[string][n][4])

                                            strings[string][n][0] = i   #same index
                                            strings[string][n][2] = strings[b][note][2] #give it a new string
                                            strings[string][n][3] = strings[b][note][3] #give it a new flag
                                            strings[string][n][4] = strings[b][note][4] #give it a new string numerically

                                            newPlacement = [strings[string][n][0],strings[string][n][1],strings[string][n][2],
                                            strings[string][n][3],strings[string][n][4],strings[string][n][5]]

                                            MidiNotes[i][0] = MidiNotes[n][0]   #reassign Midi Note(slowly weeding this out)
                                            MidiNotes[i][1] = MidiNotes[n][1]

                                            print('string: ',b,'note:',note,' of: ',changeLen)
                                            #insert newPLacement into the appropriate string. look for the correct position and move it there
                                            for q in range(len(strings)):
                                                tempLen =len(strings[q])
                                                for t in range(tempLen):        #fits within two values we'll use the index of the
                                                    if len(strings[q])>0 and q<string:
                                                        if( ((t > 0) and (t<(len(strings[q])-1))) and (strings[q][t+1][0] > strings[b][note][0]) and
                                                         (strings[q][t-1][0] < strings[b][note][0]) and (int(strings[q][t][4]) == int(strings[b][note][4])) and
                                                         (int(strings[b][note-1][3]) ==0)): # and (q<b)
                                                            strings[q].insert(int(t)+1,newPlacement)   #Insert new element into desired location

                                                            print('*******************Changed stuff********************')
                                                            print('New: index: ',strings[string][n][0],' note ',strings[string][n][1],
                                                            'string',strings[string][n][2],' finger pos ',strings[string][n][3],
                                                            'string',strings[string][n][4])

                                                            print('New difference: ', strings[string][n][1], '-',strings[b][note][1],'= ',int(strings[string][n][1] -strings[b][note][1]) )
                                                            del strings[string][n]  #delete old member of list

                                                            pls = i+1   #saves location
                                                            for f in range(len(strings)):
                                                                print('\nString:',f,strings[f])
                                                            print('Recursion time bb: ', pls)   #R*c*rs*on? in MY code?
                                                            strings = Preview(MidiNotes,strings,notePos,pls)    #got rid of index error bc my mind
                                                            return strings  #probably not used tbh




                            print('move Stepper on string ',string,' aka ',OpenStrings[string][1],difference,' steps')
                            for x in range(len(OpenStrings)):
                                if len(strings[x])> 0:
                                    if  strings[string][n][4] is OpenStrings[x][0]: #play, ft not a single use of MidiNote list
                                        if pluck[x] == False:
                                            pluck[x] = True
                                        elif pluck[x] == True:
                                            pluck[x] = False
                                        else:
                                            continue
                                        print('play ' + OpenStrings[x][1],'pick', pluck[x])
                                        strings[string][n-1][3] = 0;
                                        # GPIO.output(OpenStrings[n][2],pluck[n])
                                        print('time delay: ', strings[x][n][5]) #added the time delays to strings
                                        # time.sleep(MidiNotes[i][1])
                                else:
                                    continue
                        else:
                            print('--------------------------------------------------------------------------')
                            print('since this is the first note played on this string, move to its distance') #will def be changing considering we might start with open notes
                            print(i,' note: ',strings[string][n][1] )
                            usable = int(strings[string][n][1])-int(OpenStrings[string][3])
                            difference = int(notePos[str(usable)])   #move to note we need
                            print('move Stepper on string ',string,' aka ',OpenStrings[string][1],'\t',difference,' steps')
                            for x in range(len(OpenStrings)):
                                if len(strings[x])> 0:
                                    if  strings[string][n][4] == OpenStrings[x][0]:
                                        if pluck[x] == False:
                                            pluck[x] = True
                                        elif pluck[x] == True:
                                            pluck[x] = False
                                        else:
                                            continue
                                        print('play ' + OpenStrings[x][1],'pick pos', pluck[x])
                                        strings[string][n-1][3] = 0;
                                        # GPIO.output(OpenStrings[n][2],pluck[n])
                                        print('time delay: ',strings[x][n][5])
                                        # time.sleep(MidiNotes[i][1])
                                else:
                                    continue
    else:
        for f in range(len(strings)):   #if we make it to the end with no recursion, skedaddle
            print('String:',f,strings[f])
    return strings

def LetsPlay(MidiNotes,strings,notePos):

    # picks = guitar([2])
    S0 = guitar([1,1,2,3,0])
    S1 = guitar([1,4,5,6,1])
    S2 = guitar([1,7,8,9,2])
    S3 = guitar([1,10,11,12,3])
    S4 = guitar([1,13,14,15,4])
    S5 = guitar([2,9,10,11,5])

    OpenStrings = [[0,'E4',1,64],[1,'B3',2,59],[2,'G3',3,55],[3,'D2',4,50],[4,'A2',5,45],[5,'E2',6,40]]
    pluck = ar.array('B',(False for v in range(0,len(OpenStrings))))
    for i in range(len(MidiNotes)):
        for string in range(len(strings)):
            for n in range(len(strings[string])):
                if int(strings[string][n][0]) == i:
                    if n>0:
                        prevPos = int(strings[string][n-1][1])-int(OpenStrings[string][3])
                        currPos = int(strings[string][n][1])-int(OpenStrings[string][3])

                        difference = int(notePos[str(prevPos)])- int(notePos[str(currPos)])

                        direction = 2 if difference > 0 else 1
                        difference = abs(difference)
                        print('--------------------------------------------------------------------------')
                        print(i,' note: ',strings[string][n][1] )
                        print('index of previous note on this string: ',strings[string][n-1][0])
                        print('steps from the end: ',notePos[str(prevPos)])
                        print('index of current note on this string: ',strings[string][n][0])
                        print('steps from the end: ',notePos[str(currPos)])
                        print(prevPos, '-', currPos)
                        print(direction)
                        strings[string][n][3]=1

                        # subThis = 0
                        if strings[string][n][4] == 0:  #E4
                            done = S0.step(difference,direction)
                        elif strings[string][n][4] == 1:   #B3
                            done = S1.step(difference,direction)
                        elif strings[string][n][4] == 2:   #G3
                            done = S2.step(difference,direction)
                        elif strings[string][n][4] == 3:   #D2
                            done = S3.step(difference,direction)
                        elif strings[string][n][4] == 4:   #A2
                            done = S4.step(difference,direction)
                        elif strings[string][n][4] == 5:   #E2
                            done = S5.step(difference,direction)
                        else:
                            continue

                        if done:
                            print('move Stepper on string ',string,' aka ',OpenStrings[string][1],difference,' steps')
                            for x in range(len(OpenStrings)):
                                if len(strings[x])> 0:
                                    if  strings[string][n][4] is OpenStrings[x][0]:
                                        if pluck[x] == False:
                                            pluck[x] = True
                                        elif pluck[x] == True:
                                            pluck[x] = False
                                        else:
                                            continue
                                        print('play ', OpenStrings[x][1],'pin',OpenStrings[x][2],'pick', pluck[x])
                                        strings[string][n-1][3] = 0;
                                        picks = guitar([2])
                                        wait = picks.Plucking(OpenStrings[x][2],pluck[x])

                                        if wait:
                                            # totalDelay = float(strings[x][n][5]) - subThis
                                            #
                                            # print(strings[x][n][5],'-',subThis)
                                            # print('before:', totalDelay)
                                            # totalDelay = 0 if totalDelay <= 0.0 else totalDelay
                                            # print('time delay: ', totalDelay)
                                            time.sleep(float(strings[x][n][5]))
                                else:
                                    continue
                        else:
                            print('error at index ',n)
                            break
                    else:
                        print('--------------------------------------------------------------------------')
                        print('since this is the first note played on this string, move to its distance') #will def be changing considering we might start with open notes
                        print(i,' note: ',strings[string][n][1] )
                        difference = int(strings[string][n][1]) - int(OpenStrings[string][3])
                        direction = 1 if difference > 0 else 2
                        difference = abs(difference)
                        difference = int(notePos[str(difference)])
                        print('move Stepper on string ',string,' aka ',OpenStrings[string][1],'\t',difference,' steps')

                        subThis = 0
                        if strings[string][n][4] == 0:  #E4
                            done = S0.step(difference,direction)
                        elif strings[string][n][4] == 1:   #B3
                            done = S1.step(difference,direction)
                        elif strings[string][n][4] == 2:   #G3
                            done = S2.step(difference,direction)
                        elif strings[string][n][4] == 3:   #D2
                            done = S3.step(difference,direction)
                        elif strings[string][n][4] == 4:   #A2
                            done = S4.step(difference,direction)
                        elif strings[string][n][4] == 5:   #E2
                            done = S5.step(difference,direction)
                        else:
                            continue
                        if done:
                            for x in range(len(OpenStrings)):
                                if len(strings[x])> 0:
                                    if  strings[string][n][4] == OpenStrings[x][0]:
                                        if pluck[x] == False:
                                            pluck[x] = True
                                        elif pluck[x] == True:
                                            pluck[x] = False
                                        else:
                                            continue
                                        print('play ', OpenStrings[x][1],'pin',OpenStrings[x][2],'pick', pluck[x])
                                        strings[string][n-1][3] = 0;

                                        picks = guitar([2])
                                        wait = picks.Plucking(OpenStrings[x][2],pluck[x])

                                        if wait:
                                            # totalDelay = float(strings[x][n][5]) - subThis
                                            # totalDelay = 0.0 if totalDelay <= 0.0 else totalDelay
                                            # print('time delay: ', totalDelay)
                                            time.sleep(float(strings[x][n][5]))


                                else:
                                    continue

    return strings

def reset(strings,notePos):
    OpenStrings = [[0,'E4',1,64],[1,'B3',2,59],[2,'G3',3,55],[3,'D2',4,50],[4,'A2',5,45],[5,'E2',6,40]]
    S0 = guitar([1,1,2,3,0])
    S1 = guitar([1,4,5,6,1])
    S2 = guitar([1,7,8,9,2])
    S3 = guitar([1,10,11,12,3])
    S4 = guitar([1,13,14,15,4])
    S5 = guitar([2,9,10,11,5])
    for string in range(len(strings)):
        if len(strings[string]) >0:
            # for n in range(len(strings[string])):
            n = len(strings[string])-1
            difference = int(OpenStrings[string][3])-int(strings[string][n][1])
            direction = 1 if difference > 0 else 2
            difference = abs(difference)
            difference = int(notePos[str(difference)])
# index, note, string as string, finger flag, string as number, time delay of note
            if strings[string][n][4] == 0:  #E4
                done = S0.step(difference,direction)
            elif strings[string][n][4] == 1:   #B3
                done = S1.step(difference,direction)
            elif strings[string][n][4] == 2:   #G3
                done = S2.step(difference,direction)
            elif strings[string][n][4] == 3:   #D2
                done = S3.step(difference,direction)
            elif strings[string][n][4] == 4:   #A2
                done = S4.step(difference,direction)
            elif strings[string][n][4] == 5:   #E2
                done = S5.step(difference,direction)
            else:
                continue
            if done:
                print('moved Stepper on string ',string,' aka ',OpenStrings[string][1],difference,' steps')
            # print('moved stepper ',strings[string][n][4],  )

def main():
    #Start here

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

    # print('Open string Midi Notes \n', MidiNotes)
    print('strings\n ', strings)
    pls = 0
    unchanged = []
    strings = Preview(MidiNotes,strings, notePos,pls)
    # print(strings)


    # for f in range(len(strings)):
    #     if len(strings[f])>0:
    #         # for n in range(len(strings[f])):
    #         strings[f]=sorted(strings[f], key = lambda x : x[0])
    #     print('\nString:',f,strings[f])
    # print('These should now be sorted!:')

    strings = LetsPlay(MidiNotes,strings, notePos)
    print('strings\n ', strings)
    reset(strings,notePos)

    # print('got back')
    # # if(Yay==1):
    # for i in range(len(MidiNotes)):
    #     for string in range(len(strings)):
    #         if len(strings[string])>0:
    #             for wumbo in range(len(strings[string])):
    #                 if strings[string][wumbo][0]==i:
    #                     print(i,strings[string][wumbo][1],strings[string][wumbo][2],)
    #                 else:
    #                     continue
    #
    # print('done')

if __name__ == '__main__':
    main()
