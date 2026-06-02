// ------------- UI ELEMENTS -------------
let hideNotes = false;

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
const showCaged      = document.getElementById("showCaged");

showScale.addEventListener("change", () => {
  if (showScale.checked) hideScale.checked = false;
  render();
});
hideScale.addEventListener("change", () => {
  if (hideScale.checked) {
    showScale.checked = false;
    hideChord.checked = false;
  }
  render();
});
hideChord.addEventListener("change", () => {
  if (hideChord.checked) {
    showScale.checked = true;
    hideScale.checked = false;
    showCaged.checked = false;
  } else {
    if (hideScale.checked) {
      showScale.checked = false;
    }
  }
  render();
});
showCaged.addEventListener("change", () => {
  if (showCaged.checked) {
    hideChord.checked = false;
  }
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

// ------------- DRAW FRETBOARD -------------
function drawFretboard(strings, reversed=false) {
  ctx.clearRect(0,0,canvas.width,canvas.height);
  const h = canvas.height / (strings.length+1);

  // frets
  for (let f=0; f<=FRETS; f++) {
    ctx.strokeStyle = f === 1 ? "#fff" : "#666";
    ctx.lineWidth = f === 1 ? 6 : 2;
    const x = 50 + f*70;
    ctx.beginPath();
    ctx.moveTo(x, h);
    ctx.lineTo(x, h*strings.length);
    ctx.stroke();
    
    if (strings.length >= 4) {
      // Fretboard position markers (3, 5, 7, 12)
      const markerFrets = [3, 5, 7, 9, 12, 15, 17, 19, 21, 24];
      if (markerFrets.includes(f)) {
        const dotX = x + 35; // center between frets
        const midY = (h + h * strings.length) / 2;

        ctx.fillStyle = "#000"; // black, unobtrusive

        if (f === 12 || f === 24) {
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
  ctx.strokeStyle="#a70";
  for (let s=1; s<=strings.length; s++) {
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

function plotChord(strings, chordNotes, color, {
    minFret = 0,
    maxFret = FRETS,
    minString = 1,
    maxString = strings.length,
    alpha = 1.0,
    border = true
  } = {}) {

  const h = canvas.height / (strings.length + 1);
  ctx.globalAlpha = alpha;

  const chordRoot = chordRootSel.value;
  const scaleRoot = scaleRootSel.value;
  const mode = showScale.checked ? "scale" : "chord";

  for (let s = 0; s < strings.length; s++) {

    // Skip strings outside the allowed range
    const stringNumber = s + 1;
    if (stringNumber < minString || stringNumber > maxString) continue;

    const open = strings[s];

    for (let f = minFret; f <= maxFret; f++) {

      const rawNote = noteAt(open, f);

      // Only plot notes that belong to the chord
      if (!chordNotes.includes(rawNote)) continue;

      const display = displayNote(rawNote, useFlats.checked);

      const x = 50 + f * 70 + 35;
      const y = h * (s + 1);

      // Filled circle
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(x, y, 13, 0, Math.PI * 2);
      ctx.fill();

      // Root highlighting (same logic as plotNotes)
      if (showRoot.checked) {
        const isRoot =
          (mode === "scale" && rawNote === scaleRoot) ||
          (mode === "chord" && rawNote === chordRoot);

        if (isRoot) {
          ctx.strokeStyle = "#fff";
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.arc(x, y, 24, 0, Math.PI * 2);
          ctx.stroke();
        }
      }

      // Optional border ring
      if (border) {
        ctx.lineWidth = 3;
        ctx.strokeStyle = "#fff";
        ctx.beginPath();
        ctx.arc(x, y, 18, 0, Math.PI * 2);
        ctx.stroke();
      }

      // Note label
      ctx.fillStyle = "#000";
      ctx.font = "14px sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(display, x, y);
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

  if (!hideNotes) {
    if (showCaged.checked) {
      //console.log("Plot CAGED");
      plotCAGEDChord(strings, chordRoot, chordType, "#f60");
    } else {
      if (showScale.checked) {
        // scale bright, chord dim
        if (!hideScale.checked) plotNotes(strings, scaleNotes, "#0af", 1.0, false);
        if (!hideChord.checked) plotNotes(strings, chordNotes, "#ff0", 0.33, true);
      } else {
        // chord bright, scale dim
        if (!hideScale.checked) plotNotes(strings, scaleNotes, "#0af", 0.50, false);
        if (!hideChord.checked) plotNotes(strings, chordNotes, "#f60", 1.0, true);
      }
    }
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

document.addEventListener("keydown", (e) => {
  //console.log(e.key);
  
  if (e.key === "h" || e.key === "H") {
    // hide the notes
    hideNotes = !hideNotes;
    console.log("[H]ide notes", hideNotes);
    render();
  }
});