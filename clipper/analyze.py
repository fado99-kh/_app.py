import json, subprocess, sys, numpy as np
from faster_whisper import WhisperModel
src = sys.argv[1]
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",src,"-vn","-ac","1","-ar","16000","work/a.wav"],check=True)
import wave
w = wave.open("work/a.wav"); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)/32768
sr = 16000; n = len(a)//sr
rms = np.array([np.sqrt(np.mean(a[i*sr:(i+1)*sr]**2)) for i in range(n)])
m = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=4)
segs, _ = m.transcribe(a, word_timestamps=True, vad_filter=True)
words = [{"s":w.start,"e":w.end,"w":w.word.strip()} for s in segs for w in s.words]
json.dump({"rms":rms.tolist(),"words":words}, open("work/analysis.json","w"))
print("seconds", n, "words", len(words))
