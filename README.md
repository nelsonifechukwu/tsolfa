# tsolfa

Scan a black-and-white music sheet and output its tonic solfa
(do-re-mi-fa-so-la-ti) notation.

## Project layout

```text
tsolfa/
├── core/
│   ├── transcription.py    SheetTranscriber — orchestrates the pipeline
│   ├── notation.py         SolfaConverter — note name -> solfa given a key
│   └── theory.py           MusicalTheory — keys, scales, accidentals
├── vision/
│   ├── preprocessing.py    SheetPreprocessor — image -> binary, staff lines
│   └── segmentation.py     SymbolSegmenter — note-head bounding boxes
├── data/sheets/            test sheet-music PNGs
└── tests/unit/             pytest unit tests

examples/                   runnable usage examples
```

## What each module does today

- **`vision/preprocessing.py`** — ✅ working. Otsu binarization,
  staff-line detection, staff-line removal.
- **`vision/segmentation.py`** — ✅ working for note heads only.
  Finds note-head bounding boxes via morphological closing + contour
  filtering.
- **`core/theory.py`** — 🟡 partial. Circle of fifths, key-signature →
  accidentals map, major↔minor conversion, scale degrees.
  `detect_key_from_accidentals` is still a stub.
- **`core/notation.py`** — ❌ stubs. `SolfaConverter` exists but
  `convert_to_solfa`, `format_solfa_output`, and the key-mappings init
  are all unimplemented.
- **`core/transcription.py`** — 🟡 partial. Wires preprocessor +
  segmenter. `transcribe()` runs the CV pipeline but returns nothing
  yet (no pitch mapping, no key detection, no solfa output).

## Pipeline

```text
sheet.png
    │  preprocessor.binarize
    ▼
binary image
    │  preprocessor.detect_staff_lines
    ▼
staff-line bands  ────┐
    │  preprocessor.remove_staff_lines
    ▼                 │
notes-only binary     │
    │  segmenter.detect_note_heads
    ▼                 │
(cx, cy, w, h) boxes ◀┘   ←── pipeline currently ends here
    │
    │  [TODO] map cy + staff lines → pitch (C4, D4, …)
    ▼
note pitches
    │  [TODO] detect key signature → MusicalTheory.detect_key_from_accidentals
    ▼
key
    │  [TODO] SolfaConverter.convert_to_solfa(pitches, key)
    ▼
solfa output ("do re mi …")
```

## Quickstart

```bash
make install-dev
make test
```

```python
from tsolfa import SheetTranscriber

# silent (default)
SheetTranscriber().transcribe("tsolfa/data/sheets/sheet.png")

# with cv2.imshow debug windows at each pipeline stage
SheetTranscriber(debug=True).transcribe("tsolfa/data/sheets/sheet.png")
```

## Resume here — implementation roadmap

Each step says where to put the code and what to write next. Do them in
order; each one feeds the next.

### Step 1 — Map note-head Y → pitch

**File:** new method in `vision/segmentation.py`, e.g.
`assign_pitches(note_heads, staff_lines) -> List[Tuple[box, pitch_name]]`

For a treble clef, the five staff lines top-to-bottom are F5, D5, B4, G4,
E4; the four spaces between are E5, C5, A4, F4. Below/above the staff,
each ledger-line step is one diatonic step (D4, C4, …; G5, A5, …).

Compute the y-center of each staff line and the staff spacing
(`staff_lines[1].center - staff_lines[0].center`). For each note head's
`center_y`, find which line/space slot it falls into and assign the
corresponding pitch name. Start by hardcoding treble clef — clef
detection comes later.

### Step 2 — Implement `MusicalTheory.detect_key_from_accidentals`

**File:** `core/theory.py`

The function takes `(sharps: int, flats: int)` and returns a
`KeySignature`. The order of sharps in a key signature is fixed:
F#, C#, G#, D#, A#, E#, B# (so 1 sharp = G major, 2 = D major, …).
The order of flats: Bb, Eb, Ab, Db, Gb, Cb, Fb (1 flat = F major, …).
Hand-write the lookup; it's 15 cases.

### Step 3 — Detect the key signature on the sheet

**File:** new method in `vision/segmentation.py`, e.g.
`detect_key_signature_accidentals(binary_img, staff_lines)`

The key signature is the cluster of sharps or flats just after the clef
at the start of each staff. Scan the leftmost ~15% of the staff region
for "#" and "♭" shapes (template match or contour shape). Output
`(sharps_count, flats_count)`, hand that to
`MusicalTheory.detect_key_from_accidentals`.

For a quick first version, just hardcode the key (e.g. C major) and come
back to this once the rest of the pipeline works end-to-end.

### Step 4 — Implement `SolfaConverter`

**File:** `core/notation.py`

- `_initialize_key_mappings`: for each `KeySignature`, build a dict
  `{note_name: SolfaNote}` where the key's tonic maps to `DO`, second
  scale degree to `RE`, etc. `MusicalTheory.get_scale_degrees(key)`
  already returns the seven notes of the scale in order.
- `convert_to_solfa(notes, key)`: look up each note name in the
  appropriate key's mapping.
- `format_solfa_output(solfa_notes)`: join `.value` with spaces.

### Step 5 — Wire it all up in `SheetTranscriber.transcribe`

**File:** `core/transcription.py`

Populate and return `TranscriptionResult`:

```python
def transcribe(self, image_path):
    binary = self.preprocessor.binarize(image_path)
    _, staff_lines = self.preprocessor.detect_staff_lines(binary)
    img_no_lines = self.preprocessor.remove_staff_lines(binary, staff_lines)
    note_heads = self.segmenter.detect_note_heads(img_no_lines, staff_lines)

    pitches = self.segmenter.assign_pitches(note_heads, staff_lines)       # step 1
    sharps, flats = self.segmenter.detect_key_signature_accidentals(...)   # step 3
    key = MusicalTheory().detect_key_from_accidentals(sharps, flats)       # step 2

    self.converter = SolfaConverter()                                       # step 4
    solfa = self.converter.convert_to_solfa([p for _, p in pitches], key.value)
    return TranscriptionResult(
        solfa_notation=[s.value for s in solfa],
        key_signature=key.value,
    )
```

### Step 6 — Un-skip the tests

**File:** `tsolfa/tests/unit/test_*.py`

Both test files have `@pytest.mark.skip("Implementation pending")` cases
for `test_convert_to_solfa`, `test_format_solfa_output`,
`test_transcribe_single_sheet`, `test_transcribe_batch`. Remove the
skip markers and fill in real assertions as each step lands.

## Later phases (post-solfa)

Original stretch goals, deferred until the solfa pipeline works:

- Find the beat / note durations (whole/half/quarter notes from stem
  and flag detection)
- Synthesize singing playback from solfa + durations
- Hum / sing-song recognition (audio in → solfa)
- Train an ML model end-to-end: raw sheet image → transcribed solfa.
  (When you start this, recreate `tsolfa/vision/recognition.py` — it
  was removed because the symbol-recognition phase hadn't started.)
