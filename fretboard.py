# _*_ coding: utf-8 _*_
#!/usr/bin/python3

# Intervals, Notes & Postions

# Some Theory Notes
# https://www.8notes.com/piano_chord_chart/c7.asp
# https://en.wikipedia.org/wiki/Circle_of_fifths
# Cb,Gb,Db,Ab,Eb,Bb,F,C,G,D,A,E,B,F#,C#
# -------------------------
# 0 Unison = 0
# 1 Minor 2nd = 1/2
# 2 Major 2nd = 1
# 3 Minor 3rd = 1 1/2
# 4 Major 3rd = 2
# 5 Perfect 4th = 2 1/2
# 6 Augmented 4th = 3
# 7 Perfect 5th = 3 1/2
# 8 Minor 6th (Augmented 5th) = 4
# 9 Major 6th = 4 1/2
# 10 Minor 7th = 5
# 11 Major 7th = 5 1/2
# 12 Octave = 6

# https://medium.com/better-programming/how-to-learn-guitar-with-python-978a1896a47

# https://matplotlib.org/3.1.1/index.html
# https://matplotlib.org/3.1.0/gallery/color/named_colors.html
# https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.patches.Patch.html#matplotlib.patches.Patch.set_color

# https://briancaffey.github.io/2018/04/26/generating-music-from-guitar-tabs-with-python.html/
import argparse
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import enum
import os
import sys
add_paths = [
  f"{os.environ['_path_py_lib']}",
]
for path in reversed(add_paths):
  if path not in sys.path:
    sys.path.insert(0, path)

from printcon import *


# http://www.all-guitar-chords.com/

# TODO: support alternate tunings
# TODO: figure out notes based on key and interval
# TODO: figure out chord based on key and intervals
# TODO: plot specific patterns that have specific string locations
# TODO: plot chord based on chord only

# 1 Ionian
# 2 Dorian
# 3 Phrygian
# 4 Lydian
# 5 Mixolydian
# 6 Aeolian
# 7 Locrian

# https://www.guitarhabits.com/building-scales-using-the-whole-half-step-formula/
scales = {
  "major" : [0, 2, 4, 5, 7, 9, 11],             # 0R 1W 2W 3H 4W 5W 6W 7H 8R
  "minor" : [0, 2, 3, 5, 7, 8, 10],             # 0R 1W 2H 3W 4W 5H 6W 7W 8R
  "dorian" : [0, 2, 3, 5, 7, 9, 10],
  "phrygian" : [0, 1, 3, 5, 7, 8, 10],
  "major_pentatonic" : [0, 2, 4, 7, 9],
  "minor_pentatonic" : [0, 3, 5, 7, 10],
  "harmonic_minor" : [0, 2, 3, 5, 7, 8, 10],
  "mixolydian": [0, 2, 4, 5, 7, 9, 10],
  "minor_blues" : [0, 3, 5, 6, 7, 10],
  "locrian" : [0, 1, 3, 5, 6, 8, 10],
  "lydian" :[0, 2, 4, 6, 7, 9, 11],
  "blue_minor" :[0, 2 , 3, 5, 6, 7, 8, 10],
  "circleof5ths" :[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
  "chromatic" :[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
  "chromatic_rainbow" :[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
  "purple_trans" :[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
  "petonian" :[0, 2, 4, 5, 6, 7, 9, 10, 11],
}
# https://www.bellandcomusic.com/music-chords.html
# Chord names from http://www.all-guitar-chords.com/index.php?ch=C&mm=6&get=Get
# https://muted.io/chord-formulas-intervals/
# https://theoryandsound.com/chord-construction/
# https://appliedguitartheory.com/lessons/intervals-on-guitar/
# https://themusicambition.com/guitar-intervals/
# https://www.richmanmusicschool.com/articles/easy-chord-construction-formulas
# https://yourguitarbrain.com/chord-interval-chart-how-chords-are-made/ *******
# https://bandnotes.info/tidbits/scales/half-whl.htm
# search: how many steps in a diminished interval
# https://jadebultitude.com/how-to-work-out-augmented-and-diminished-intervals/
# https://musicstudent101.com/09-simple-intervals,-in-theory.html
# 3=4steps, b3=3steps
# major steps that are the base
# 1,2,3,4,5,6,7 ,8 ,9 ,10,11,12,13,14     Index
# 0,2,2,1,2,2,2 ,1 ,2 ,2 ,1 ,2 ,2 ,2 ,1   Steps
# 0,2,4,5,7,9,11,12,14,16,17,19,21,23,24  Accumulated Steps
# 1,3,5,7,9,11,13 = 0,4,7,11,14,17,21     
chords = {                    # Chord -
  '': [0,4,7],                # Major                         (1,3,5)
  '-5': [0,4,6],              # Major Diminished 5th
  '5': [0,7],                 # Power Chord
  '6': [0,4,7,9],             # Major 6th                     (1,3,5,6)
  '6/9': [0,4,7,9,14],        # Major 6/9                     (1,3,5,6,9)
  '7': [0,4,7,10],            # Dominant 7th
  '9': [0,4,7,11,14],         # Dominant 9th
  '11': [0,4,7,11,17],        # Dominant 11th - '11': [0,4,7,11,14,17], 
  '13': [0,4,7,11,21],        # Dominant 13th - '13': [0,4,7,11,14,17,21],
  'm': [0,3,7],               # Minor
  'm7': [0,3,7,10],           # Minor 7th
  'm9': [0,3,7,10,14],        # Minor 9th
  'm11': [0,3,7,17],          # Minor 11th
  'm13': [0,3,7,21],          # Minor 13th
  'm6': [0,3,7,9],            # Minor 6th
  'mmaj7': [0,3,7,11],        # Minor Major 7th
  'madd9': [0,3,7],           # Minor Add 9
  'm6add9': [0,3,7],          # Minor 6 Add 9
  'mmaj9': [0,3,7],           # Minor Major 9th
  'm7#5': [0,3,7],            # Minor 7 # 5
  'm7b5': [0,3,7],            # Half Diminished Minor 7
  'maj7': [0,4,7,11],     # Major 7th
  'maj9': [],             # Major 9th
  'maj11': [],            # Major 11th
  'maj13': [],            # Major 13th
  'maj9#11': [],          # Major 9 sharp 11
  'maj13#11': [],         # Major 13 sharp 11
  'add9': [],             # Major Add 9
  'add11': [],            # Major Add 11
  '6add9': [],            # Major 6 Add 9
  'maj7b5': [],           # Major 7 Flat 5
  'maj7#5': [],           # Major 7 Sharp 5
  'dim': [0,3,6],         # Diminished - https://splice.com/blog/what-is-a-diminished-chord/
  'dim7': [0,3,6],        # Diminished 7
  'halfdim': [0,3,6],     # Half Diminished
  'aug': [0,4,8],         # Augmented
  'aug7': [0,4,8],        # Augmented 7
  'sus4': [],             # Suspended 4th
  'sus2': [],             # Suspended 2nd
  'sus2sus4': [],         # Suspended 2nd 4th
  '7sus4': [],            # 7 Suspended 4th
  #'7sus4': [],            # Dominant 7th Suspended 4th
  '7b5': [],              # Dominant 7th Flat 5
  '7#5': [],              # Dominant 7th Sharp 5
  '7b9': [],              # Dominant 7th Flat 9
  '7#9': [],              # Dominant 7th Sharp 9
  '9b5': [],              # Dominant 9th Flat 5
  '9#5': [],              # Dominant 9th Sharp 5
  '11b9': [],             # Dominant 11th Flat 9
  '13#11': [],            # Dominant 13th Sharp 11
  '13b9': [],             # Dominant 13th Flat 9
  '7(b5,b9)': [],         # Dominant 7th Flat 5 Flat 9
  '7(b5,#9)': [],         # Dominant 7th Flat 5 Sharp 9
  '7(#5,b9)': [],         # Dominant 7 Sharp 5 Flat 9
  '7(#5,#9)': [],         # Dominant 7 Sharp 5 Sharp 9
  }


split_chords = [
  'C/E',
  'C/F',
  'C/G',
  'D/F#',
  'D/A',
  'D/Bb',
  'D/B',
  'D/C',
  'E/B',
  'E/C#',
  'E/D',
  'E/D#',
  'E/F',
  'E/F#',
  'E/G',
  'E/G#',
  'Em/B',
  'Em/C#',
  'Em/D',
  'Em/D#',
  'Em/F',
  'Em/F#',
  'Em/G',
  'Em/G#',
  'F/C',
  'F/D',
  'F/D#',
  'F/E',
  'F/G',
  'F/A',
  'Fm/C',
  'G/B',
  'G/D',
  'G/E',
  'G/F',
  'G/F#',
  'A/C#',
  'A/E',
  'A/F',
  'A/F#',
  'A/G',
  'A/G#',
  'Am/C',
  'Am/E',
  'Am/F',
  'Am/F#',
  'Am/G',
  'Am/G#'
  ]

# &#9837 or &#x266d for flat
# &#9838 or &#x266f for sharp
# a sufficiently long sequence of notes to slice from
whole_notes_sharp = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
whole_notes_flat  = ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']
whole_notes=whole_notes_sharp*5

# https://www.tunemybass.com/
# https://www.studybass.com/tools/tuning-notes/

# tunings
# https://www.guitarworld.com/lessons/11-alternate-tunings-every-guitarist-should-know
# https://guitargearfinder.com/guides/alternate-tunings/
guitar_five_string_standard_tuning=['E','A','G','B','E']   # standard tuning for six string
guitar_six_string_standard_tuning=['E','A','D','G','B','E']   # standard tuning for six string
guitar_seven_string_standard_tuning=['B','E','A','D','G','B','E']   # standard tuning for seven string
guitar_eight_string_standard_tuning=['G','B','E','A','D','G','B','E']   # standard tuning for eight string
guitar_six_string_dropD_tuning46=['D','A','D','G','B','E']      # drop D tuning for six string
guitar_six_string_dropD2_tuning46=['D','A','D','G','B','D']     # double drop D tuning for six string
guitar_six_string_openD_tuning46=['D','A','D','F#','A','D']     # open D tuning for six string
guitar_six_string_openE_tuning46=['E','B','E','G#','B','E']     # open E tuning for six string
guitar_six_string_openG_tuning46=['D','G','D','G','B','D']      # open G tuning for six string
guitar_six_string_openA_tuning46=['E','A','E','A','C#','E']     # open A tuning for six string
guitar_six_string_rainsong_tuning=['D','G','C','G','C','D']     # The Rain Song Tuning for six string
guitar_six_string_openC6_tuning46=['C','A','C','G','C','E']     # open C6 tuning for six string
guitar_six_string_openC_tuning46=['C','G','C','G','C','E']      # open C tuning for six string
guitar_six_string_eeeebe_tuning46=['E','E','E','E','B','E']     # Bruce Palmer modal tuning
guitar_six_string_ccccgc_tuning46=['C','C','C','C','G','C']     # Stills Palmer modal tuning (use thick strings)

bass_guitar_four_string_standard_tuning=['E','A','D','G']
bass_guitar_five_string_standard_tuning=['B','E','A','D','G']

violin_standard_tuning=['G','D','A','E']
cello_standard_tuning=['C','G','D','A']

banjo_standard_tuning=['G','D','G','B','D']
mandolin_standard_tuning=['G','D','A','E']
ukelele_standard_tuning=['G','C','E','A']

three_note_tuning=['G','A','D']
two_note_tuning=['G','A']
tub_bass_tuning=['G']

# double bass open strings are E1 A1 D2 G2
# six string guitar open strings are E2 A2 D3 G3 B3 E4
#

# TODO: visualize by numbers and intervals like this
# https://www.youtube.com/watch?v=jlScNZSWpX4

# guitars
strings_tub_bass=[1]
strings_guitar_two_note=[2,1]
strings_guitar_three_note=[1,2,1]
strings_ukelele=[4,3,2,1]
strings_violin=[4,3,2,1]
strings_cello=[4,3,2,1]
strings_mandolin=[4,3,2,1]
strings_banjo=[5,4,3,2,1]
strings_bass_guitar_four_string=[4,3,2,1]
strings_bass_guitar_five_string=[5,4,3,2,1]
strings_guitar_five_string=[5,4,3,2,1]
strings_guitar_six_string=[6,5,4,3,2,1]       #six_string=[1,2,3,4,5,6]
strings_guitar_seven_string=[7,6,5,4,3,2,1]   #seven_string=[1,2,3,4,5,6,7]
strings_guitar_eight_string=[8,7,6,5,4,3,2,1]

max_limiter=strings_guitar_eight_string

# settings
tuning_setup=guitar_six_string_standard_tuning
fretboard_setup=strings_guitar_six_string

# string limiters
double_tops=[1,2]
double_stops=[3,2]
three_strings=[3,2,1]
four_strings=[4,3,2,1]
five_strings=[5,4,3,2,1]
six_strings=strings_guitar_six_string
seven_strings=strings_guitar_seven_string
eight_strings=strings_guitar_eight_string
blackbird_style=[5,2]

#title = ''

class Fretboards(enum.Enum):
  Guitar = 1
  Guitar5s = 2
  Guitar6s = 1
  Guitar7s = 3
  Guitar8s = 4
  Bass = 5
  Bass4s = 5
  Bass5s = 6
  Cello = 7
  Violin = 8
  Mandolin = 9
  Banjo = 10
  Ukelele = 11
  TubBass = 12


def get_fretboard_from_string(name):
    if name == "Guitar":
      return Fretboards.Guitar
    elif name == "Guitar5s":
      return Fretboards.Guitar5s
    elif name == "Guitar6s":
      return Fretboards.Guitar6s
    elif name == "Guitar7s":
      return Fretboards.Guitar7s
    elif name == "Guitar8s":
      return Fretboards.Guitar8s
    elif name == "Bass":
      return Fretboards.Bass
    elif name == "Bass4s":
      return Fretboards.Bass4s
    elif name == "Bass5s":
      return Fretboards.Bass5s
    elif name == "Cello":
      return Fretboards.Cello
    elif name == "Violin":
      return Fretboards.Violin
    elif name == "Mandolin":
      return Fretboards.Mandolin
    elif name == "Banjo":
      return Fretboards.Banjo
    elif name == "Ukelele":
      return Fretboards.Ukelele
    elif name == "TubBass":
      return Fretboards.TubBass
    else:
      return Fretboards.Guitar


def set_tuning(tuning):
  global tuning_setup
  loginfo("Setting Tuning to", tuning)
  tuning_setup=tuning


def set_strings(guitar):
  global fretboard_setup
  loginfo("Setting Strings to", guitar)
  fretboard_setup=guitar


def set_to_tub_bass():
  loginfo("Setting Fretboard to Tub Bass")
  set_tuning(tub_bass_tuning)
  set_strings(strings_tub_bass)


def set_to_banjo():
  loginfo("Setting Fretboard to Banjo")
  set_tuning(banjo_standard_tuning)
  set_strings(strings_banjo)


def set_to_mandolin():
  loginfo("Setting Fretboard to Mandolin")
  set_tuning(mandolin_standard_tuning)
  set_strings(strings_mandolin)


def set_to_violin():
  loginfo("Setting Fretboard to Violin")
  set_tuning(violin_standard_tuning)
  set_strings(strings_violin)


def set_to_cello():
  loginfo("Setting Fretboard to Cello")
  set_tuning(cello_standard_tuning)
  set_strings(strings_cello)


def set_to_ukelele():
  loginfo("Setting Fretboard to Ukelele")
  set_tuning(ukelele_standard_tuning)
  set_strings(strings_ukelele)


def set_to_guitar():
  loginfo("Setting Fretboard to Guitar")
  set_tuning(guitar_six_string_standard_tuning)
  set_strings(strings_guitar_six_string)


def set_to_bass():
  loginfo("Setting Fretboard to Bass")
  set_tuning(bass_guitar_four_string_standard_tuning)
  set_strings(strings_bass_guitar_four_string)

def set_to_five_string_guitar():
  loginfo("Setting Fretboard to Five String Guitar")
  set_tuning(guitar_five_string_standard_tuning)
  set_strings(strings_guitar_five_string)

def set_to_seven_string_guitar():
  loginfo("Setting Fretboard to Seven String Guitar")
  set_tuning(guitar_seven_string_standard_tuning)
  set_strings(strings_guitar_seven_string)


def set_to_eight_string_guitar():
  loginfo("Setting Fretboard to Eight String Guitar")
  set_tuning(guitar_eight_string_standard_tuning)
  set_strings(strings_guitar_eight_string)


def set_to_five_string_bass_guitar():
  loginfo("Setting Fretboard to Five String Bass")
  set_tuning(bass_guitar_five_string_standard_tuning)
  set_strings(strings_bass_guitar_five_string)


def get_fretboard():
  global fretboard_setup
  return fretboard_setup


def get_tuning():
  global tuning_setup
  return tuning_setup


def set_fretboard(fretboard):
  loginfo("Fretboard is",fretboard)
  switcher.get(fretboard, set_to_guitar)()


switcher = {
    Fretboards.Guitar: set_to_guitar,
    Fretboards.Guitar7s: set_to_seven_string_guitar,
    Fretboards.Guitar8s: set_to_eight_string_guitar,
    Fretboards.Bass: set_to_bass,
    Fretboards.Bass5s: set_to_five_string_bass_guitar,
    Fretboards.Banjo: set_to_banjo,
    Fretboards.Mandolin: set_to_mandolin,
    Fretboards.Violin: set_to_violin,
    Fretboards.Cello: set_to_cello,
    Fretboards.Ukelele: set_to_ukelele,
    Fretboards.TubBass: set_to_tub_bass,
  }


def note_to_index(note, scale, default=0):
  """ Convert the note to an index in the scale and return index or return default if not found """
  for i in range(len(scale)-1):
    if note == scale[i]: return i
  return default


"""
call once, no params, call successive times putting returned params back in
never adjust params except for s, the slide value, just feed them back in to
generate the next rgb values
this is a hack to sort of objectize this function and as such would be simpler as a class
"""
def rgb_slider(s=0.3,r=0,g=0,b=0,c=0,c0=0.1,c1=0.0):
# 1.0 / 12 = 0.83333...
# 0.3 iterates nicely over 12
  """ Changes color through the color spectrum each call depending on the slide value putting output back into the input or changing this as desired """
  if r == 0 and g == 0 and b == 0: c0=1.0;c1=0.0;c=0
  if (c0 < 0.0):
    c0 = 1.0
    c = (c + 1) % 3
  if (c1 > 1.0):
    c1 = 0.0
  if c == 0: r=c0;g=0.0;b=c1
  if c == 1: r=0.0;g=c1;b=c0
  if c == 2: r=c1;g=c0;b=0.0
  c0=c0-s
  c1=c1+s
  assert c <= 3
  return s,r,g,b,c,c0,c1


def setup_strings():
#def setup_strings(key='C'):
  #global tuning_setup
  #global fretboard_setup

  #set_fretboard(fretboard)

  fretboard_setup = get_fretboard()
  tuning_setup = get_tuning()

  # initializing a dict with the name of the strings as keys
  strings = {i:[] for i in fretboard_setup}

  loginfo("Fretboard",fretboard_setup,", Tuning",tuning_setup)
  #loginfo("Setup Strings for the key of", key)
  arrind=1
  for key in strings.keys():
    # finding the index of first note in the string
    loginfo("Key",key,", Array Index",arrind,", String Key",tuning_setup[arrind-1])
    loginfo("Whole Notes",whole_notes)
    start = whole_notes.index(tuning_setup[arrind-1])
    # taking a slice of 24 elements
    strings[fretboard_setup[arrind-1]] = whole_notes[start:start+24]
    loginfo("String",fretboard_setup[arrind-1],strings[fretboard_setup[arrind-1]])
    arrind = arrind + 1

  loginfo("Strings",strings)
  return strings


def get_notes(key, intervals, sig=''):
  global whole_notes

  #print("Whole notes are",whole_notes)
  
  loginfo("Intervals are", intervals)
  loginfo("Signature is", sig)
  
  if sig == 'b': whole_notes=whole_notes_flat*5
  if sig == '#': whole_notes=whole_notes_sharp*5
  #print("Whole notes are",whole_notes)
  # finding start of slice
  try:
    root = whole_notes.index(key)
    root = root + 12 # so we have room to move up and down in our note array
    if sig == '#':
      root = root+1
    if sig == 'b':
      root = root-1
    logatten(type(root), root, "/", str(len(whole_notes)))
  except ValueError as e:
    print("Exception", e)
    try:
      if sig == '#':
        loginfo("Changing to flat chromatic scale")
        whole_notes=whole_notes_flat*5
        root = whole_notes.index(key)
      else:
        loginfo("Changing to sharp chromatic scale")
        whole_notes=whole_notes_sharp*5
        root = whole_notes.index(key)
    except ValueError as e:
      print("Exception to the Exception", e)
  #print("Root is", root)
  #print("Whole notes are",whole_notes)
  # taking 12 consecutive elements
  #octave = whole_notes[root:root+13]
  #octave = whole_notes[root:root+25]
  octave = whole_notes[root:root+36]
  #print("Octave is", octave)
  # BUG: this assumes the root so maybe this is not good info?
  loginfo("Octave is",[octave[i] for i in scales['major']])
  # accesing indices specified by `intervals` to retrieve notes
  notes = [octave[i] for i in intervals]
  return notes


def chord_intervals_from_scale(ax, keyof, name, root, group):
  # chord_intervals_from_scale(ax, scale, root, group)
  """ Return intervals for specified Chord in the specified Key """
  intervals = scales[name.lower()]
  #loginfo(whole_notes)
  #loginfo(intervals)
  scale = get_notes(keyof, intervals)
  loginfo("KeyOf",keyof,", Root",root,", Group",group,", Scale",scale)
  r = scale.index(root)
  ichord = []
  for i in range(0,group,2):
    ichord.append(intervals[(i+r)%len(intervals)])
  loginfo("Intervals are", ichord)
  #for limit in slim:
  #  if num == limit:
  return ichord


def show_graph():
  # plot ready, time for the show
  plt.show()


def set_title(title):
  #title = Fretboards.ToString() + " " + title
  plt.title(title)


def find_all_positions(strings,notes,slim=max_limiter):
# find position of notes of a given scale in the guitar
  #fretboard_setup = get_fretboard()
  loginfo("String Limiter is",slim)
  loginfo("Fretboard Setup is",fretboard_setup)
  loginfo("Notes are",notes)
  plots = {i:[] for i in fretboard_setup}
  # for every string
  for num in strings.keys():
    # we create an empty list of indices
    indices = []
    for index,value in enumerate(strings[num]):
      for note in notes: #for note in scale.notes:
      # append index where note of the scale is found in
        if value == note and index == 0:
          indices.append(index)
        else:
          if value == note:
            if len(slim):
              for limit in slim:
                if num == limit:
                  indices.append(index)
            else:
              indices.append(index)
    plots[num] = indices
  loginfo("Plots", plots)
  return plots


def find_chord_by_position_new(strings, notes, pos=0, frets=24, root=True,
                           inversion=0, slim=max_limiter):
  """
  Plot notes based on fret position to fret position allowing string limitations
  """
  loginfo("String Limiter is",slim)
  loginfo("Fretboard Setup is",fretboard_setup)
  loginfo("Notes are",notes)
  #fretboard_setup = get_fretboard()
  plots = {i:[] for i in fretboard_setup}
  insert=not root
  if inversion >= len(notes): inversion = inversion % len(notes) # loop values on limit


def find_chord_by_position_old(strings, notes, pos=0, frets=24, root=True,
                           inversion=0, slim=max_limiter):
  """
  Plot notes based on fret position to fret position allowing string limitations
  """
  # BUG: adds first not found but this is not necessarily the chord so all notes need to be listed or fingering must be figured out somehow. Could try using the last one found? Can add multiple option for this?
  loginfo("String Limiter is",slim)
  loginfo("Fretboard Setup is",fretboard_setup)
  loginfo("Notes are",notes)
  loginfo("Max limiter", max_limiter)
  #fretboard_setup = get_fretboard()
  plots = {i:[] for i in fretboard_setup}
  insert=not root
  if len(notes) ==0: return plots
  if len(notes) and inversion >= len(notes): inversion = inversion % len(notes) # loop values on limit
  #if first position consider open strings first
  # do this if including open strings only! probably need a setting here
  if pos == 1:
    for num in strings.keys():
      key = tuning_setup[fretboard_setup.index(num)]
      indices = []
      if len(slim):
        for limit in slim:
          if num == limit:
            if strings[num][0] == notes[inversion]:
              insert = True
            for note in notes:
              if strings[num][0] == note and insert is True:
                loginfo("Pre Key is",key,end=', ')
                loginfo("Appending",0)
                indices.append(0)
            plots[num] = indices
      else:
        if strings[num][0] == notes[inversion]:
          print("Insert is True")
          insert = True
        for note in notes:
          if strings[num][0] == note and insert is True:
            loginfo("Pre Key is",key,end=', ')
            loginfo("Appending",0)
            indices.append(0)
        plots[num] = indices

  # for every string
  for num in strings.keys():
    if len(slim):
      for limit in slim:
        if num == limit:
          key = tuning_setup[fretboard_setup.index(num)]
          # we create an empty list of indices
          #loginfo("Plots are",plots)
          #loginfo("Num",num,"Key",key)
          #loginfo("Strings",strings)
          if len(plots[num]) == 0: # only one
            loginfo("Key is",key,end=', ')
            indices = []
            # https://www.techiedelight.com/loop-through-list-with-index-python/
            for index,value in enumerate(strings[num]):
              if index >= pos and index <= pos + frets: # only if @ pos to pos + 4
                if strings[num][index] == notes[inversion]: insert = True
                for note in notes:
                  if strings[num][index] == note:
                    #if len(indices) == 0 and insert is True: # only append the first one
                    if insert is True:
                      loginfo("Appending",index,"Value",value)
                      indices.append(index)
            plots[num] = indices
      else:
        key = tuning_setup[fretboard_setup.index(num)]
        # we create an empty list of indices
        #loginfo("Plots are",plots)
        #loginfo("Num",num,"Key",key)
        #loginfo("Strings",strings)
        if len(plots[num]) == 0: # only one
          loginfo("Key is",key,end=', ')
          indices = []
          # https://www.techiedelight.com/loop-through-list-with-index-python/
          for index,value in enumerate(strings[num]):
            if index >= pos and index <= pos + frets: # only if @ pos to pos + 4
              if strings[num][index] == notes[inversion]: insert = True
              for note in notes:
                if strings[num][index] == note:
                  #if len(indices) == 0 and insert is True: # only append the first one
                 if insert is True:
                    loginfo("Appending",index,"Value",value)
                    indices.append(index)
          #else:
          #  loginfo(key,"Already Assigned")
          plots[num] = indices
  # do this again for open strings on empty indices and fill em in if applicable
  loginfohighlight(plots)
  return plots # TODO: do we want to do the below or not?
  # for num in strings.keys():
    # if len(slim):
      # for limit in slim:
        # if num == limit:
          # key = tuning_setup[num-1]
          # we create an empty list of indices
          # if len(plots[num]) == 0:
            # loginfo("Empty Key is",key,end=', ')
            # indices = []
            # for note in notes:
              # if strings[num][0] == note:
                # loginfo("Appending",0)
                # indices.append(0)
            # plots[num] = indices
    # else:
      # key = tuning_setup[num-1]
      # we create an empty list of indices
      # if len(plots[num]) == 0:
        # loginfo("Empty Key is",key,end=', ')
        # indices = []
        # for note in notes:
          # if strings[num][0] == note:
            # loginfo("Appending",0)
            # indices.append(0)
        # plots[num] = indices
  # return plots
find_chord_by_position=find_chord_by_position_old


def plot_fretboard(title='Plot',
                   fretboard=Fretboards.Guitar,
                   color='black',
                   fret=True,
                   string=True):

  set_fretboard(fretboard)
  #strings = setup_strings(fretboard=fretboard)

  # overall window size
  # https://matplotlib.org/3.1.1/api/axes_api.html#subplots
  # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.figure.html#matplotlib.pyplot.figure

  fig, ax = plt.subplots(figsize=(13, len(fretboard_setup)/1.3)) #(20,6)

  size = 23
  # setting height and width of displayed guitar
  ax.set_xlim([0, size])
  ax.set_ylim([0.4, len(fretboard_setup)+0.5])

  # setting color of the background using argument night
  ax.set_facecolor(color)

  # Plot Strings
  if string is True:
    for i in range(1,len(fretboard_setup)+1):
        ax.plot([i for a in range(size+2)])

  # Plotting Frets
  if fret is True:
    for i in range(1, size+1):
        # add nut
        if i == 1:
            ax.axvline(x=i, color='white', linewidth=5)
            continue
        # add position dots
        dotcolor=(0.3, 0.3, 0.3, 0.2)
        if i == 1 or i == 3 or i == 5 or i == 7 or i == 9 or \
           i == 15 or i == 17 or i == 19 or i == 21:
          p = mpatches.Circle((i+0.5, 3.5), 0.2, color=dotcolor)
          ax.add_patch(p)
        # decorates the twelve fret with a thick gray fret
        if i == 12:
            #ax.axvline(x=i, color='gray', linewidth=3.5)
            p = mpatches.Circle((i+0.5, 2.5), 0.2, color=dotcolor)
            ax.add_patch(p)
            p = mpatches.Circle((i+0.5, 4.5), 0.2, color=dotcolor)
            ax.add_patch(p)
            #continue
        # trace a vertical line (a fret)
        # for some reason white is a strong gray in this case
        ax.axvline(x=i, color='white', linewidth=0.5)
    ax.set_axisbelow(True)

  # title and ticks
  if len(title) > 0:
    plt.title(title)

  # set bottom ticks to fret number
  plt.yticks(np.arange(1,len(fretboard_setup)+1), tuning_setup)
  plt.xticks(np.arange(size+1)+0.5, np.arange(0, size+1))

  # margins
  left = 0.036    # the left side of the subplots of the figure - def = 0.125
  right = 0.995   # the right side of the subplots of the figure - def = 0.9
  bottom = 0.1    # the bottom of the subplots of the figure - def = 0.1
  top = 0.9       # the top of the subplots of the figure - def = 0.9
  wspace = 0.126  # the amount of width reserved for space between subplots,
                  # expressed as a fraction of the average axis width - def = 0.2
  hspace = 0.512  # the amount of height reserved for space between subplots,
                  # expressed as a fraction of the average axis height - def = 0.2

  plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)

  return fig,ax #,strings


def plot_intervals(ax, keyof, intervals,
                   slim=max_limiter,
                   theme={-1:{'color':'royalblue'},0:{'color':'darkgreen'}},
                   sig=''):
# plot(ax, to_plot, scale, chord)
  #loginfo("Scale is", scale)
  #loginfo("Key is", keyof)
  #loginfo("Intervals are",intervals)

  notes = get_notes(keyof, intervals, sig=sig)

  loginfo("Notes are", notes)

  strings = setup_strings()

  # finding note positions of the notes in the guitar
  to_plot = find_all_positions(strings, notes, slim=slim)

  # for every note of the notes in every string make a circle
  # with the note's name as label in the corresponding fret
  for strnum, strlet in zip(fretboard_setup, tuning_setup):
    for i in to_plot[strnum]:
      x = i+0.5  # shift the circles to the right
      note = strings[strnum][i]
      # if note is the root make it a bit bigger
      for key in theme:
        if key != -1 and note == notes[key]: # theme to apply to specific notes like the root
          p = mpatches.Circle((x, fretboard_setup.index(strnum)+1), 0.3, color='darkgreen')
          # add label to middle of the circle
          ax.annotate(note, (i+0.5, fretboard_setup.index(strnum)+1), color='w', weight='bold',
                             fontsize=14.5, ha='center', va='center')
        elif key == -1: # theme to apply to all others
          p = mpatches.Circle((x, fretboard_setup.index(strnum)+1), 0.275, color='royalblue')
          # add label to middle of the circle
          ax.annotate(note, (i+0.5, fretboard_setup.index(strnum)+1), color='w', weight='bold',
                        fontsize=12, ha='center', va='center')
        else: # no theme patch
          p = mpatches.Circle((x, fretboard_setup.index(strnum)+1), 0.275, color='royalblue')
          # add label to middle of the circle
          ax.annotate(note, (i+0.5, fretboard_setup.index(strnum)+1), color='w', weight='bold',
                        fontsize=12, ha='center', va='center')

      # ready add the patch
      ax.add_patch(p)


def plot_scale(ax, keyof, mode='', slim=max_limiter, sig='#'):

  intervals = scales[mode.lower()]
  scale = get_notes(keyof, intervals, sig=sig)
  loginfo("Scale is", scale)
  strings = setup_strings()
  # finding note positions of the scale in the guitar
  to_plot = find_all_positions(strings, scale, slim=slim)

  rgbcolors = {'r':[],'g':[],'b':[]};
  colors = []
  if mode.lower() == 'circleof5ths':
    colors.append('maroon')
    colors.append('red')
    colors.append('coral')
    colors.append('darkgoldenrod')
    colors.append('khaki')
    colors.append('forestgreen')
    colors.append('teal')
    colors.append('navy')
    colors.append('cornflowerblue')
    colors.append('slateblue')
    colors.append('indigo')
    colors.append('purple')
  elif mode.lower() == 'chromatic_rainbow':
    s,r,g,b,c,c0,c1 = rgb_slider() # taste the rainbow
    for i in range(12):
      s,r,g,b,c,c0,c1 = rgb_slider(s,r,g,b,c,c0,c1)
      rgbcolors["r"].append(r)
      rgbcolors["g"].append(g)
      rgbcolors["b"].append(b)

  # for every note of the scale in every string make a circle
  # with the note's name as label in the corresponding fret
  for strnum, strlet in zip(fretboard_setup, tuning_setup):
    for i in to_plot[strnum]:
      x = i+0.5  # shift the circles to the right
      note = strings[strnum][i]
      # customize scale type look
      if mode.lower() == 'major': # non-pentatonic
        if note == scale[0]: # root
          p = mpatches.Circle((x, fretboard_setup.index(strnum)+1), 0.3, color='darkgreen')
          # add label to middle of the circle
          ax.annotate(note, (i+0.5, fretboard_setup.index(strnum)+1), color='w', weight='bold',
                        fontsize=14.5, ha='center', va='center')
        elif note == scale[3] or note == scale[6]:
          p = mpatches.Circle((x, fretboard_setup.index(strnum)+1), 0.25, color='tab:blue')
          # add label to middle of the circle
          ax.annotate(note, (i+0.5, fretboard_setup.index(strnum)+1), color='w', weight='bold',
                        fontsize=12, ha='center', va='center')
        else:
          p = mpatches.Circle((x, fretboard_setup.index(strnum)+1), 0.275, color='royalblue')
          # add label to middle of the circle
          ax.annotate(note, (i+0.5, fretboard_setup.index(strnum)+1), color='w', weight='bold',
                        fontsize=12, ha='center', va='center')
      # minor notes
      elif mode.lower() == 'minor': # non-pentatonic
        if note == scale[0]: # root
          p = mpatches.Circle((x, fretboard_setup.index(strnum)+1), 0.3, color='darkgreen')
          # add label to middle of the circle
          ax.annotate(note, (i+0.5, fretboard_setup.index(strnum)+1), color='w', weight='bold',
                        fontsize=14.5, ha='center', va='center')
        elif note == scale[1] or note == scale[5]:
          p = mpatches.Circle((x, fretboard_setup.index(strnum)+1), 0.25, color='tab:blue')
          # add label to middle of the circle
          ax.annotate(note, (i+0.5, fretboard_setup.index(strnum)+1), color='w', weight='bold',
                        fontsize=12, ha='center', va='center')
        else:
          p = mpatches.Circle((x, fretboard_setup.index(strnum)+1), 0.275, color='royalblue')
          # add label to middle of the circle
          ax.annotate(note, (i+0.5, fretboard_setup.index(strnum)+1), color='w', weight='bold',
                        fontsize=12, ha='center', va='center')
      # minor blues
      elif mode.lower() == 'minor_blues' and note == scale[3]:
        if note == scale[0]: # root
          p = mpatches.Circle((x, fretboard_setup.index(strnum)+1), 0.3, color='darkgreen')
          # add label to middle of the circle
          ax.annotate(note, (i+0.5, fretboard_setup.index(strnum)+1), color='w', weight='bold',
                        fontsize=14.5, ha='center', va='center')
        else:
          p = mpatches.Circle((x, fretboard_setup.index(strnum)+1), 0.25, color='darkblue')
          # add label to middle of the circle
          ax.annotate(note, (i+0.5, fretboard_setup.index(strnum)+1), color='w', weight='bold',
                        fontsize=12, ha='center', va='center')
      # Blue Minor
      elif mode.lower() == 'blue_minor' and note == scale[4]:
        if note == scale[0]: # root
          p = mpatches.Circle((x, fretboard_setup.index(strnum)+1), 0.3, color='darkgreen')
          # add label to middle of the circle
          ax.annotate(note, (i+0.5, fretboard_setup.index(strnum)+1), color='w', weight='bold',
                        fontsize=14.5, ha='center', va='center')
        else:
          p = mpatches.Circle((x, fretboard_setup.index(strnum)+1), 0.275, color=(0.25,0,1,0.25))
          # add label to middle of the circle
          ax.annotate(note, (i+0.5, fretboard_setup.index(strnum)+1), color='w', weight='bold',
                        fontsize=12, ha='center', va='center')
      # Cirle of 5ths
      elif mode.lower() == 'circleof5ths':
        c = note_to_index(note,scale)
        p = mpatches.Circle((x, fretboard_setup.index(strnum)+1), 0.275, color=(colors[c]))
        # add label to middle of the circle
        ax.annotate(note, (i+0.5, fretboard_setup.index(strnum)+1), color='k', weight='bold',
                      fontsize=12, ha='center', va='center')
      # Chromatic Rainbow
      elif mode.lower() == 'chromatic_rainbow':
        c = note_to_index(note,scale)
        r = rgbcolors["r"][c];g = rgbcolors["g"][c];b = rgbcolors["b"][c]
        p = mpatches.Circle((x, fretboard_setup.index(strnum)+1), 0.275, color=(r,g,b,0.25))
        # add label to middle of the circle
        ax.annotate(note, (i+0.5, fretboard_setup.index(strnum)+1), color='w', weight='bold',
                      fontsize=12, ha='center', va='center')
      # Purple Trans
      elif mode.lower() == 'purple_trans':
        p = mpatches.Circle((x, fretboard_setup.index(strnum)+1), 0.275, color=(1,0,1,0.25))
        # add label to middle of the circle
        ax.annotate(note, (i+0.5, fretboard_setup.index(strnum)+1), color='w', weight='bold',
                      fontsize=12, ha='center', va='center')
      else:
        if note == scale[0]: # root
          p = mpatches.Circle((x, fretboard_setup.index(strnum)+1), 0.3, color='darkgreen')
          # add label to middle of the circle
          ax.annotate(note, (i+0.5, fretboard_setup.index(strnum)+1), color='w', weight='bold',
                        fontsize=14.5, ha='center', va='center')
        elif note == scale[4]:
          p = mpatches.Circle((x, fretboard_setup.index(strnum)+1), 0.3, color='darkblue', fill=0)
          # add label to middle of the circle
          ax.annotate(note, (i+0.5, fretboard_setup.index(strnum)+1), color='w', weight='bold',
                        fontsize=14.5, ha='center', va='center')
        else:
          p = mpatches.Circle((x, fretboard_setup.index(strnum)+1), 0.275, color='royalblue')
          # add label to middle of the circle
          ax.annotate(note, (i+0.5, fretboard_setup.index(strnum)+1), color='w', weight='bold',
                        fontsize=12, ha='center', va='center')

      # ready add the patch
      ax.add_patch(p)


def plot_chord_from_scale(ax, keyof, name, root, group,
                          slim=fretboard_setup, typeof='interval', bgcolor='k'):
# plot_chord_from_scale(ax, to_plot, scale, 'C#', 5)
  """ Create chord from a scale returning chord intervals """
  chord = chord_intervals_from_scale(ax, keyof, name, root, group)
  loginfo("Chord Intervals are", chord)
  #strings = setup_strings()
  plot_intervals(ax, keyof, chord, slim=slim)


def plot_custom_chord(name):
  # http://www.all-guitar-chords.com/
  # Note(1-2,1 req),          E.g. C
  # Pitch(1, 0 req),          E.g. #
  # Mode(alpha, 0 req)        E.g. dim
  # Pos(numeric, 0 req)       E.g. 11
  # PitchAdj(pitch, 0 req)    E.g. b
  # Adj(numeric, 0 req)       E.g. 7
  note=''
  mode=''
  pitch=''
  pitchadj=''
  size = len(name)
  pos = 0
  adj = 0
  start = 0
  index = 0
  sz = 1

  if index >= size: print();return

  # Note(1-2,1 req)
  note = name[index]
  index = index + 1
  print("Note '"+note+"',",end=' ')

  if index >= size: print();return

  # Pitch(1, 0 req)
  if name[index] == '#' or name[index] == 'b':
      pitch = name[index]
      index = index + 1
  print("Pitch '"+pitch+"',",end=' ')

  if index >= size: print();return

  # Mode(alpha, 0 req)
  # https://careerkarma.com/blog/python-isalpha-isnumeric-isalnum/
  start = index
  sz = 1
  while index < size and name[start:start+sz].isalpha():
    #print(name[index],end=' ')
    index = index + 1
    sz = sz + 1
  if index > start: mode = name[start:start+(sz-1)]
  print("Mode '"+mode+"',",end=' ')

  if index >= size: print();return
  #print(name[:index])
  # Pos(numeric, 0 req)
  sz = 1
  start = index
  while index < size and name[start:start+sz].isnumeric():
    index = index + 1
    sz = sz + 1
  if index > start: pos = int(name[start:start+(sz-1)])
  print("Pos '"+str(pos)+"',",end=' ')

  if index >= size: print();return

  # PitchAdj(pitch, 0 req)
  start = index
  sz = 1
  while index < size and name[start:start+sz].isalpha():
    index = index + 1
    sz = sz + 1
  if index > start: pitchadj = name[start:start+(sz-1)]
  print("PitchAdj '"+pitchadj+"',",end=' ')

  # Adj(numeric, 0 req)
  start = index
  sz = 1
  while index < size and name[start:start+sz].isnumeric():
    index = index + 1
    sz = sz + 1
  if index > start: adj = int(name[start:start+(sz-1)])
  print("Adj '"+str(adj)+"',",end=' ')
  print()


def plot_chord_by_position(ax, notes, pos=0, frets=24,
                           root=True, inversion=0, slim=max_limiter):
  #global title
  show_bubbles=True
  show_notes=True
  strings = setup_strings()
  plots = find_chord_by_position(strings, notes, pos=pos, frets=frets, root=root, inversion=inversion, slim=slim)
  loginfoloud(plots)
  #add_note_bubbles(ax, strings, plots, notes)
  # def add_note_bubbles(ax, strings, plots, notes, show_bubbles=True, show_notes=True):
  # https://matplotlib.org/3.2.1/api/patches_api.html
  for strnum, strlet in zip(fretboard_setup, tuning_setup):
    for i in plots[strnum]:
      x = i+0.5  # shift the circles and fonts to the right
      note = strings[strnum][i]
      # if note is the root make it a bit bigger
      if note == notes[0]:
        w=h=0.6
        if show_bubbles is True:
          #p = mpatches.Rectangle((i+(1-w)/2, strnum-h/2), height=h,width=w, color='darkgreen')
          p = mpatches.Circle((x, fretboard_setup.index(strnum)+1), w/2, color='darkgreen')
        if show_notes is True:
          # add label to middle of the circle
          ax.annotate(note, (x, fretboard_setup.index(strnum)+1), color='w', weight='bold',
                        fontsize=14.5, ha='center', va='center')
      else:
        w=h=0.275*2
        x=i+w
        if show_bubbles is True:
          p = mpatches.Circle((x, fretboard_setup.index(strnum)+1), w/2, color='royalblue')
        if show_notes is True:
          # add label to middle of the circle
          ax.annotate(note, (x, fretboard_setup.index(strnum)+1), color='w', weight='bold',
                        fontsize=12, ha='center', va='center')
      # ready add the patch
      ax.add_patch(p)


def plot_chord(name,**kwargs):
  found=False
  start=1
  colw=10
  if len(name) < 2:
    c1w=colw-len(name)
    print(name," "*c1w,name,**kwargs); return True
  if name[1] == '#' or name[1] == 'b': start=2;
  for c in chords.keys():
    if name[start:] == c:
      c1w=colw-len(name)
      c2w=colw-len(name[0:start])
      print(name," "*c1w,name[0:start]," "*c2w,name[start:],**kwargs)
      found=True
  if found is False:
    for s in split_chords:
      if name == s:
        c1w=colw-len(name)
        print(name," "*c1w,"Split",**kwargs)
        found=True
  if found is False:
    print("Error",name," ... is not found!",**kwargs)
    return False
  return True


def interval_graph(title, note, chord, sig='', fretboard=Fretboards.Guitar, color='k', fret=True, string=True):
  # plotting intervals will do a chord over the entire fretboard
  fig,ax = plot_fretboard(title=title,
                          fretboard=fretboard,
                          color=color,
                          fret=fret,
                          string=string)
  plot_intervals(ax, note, chord, sig=sig)
  # get_notes
  # setup_strings
  # find_all_positions
  show_graph()


def scale_graph(title, note, mode, sig='', fretboard=Fretboards.Guitar, color='k', fret=True, string=True):

  fig,ax = plot_fretboard(title=title,
                          fretboard=fretboard,
                          color=color,
                          fret=fret,
                          string=string)

  plot_scale(ax, note, mode=mode, sig=sig) # missing B
  # get_notes
  # setup_strings
  # find_all_positions
  show_graph()


def chord_position_graph(title, note, chord, sig='', pos=0, frets=4, inversion=0, fretboard=Fretboards.Guitar, color='k', fret=True, string=True):

  fig,ax = plot_fretboard(title=title,
                          fretboard=fretboard,
                          color=color,
                          fret=fret,
                          string=string)

  notes = get_notes(note, chord, sig=sig)
  loginfohighlight(notes)
  plot_chord_by_position(ax, notes, pos=pos, frets=frets, inversion=inversion)
  # setup_strings
  # find_chord_by_position
  # add_note_bubbles
  show_graph()


def chord_scale_graph(title, note, mode, root, group, slim=[], fretboard=Fretboards.Guitar, color='k', fret=True, string=True):

  fig,ax = plot_fretboard(title=title,
                          fretboard=fretboard,
                          color=color,
                          fret=fret,
                          string=string)
  plot_chord_from_scale(ax, note, mode, root, group, slim=slim) # experimental
  # chord_intervals_from_scale
  #   get_notes
  # plot_intervals
  #   get_notes
  #   setup_strings
  #   find_all_positions
  show_graph()


def test_chord_parsing():
  error_msg="              >>>>>>>>>>>> Test FAILED!"
  print("This is a test, this is only a test")
  if plot_chord('Amaj9#11',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('F-5',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('F#-5',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('Eb-5',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('E9#5',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('C7(#5,b9)',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('C#7(#5,b9)',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('Emadd9',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('Ebmadd9',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('Emmaj9',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('Ebmmaj9',end=' ')  == False: print(error_msg)
  else: print()
  if plot_chord('Cm',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('Cm7',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('F#m',end=' ')  == False: print(error_msg)
  else: print()
  if plot_chord('F#m7',end=' ')  == False: print(error_msg)
  else: print()
  if plot_chord('Bdim',end=' ')  == False: print(error_msg)
  else: print()
  if plot_chord('Dbm',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('G',end=' ')  == False: print(error_msg)
  else: print()
  if plot_chord('F#',end=' ')  == False: print(error_msg)
  else: print()
  if plot_chord('C7',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('C#7',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('Fmaj7',end=' ')  == False: print(error_msg)
  else: print()
  if plot_chord('E11b9',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('Eb11b9',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('Dsus2',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('Bsus2sus4',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('Ebsus2sus4',end=' ')  == False: print(error_msg)
  else: print()
  if plot_chord('F#sus2sus4',end=' ')  == False: print(error_msg)
  else: print()
  if plot_chord('F5',end=' ')  == False: print(error_msg)
  else: print()
  if plot_chord('Eb5',end=' ')  == False: print(error_msg)
  else: print()
  if plot_chord('C#5',end=' ')  == False: print(error_msg)
  else: print()
  if plot_chord('Aaug',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('Bbaug',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('G#aug',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('G7b5',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('G#7b5',end=' ')  == False: print(error_msg)
  else: print()
  if plot_chord('E6add9',end=' ')  == False: print(error_msg)
  else: print()
  if plot_chord('Eb6add9',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('D#add9',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('C13',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('C#13',end=' ')  == False: print(error_msg)
  else: print()
  if plot_chord('Db13',end=' ') == False: print(error_msg)
  else: print()
  if plot_chord('D/F#',end=' ')  == False: print(error_msg)
  else: print()
  if plot_chord('Em/C#',end=' ') == False: print(error_msg)
  else: print()
  # bad chords, negative testing
  print("\nNegative testing (these should all fail) ... ")
  if plot_chord('H',end=' ') == True: print(error_msg)
  else: print()
  if plot_chord('Efloc',end=' ') == True: print(error_msg)
  else: print()
  if plot_chord('X#13',end=' ') == True: print(error_msg)
  else: print()
  if plot_chord('E7c5',end=' ') == True: print(error_msg)
  else: print()
  if plot_chord('Aaaug',end=' ') == True: print(error_msg)
  else: print()
  if plot_chord('F#sus2sus4Sus2',end=' ')  == True: print(error_msg)
  else: print()


def self_test():
  """ Runs smoke regression tests on this module but doesn't display so it can do many plots. Still need visual confirmation as this is not verifying the notes are plotted correctly just that no errors or exceptions are hit so this is really only good for smoke testing. """
  title='Multi Plot - '
  keyof='C'
  mode='major'
  color='k'

  # run all to test but only the last one will be used
  set_to_tub_bass()
  set_to_banjo()
  set_to_mandolin()
  set_to_violin()
  set_to_cello()
  set_to_ukelele()
  set_to_bass()
  set_to_seven_string_guitar()
  set_to_five_string_bass_guitar()
  set_to_guitar()

  fig,ax = plot_fretboard(title='',
                          fretboard=Fretboards.Bass5s,
                          color=color,
                          fret=True,
                          string=True)

  # Test 1 - scales
  title = "D minor Scale (plot_scale)"
  plot_scale(ax, 'D', mode='minor') # missing B

  # Test 2 - intervals
  title = "B Diminished Chord Notes (plot_intervals)"
  #intervals = scales[mode.lower()]
  #scale = get_notes(keyof,intervals)
  plot_intervals(ax, 'B', chords['dim']) # works!

  # Test 3 - chord from scale w/ limiter
  title = "G Chord determined from scale with blackbird string limiter (plot_chord_from_scale)"
  plot_chord_from_scale(ax, keyof, mode, 'G', 5, slim=blackbird_style) # experimental

  # Test 4 - chords
  title = "B Diminished Chords by Position (plot_chord_by_position) - "
  ctype='dim'
  notes = get_notes('B', chords[ctype])

  pos=2
  title = title + notes[0] + ctype + " chord " + str(pos) + "nd fret"
  plot_chord_by_position(ax,notes,pos=pos,frets=3,inversion=0)

  pos=7
  title = title + ", " + notes[0] + ctype + " chord " + str(pos) + "th fret"
  plot_chord_by_position(ax,notes,pos=pos,frets=3,root=False,inversion=0)

  pos=12
  title = title + ", " + notes[0] + ctype + " chord " + str(pos) + "th fret"
  plot_chord_by_position(ax,notes,pos=pos,frets=3,inversion=0)

  test_chord_parsing(); return

  plot_intervals(ax, 'C', [0]) #

  plot_intervals(ax, 'C', chords['']) # works!

  # no show so it can run all and continue, this tests it doesn't display
  set_title(title)


def test_plot_chord_by_position():
  # Intervals, Notes & Postions

  fig,ax = plot_fretboard(title="B dim Chord (plot chord by position)",
                            fretboard=Fretboards.Guitar,
                            color='k',
                            fret=True,
                            string=True)

  #plot_scale(ax, 'D', mode='minor', sig='b') # missing B

  notes = get_notes('B', chords['dim'], sig='#')
  plot_chord_by_position(ax, notes, pos=0, frets=3, inversion=0)

  set_title("D minor chord")
  show_graph()


def test_plot_scale():

  fig,ax = plot_fretboard(title="D minor Scale (plot_scale)",
                          fretboard=Fretboards.Guitar,
                          color='k',
                          fret=True,
                          string=True)

  # Test 1 - scales
  title = "D minor Scale (plot_scale)"
  plot_scale(ax, 'D', mode='minor', sig='b') # missing B

  show_graph()


def test_plot_intervals():

  fig,ax = plot_fretboard(title="B dim Chord (plot intervals)",
                          fretboard=Fretboards.Guitar,
                          color='k',
                          fret=True,
                          string=True)

  plot_intervals(ax, 'B', chords['dim']) # works!

  show_graph()


def test_plot_chord_from_scale():
  keyof='C'
  mode='major'
  fig,ax = plot_fretboard(title="",
                          fretboard=Fretboards.Guitar,
                          color='k',
                          fret=True,
                          string=True)

  # Test 3 - chord from scale w/ limiter
  title = "G Chord determined from scale with string limiter (plot_chord_from_scale)"
  plot_chord_from_scale(ax, keyof, mode, 'G', 5, slim=blackbird_style) # experimental

  set_title(title)
  show_graph()


def test_mutltiplot_chord_by_position():

  fig,ax = plot_fretboard(title="",
                          fretboard=Fretboards.Guitar,
                          color='k',
                          fret=True,
                          string=True)
  title='Multi Plot - '
  pos=2
  ctype='dim'
  notes = get_notes('B', chords[ctype])
  title = title + notes[0] + ctype + " chord " + str(pos) + "nd fret"
  plot_chord_by_position(ax,notes,pos=pos,frets=3,inversion=0)

  pos=7
  title = title + ", " + notes[0] + ctype + " chord " + str(pos) + "th fret"
  plot_chord_by_position(ax,notes,pos=pos,frets=3,root=False,inversion=0)

  pos=12
  title = title + ", " + notes[0] + ctype + " chord " + str(pos) + "th fret"
  plot_chord_by_position(ax,notes,pos=pos,frets=3,inversion=0)

  set_title(title)
  show_graph()


def visual_confirmation_test():
  """ Runs a visual confirmation test. Visualy confirm the results are correct then exit the graph for the next one to display and visually confirm. """
  test_plot_scale()
  test_plot_intervals()
  test_plot_chord_from_scale()
  test_plot_chord_by_position()
  test_mutltiplot_chord_by_position()


def interval_test():
  interval_graph("G Major chord", 'G', chords[''], fretboard=Fretboards.Guitar, color='k', fret=True, string=True)
  interval_graph("A Minor chord", 'A', chords['m'], fretboard=Fretboards.Guitar, color='k', fret=True, string=True)
  interval_graph("F Major chord", 'F', chords[''], fretboard=Fretboards.Guitar, color='k', fret=True, string=True)
  interval_graph("C Major chord", 'C', chords[''], fretboard=Fretboards.Guitar, color='k', fret=True, string=True)


def api_test():
  global chord

  # basic test of the high level abstraction I created. the data could be set by user after selecting graph type. in this case we are just going to get all four types. this is UI level ready.
  note = 'C'
  kind = '' # Major/minor etc
  chord = chords[kind]
  mode='major'
  sig = ''
  pos=0
  frets=4
  color='k'
  fret=True
  string=True
  inversion=0
  #root=note
  #group=5
  fretboard=Fretboards.Guitar
  title_chord = note + sig + ''.join(map(str, kind)) + ' chord'
  title_scale = note + sig + ' ' + mode + ' scale'

  # chord by pos
  chord_position_graph(title_chord, note, chord, sig=sig, pos=pos, frets=frets, inversion=inversion, fretboard=fretboard, color=color, fret=fret, string=string)

  # show a scale
  scale_graph(title_scale, note, mode, sig=sig, fretboard=fretboard, color=color, fret=fret, string=string)

  # show intervals like a G Major cord over the fretboard
  interval_graph(title_chord, note, chord, sig=sig, fretboard=fretboard, color=color, fret=fret, string=string)

  # TODO: chord from scale seems to duplicate the scale letter
  chord_scale_graph(title_chord + ' with string limiter', note, mode, note, 5, slim=[5,2], fretboard=fretboard, color=color, fret=fret, string=string)


def one_chord(note, kind='', sig='', pos=0, frets=4, color='k', fret=True, string=True, inversion=0, fretboard=Fretboards.Guitar):
  global chords
  #note = 'B'            # A B C D E F or G
  #kind = ''             # '', 'm', 'dim', etc
  chord = chords[kind]  # the the kind of chord specified
  #mode='major'          # 'major', 'minor', etc
  #sig = ''              # 'b', '#' or ''
  #pos = 0               # start fret to plot from
  #frets = 4             # number of frets to plot
  #color = 'k'           # 'k','w','b', etc
  #fret = True           # show frets or not True or False
  #string = True         # show strings or not True or False
  #inversion = 0         # chord inversion
  title = note + sig + ''.join(map(str, kind)) + ' chord'
  # chord by pos
  chord_position_graph(title, note, chord, sig=sig, pos=pos, frets=frets, inversion=inversion, fretboard=fretboard, color=color, fret=fret, string=string)


def one_scale(note, mode='major', sig='', pos=0, frets=4, color='k', fret=True, string=True, inversion=0, fretboard=Fretboards.Guitar):
  title = note + sig + " " + ''.join(map(str, mode)) + ' scale'
  scale_graph(title, note, mode, sig=sig, fretboard=fretboard, color=color, fret=fret, string=string)


class Fretboard():

  def __init__(self, **params):
    loginfohighlight(params)
    self.board = get_fretboard_from_string(params.get('board', "Guitar"))
    self.chord = params.get('chord', False)
    self.scale = params.get('scale', False)
    self.note = params.get('note', 'C')
    self.kind = params.get('kind', '')
    self.mode = params.get('mode', 'major')
    self.signature = params.get('signature', '')
    self.position = int(params.get('pos', 0))
    self.frets = int(params.get('frets', 4))
    self.color = params.get('color', 'k')
    self.fretsoff = params.get('fretsoff', False)
    self.stringsoff = params.get('stringsoff', False)
    self.inversion = 0


  def plot(self):
    print(self.signature)
    if self.chord:
      one_chord(self.note,
                kind=self.kind,
                sig=self.signature,
                pos=self.position,
                frets=self.frets,
                color=self.color,
                fret=not self.fretsoff,
                string=not self.stringsoff,
                inversion=self.inversion,
                fretboard=self.board)
    elif self.scale:
      one_scale(self.note,
                mode=self.mode,
                sig=self.signature,
                pos=self.position,
                frets=self.frets,
                color=self.color,
                fret=not self.fretsoff,
                string=not self.stringsoff,
                inversion=self.inversion,
                fretboard=self.board)
    else:
      return False
    return True



# title=f"{scale[0]:} {name:} {typeof:}",
def get_args(name, description):
  parser = argparse.ArgumentParser(prog=name, description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('-b', '--board', default="Guitar", help="Fretboard")
  parser.add_argument('-d', '--chord', default=False, action='store_true', help="Root note. Default C")
  parser.add_argument('-a', '--scale', default=False, action='store_true', help="Root note. Default C")
  parser.add_argument('-n', '--note', default='C', help="Root note. Default C")
  parser.add_argument('-k', '--kind', default='', help="Kind of chord. Default None")
  parser.add_argument('-m', '--mode', default='major', help="Mode to use. Default major")
  parser.add_argument('-s', '--signature', default='', help="Signature. Default None")
  parser.add_argument('-p', '--pos', default=0, help="Start fret position. Default 0")
  parser.add_argument('-f', '--frets', default=4, help="Number of frets to span. Default 4")
  parser.add_argument('-c', '--color', default='k', help="Color to use. Default k")
  parser.add_argument('-e', '--fretsoff', default=False, help="Don't show frets. Default False")
  parser.add_argument('-o', '--stringsoff', default=False, help="Don't show strings. Default False")
  parser.add_argument('-r', '--runtest', help="Runs test specified by number.")
  parser.add_argument('-i', '--inversion', default=0, help="Chord inversion. Default 0.")
  parser.add_argument('-l', '--loglevel', default="Warn", help="Set logging level.")
  parser.add_argument('-t', '--tracelevel', default=0, help="Set trace level.")
  switches = parser.parse_args()
  args=vars(switches)
  arguments = {'name': name, 'description': description}
  for arg in args:
    arguments[arg] = getattr(switches, arg)
    if arguments[arg] == None:
      del arguments[arg]
  for key, value in arguments.items():
    if type(value) is str:
      if value.upper() == 'TRUE':
        arguments[key] = True
      if value.upper() == 'FALSE':
        arguments[key] = False

  return arguments


def main(classname, description):
  params = get_args(classname.__name__, description)
  setloglevel(params['loglevel'])
  settracelevel(int(params['tracelevel']))
  loginfo(params)
  if gettracelevel() > 0: logmainentry(classname.__name__)
  try:
    if 'runtest' in params:
      self_test()
    else:
      if classname(**params).plot() is False:
        print("Please specify the type of plot: enter -d for chord or -a for scale")
  except KeyboardInterrupt:
    pass
  if gettracelevel() > 0: logmainexit(classname.__name__)


if __name__ == "__main__":
  main(Fretboard, "Fretboard Plotter")
  #params = get_args("Fretboard", "MatplotLib for stringed instruments")
  #setloglevel(params['loglevel'])
  #settracelevel(int(params['tracelevel']))
  #visual_confirmation_test()
  #interval_test()
  #api_test()
  #one_chord()
#-------------------------------------------------------------------------------
#
# <|:) Wizard
#
#-------------------------------------------------------------------------------
