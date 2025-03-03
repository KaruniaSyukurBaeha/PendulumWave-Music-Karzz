import pygame
import numpy as np
import time
import os
from audio_processor import process_audio, extract_chords

# Konstanta fisika
g = 9.81  # Gravitasi (m/s^2)
NUM_PENDULUMS = 12  # Jumlah pendulum sesuai jumlah chord
LENGTHS = np.linspace(1, 2, NUM_PENDULUMS)  # Panjang pendulum bervariasi

# Warna untuk setiap chord
CHORD_COLORS = {
    "C": (255, 0, 0), "C#": (200, 50, 50),
    "D": (0, 255, 0), "D#": (0, 200, 50),
    "E": (0, 0, 255),
    "F": (255, 255, 0), "F#": (200, 200, 50),
    "G": (255, 165, 0), "G#": (200, 140, 50),
    "A": (128, 0, 128), "A#": (100, 0, 100),
    "B": (0, 255, 255)
}
CHORDS = list(CHORD_COLORS.keys())  # Urutan tetap chord

class Pendulum:
    def __init__(self, index, x, length, chord):
        self.index = index
        self.x = x
        self.length = length * 250  # Panjang lebih panjang
        self.chord = chord
        self.y = 150
        self.active = False
        self.color = CHORD_COLORS[chord]
        self.glow = 0

    def update(self, t, active_chord):
        if self.chord == active_chord:
            self.active = True
            self.y = int(200 + np.sin(t * np.pi / 2) * self.length)
            self.glow = min(self.glow + 10, 150)
        else:
            self.active = False
            self.y = 200 + self.length // 2  # Panjang tali lebih panjang saat tidak aktif
            self.glow = max(self.glow - 10, 0)

    def draw(self, screen, font):
        pygame.draw.aaline(screen, (255, 255, 255), (450, 50), (self.x, self.y))
        pygame.draw.circle(screen, self.color, (self.x, self.y), 15)
        pygame.draw.circle(screen, (self.color[0], self.color[1], self.color[2], self.glow), (self.x, self.y), 25, 2)
        text_surface = font.render(self.chord, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.x, self.y))  # Menyesuaikan posisi teks agar tetap di dalam lingkaran
        screen.blit(text_surface, text_rect)

def run_simulation(file_path):
    pygame.init()
    pygame.mixer.init()
    WIDTH, HEIGHT = 900, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    file_path = os.path.abspath(file_path)
    if not os.path.exists(file_path):
        print(f"Error: File tidak ditemukan di {file_path}")
        return
    print(f"Menggunakan file musik: {file_path}")

    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    tempo, beat_times = process_audio(file_path)
    chords = extract_chords(file_path)
    chord_index = 0
    start_time = time.time()
    music_duration = pygame.mixer.Sound(file_path).get_length()

    pendulums = [Pendulum(i, WIDTH // 14 * (i + 1), LENGTHS[i], CHORDS[i]) for i in range(NUM_PENDULUMS)]

    running = True
    while running:
        screen.fill((5, 5, 25))  # Background lebih gelap dan modern
        
        top_x = WIDTH // 2
        top_y = 50
        for pendulum in pendulums:
            pygame.draw.aaline(screen, (180, 180, 255), (top_x, top_y), (pendulum.x, pendulum.y))
        
        t = time.time() - start_time  

        if t >= music_duration:
            running = False

        if chord_index < len(chords) and t >= chords[chord_index][0]:
            active_chord = chords[chord_index][1][:2] if len(chords[chord_index][1]) > 1 and chords[chord_index][1][1] == "#" else chords[chord_index][1][:1]
            chord_index += 1
        else:
            active_chord = None

        for pendulum in pendulums:
            pendulum.update(t, active_chord)
            pendulum.draw(screen, font)
        
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    file_path = os.path.join("assets", "sample.mp3")
    run_simulation(file_path)
