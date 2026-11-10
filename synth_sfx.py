import math
import wave
import struct
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
AUDIO_DIR = BASE_DIR / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

def write_wav(filename, samples, sample_rate=44100):
    filepath = AUDIO_DIR / filename
    with wave.open(str(filepath), 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        frames = []
        for s in samples:
            val = max(-32767, min(32767, int(s * 32767)))
            frames.append(struct.pack('<h', val))
        wav.writeframes(b''.join(frames))
    print(f"[SFX] Synthesized: {filename}")

# 1. 裁判哨聲 (經典少林足球哨子：雙頻差頻拍音)
def make_whistle(filename="sfx_whistle.wav", duration=0.45, sample_rate=44100):
    n = int(sample_rate * duration)
    samples = []
    for i in range(n):
        t = i / sample_rate
        # 顫音調制 (trill)
        tremolo = 1.0 + 0.15 * math.sin(2 * math.pi * 32 * t)
        env = min(1.0, t * 40.0) * max(0.0, 1.0 - (t / duration) ** 2)
        # 2850Hz + 3120Hz 雙主音產生刺耳清脆金屬哨音
        sig = 0.5 * math.sin(2 * math.pi * 2850 * t * tremolo) + 0.5 * math.sin(2 * math.pi * 3120 * t * tremolo)
        # 加入微量白噪聲
        noise = (math.sin(t * 89231.2) * 43758.5453 % 1.0 - 0.5) * 0.1
        samples.append((sig + noise) * env * 0.85)
    write_wav(filename, samples, sample_rate)

# 2. 破風滑翔咻聲 (Whoosh / Swish: 空氣高速切割)
def make_whoosh(filename="sfx_whoosh.wav", duration=0.4, sample_rate=44100):
    n = int(sample_rate * duration)
    samples = []
    for i in range(n):
        t = i / sample_rate
        u = t / duration
        # 頻率從低掃到高再降回，模擬多普勒效應
        center_f = 300 + 1600 * math.sin(math.pi * u)
        env = math.sin(math.pi * u) ** 1.8
        # 調頻風噪
        noise = (math.sin(t * 99123.1) * 23421.1 % 1.0 - 0.5)
        tone = math.sin(2 * math.pi * center_f * t)
        samples.append((tone * 0.4 + noise * 0.6) * env * 0.9)
    write_wav(filename, samples, sample_rate)

# 3. 巨石/胖胖重擊悶雷聲 (Seismic Thud: 低頻沉重重擊)
def make_thud(filename="sfx_thud.wav", duration=0.6, sample_rate=44100):
    n = int(sample_rate * duration)
    samples = []
    for i in range(n):
        t = i / sample_rate
        f = 120 * math.exp(-t * 18.0) + 45  # 快速掉音頻 (120Hz -> 45Hz)
        env = math.exp(-t * 9.0)
        distortion = math.tanh(math.sin(2 * math.pi * f * t) * 2.5) * 0.6
        samples.append(distortion * env * 0.95)
    write_wav(filename, samples, sample_rate)

# 4. 高科技戰術激光光束 (Laser blip: NotebookLM 戰術光線)
def make_laser(filename="sfx_laser.wav", duration=0.35, sample_rate=44100):
    n = int(sample_rate * duration)
    samples = []
    for i in range(n):
        t = i / sample_rate
        f = 3200 * math.exp(-t * 22.0) + 300  # 急速激光降頻
        env = math.exp(-t * 10.0)
        sig = math.sin(2 * math.pi * f * t)
        samples.append(sig * env * 0.8)
    write_wav(filename, samples, sample_rate)

# 5. 相機快門喀嚓聲 (Camera Shutter: Google Photos 拍照定格)
def make_shutter(filename="sfx_shutter.wav", duration=0.25, sample_rate=44100):
    n = int(sample_rate * duration)
    samples = []
    for i in range(n):
        t = i / sample_rate
        # 雙點擊 (喀 - 嚓)
        click1 = math.exp(-abs(t - 0.03) * 120.0) * math.sin(2 * math.pi * 1800 * t)
        click2 = math.exp(-abs(t - 0.10) * 100.0) * math.sin(2 * math.pi * 1200 * t)
        samples.append((click1 * 0.7 + click2 * 0.85) * 0.9)
    write_wav(filename, samples, sample_rate)

# 6. 卡通彈跳蹦聲 (Boing / Spring: 起跳與擠壓拉伸)
def make_boing(filename="sfx_boing.wav", duration=0.45, sample_rate=44100):
    n = int(sample_rate * duration)
    samples = []
    for i in range(n):
        t = i / sample_rate
        env = math.exp(-t * 5.2)
        # 彈跳向上滑頻
        f = 160 + 380 * math.sin(math.pi * (t / duration) ** 0.6)
        # 顫音
        wobble = 1.0 + 0.12 * math.sin(2 * math.pi * 26 * t)
        sig = math.sin(2 * math.pi * f * wobble * t)
        samples.append(sig * env * 0.88)
    write_wav(filename, samples, sample_rate)

# 7. 水晶叮聲 (Ding: 高雅提示音)
def make_ding(filename="sfx_ding.wav", duration=0.6, sample_rate=44100):
    n = int(sample_rate * duration)
    samples = []
    for i in range(n):
        t = i / sample_rate
        env = math.exp(-t * 6.5)
        sig = (0.7 * math.sin(2 * math.pi * 1318.5 * t) + 
               0.3 * math.sin(2 * math.pi * 2637.0 * t))
        samples.append(sig * env * 0.85)
    write_wav(filename, samples, sample_rate)

# 8. 木質咚聲 (Dong: 沉穩打擊樂確認)
def make_dong(filename="sfx_dong.wav", duration=0.4, sample_rate=44100):
    n = int(sample_rate * duration)
    samples = []
    for i in range(n):
        t = i / sample_rate
        env = math.exp(-t * 9.0)
        sig = 0.8 * math.sin(2 * math.pi * 440.0 * t) + 0.2 * math.sin(2 * math.pi * 880.0 * t)
        samples.append(sig * env * 0.9)
    write_wav(filename, samples, sample_rate)

# 9. 璀璨金鈴鏘聲 (Chiang: 金牌頒獎高潮)
def make_chiang(filename="sfx_chiang.wav", duration=1.2, sample_rate=44100):
    n = int(sample_rate * duration)
    samples = []
    freqs = [1760.0, 2093.0, 3136.0, 4186.0]
    for i in range(n):
        t = i / sample_rate
        env = math.exp(-t * 3.8)
        sig = sum(math.sin(2 * math.pi * f * t) for f in freqs) / len(freqs)
        samples.append(sig * env * 0.9)
    write_wav(filename, samples, sample_rate)

# 10. Pingu 招牌「Noot Noot!」喇叭嘴叫聲（經典雙音階連吹）
def make_pingu_noot(filename="vo_pingu_noot.wav", sample_rate=44100):
    # Noot 1 (0.2s, 620Hz) + 短暫停頓 + Noot 2 (0.35s, 880Hz 喇叭諧波)
    dur = 0.65
    n = int(sample_rate * dur)
    samples = []
    for i in range(n):
        t = i / sample_rate
        sig = 0.0
        # 第一聲 Noot (0.05 ~ 0.25)
        if 0.04 <= t <= 0.24:
            local_t = t - 0.04
            env = math.sin(math.pi * (local_t / 0.20))
            f = 587.33  # D5
            sig = (math.sin(2*math.pi*f*local_t) + 0.5*math.sin(4*math.pi*f*local_t) + 0.25*math.sin(6*math.pi*f*local_t)) * env
        # 第二聲拉長 Noot!! (0.28 ~ 0.62)
        elif 0.28 <= t <= 0.62:
            local_t = t - 0.28
            env = math.sin(math.pi * (local_t / 0.34))
            f = 880.00  # A5 (高亢喇叭)
            # 奇次泛音營造玩具小號感
            sig = (math.sin(2*math.pi*f*local_t) + 0.6*math.sin(4*math.pi*f*local_t) + 0.4*math.sin(6*math.pi*f*local_t)) * env * 1.2
        samples.append(sig * 0.85)
    write_wav(filename, samples, sample_rate)

# 11. Pingu 疑惑驚呼「Huh?!」
def make_pingu_huh(filename="vo_pingu_huh.wav", duration=0.3, sample_rate=44100):
    n = int(sample_rate * duration)
    samples = []
    for i in range(n):
        t = i / sample_rate
        # 上揚音調 (350Hz -> 650Hz)
        f = 350 + 300 * (t / duration) ** 1.5
        env = math.sin(math.pi * (t / duration)) ** 1.2
        sig = (math.sin(2*math.pi*f*t) + 0.4*math.sin(4*math.pi*f*t)) * env
        samples.append(sig * 0.85)
    write_wav(filename, samples, sample_rate)

# 12. Pingu 得意大笑「Hehehe!」
def make_pingu_hehe(filename="vo_pingu_hehe.wav", duration=0.45, sample_rate=44100):
    n = int(sample_rate * duration)
    samples = []
    for i in range(n):
        t = i / sample_rate
        # 三段跳躍小笑聲
        cycle = (t * 8.0) % 1.0
        env = math.sin(math.pi * cycle) if cycle < 0.7 else 0.0
        f = 740 + 60 * math.sin(t * 20)
        sig = math.sin(2 * math.pi * f * t) * env
        samples.append(sig * 0.8)
    write_wav(filename, samples, sample_rate)

# 13. 程序化熱血少林卡林巴與戰鬥節奏 (BGM)
def generate_shaolin_clay_bgm(filename="bgm_kalimba.wav", total_duration=65.0, sample_rate=44100):
    bpm = 118
    beat_dur = 60.0 / bpm
    step_dur = beat_dur / 2.0  # 八分音符
    
    NOTE_FREQ = {
        "C3": 130.81, "G3": 196.00, "C4": 261.63, "D4": 293.66, "Eb4": 311.13, "E4": 329.63,
        "F4": 349.23, "G4": 392.00, "Ab4": 415.30, "A4": 440.00, "Bb4": 466.16, "B4": 493.88,
        "C5": 523.25, "D5": 587.33, "Eb5": 622.25, "E5": 659.25, "G5": 783.99, "C6": 1046.50
    }
    
    # 少林功夫感律動 (C 小調 / C 大調交織，帶有衝勁與幽默感)
    pattern = [
        ("C4", 0.0), ("C4", 0.5), ("G4", 1.0), ("C5", 1.5), ("Eb5", 2.0), ("D5", 2.5), ("C5", 3.0), ("G4", 3.5),
        ("Ab4", 4.0), ("C5", 4.5), ("Eb5", 5.0), ("G5", 5.5), ("G4", 6.0), ("B4", 6.5), ("D5", 7.0), ("F4", 7.5),
        ("C4", 8.0), ("Eb4", 8.5), ("G4", 9.0), ("C5", 9.5), ("D5", 10.0), ("C5", 10.5), ("G4", 11.0), ("Eb4", 11.5),
        ("F4", 12.0), ("Ab4", 12.5), ("C5", 13.0), ("Eb5", 13.5), ("G4", 14.0), ("D5", 14.5), ("C5", 15.0), ("C4", 15.5)
    ]
    
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
            
            note_len = int(sample_rate * 0.9)
            for s in range(note_len):
                idx = start_sample + s
                if idx >= total_samples:
                    break
                t = s / sample_rate
                # 琴鍵聲 + 輕快小鼓敲擊感
                tone = (0.7 * math.sin(2 * math.pi * freq * t) +
                        0.25 * math.sin(2 * math.pi * 3.0 * freq * t) +
                        0.05 * math.sin(2 * math.pi * 5.2 * freq * t))
                decay = math.exp(-t * 5.0)
                buffer[idx] += tone * decay * 0.38
                
        current_time += loop_dur

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
        
    print(f"[BGM] Synthesized Shaolin Clay Comedy BGM: {filename} ({total_duration:.1f}s)")

def synthesize_all():
    print("=== Synthesizing Full Shaolin Clay Stop-Motion Foley Arsenal ===")
    make_whistle()
    make_whoosh()
    make_thud()
    make_laser()
    make_shutter()
    make_boing()
    make_ding()
    make_dong()
    make_chiang()
    make_pingu_noot()
    make_pingu_huh()
    make_pingu_hehe()
    generate_shaolin_clay_bgm(total_duration=65.0)
    print("=== All 13 Sound Assets Successfully Generated! ===")

if __name__ == "__main__":
    synthesize_all()
