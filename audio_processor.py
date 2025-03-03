import librosa
import numpy as np
import os

def process_audio(file_path):
    """
    Memproses file MP3 untuk mengekstrak tempo (BPM) dan beat.
    """
    y, sr = librosa.load(file_path, sr=None)  # Load file dengan sample rate asli
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    
    return tempo, beat_times

def extract_chords(file_path):
    """
    Menganalisis chord progression dari file audio.
    """
    y, sr = librosa.load(file_path, sr=None)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chord_times = librosa.frames_to_time(np.argmax(chroma, axis=0), sr=sr)
    
    chord_labels = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    detected_chords = [chord_labels[np.argmax(chroma[:, i])] for i in range(chroma.shape[1])]
    
    return list(zip(chord_times, detected_chords))

if __name__ == "__main__":
    #file_path = "assets/sample.mp3"
    file_path = os.path.join("assets", "sample.mp3")
    tempo, beat_times = process_audio(file_path)
    print(f"Detected Tempo: {float(tempo):.2f} BPM")
    print("Beat Times:", beat_times)
    # print("Mencari file di:", os.path.abspath(file_path))

