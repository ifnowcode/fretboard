// Strings are 6 → 1 (low to high), null = unused/muted, 0 = open in the shape
const CAGED_SHAPES = [
  {
    name: "C",
    pattern: [null, 3, 2, 0, 1, 0] // x32010
  },
  {
    name: "A",
    pattern: [null, 0, 2, 2, 2, 0] // x02220
  },
  {
    name: "G",
    pattern: [3, 2, 0, 0, 0, 3]    // 320003
  },
  {
    name: "E",
    pattern: [0, 2, 2, 1, 0, 0]    // 022100
  },
  {
    name: "D",
    pattern: [null, null, 0, 2, 3, 2] // xx0232
  }
];

function alignPatternToStrings(pattern, strings) {
  // If strings are reversed, reverse the pattern too
  if (flipSel.checked) {
    return [...pattern].reverse();
  }
  return pattern;
}

function notesForShapeAtOffset(strings, shape, offset) {
  // returns { frets: [...], notes: [...], hasRoot: bool, allInChord: bool }
  const pattern = alignPatternToStrings(shape.pattern, strings);
  
  const frets = [];
  const notes = [];

  for (let s = 0; s < strings.length; s++) {
    const relFret = pattern[s];
    if (relFret == null) {
      frets.push(null);
      notes.push(null);
      continue;
    }

    const absFret = relFret + offset;
    frets.push(absFret);

    const open = strings[s];
    const n = noteAt(open, absFret);
    notes.push(n);
  }

  return { frets, notes };
}


function findRootPositions(strings, rootNote) {
  const positions = []; // { stringIndex, fret }

  for (let s = 0; s < strings.length; s++) {
    const open = strings[s];
    for (let f = 0; f <= FRETS; f++) {
      const n = noteAt(open, f);
      if (n === rootNote) {
        positions.push({ stringIndex: s, fret: f });
      }
    }
  }
  return positions;
}


function resolveCAGEDShapes(strings, chordRoot, chordNotes) {
  const results = []; // { name, frets, minFret, maxFret }

  for (const shape of CAGED_SHAPES) {
    // Reasonable offset range: allow shapes to start slightly below 0 (for open)
    // and up to where they still fit on the board.
    for (let offset = -5; offset <= FRETS; offset++) {
      const { frets, notes } = notesForShapeAtOffset(strings, shape, offset);

      // Discard if any fretted note is off the board
      const usedFrets = frets.filter(f => f != null);
      if (!usedFrets.length) continue;
      if (Math.min(...usedFrets) < 0 || Math.max(...usedFrets) > FRETS) continue;

      // Must contain the root somewhere
      if (!notes.includes(chordRoot)) continue;

      // All fretted notes must be in the chord
      const allInChord = notes.every(n => n == null || chordNotes.includes(n));
      if (!allInChord) continue;

      const minFret = Math.min(...usedFrets);
      const maxFret = Math.max(...usedFrets);

      results.push({
        name: shape.name,
        frets,
        minFret,
        maxFret
      });
    }
  }

  // Sort by position up the neck, then by shape name
  results.sort((a, b) => a.minFret - b.minFret || a.name.localeCompare(b.name));

  // Optionally, keep only the first 5 distinct shapes by name
  const seen = new Set();
  const filtered = [];
  for (const r of results) {
    if (!seen.has(r.name)) {
      seen.add(r.name);
      filtered.push(r);
    }
    if (filtered.length === 5) break;
  }

  return filtered;
}

function plotCAGEDChord(strings, chordRoot, chordType, color) {
  const chordNotes = getNotes(chordRoot, CHORD_INTERVALS[chordType]);
  const shapes = resolveCAGEDShapes(strings, chordRoot, chordNotes);

  for (const shape of shapes) {

    // Draw the chord tones inside the shape window
    plotChord(strings, chordNotes, color, {
      minFret: shape.minFret,
      maxFret: shape.maxFret,
      minString: 1,
      maxString: strings.length,
      alpha: 0.95,
      border: true
    });

    // Compute bounding box
    const bounds = getShapeBounds(shape.frets);

    // Draw outline
    drawShapeOutline(strings, bounds, getRandomColor());

    // Draw label
    drawShapeLabel(strings, bounds, shape.name, "#ff0");
  }
}


function getShapeBounds(frets) {
  let minFret = Infinity;
  let maxFret = -Infinity;
  let minString = Infinity;
  let maxString = -Infinity;

  for (let s = 0; s < frets.length; s++) {
    const f = frets[s];
    if (f == null) continue;

    if (f < minFret) minFret = f;
    if (f > maxFret) maxFret = f;

    if (s < minString) minString = s;
    if (s > maxString) maxString = s;
  }

  return { minFret, maxFret, minString, maxString };
}

function drawShapeOutline(strings, bounds, color = "#fff") {
  const { minFret, maxFret, minString, maxString } = bounds;
  const h = canvas.height / (strings.length + 1);

  const x1 = 50 + minFret * 70;
  const x2 = 50 + maxFret * 70 + 70;
  const y1 = h * (minString + 1) - 25;
  const y2 = h * (maxString + 1) + 25;

  ctx.strokeStyle = color;
  ctx.lineWidth = 4;
  ctx.setLineDash([10, 6]);

  ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

  ctx.setLineDash([]);
}

function drawShapeTag(strings, bounds, label, color = "#fff") {
  const { minFret, minString } = bounds;
  const h = canvas.height / (strings.length + 1);

  const x = 50 + minFret * 70 + 10;
  const y = h * (minString + 1) - 35;

  ctx.fillStyle = "rgba(0,0,0,0.7)";
  ctx.fillRect(x - 6, y - 16, 40, 22);

  ctx.fillStyle = color;
  ctx.font = "16px sans-serif";
  ctx.textAlign = "left";
  ctx.textBaseline = "middle";
  ctx.fillText(label, x, y);
}

function drawShapeLabel(strings, bounds, label, color = "#fff") {
  const { minFret, maxFret, minString, maxString } = bounds;
  const h = canvas.height / (strings.length + 1);

  // Compute center of bounding box
  const x1 = 50 + minFret * 70;
  const x2 = 50 + maxFret * 70 + 70;
  const y1 = h * (minString + 1) - 25;
  const y2 = h * (maxString + 1) + 25;

  const cx = (x1 + x2) / 2;
  const cy = (y1 + y2) / 2;
  
  ctx.globalAlpha = 0.5;

  // Large, centered label with transparent background
  ctx.fillStyle = color;
  ctx.font = "bold 72px sans-serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";

  ctx.fillText(label, cx, cy);
  
  ctx.globalAlpha = 1.0;
}

