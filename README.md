# 🎸 Fretboard Visualizer

A fast, deterministic, browser‑based fretboard engine for exploring **scales, chords, tunings, intervals, enharmonics, and generated progressions** across multiple stringed instruments. Built with clean, modular JavaScript and a canvas‑based rendering pipeline.

--

## ✨ Features

* Independent chord + scale selection  
Choose any chord over any scale (e.g., D major over C Ionian).

  * **Full enharmonic control**  
  Toggle flats/sharps with correct rendering and canonical internal note logic.

  * **Chord dictionary + interval engine** 
  Supports major, minor, dominant, altered, suspended, extended, jazz chords, and more.

  *  **Scale/mode system**  
  Includes major modes, pentatonics, blues, harmonic minor, chromatic, and custom sets.

  * **Multi‑instrument tunings** 
  Guitar, bass, violin, cello, mandolin, ukulele, banjo, and custom tunings.

  * **Root highlighting**  
  Optional root‑note detection with visual emphasis.

  * **Fretboard markers**
  Standard 3‑5‑7‑12 markers with double‑dot at 12.

  * **Song generator (GenSong)** 
  Random or key‑specific chord progressions with serialization to/from `localStorage`.

---

## 🧩 Architecture

  * `index.html` — UI layout and control bars

  * `fretboard.js` — rendering engine, enharmonic logic, event system

  * `gensong.js` — chord‑progression generator with save/load support

  * **CHORD_INTERVALS / MODES / TUNINGS** — declarative musical data tables

  * **Canvas renderer** — deterministic, no DOM churn, no leaks

---

## 🚀 Usage

#### Fretboard

  * Select **Chord Root, Chord Type, Scale Root, Scale Mode**

  * Toggle **Show Scale, Hide Chord, Hide Scale, Show Root, Flats**

  * Flip string order for left‑handed or upside‑down visualization

#### GenSong

js
```
const g = new GenSong();
g.random();          // random key
g.inKeyOf("Db", 8);  // fixed key
g.save("idea1");     // persist
g.load("idea1");     // restore
console.log(g.song());
```

---

## 📦 Local Storage Integration

The generator supports:

  * **save(name)** — serialize current progression

  * **load(name)** — restore a saved progression

Useful for sketching musical ideas and recalling them later.

---

## 🛠 Development

  * Pure JavaScript, no dependencies

  * Canvas‑based rendering

  * Deterministic event‑driven UI

  * Modular data tables for chords, scales, tunings

  * Clean separation of display vs. internal canonical note logic