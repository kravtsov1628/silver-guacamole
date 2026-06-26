import math
import struct
import pygame


BUTTONS = {
    "UP": 26,
    "DOWN": 19,
    "LEFT": 5,
    "RIGHT": 6,
    "A": 13,
    "B": 21,
    "X": 20,
    "Y": 16,
    "START": 24,
    "SELECT": 12
}

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    for pin in BUTTONS.values():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    HAS_GPIO = True
except (ImportError, RuntimeError):
    HAS_GPIO = False


def pressed(button):
    if HAS_GPIO:
        return GPIO.input(BUTTONS[button]) == GPIO.LOW

    keys = pygame.key.get_pressed()
    if button == "UP":
        return keys[pygame.K_UP] or keys[pygame.K_w]
    elif button == "DOWN":
        return keys[pygame.K_DOWN] or keys[pygame.K_s]
    elif button == "LEFT":
        return keys[pygame.K_LEFT] or keys[pygame.K_a]
    elif button == "RIGHT":
        return keys[pygame.K_RIGHT] or keys[pygame.K_d]
    elif button == "A":
        return keys[pygame.K_z] or keys[pygame.K_j]
    elif button == "B":
        return keys[pygame.K_x] or keys[pygame.K_k]
    elif button == "X":
        return keys[pygame.K_c] or keys[pygame.K_u]
    elif button == "Y":
        return keys[pygame.K_v] or keys[pygame.K_i]
    elif button == "START":
        return keys[pygame.K_RETURN]
    elif button == "SELECT":
        return keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]
    return False


def cleanup():
    if HAS_GPIO:
        GPIO.cleanup()

def generate_sweep(start_freq, end_freq, duration, wave_type="sine", volume=0.08):
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=22050, size=-16, channels=1)
    except Exception:
        return None

    sample_rate = 22050
    num_samples = int(sample_rate * duration)
    buffer = bytearray()

    for i in range(num_samples):
        t = i / sample_rate
        k = (end_freq - start_freq) / duration
        phase = 2 * math.pi * (start_freq * t + 0.5 * k * t * t)

        if wave_type == "sine":
            val = math.sin(phase)
        elif wave_type == "square":
            val = 1.0 if math.sin(phase) >= 0 else -1.0
        elif wave_type == "triangle":
            val = 2.0 * abs(2.0 * ((phase / (2 * math.pi)) - math.floor((phase / (2 * math.pi)) + 0.5))) - 1.0
        elif wave_type == "sawtooth":
            val = 2.0 * ((phase / (2 * math.pi)) - math.floor((phase / (2 * math.pi)) + 0.5))
        else:
            val = math.sin(phase)

        envelope = 1.0 - (i / num_samples)
        sample = int(val * 32767 * volume * envelope)
        buffer.extend(struct.pack('<h', sample))

    try:
        return pygame.mixer.Sound(buffer=bytes(buffer))
    except Exception:
        return None


def generate_melody(notes, tempo=180, wave_type="square", volume=0.08):
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=22050, size=-16, channels=1)
    except Exception:
        return None

    sample_rate = 22050
    buffer = bytearray()
    beat_duration = 60.0 / tempo

    for freq, duration_ratio in notes:
        duration = beat_duration * duration_ratio
        num_samples = int(sample_rate * duration)

        for i in range(num_samples):
            t = i / sample_rate
            val = math.sin(2 * math.pi * freq * t)
            if wave_type == "square":
                val = 1.0 if val >= 0 else -1.0
            elif wave_type == "triangle":
                val = 2.0 * abs(2.0 * (t * freq - math.floor(t * freq + 0.5))) - 1.0
            elif wave_type == "sawtooth":
                val = 2.0 * (t * freq - math.floor(t * freq + 0.5))

            envelope = max(0.0, 1.0 - (i / num_samples))
            sample = int(val * 32767 * volume * envelope)
            buffer.extend(struct.pack('<h', sample))

    try:
        return pygame.mixer.Sound(buffer=bytes(buffer))
    except Exception:
        return None


class SoundManager:
    def __init__(self):
        self.enabled = True
        self.is_bgm_playing = False
        self.bgm_sound = None
        self.bgm_channel = None
        self.eat_sound = generate_sweep(450, 900, 0.06, "sine", 0.12)
        self.power_eat_sound = generate_sweep(250, 1000, 0.15, "triangle", 0.18)
        self.death_sound = generate_sweep(350, 40, 0.6, "sawtooth", 0.22)
        start_notes = [(523.25, 0.5), (659.25, 0.5), (783.99, 0.5), (1046.50, 1.0)]
        self.start_sound = generate_melody(start_notes, tempo=300, wave_type="square", volume=0.1)
        victory_notes = [
            (523.25, 0.5), (587.33, 0.5), (659.25, 0.5), (698.46, 0.5),
            (783.99, 0.7), (880.00, 0.7), (987.77, 0.7), (1046.50, 1.5)
        ]
        self.victory_sound = generate_melody(victory_notes, tempo=330, wave_type="square", volume=0.1)
        game_over_notes = [(392.00, 1.0), (349.23, 1.0), (311.13, 1.0), (261.63, 2.5)]
        self.game_over_sound = generate_melody(game_over_notes, tempo=150, wave_type="sawtooth", volume=0.12)
        bgm_notes = [
            (110.00, 1.0), (165.00, 1.0), (220.00, 1.0), (165.00, 1.0),
            (130.81, 1.0), (196.00, 1.0), (261.63, 1.0), (196.00, 1.0),
            (146.83, 1.0), (220.00, 1.0), (293.66, 1.0), (220.00, 1.0),
            (130.81, 1.0), (196.00, 1.0), (261.63, 1.0), (196.00, 1.0)
        ]
        self.bgm_sound = generate_melody(bgm_notes, tempo=333, wave_type="triangle", volume=0.035)

    def play_eat(self):
        if self.enabled and self.eat_sound:
            self.eat_sound.play()

    def play_power_eat(self):
        if self.enabled and self.power_eat_sound:
            self.power_eat_sound.play()

    def play_death(self):
        if self.enabled and self.death_sound:
            self.death_sound.play()

    def play_start(self):
        if self.enabled and self.start_sound:
            self.start_sound.play()

    def play_victory(self):
        if self.enabled and self.victory_sound:
            self.victory_sound.play()

    def play_game_over(self):
        if self.enabled and self.game_over_sound:
            self.game_over_sound.play()

    def start_bgm(self):
        if self.enabled and self.bgm_sound and not self.is_bgm_playing:
            self.bgm_channel = self.bgm_sound.play(loops=-1)
            self.is_bgm_playing = True

    def stop_bgm(self):
        if self.bgm_sound and self.is_bgm_playing:
            self.bgm_sound.stop()
            self.is_bgm_playing = False
            self.bgm_channel = None
