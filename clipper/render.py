import json, subprocess, sys
src, start, end, out, title = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], sys.argv[5]
words = [w for w in json.load(open("work/analysis.json"))["words"] if start <= w["s"] < end]
def ts(t):
    t = max(0, t - start); return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
groups, cur = [], []
for w in words:
    if cur and (len(cur) >= 3 or w["s"] - cur[-1]["e"] > 0.6): groups.append(cur); cur = []
    cur.append(w)
if cur: groups.append(cur)
ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,DejaVu Sans,78,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,7,2,5,60,60,0,1
Style: Title,DejaVu Sans,58,&H00FFFFFF,&H00FFFFFF,&H00B4288C,&H00000000,1,0,0,0,100,100,0,0,3,14,0,8,60,60,70,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ass += f"Dialogue: 1,0:00:00.00,{ts(end)},Title,,0,0,0,,{title}\n"
for i, g in enumerate(groups):
    e = min(g[-1]["e"] + 0.25, groups[i+1][0]["s"] if i+1 < len(groups) else end)
    txt = " ".join(w["w"] for w in g).upper()
    ass += f"Dialogue: 0,{ts(g[0]['s'])},{ts(e)},Cap,,0,0,0,,{{\\pos(540,760)}}{txt}\n"
open("work/cap.ass", "w").write(ass)
fc = ("[0:v]split=2[a][b];"
      "[a]crop=284:193:0:290,scale=1080:734:flags=lanczos[cam];"
      "[b]crop=582:640:480:40,scale=1080:1186:flags=lanczos[game];"
      "[cam][game]vstack,ass=work/cap.ass[v]")
subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",str(start),"-to",str(end),"-i",src,
    "-filter_complex",fc,"-map","[v]","-map","0:a","-r","30","-c:v","libx264","-preset","veryfast","-crf","21",
    "-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-af","loudnorm=I=-14:TP=-1.5","-movflags","+faststart",out],check=True)
