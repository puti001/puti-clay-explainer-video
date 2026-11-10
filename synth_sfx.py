import math
import wave
import struct
from pathlib import Path
import json
import subprocess

BASE = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法")
AUDIO_DIR = BASE / "audio"
SFX_DIR = Path(r"C:\antigravity\影片\shanshiba-workflow-colab\sfx")
BGM_PATH = Path(r"C:\antigravity\影片\minimax_task\bgm.mp3")

# Synthesize pure crystal bells & dings for UI cartoon Foley (叮、咚、鏘)
def make_chime(filename, freqs, duration=0.8, sample_rate=44100):
    n_samples = int(sample_rate * duration)
    with wave.open(str(AUDIO_DIR / filename), 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        frames = []
        for i in range(n_samples):
            t = i / sample_rate
            # Harmonic decay
            decay = math.exp(-t * 7.0)
            sample = 0
            for f in freqs:
                sample += math.sin(2 * math.pi * f * t)
            sample = (sample / len(freqs)) * decay * 0.9
            val = int(sample * 32767)
            frames.append(struct.pack('<h', max(-32767, min(32767, val))))
        wav.writeframes(b''.join(frames))
    print(f"Synthesized: {filename}")

# 1. 叮 (Ding): 1318.5 Hz (High E6 crystal chime)
make_chime("sfx_ding.wav", [1318.5, 2637.0], duration=0.6)
# 2. 咚 (Dong): 440 Hz (Woody warm pop)
make_chime("sfx_dong.wav", [440.0, 880.0], duration=0.4)
# 3. 鏘 (Chiang - Golden Bell for winner card): 1760 Hz + 2093 Hz harmonics
make_chime("sfx_chiang.wav", [1760.0, 2093.0, 3520.0], duration=1.2)
# 4. 蹦 (Cartoon Boing): frequency slide
def make_boing(filename, duration=0.4, sample_rate=44100):
    n_samples = int(sample_rate * duration)
    with wave.open(str(AUDIO_DIR / filename), 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        frames = []
        for i in range(n_samples):
            t = i / sample_rate
            decay = math.exp(-t * 5.0)
            f = 220 + math.sin(t * 35.0) * 80 + t * 200
            sample = math.sin(2 * math.pi * f * t) * decay * 0.85
            val = int(sample * 32767)
            frames.append(struct.pack('<h', max(-32767, min(32767, val))))
        wav.writeframes(b''.join(frames))
    print(f"Synthesized: {filename}")

make_boing("sfx_boing.wav", duration=0.45)
