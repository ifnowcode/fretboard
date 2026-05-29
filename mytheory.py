# _*_ coding: utf-8 _*_
#!/usr/bin/python3

# 12, 34, 56, 71 (Binary Analysis for even based time signatures)
# 123, 456, 712, (Trinary Analysis for odd based time signatures)
# movement of two is bad? i.e. 13,31,24,42,35,53,64,46,75,57
# https://www.youtube.com/watch?v=yknBXOSlFQs Songs that rip of classical music
# *** Canon in D by Johann Pachelbel ***
# 15, 63, 41, 45, (Binary Analysis for even based time signatures)
# 1 + 4, + 1 - 3, + 1 - 3, + 3 + 1, - 4
# moving by 5ths { 1 to 5 and 6 to 3 and 4 to 1 }, 4 to 5 is two 5ths
#
# *** All Out Of Love by Air Supply in G ***
# Intro {15, 64, 5} - Verse {41, 41, 43, 45} - Chorus {14, 45, 14, 45, 1}
# 1 + 4, + 1 - 2, + 1
#
# *** Bridge Over Troubled Water by Simon and Garfunkel in F ***
# 51, 51, 41, 51, 51, 51, 52, 32, 15 ...
# 5 - 4, + 4 - 4, + 3 - 3, + 4 - 4, + 4 - 4, + 4 - 4, + 4 - 3, + 1 - 1, - 1 + 4
# *** Danny Boy by Traditional in C ***
#
# *** Behind Blue Eyes by The Who in G ***
# 61, 54, - 45, 14, . , 34,
# Verse {{6,1}, {5,4}, {2ndDom}} ; Chorus1 {{4,5}, {1,4}, {5,?(E)}, {3,4}, {5,2ndDom}} ; Chorus2 (mod D) {{1,6}, {5,2ndDom}, {6,4}, {1,6}, {5,2ndDom}, {6,{5,2ndDom}
# 6 - 5, + 4 - 1 ... 4 + 1, - 4 + 3,
#
# https://tabs.ultimate-guitar.com/tab/misc-traditional/danny-boy-chords-1170325
# https://www.e-chords.com/chords/misc-irish/danny-boy
#
#
# https://realpython.com/playing-and-recording-sound-python/
# https://wiki.python.org/moin/PythonInMusic
# https://pypi.org/project/music/
# https://jythonmusic.me/
# https://www.codespeedy.com/build-a-music-player-with-tkinter-and-pygame-in-python/

# https://www.circleoffifths.com/page-7

# http://www.unicode-symbol.com/u/266D.html
# U+266D
import sys
import random

# TODO: Plug in chords rather then generating them to get the scales and chords in all keys etc.

chords = [1, 2, 3, 4, 5, 6]
weighted_chords = [1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 7]
weighted_key_indices = [0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8, 9, 10, 11, 11]

# https://www.basicmusictheory.com/
        #  https://www.basicmusictheory.com/c-major-scale
keys = [['C','Dm','Em','F','G','Am','Bdim  (x2343x)'],
        #  https://www.basicmusictheory.com/g-major-scale
        ['G','Am','Bm','C','D','Em','F#dim (xx421x)'],
        #  https://www.basicmusictheory.com/d-major-scale
        ['D','Em','F#m','G','A','Bm','C#dim (xxxo2o)'],
        # https://www.basicmusictheory.com/a-major-scale
        ['A','Bm','C#m','D','E','F#m','G#dim (xxx13o)'],
        # https://www.basicmusictheory.com/e-major-scale
        ['E','F#m','G#m','A','B','C#m','D#dim (xxx242)'],
        # https://www.basicmusictheory.com/b-major-scale
        ['B','C#m','D#m','E','F#','G#m','A#dim (x1232x)'],
        # https://www.basicmusictheory.com/f-sharp-major-scale
        ['F#','G#m','A#m','B','C#','D#m','E#dim (1231xx)'],
        # https://www.basicmusictheory.com/g-flat-major-scale
        ['Gb','Abm','Bbm','Cb','Db','Ebm','Fdim  (xx31ox)'],
        # https://www.basicmusictheory.com/d-flat-major-scale
        ['Db','Ebm','Fm','Gb','Ab','Bbm','Cdim  (x3454x)'],
        # https://www.basicmusictheory.com/a-flat-major-scale
        ['Ab','Bbm','Cm','Db','Eb','Fm','Gdim  (xx532x)'],
        # https://www.basicmusictheory.com/e-flat-major-scale
        ['Eb','Fm','Gm','Ab','Bb','Cm','Ddim  (xxo1x1)'],
        # https://www.basicmusictheory.com/b-flat-major-scale
        ['Bb','Cm','Dm','Eb','F','Gm','Adim  (xo121x)'],
        #  https://www.basicmusictheory.com/f-major-scale
        ['F','Gm','Am','Bb','C','Dm','Edim  (o12oxx)']
       ]
notes = []

# check args
if len(sys.argv) > 1 and sys.argv[1] is not None:
  amount = int(sys.argv[1])
  if (amount < 3): 
    print("Note! Number of chords will always be at least three")
    amount = 3
else:
  amount = random.randint(3, 12)

# get random key
key = random.choice(weighted_key_indices)

# get random chords
first = random.choice(chords)
notes.append(first)

for x in range(amount - 1):
  chord = random.choice(chords)
  while chord == notes[x]:
    chord = random.choice(chords)
  notes.append(chord)

# make sure the last chord is not the first chord so there is some kind of turnaround
last = random.choice(chords)
while last == first:
  last = random.choice(chords)

notes.append(last)

# key
print()
print("In the Key of", keys[key][0])
print()
print(notes)
print()

# generated chords in generated key by number
print("Jazz Notation:",end=' ')
for note in notes:
  relminor = note + 2
  if relminor == 8: relminor = 1
  print("{:6}".format(str(note) + "(" + str(relminor) + ")"), end=' ')
print()
print()

# generated chords in generated key by chord
if len(keys[key][0]) == 1:
  print("In Key of", keys[key][0], " :", end=' ')
else:
  print("In Key of", keys[key][0], ":", end=' ')
for note in notes:
  print("{:6}".format(keys[key][note-1]), end=' ')
print()
print()

# to assist in the creation of music
print("Resources ---")
print()

# print generated chords in all keys by chord
for key in keys:
  if len(key[0]) == 1:
    print("In Key of", key[0], " :", end=' ')
  else:
    print("In Key of", key[0], ":", end=' ')

  for note in notes:
    print("{:6}".format(key[note-1]), end=' ')
  print()

# print all keys
print()
print("Position     :",end=' ')
for i in range(1,8):
  print("{:6}".format(str(i)), end=' ')
print()
for key in keys:
  if len(key[0]) == 1:
    print("Key of", key[0], "    :", end=' ')
  else:
    print("Key of", key[0], "   :", end=' ')
  for note in key:
    print("{:6}".format(note), end=' ')
  print()

#-------------------------------------------------------------------------------
#
# <|:) Wizard
#
#-------------------------------------------------------------------------------
