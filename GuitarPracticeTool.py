import math
import random

import PySimpleGUI as sg

# Global Variables

NOTES = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G'
]

ACCIDENTALS = [
    '#', '♮', 'b'
]

COMMON_SCALES = [
    'major',
    'harmonic minor',
    'melodic minor',
    'natural minor',
    'pentatonic major',
    'pentatonic minor',
    'pentatonic blues',
    'pentatonic neutral'
]

MODES = [
    'ionian',
    'dorian',
    'phrygian',
    'lydian',
    'mixolydian',
    'aeolian',
    'locrian',
]

CHORDS = [
    'Major',
    'Minor',
    '7',
    '5',
    'dim',
    'dim7',
    'aug',
    'sus2',
    'sus4',
    'maj7',
    'm7',
    '7sus4'
]

KEYS = {

}

for key in [*NOTES, *ACCIDENTALS, *COMMON_SCALES, *MODES, *CHORDS]:
    KEYS[key] = True

# Functions


def generatePractice() -> str:
    enabledNotes = list(filter(lambda note: KEYS[note], NOTES))
    enabledScalesAndChords = list(
        filter(lambda scale: KEYS[scale], [*COMMON_SCALES, *MODES, *CHORDS]))
    enabledAccidentals = list(filter(lambda acc: KEYS[acc], ACCIDENTALS))

    warnings = []

    if (len(enabledNotes) == 0):
        warnings.append('at least one note')

    if (len(enabledScalesAndChords) == 0):
        warnings.append('at least one scale or chord')

    if (len(warnings) > 0):
        return 'Please select' + ", and ".join(warnings) + '.'

    accidental = ''
    if (len(enabledAccidentals) > 0):
        accidental = random.choice(enabledAccidentals)

    if (accidental == '♮'):
        accidental = ''

    return random.choice(enabledNotes) + accidental + \
        ' ' + random.choice(enabledScalesAndChords)


# Components


def labeledCheckbox(label: str, key: str, initialState: bool) -> list:
    return sg.Checkbox(label, initialState, key='-%s-' % key, enable_events=True)


def checkBoxFrame(values, title) -> list:
    layout = [labeledCheckbox('all', title, initialState=True)]
    for value in values:
        layout.append(labeledCheckbox(value, value, KEYS[value]))
    return [sg.Frame(title, [layout])]

# Window


window = sg.Window(title="Scale Generator", layout=[
                   [checkBoxFrame(NOTES, 'Notes'), [checkBoxFrame(ACCIDENTALS, 'Accidentals'), sg.Text('(If none are selected, ♮ will be assumed)')], checkBoxFrame(COMMON_SCALES, 'Common Scales'), checkBoxFrame(MODES, 'Modes'), checkBoxFrame(CHORDS, 'Chords'), [sg.Text("Click 'Next Scale' to randomly pick a scale from the options you have selected.", key='-Readout-')], [sg.Button('Next Challenge', key='-Generate-')]]])

# Event Loop

while True:
    event, values = window.read()

    if (event == sg.WIN_CLOSED or event == 'end'):
        break
    elif (any('-%s-' % key == event for key in [*NOTES, *ACCIDENTALS, *COMMON_SCALES, *MODES])):
        key = event.replace('-', '')
        KEYS[key] = not KEYS[key]
    elif (event == '-Notes-'):
        targetValue = window[event].get()
        for note in NOTES:
            KEYS[note] = targetValue
            window['-%s-' % note].update(targetValue)
    elif (event == '-Common Scales-'):
        targetValue = window[event].get()
        for scale in COMMON_SCALES:
            KEYS[scale] = targetValue
            window['-%s-' % scale].update(targetValue)
    elif (event == '-Modes-'):
        targetValue = window[event].get()
        for mode in MODES:
            KEYS[mode] = targetValue
            window['-%s-' % mode].update(targetValue)
    elif (event == '-Accidentals-'):
        targetValue = window[event].get()
        for acc in ACCIDENTALS:
            KEYS[acc] = targetValue
            window['-%s-' % acc].update(targetValue)
    elif (event == '-Chords-'):
        targetValue = window[event].get()
        for chord in CHORDS:
            KEYS[chord] = targetValue
            window['-%s-' % chord].update(targetValue)
    elif (event == '-Generate-'):
        window['-Readout-'].update(generatePractice())
