import math
import wave
import struct
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent
AUDIO_DIR = BASE_DIR / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# 1. 產生純數學程序化音效 (叮、咚、鏘、蹦) - 零版權風險、免外部依賴
def make_chime(filename, freqs, duration=0.8, sample_rate=44100):
    n_samples = int(sample_rate * duration)
    filepath = AUDIO_DIR / filename
    with wave.open(str(filepath), 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        frames = []
        for i in range(n_samples):
            t = i / sample_rate
            decay = math.exp(-t * 7.0)
            sample = 0.0
            for f in freqs:
                sample += math.sin(2.0 * math.pi * f * t)
            sample = (sample / len(freqs)) * decay * 0.9
            val = int(sample * 32767)
            frames.append(struct.pack('<h', max(-32767, min(32767, val))))
        wav.writeframes(b''.join(frames))
    print(f"[SFX] Synthesized: {filepath.name}")

def make_boing(filename, duration=0.4, sample_rate=44100):
    n_samples = int(sample_rate * duration)
    filepath = AUDIO_DIR / filename
    with wave.open(str(filepath), 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        frames = []
        for i in range(n_samples):
            t = i / sample_rate
            decay = math.exp(-t * 5.0)
            freq = 180 + 350 * math.sin(math.pi * (t / duration))
            sample = math.sin(2.0 * math.pi * freq * t) * decay * 0.85
            val = int(sample * 32767)
            frames.append(struct.pack('<h', max(-32767, min(32767, val))))
        wav.writeframes(b''.join(frames))
    print(f"[SFX] Synthesized: {filepath.name}")

# 2. 產生程序化 Kalimba (卡林巴琴) 溫潤背景音樂 - 100% 程式碼生成
def generate_procedural_kalimba_bgm(filename="bgm_kalimba.wav", total_duration=65.0, sample_rate=44100):
    """
    使用正弦泛音與指數衰減合成卡林巴琴音色，
    以 C 大調五度進行 (C - G - Am - F) 循環演奏輕快溫潤旋律。
    """
    bpm = 108
    beat_dur = 60.0 / bpm
    step_dur = beat_dur / 2.0  # 八分音符
    
    # 頻率對照表 (Hz)
    NOTE_FREQ = {
        "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23, "G4": 392.00, "A4": 440.00, "B4": 493.88,
        "C5": 523.25, "D5": 587.33, "E5": 659.25, "F5": 698.46, "G5": 783.99, "A5": 880.00, "B5": 987.77,
        "C6": 1046.50
    }
    
    # 和弦分解樣式 (4 小節循環)
    # C - G - Am - F
    pattern = [
        # Bar 1: C
        ("C4", 0.0), ("G4", 0.5), ("C5", 1.0), ("E5", 1.5), ("G4", 2.0), ("C5", 2.5), ("E5", 3.0), ("G5", 3.5),
        # Bar 2: G
        ("G3", 4.0), ("D4", 4.5), ("B4", 5.0), ("D5", 5.5), ("G4", 6.0), ("B4", 6.5), ("D5", 7.0), ("G5", 7.5),
        # Bar 3: Am
        ("A3", 8.0), ("E4", 8.5), ("C5", 9.0), ("E5", 9.5), ("A4", 10.0), ("C5", 10.5), ("E5", 11.0), ("A5", 11.5),
        # Bar 4: F
        ("F3", 12.0), ("C4", 12.5), ("A4", 13.0), ("C5", 13.5), ("F4", 14.0), ("A4", 14.5), ("C5", 15.0), ("E5", 15.5)
    ]
    # G3, A3, F3 frequencies
    NOTE_FREQ.update({"F3": 174.61, "G3": 196.00, "A3": 220.00})
    
    loop_dur = 16.0 * step_dur
    total_samples = int(sample_rate * total_duration)
    buffer = [0.0] * total_samples
    
    current_time = 0.0
    while current_time < total_duration:
        for note, beat_offset in pattern:
            note_time = current_time + (beat_offset * step_dur)
            if note_time >= total_duration:
                break
            start_sample = int(note_time * sample_rate)
            freq = NOTE_FREQ.get(note, 440.0)
            
            # 單音合成：卡林巴琴特徵 (基音 + 微弱金屬高次諧波 + 柔和擊搥 transient)
            note_len = int(sample_rate * 1.2)
            for s in range(note_len):
                idx = start_sample + s
                if idx >= total_samples:
                    break
                t = s / sample_rate
                # 泛音結構
                tone = (
                    0.75 * math.sin(2.0 * math.pi * freq * t) +
                    0.20 * math.sin(2.0 * math.pi * 3.0 * freq * t) +
                    0.05 * math.sin(2.0 * math.pi * 5.2 * freq * t)
                )
                decay = math.exp(-t * 4.2)
                buffer[idx] += tone * decay * 0.35
                
        current_time += loop_dur

    # 輸出 WAV
    filepath = AUDIO_DIR / filename
    with wave.open(str(filepath), 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        frames = []
        for val in buffer:
            clipped = max(-0.95, min(0.95, val))
            frames.append(struct.pack('<h', int(clipped * 32767)))
        wav.writeframes(b''.join(frames))
        
    print(f"[BGM] Synthesized Procedural Kalimba BGM: {filepath.name} ({total_duration:.1f}s)")

def synthesize_all():
    print("=== Synthesizing All Procedural Audio Assets ===")
    make_chime("sfx_ding.wav", [1318.5, 2637.0], duration=0.6)
    make_chime("sfx_dong.wav", [440.0, 880.0], duration=0.4)
    make_chime("sfx_chiang.wav", [1760.0, 2093.0, 3520.0], duration=1.2)
    make_boing("sfx_boing.wav", duration=0.4)
    generate_procedural_kalimba_bgm("bgm_kalimba.wav", total_duration=65.0)
    print("=== All Audio Synthesis Complete! ===")

if __name__ == "__main__":
    synthesize_all()
