import numpy as np
import simpleaudio as sa
import argparse


def play_flow(playable_flow, sample_rate):
    # Combine all audio segments into one array
    if not playable_flow:
        print("No audio to play.")
        return

    combined_audio = np.concatenate(playable_flow)
    play_obj = sa.play_buffer(combined_audio, 1, 2, sample_rate)
    play_obj.wait_done()


def make_sine(frequency, duration, sample_rate, amplitude):
    # Generate the time axis
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # Generate the sine wave
    wave = amplitude * np.sin(2 * np.pi * frequency * t)

    # Ensure that the sound is in 16-bit format
    audio = (wave * 32767).astype(np.int16)

    return audio


def make_cosine(frequency, duration, sample_rate, amplitude, phase):
    # Generate the time axis
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # Generate the cosine wave
    wave = amplitude * np.sin(2 * np.pi * frequency * t + phase)

    # Ensure that the sound is in 16-bit format
    audio = (wave * 32767).astype(np.int16)

    return audio


def mk_note(note, duration, sample_rate):
    note_frequencies = {
        'C4': 261.63,
        'D4': 293.66,
        'E4': 329.63,
        'F4': 349.23,
        'G4': 392.00,
        'A4': 440.00,
        'B4': 493.88,
        'C5': 523.25
    }

    if note not in note_frequencies:
        print(f"Unknown note: {note}")
        return None

    frequency = note_frequencies[note]
    amplitude = 0.5

    audio = make_sine(frequency, duration, sample_rate, amplitude)

    return audio


def runtime(filename):
    playable_flow = []
    sample_rate = None

    with open(filename, 'r') as file:
        for line in file:
            tokens = line.strip().split()
            print(tokens)
            match tokens[0]:
                case 'sine':
                    amplitude = float(tokens[1])
                    frequency = float(tokens[2])
                    duration = float(tokens[3])
                    sample_rate = int(tokens[4])
                    audio = make_sine(frequency, duration, sample_rate, amplitude)
                    playable_flow.append(audio)
                    print(playable_flow)
                case 'cosine':
                    amplitude = float(tokens[1])
                    frequency = float(tokens[2])
                    duration = float(tokens[3])
                    sample_rate = int(tokens[4])
                    phase = int(tokens[5])
                    audio = make_cosine(frequency, duration, sample_rate, amplitude, phase)
                    playable_flow.append(audio)
                    print(playable_flow)
                case 'note':
                    note = str(tokens[1])
                    duration = float(tokens[2])
                    sample_rate = int(tokens[3])
                    audio = mk_note(note, duration, sample_rate)
                    if audio is not None:
                        playable_flow.append(audio)
                case 'play_flow':
                    play_flow(playable_flow, sample_rate)
                case _: print("Unknown Keyword")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lambda Voice Synth")
    parser.add_argument('file', type=str, help='Voix code file')
    args = parser.parse_args()

    """frequency = 440  # Frequency in Hz (A4 note)
    duration = 2  # Duration in seconds
    sample_rate = 44100  # Samples per second"""
    runtime(args.file)
