'''
Created on Aug 27, 2012

@author: Glavin Wiechert
'''

#************************************************ FEATURES ******************************************
# Count notes with parameters
def countNotes(
               score,
               pitch,
               duration
               ):
    # Flatten score
    score = score.flat
    # Get notes from flattened score
    allNotes = score.notes
    # Count notes with *pitch* and *duration*
    count = 0
    for n in allNotes:
        if (pitch is not None and duration is None):
            #print "Pitch:",pitch
            if (n.pitch.name == pitch):
                count+=1
            #print n.pitch.name
        elif (duration is not None and pitch is None):
            #print "Duration:",duration
            if (n.duration.type == duration):
                count+=1
            #print n.duration.type
        elif (duration is not None and pitch is not None):
            #print "Pitch:",pitch,", ","Duration:",duration
            if (n.duration.type == duration and n.pitch.name == pitch):
                count+=1
            #print n, n.duration.type, n.pitch.name
        elif (duration is None and pitch is None):
            count+=1
            #print n, n.duration.type, n.pitch.name
    return count

# Count bars in score
def countBars(
              score
              ):
    # Get bars from score
    allBars = score.parts[0].getElementsByClass("Measure")
    return len(allBars)

# Get 'n' notes following after note with the pitch and duration provided.
def getFollowingNotes(
                      score,
                      pitch = None,
                      duration = None,
                      startpos = 0,
                      endpos = 1
                      ):
    # Flatten score
    score = score.flat
    # Get notes from flattened score
    allNotes = score.notes
    # Create array for storing found "following notes".
    followingNotes = []
    # Find notes with *pitch* and *duration*
    for n in range(len(allNotes)):
        note = allNotes[n-1]
        isFound = False
        if (pitch is not None and duration is None):
            if (note.pitch.name == pitch):
                isFound = True
        elif (duration is not None and pitch is None):
            if (note.duration.type == duration):
                isFound = True
        elif (duration is not None and pitch is not None):
            if (note.duration.type == duration and note.pitch.name == pitch):
                isFound = True
        elif (duration is None and pitch is None):
            isFound = True

        # If found note with desired pitch and duration
        if (isFound):
            # Get 'count' number of notes following after this note.
            followingNotes.append([])
            #followingNotes[len(followingNotes)-1].append(allNotes[n:count]) # Doesn't work.
            for a in range(min(len(allNotes)-n,endpos-startpos)):
                followingNotes[len(followingNotes)-1].append(allNotes[n+startpos+a])

    return followingNotes

#
def midiToList(
               midiStream
               ):
    # To Stream
    allNotes = midiStream.flat.notes
    #print midiStream
    # List
    list = []

    # Get properties
    mm = midiStream.flat.getElementsByClass(tempo.MetronomeMark)[0]
    #print mm
    miliPerQuarter = 1000 * mm.secondsPerQuarter()

    # Add note, start, duration, to list
    for n in range(len(allNotes)):
        currNote = allNotes[n]
        duration = currNote.seconds * 1000 # quarterLength * 1000 milliseconds per second
        start = currNote.offset * miliPerQuarter # mm.durationToSeconds(currNote.offset) * 1000 # (quarterLength to seconds) * 1000 milliseconds per second
        itemInfo = [currNote, start, duration]
        list.append(itemInfo)
    return list

# Create midi stream
def createGeneratedStream(
                          length, # length of generated stream should be the same as Data Stream if not greater.
                          metronome = None, # Metronome Mark
                          timeSig = None, # Time Signature
                          offsetConstant = 0, #
                          betweenNotes = 1, #
                          # subBeats = None # Number of sub-beats between each beat.
                          ):
    # Create streams
    s = stream.Stream()
    sP = stream.Part()
    # Metronome Mark
    if (metronome != None):
        mm = metronome
    else:
        mm = tempo.MetronomeMark(referent=1.0, number=60.0) # referent=multiplier of speed, number=BPM
    # Time Signature
    if (timeSig != None):
        ts = timeSig
    else:
        ts = meter.TimeSignature('4/4')
    # Create Notes
    sP.append(mm)
    sP.append(ts)
    pos = offsetConstant
    while (sP.duration.quarterLength <= length.quarterLength):
        currNote = note.Note('G')
        currNote.duration.quarterLength = 1.0
        sP.insert(pos,currNote)
        #print "pos:", pos
        pos += betweenNotes
    s.append(sP)
    #s.show('text')
    #s.show()
    midiStream = s
    # Convert to midi file object
    '''
    midiObject = midi.translate.streamToMidiFile(s)
    #print midiObject
    # Write to file
    # midiObject = midi.MidiFile()
    '''
    return midiStream

# Create midi stream
def createSampleDataStream(
                           length, # length of sample data
                           metronome = None, # Metronome Mark
                           timeSig = None, # Time Signature
                           error = 0 # maximum error in milliseconds
                           ):
    # Create streams
    s = stream.Stream()
    sP = stream.Part()
    # Metronome Mark
    if (metronome != None):
        mm = metronome
    else:
        mm = tempo.MetronomeMark(referent=1.0, number=60.0) # referent=multiplier of speed, number=BPM
    # Time Signature
    if (timeSig != None):
        ts = timeSig
    else:
        ts = meter.TimeSignature('4/4')
    # Create Notes
    sP.append(mm)
    sP.append(ts)
    offset = 0
    count = 0
    while ((sP.duration.quarterLength) <= length.quarterLength):
        if error != 0:
            #r = metronome.secondsPerQuarter()/error # ((random.randrange(0,2*error,1)-error)/1000.0)
            r = ((random.randrange(0,2*error,1)-error)/1000.0)
            #print "r:", r
            if (offset+r) < 0:
                r = 0
        else:
            r = 0
        #print "Random:", r

        currNote = note.Note('D')
        currNote.duration.quarterLength = 1.0
        #sP.append(currNote)
        sP.insert(offset + r, currNote)
        #print "Offset:", currNote.offset

        offset += 1                # CHANGE LATER
        count += 1
    s.append(sP)
    #s.show('text')
    #s.show()
    midiStream = s
    # Convert to midi file object
    '''
    midiObject = midi.translate.streamToMidiFile(s)
    #print midiObject
    # Write to file
    # midiObject = midi.MidiFile()
    '''
    return midiStream


#****************************************** Analysis *********************************************
def energy(
           dataStream, # data stream
           genStream    # generated stream, for comparing
           ):
    # Total cumulative energy
    e = 0

    # Convert to special list: [note, start, duration]
    dList = midiToList(dataStream)
    gList = midiToList(genStream)

    # Get list of starting times.
    dOffsets = []
    for d in dList:
        dOffsets.append(d[1]) # start time
    print "dOffsets:", dOffsets
    gOffsets = []
    for g in gList:
        gOffsets.append(g[1]) # start time
    print "gOffsets:", gOffsets

    # Iterate through all of dataStream's start times and find closest.
    for currOffset in dOffsets:
        # Source: http://stackoverflow.com/questions/9706041/finding-index-of-an-item-closest-to-the-value-in-a-list-thats-not-entirely-sort
        print "currOffset:", currOffset
        closest = min(enumerate(gOffsets), key=lambda x: abs(x[1]-currOffset))
        '''
        Explanation of the above line:
        enumerate(gOffsets) : see below for sample from Python documentation
            >>> seasons = ['Spring', 'Summer', 'Fall', 'Winter']
            >>> list(enumerate(seasons))
            [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
        closest = (index, offset)
            index : the index of the note in generated stream that is closest to this note.
            (key=) offset : absolute value of (x[1]-currOffset) if x = a sequential item in [(0, gOffsets[0]),(1, gOffsets[1]),...,(n, gOffsets[n])] as iterated to by the min() function
                            given that offset is the key, it uses that value when sorting and deciding what the minimum is.
        '''
        print "Closest:", closest
        #e += abs('%.1f' % round(closest[1], 1)-currOffset)
        e += abs(closest[1]-currOffset)
        print "e:", e

    '''
    # Energy = Energy (offset milliseconds) over time (duration of score in milliseconds)
    # Get properties
    mm = dataStream.flat.getElementsByClass(tempo.MetronomeMark)[0]
    milliPerQuarter = 1000 * mm.secondsPerQuarter()
    e = 1.0*e/(dataStream.duration.quarterLength * milliPerQuarter)
    '''

    # Energy = Energy (offset milliseconds) per note (notes per dataStream)
    e = 1.0*e/(len(dList))
    print "Energy:", e
    return e

def bestEnergy(
                  dataStream, #  Music Data to be used in comparison
                  threshold = 0 # Maximum acceptable energy value
                  ):

    matrix = []

    durationBetweenNotes = 1    # Positive number.
    durationOffset = 0  # Between -1.0 and +1.0
    offsetDirection = 1 # Direction of offset movement/change
    adjustVal = 0.1
    lastEnergy = float("inf")

    '''
    # Determine best durationOffset
    continuing = True
    while (continuing):
        # Create generated beat stream to compare with.
        genStream = createGeneratedStream(dataScore.duration, tempo.MetronomeMark(referent=1.0, number=60.0), meter.TimeSignature('4/4'), durationOffset, durationBetweenNotes)
        #genStream.show('text')
        # genStream.show()

        # Calculate energy
        e = energy(dataScore, genStream)
        #print "E:", e # print energy

        # Determine if energy is acceptable
        if (e <= threshold):
            continuing = False
        else:
            # Improve energy by moving durationOffset
            if (e >= lastEnergy):
                if (adjustVal < 0.001):
                    # continuing = False # Stop looping, but return line below. False==No case below threshold.
                    break
                durationOffset -= adjustVal # increment by the adjustVal from previous run
                adjustVal = adjustVal / 10 # 0.1 ==> 0.01 ==> 0.001
            durationOffset += adjustVal

            # 1) Check for directional improvement
            #if (e > lastEnergy):
            #    # Change direction
            #    offsetDirection *= -1
            # 2) Increment offset
            #    adjustVal = (offsetDirection * 0.001) # one millisecond, depending on offsetDirection
            #    durationOffset +=  adjustVal

            lastEnergy = e

    # Determine best durationBetweenNotes
    continuing = True
    adjustVal = 0.1 # decrement by one tenth of a second
    while (continuing):
        # Create generated beat stream to compare with.
        genStream = createGeneratedStream(dataScore.duration, tempo.MetronomeMark(referent=1.0, number=60.0), meter.TimeSignature('4/4'), durationOffset, durationBetweenNotes)
        #genStream.show('text')
        #genStream.show()

        # Calculate energy
        e = energy(dataScore, genStream)
        #print "E:", e # print energy

        # Determine if energy is acceptable
        if (e <= threshold):
            continuing = False
        else:
            # Improve energy by decreasing durationBetweenNotes
            # 1) Check for improvement
            if (e >= lastEnergy):
                if (adjustVal < 0.001):
                    # continuing = False # Stop looping, but return line below. False==No case below threshold.
                    return [False, e, genStream, durationOffset, durationBetweenNotes]
                durationBetweenNotes += adjustVal # increment by the adjustVal from previous run
                adjustVal = adjustVal / 10 # 0.1 ==> 0.01 ==> 0.001
            durationBetweenNotes -= adjustVal
            lastEnergy = e
    '''

    # Determine best durationOffset
    continuing1 = True
    while (continuing1):
        # Create generated beat stream to compare with.
        #genStream = createGeneratedStream(dataScore.duration, tempo.MetronomeMark(referent=1.0, number=60.0), meter.TimeSignature('4/4'), durationOffset, durationBetweenNotes)
        #genStream.show('text')
        # genStream.show()

        row = []

        # Determine best durationBetweenNotes
        continuing2 = True
        adjustVal = 0.1 # decrement by one tenth of a second
        while (continuing2):
            # Create generated beat stream to compare with.
            genStream = createGeneratedStream(dataScore.duration, tempo.MetronomeMark(referent=1.0, number=60.0), meter.TimeSignature('4/4'), durationOffset, durationBetweenNotes)
            #genStream.show('text')
            #genStream.show()

            # Calculate energy
            e = energy(dataScore, genStream)
            #print "E:", e # print energy

            row.append(random.random())

            # Determine if energy is acceptable
            if (e <= threshold):
                continuing2 = False
            else:
                # Improve energy by decreasing durationBetweenNotes
                # 1) Check for improvement
                if (e >= lastEnergy):
                    if (adjustVal < 0.001):
                        # continuing = False # Stop looping, but return line below. False==No case below threshold.
                        return [False, e, genStream, durationOffset, durationBetweenNotes]
                    durationBetweenNotes += adjustVal # increment by the adjustVal from previous run
                    adjustVal = adjustVal / 10 # 0.1 ==> 0.01 ==> 0.001
                durationBetweenNotes -= adjustVal
                lastEnergy = e

        matrix.append(row)

        # Calculate energy
        e = energy(dataScore, genStream)
        #print "E:", e # print energy

        # Determine if energy is acceptable
        if (e <= threshold):
            continuing1 = False
        else:
            # Improve energy by moving durationOffset
            if (e >= lastEnergy):
                if (adjustVal < 0.001):
                    # continuing = False # Stop looping, but return line below. False==No case below threshold.
                    break
                durationOffset -= adjustVal # increment by the adjustVal from previous run
                adjustVal = adjustVal / 10 # 0.1 ==> 0.01 ==> 0.001
            durationOffset += adjustVal
            '''
            # 1) Check for directional improvement
            if (e > lastEnergy):
                # Change direction
                offsetDirection *= -1
            # 2) Increment offset
                adjustVal = (offsetDirection * 0.001) # one millisecond, depending on offsetDirection
                durationOffset +=  adjustVal
            '''
            lastEnergy = e


    return [True, e, genStream, durationOffset, durationBetweenNotes]


def energyMatrix(
                 dataScore,
                 offsetStart = 0,
                 offsetEnd = 500,
                 offsetCount = 10,
                 betweenNotesStart = 200,
                 betweenNotesEnd = 1200,
                 betweenNotesCount = 10
                 ):
    # Create Matrix
    matrix = []
    maxVal = 0
    minVal = float("inf")

    for durationOffset in range(offsetStart, offsetEnd, int((offsetEnd-offsetStart)/offsetCount)):
        row = []
        for durationBetweenNotes in range(betweenNotesStart, betweenNotesEnd, int((betweenNotesEnd-betweenNotesStart)/betweenNotesCount)):
            print "o",durationOffset, "d",durationBetweenNotes
            genStream = createGeneratedStream(dataScore.duration, tempo.MetronomeMark(referent=1.0, number=60.0), meter.TimeSignature('4/4'), float(durationOffset)/1000.0, float(durationBetweenNotes)/1000.0)
            #print "GENERATED NEW STEAM"
            e = energy(dataScore, genStream)
            #print "Energy: ", e
            maxVal = max([e,maxVal])
            minVal = min([e,minVal])
            row.append(e)
        print [durationOffset, durationBetweenNotes]
        matrix.append(row)
    return [matrix, maxVal, minVal]

def bestChanceFollowing(
                        score,
                        pitch = None,
                        duration = None,
                        pos = 0
                        ):
    # Get the following notes after note with desired pitch and duration.
    followingNotes = getFollowingNotes(score, pitch, duration, pos, pos+1)
    allFollowingNotes = list(itertools.chain.from_iterable(followingNotes))

    if (len(allFollowingNotes) > 0):
        # Count occurrences of all
        #chances = Counter(list(itertools.chain.from_iterable(followingNotes))) # Possible option
        #bestChance = allFollowingNotes[0]

        # Setup working variables
        possiNotes = []     # Possible notes.
        counts = []         # Corresponding counts.

        # Iterate through all following notes
        for i in range(len(allFollowingNotes)):
            cNote = allFollowingNotes[i]  # Current note

            # Check if current note has a chance
            if (cNote in possiNotes):
                # Already in chances
                index = possiNotes.index(cNote)
                counts[index] = counts[index]+1
            else:
                # Add note
                possiNotes.append(cNote)
                counts.append(1)

        # Get index of maximum count
        idx = counts.index(max(counts))

        #return chances
        return possiNotes[idx]


#*********************************** Display **************************************************
def displayStream(
                  canvasImage,
                  width,
                  startLevel,
                  endLevel,
                  stream
                  ):
    streamList = midiToList(stream)
    print streamList
    totalLength = streamList[-1][1]
    for beat in streamList:
        x = int( beat[1] * (width/totalLength) )
        for y in range(startLevel, endLevel):
            y = int(startLevel+y)
            canvasImage.put("#000000",(x,y))
    return canvasImage

def drawMatrix(
               canvas,
               matrix = [],
               blocksize = [1,1],
               labelAxis = True
               ):
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            e = matrix[x][y]
            rgb = (int(255*e),int(255*e),int(255*e))
            colour = rgb_to_hex(rgb)
            canvas.create_rectangle(int(x*blocksize[0]), int(y*blocksize[1]), int(x*blocksize[0]+blocksize[0]), int(y*blocksize[1]+blocksize[1]), fill=colour, outline=colour)
            if ((labelAxis) and (x==(len(matrix)-1))):
                canvas.create_text(int((x+1.0)*blocksize[0]+1), int((y+0.5)*blocksize[1]),anchor="w", text=y)

            '''
            for w in range(blocksize[0]):
                for h in range(blocksize[1]):
                    canvasImage.put(color,((x+w),(y+h)))
             '''
        if (labelAxis):
            canvas.create_text(int((x+0.5)*blocksize[0]), int((y+1.0)*blocksize[1]+1), anchor="n", text=x)

    if (labelAxis):
        canvas.create_text(int((len(matrix)+1.5)*blocksize[0]+1), int((len(matrix[0])/2)*blocksize[1]), anchor="w", text="Duration Between Notes")
        canvas.create_text(int(len(matrix)/2*blocksize[0]), int((len(matrix[0])+1.5)*blocksize[1]+1), anchor="center", text="Offset")

    return canvas

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

#************************************* MISC **************************************************
def getUserInput(
                 defaultInput = ""
                 ):
    # user_input will be set to my_input if they just press enter
    user_input = raw_input("Enter a string (default: %s):\n" % defaultInput) or defaultInput
    return user_input

#***************************************** MAIN **********************************************

from music21 import *
from collections import Counter
import itertools
#import os
import random
import datetime

from Tkinter import Tk, Canvas, PhotoImage, mainloop
from math import sin

# Parse score
#midiStream = corpus.parse('bach/bwv324.xml')
#midiStream.show()
#midiStream.show('text')

# Parse MIDI File
midiPath = "/Users/glavin/Dropbox/Workspaces/SMU/Dr._Oore/chopin.mid"  # "/Users/glavin/Dropbox/Workspaces/SMU/Dr._Oore/mazurka_2.mid"
#midiPath = getUserInput("/Users/glavin/Dropbox/Workspaces/SMU/Dr._Oore/mazurka_2.mid")
'''
fp = os.path.join(common.getSourceFilePath(), 'midi', 'testPrimitive',  'test05.mid')
mf = midi.MidiFile()
mf.open(midiPath)
mf.read()
mf.close()
midiStream = midi.translate.midiFileToStream(mf)
midiStream.show()
'''
''' # *****************
midiStream = converter.parseFile(midiPath)
midiObject = midi.translate.streamToMidiFile(midiStream)
''' # *******************
#print "Printing midiStream.show():"
#midiStream.show('text')

#print "Printing midiObject:"
#print midiObject
'''
print countNotes(midiScore,"G","quarter")
# returns: 5 "G"-quarter notes
print countBars(midiScore)
# returns: 9 bars
print getFollowingNotes(midiScore,"G","quarter",0,1)
print bestChanceFollowing(midiScore, "G", "quarter", 0)
'''


dataScore = createSampleDataStream(duration.Duration(5),tempo.MetronomeMark(referent=1.0, number=60.0),meter.TimeSignature('4/4'),100)
#dataScore = createSampleDataStream(duration.Duration(4),tempo.MetronomeMark(referent=1.0, number=60.0),meter.TimeSignature('4/4'),0)
dataScore.show('text')
#dataScore.show()

#genScore = createGeneratedStream(duration.Duration(10), metronome = None, timeSig = None, offsetConstant = 0.0, betweenNotes = 0.1)
#genScore.show('text')
# genScore.show()

# Test combine streams
'''
s = stream.Stream()
s.insert(0,dataScore.parts[0])
s.insert(0,genScore.parts[0])
s.show('text')
s.show()
'''

#e = energy(dataScore, genScore)
e = bestEnergy(dataScore, 10)
print "E:", e
e[2].show('text')

'''
class energyDisplay(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        pass

if __name__ == "__main__":
    app = energyDisplay(None)
    app.title('Energy Display')
    app.mainloop()
'''

WIDTH, HEIGHT = 500, 500
window = Tk()
canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="#ffffff")
canvas.pack()
#img = PhotoImage(width=WIDTH, height=HEIGHT)
#canvas.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")

'''
for x in range(4 * WIDTH):
    y = int(HEIGHT/2 + HEIGHT/4 * sin(x/80.0))
    img.put("#000000", (x//4,y))
'''
#img = displayStream(img, WIDTH, 10, 10, e[2])
#img = displayStream(img, WIDTH, 20, 20, dataScore)

# Create Matrix
'''
matrix = []
for x in range(0, 400):
    row = []
    for y in range(0, 300):
       row.append( float(256 * float(y/300.0)) )
    matrix.append(row)
print matrix
'''

# Make all values of the matrix a float greater than 0 and less than 1
matrix, maxVal, minVal = energyMatrix(dataScore, offsetStart = 0, offsetEnd = 600, offsetCount = 10, betweenNotesStart = 200, betweenNotesEnd = 1400, betweenNotesCount = 20)
#matrix = []
print "Matrix1:",matrix

for x in range(0, len(matrix)):
    row = []
    for y in range(0, len(matrix[x])):
       matrix[x][y] /= maxVal
    #matrix.append(row)
print "Matrix2:", matrix

# Draw Matrix - for debugging
startTime = datetime.datetime.now()
canvas = drawMatrix(canvas = canvas, matrix=matrix, blocksize=[20,20])
#canvas.create_rectangle(int(50), int(100), int(200), int(200), fill="red")
#canvas.create_rectangle(int(100), int(50), int(300), int(300), fill="blue")
endTime = datetime.datetime.now()
print "Draw time:", (endTime-startTime).microseconds
window.mainloop()
