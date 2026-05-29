// ---------------- DATA ----------------
const NOTES_SHARP = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"];
const NOTES_FLAT = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"];

const CHORDS = {
  "":     [0,4,7],            // Major
  "m":    [0,3,7],            // Minor
  "7":    [0,4,7,10],         // Dominant 7th
  "m7":   [0,3,7,10],         // Minor 7th
  "maj7": [0,4,7,11],         // Major 7th
  "dim":  [0,3,6],            // Diminished - https://splice.com/blog/what-is-a-diminished-chord/
  "aug":  [0,4,8],            // Augmented
  '-5':   [0,4,6],            // Major Diminished 5th
  '5':    [0,7],              // Power Chord
  '6':    [0,4,7,9],          // Major 6th                     (1,3,5,6)
  '6/9':  [0,4,7,9,14],       // Major 6/9                     (1,3,5,6,9)
  '9':    [0,4,7,11,14],      // Dominant 9th
  '11':   [0,4,7,11,17],      // Dominant 11th - '11': [0,4,7,11,14,17], 
  '13':   [0,4,7,11,21],      // Dominant 13th - '13': [0,4,7,11,14,17,21],
  'm9':   [0,3,7,10,14],      // Minor 9th
  'm11':  [0,3,7,17],         // Minor 11th
  'm13':  [0,3,7,21],         // Minor 13th
  'm6':   [0,3,7,9],          // Minor 6th
  'mmaj7': [0,3,7,11],        // Minor Major 7th
  'madd9': [0,3,7],           // Minor Add 9
  'm6add9': [0,3,7],          // Minor 6 Add 9
  'mmaj9': [0,3,7],           // Minor Major 9th
  'm7#5': [0,3,7],            // Minor 7 # 5
  'm7b5': [0,3,7],            // Half Diminished Minor 7
};

const CHORD_ORDER = ["", "m", "7", "m7", "maj7", "dim", "aug", "5", "6", "m6", "9", "m9", "11", "m11", "13", "m13", "mmaj7", "madd9"];

const CHORD_INTERVALS = {
  "":        [0,4,7],          // Major
  "m":       [0,3,7],          // Minor
  "5":       [0,7],            // Power chord
  "sus2":    [0,2,7],          // Suspended 2nd
  "sus4":    [0,5,7],          // Suspended 4th
  "sus2sus4":[0,2,5,7],        // Both suspensions

  // Major family
  "maj7":    [0,4,7,11],
  "maj9":    [0,4,7,11,14],
  "maj11":   [0,4,7,11,14,17],
  "maj13":   [0,4,7,11,14,17,21],
  "add9":    [0,4,7,14],
  "add11":   [0,4,7,17],
  "add13":   [0,4,7,21],
  "6":       [0,4,7,9],
  "6/9":     [0,4,7,9,14],
  "maj7#5":  [0,4,8,11],
  "maj7b5":  [0,4,6,11],
  "maj9#11": [0,4,7,11,14,18],
  "maj13#11":[0,4,7,11,14,18,21],

  // Minor family
  "m6":      [0,3,7,9],
  "m7":      [0,3,7,10],
  "m9":      [0,3,7,10,14],
  "m11":     [0,3,7,10,14,17],
  "m13":     [0,3,7,10,14,17,21],
  "madd9":   [0,3,7,14],
  "m6add9":  [0,3,7,9,14],
  "mmaj7":   [0,3,7,11],
  "mmaj9":   [0,3,7,11,14],
  "m7b5":    [0,3,6,10],       // Half‑diminished
  "m7#5":    [0,3,8,10],

  // Dominant family
  "7":       [0,4,7,10],
  "9":       [0,4,7,10,14],
  "11":      [0,4,7,10,14,17],
  "13":      [0,4,7,10,14,17,21],
  "7sus4":   [0,5,7,10],
  "7b5":     [0,4,6,10],
  "7#5":     [0,4,8,10],
  "7b9":     [0,4,7,10,13],
  "7#9":     [0,4,7,10,15],
  "9b5":     [0,4,6,10,14],
  "9#5":     [0,4,8,10,14],
  "11b9":    [0,4,7,10,13,17],
  "13b9":    [0,4,7,10,13,17,21],
  "13#11":   [0,4,7,10,14,18,21],

  // Altered dominant clusters
  "7(b5,b9)": [0,4,6,10,13],
  "7(b5,#9)": [0,4,6,10,15],
  "7(#5,b9)": [0,4,8,10,13],
  "7(#5,#9)": [0,4,8,10,15],

  // Diminished / Augmented
  "dim":     [0,3,6],
  "dim7":    [0,3,6,9],          // [0,3,6,9 is B] - Notes: D, F, Ab, C
  "halfdim": [0,3,6,10],         // same as m7b5
  "aug":     [0,4,8],
  "aug7":    [0,4,8,10]
};

const CHORD_INTERVAL_ORDER = [
  // popular quick list
  "", "m","5", "7", "m7", "maj7", "dim", "aug", "sus2", "sus4", "sus2sus4",

  // Major family
  "add9",
  "add11",
  "add13",
  "6",
  "6/9",
  "maj7",
  "maj9",
  "maj11",
  "maj13",
  "maj7#5",
  "maj7b5",
  "maj9#11",
  "maj13#11",

  // Minor family
  "m",
  "madd9",
  "m6",
  "m6add9",
  "m7",
  "m9",
  "m11",
  "m13",
  "mmaj7",
  "mmaj9",
  "m7b5",   // half‑diminished
  "m7#5",

  // Suspended
  "sus2",
  "sus4",
  "sus2sus4",
  "7sus4",

  // Dominant family
  "7",
  "9",
  "11",
  "13",
  "7b5",
  "7#5",
  "7b9",
  "7#9",
  "9b5",
  "9#5",
  "11b9",
  "13b9",
  "13#11",

  // Altered dominant clusters
  "7(b5,b9)",
  "7(b5,#9)",
  "7(#5,b9)",
  "7(#5,#9)",

  // Diminished / Augmented
  "dim",
  "dim7",
  "halfdim",  // or m7b5
  "aug",
  "aug7",

  // Power chord
  "5"
];

const MODES = {
  "Ionian (Major)"    : [0,2,4,5,7,9,11],
  "Dorian"            : [0,2,3,5,7,9,10],
  "Phrygian"          : [0,1,3,5,7,8,10],
  "Lydian"            : [0,2,4,6,7,9,11],
  "Mixolydian"        : [0,2,4,5,7,9,10],
  "Aeolian (Minor)"   : [0,2,3,5,7,8,10],
  "Locrian"           : [0,1,3,5,6,8,10],
  "Major Pentatonic"  : [0,2,4,7,9],
  "Minor Pentatonic"  : [0,3,5,7,10],
  "Harmonic Minor"    : [0,2,3,5,7,8,10],
  "Minor Blues"       : [0,3,5,6,7,10],
  "Blue Minor"        : [0,2,3,5,6,7,8,10],
  "Petonian"          : [0,2,4,5,6,7,9,10,11],
  "Chromatic"         : [0,1,2,3,4,5,6,7,8,9,10,11],
};

const TUNINGS = {
  "Guitar Standard": ["E","A","D","G","B","E"],
  "Guitar Drop D": ["D","A","D","G","B","E"],
  "Guitar Open G": ["D","G","D","G","B","D"],
  "Bass 4 String": ["E","A","D","G"],
  "Bass 5 String": ["B","E","A","D","G"],
  "Violin Standard": ["G","D","A","E"],
  "Cello Standard": ["C","G","D","A"],
  "Banjo Standard": ["G","D","G","B","D"],
  "Mandolin Standard": ["G","D","A","E"],
  "Ukulele Standard": ["G","C","E","A"],
  "Three Notes": ["G","A","D"],
  "Two Notes": ["G","A"],
  "Tub Bass": ["G"],
};

const FRETS = 15;

// ------------- UI ELEMENTS -------------
const chordRootSel = document.getElementById("chordRoot");
const chordTypeSel = document.getElementById("chordType");
const scaleRootSel = document.getElementById("scaleRoot");
const scaleModeSel = document.getElementById("scaleMode");
const tuningSel    = document.getElementById("tuning");
const showScale    = document.getElementById("showScale");
const flipSel      = document.getElementById("flip");
const hideScale      = document.getElementById("hideScale");
const hideChord      = document.getElementById("hideChord");
const showRoot      = document.getElementById("showRoot");
const useFlats      = document.getElementById("useFlats");

hideScale.addEventListener("change", () => {
  if (hideScale.checked) showScale.checked = false;
  render();
});
hideChord.addEventListener("change", () => {
  if (hideChord.checked) showScale.checked = true;
  render();
});

// populate note-based roots
NOTES_SHARP.forEach((n, i) => {
  const label = displayNote(n, useFlats.checked);
  chordRootSel.add(new Option(label,n));
  scaleRootSel.add(new Option(label, n)); // value stays canonical
});

// chord types
CHORD_INTERVAL_ORDER.forEach(c => {
  chordTypeSel.add(new Option(c, c));
});

// scale modes
Object.keys(MODES).forEach(m =>
  scaleModeSel.add(new Option(m,m))
);

// tunings
Object.keys(TUNINGS).forEach(t =>
  tuningSel.add(new Option(t,t))
);

// defaults
chordRootSel.value = "C";
chordTypeSel.value = "Maj";
scaleRootSel.value = "C";
scaleModeSel.value = "Ionian (Major)";
tuningSel.value    = "Guitar Standard";

// ------------- CANVAS / HELPERS -------------
const canvas = document.getElementById("fretboard");
const ctx = canvas.getContext("2d");
const outputDiv = document.getElementById("output");

function textout(msg) {
  outputDiv.textContent = msg == null ? "" : String(msg);
}

function htmlout(html) {
  outputDiv.innerHTML = html == null ? "" : String(html);
}

const idx = n => NOTES_SHARP.indexOf(n);
const noteAt = (open, steps) => NOTES_SHARP[(idx(open)+steps)%12];
const getNotes = (root, intervals) => intervals.map(i => noteAt(root,i));



function displayNote(note, useFlats) {
  const i = NOTES_SHARP.indexOf(note);
  //console.log("Display Note:", i);
  if (i === -1) return note; // safety fallback
  return useFlats ? NOTES_FLAT[i] : NOTES_SHARP[i];
}

// ------------- DRAW FRETBOARD -------------
function drawFretboard(strings, reversed=false) {
  ctx.clearRect(0,0,canvas.width,canvas.height);
  const h = canvas.height / (strings.length+1);

  // frets
  for (let f=0; f<=FRETS; f++) {
    ctx.strokeStyle = f===1 ? "#fff" : "#666";
    ctx.lineWidth = f===1 ? 6 : 2;
    const x = 50 + f*70;
    ctx.beginPath();
    ctx.moveTo(x, h);
    ctx.lineTo(x, h*strings.length);
    ctx.stroke();
    
    if (strings.length >= 4) {
      // Fretboard position markers (3, 5, 7, 12)
      const markerFrets = [3, 5, 7, 9, 12];
      if (markerFrets.includes(f)) {
        const dotX = x + 35; // center between frets
        const midY = (h + h * strings.length) / 2;

        ctx.fillStyle = "#000"; // black, unobtrusive

        if (f === 12) {
          // double dot at 12th fret
          ctx.beginPath();
          ctx.arc(dotX, midY - h * 1, 12, 0, Math.PI * 2);
          ctx.fill();

          ctx.beginPath();
          ctx.arc(dotX, midY + h * 1, 12, 0, Math.PI * 2);
          ctx.fill();
        } else {
          // single dot
          ctx.beginPath();
          ctx.arc(dotX, midY, 12, 0, Math.PI * 2);
          ctx.fill();
        }
      }
    }
  }
  
  // strings
  let lineWidth = reversed ? 1 : 6;
  for (let s=1; s<=strings.length; s++) {
    ctx.strokeStyle="#a70";
    ctx.lineWidth = reversed ? lineWidth++ : lineWidth--;
    ctx.beginPath();
    ctx.moveTo(50, h*s);
    ctx.lineTo(1150, h*s);
    ctx.stroke();
  }
  
}

// ------------- PLOT NOTES -------------
function plotNotes(strings, notes, color, alpha=1.0, border=false) {
  const h = canvas.height / (strings.length+1);
  ctx.globalAlpha = alpha;
  
  const chordRoot = chordRootSel.value;
  const scaleRoot = scaleRootSel.value;
  const mode = showScale.checked ? "scale" : "chord";

  for (let s=0; s<strings.length; s++) {
    const open = strings[s];
    for (let f=0; f<=FRETS; f++) {
      const rawNote = noteAt(open, f);
      const n = displayNote(rawNote, useFlats.checked);
      if (notes.includes(rawNote)) {
        const x = 50 + f*70 + 35;
        const y = h*(s+1);

        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(x,y,13,0,Math.PI*2);
        ctx.fill();
        
        if (showRoot.checked) {
          // Detect root note
          const isRoot =
            (mode === "scale" && rawNote === scaleRoot) ||
            (mode === "chord" && rawNote === chordRoot);

          if (isRoot) {
            ctx.strokeStyle = "#fff";   // or any color you want
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.arc(x, y, 24, 0, Math.PI * 2); // slightly larger than the note circle
            ctx.stroke();
          }
        }
        
        if (border) {
          ctx.lineWidth = 3;
          ctx.strokeStyle = "#fff";
          ctx.beginPath();
          ctx.arc(x,y,18,0,Math.PI*2);
          ctx.stroke();
        }

        ctx.fillStyle="#000";
        ctx.font="14px sans-serif";
        ctx.textAlign="center";
        ctx.textBaseline="middle";
        ctx.fillText(n,x,y);
      }
    }
  }
  ctx.globalAlpha = 1.0;
}

// ------------- MAIN RENDER -------------
function render() {
  let strings = [...TUNINGS[tuningSel.value]];
  if (flipSel.checked) strings.reverse();

  drawFretboard(strings, flipSel.checked);

  const chordRoot = chordRootSel.value;
  const chordType = chordTypeSel.value;
  const scaleRoot = scaleRootSel.value;
  const scaleMode = scaleModeSel.value;

  const chordNotes = getNotes(chordRoot, CHORD_INTERVALS[chordType]);
  const scaleNotes = getNotes(scaleRoot, MODES[scaleMode]);

  if (showScale.checked) {
    // scale bright, chord dim
    if (!hideScale.checked) plotNotes(strings, scaleNotes, "#0af", 1.0, false);
    if (!hideChord.checked) plotNotes(strings, chordNotes, "#ff0", 0.33, true);
  } else {
    // chord bright, scale dim
    if (!hideScale.checked) plotNotes(strings, scaleNotes, "#0af", 0.50, false);
    if (!hideChord.checked) plotNotes(strings, chordNotes, "#f60", 1.0, true);
  }
  
  textout(
    `Chord: ${displayNote(chordRootSel.value, useFlats.checked)} ${chordTypeSel.value}\n` +
    `Scale: ${displayNote(scaleRootSel.value, useFlats.checked)} ${scaleModeSel.value}\n` +
    `Tuning: ${tuningSel.value}\n\n` +
    `${gentext}`
  );
}

// ------------- EVENTS -------------
[
  chordRootSel, chordTypeSel,
  scaleRootSel, scaleModeSel,
  tuningSel, showScale, flipSel,
  showRoot, useFlats
].forEach(el => el.onchange = render);