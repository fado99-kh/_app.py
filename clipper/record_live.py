import sys, time, subprocess, urllib.request, collections
channel, seconds, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
def playlist_url():
    return subprocess.run([sys.executable, "-m", "yt_dlp", "--no-warnings", "-f", "best[height<=720]", "-g",
                           f"https://www.twitch.tv/{channel}"], capture_output=True, text=True).stdout.strip().splitlines()[-1]
def get(u, t=20):
    return urllib.request.urlopen(u, timeout=t).read()
url = playlist_url(); print("playlist", url[:34], flush=True)
seen = collections.OrderedDict(); got = 0.0; ads = 0; errs = collections.Counter()
with open(out, "wb") as f:
    while got < seconds:
        try: lines = get(url).decode().splitlines()
        except Exception as e:
            errs[type(e).__name__] += 1; url = playlist_url(); time.sleep(1); continue
        dur, title = 0, ""
        for ln in lines:
            if ln.startswith("#EXT-X-MAP:") and not f.tell():
                f.write(get(ln.split('URI="')[1].split('"')[0]))
        for ln in lines:
            if ln.startswith("#EXTINF:"):
                d, _, title = ln[8:].partition(","); dur = float(d)
            elif ln and not ln.startswith("#"):
                if ln in seen: continue
                seen[ln] = 1
                if "live" not in title: ads += 1; continue
                try: f.write(get(ln)); got += dur
                except Exception as e: errs[ln.split("/")[2] + ":" + type(e).__name__] += 1
        time.sleep(1.5)
print("recorded", round(got), "s; ad segments skipped", ads, "; errors", dict(errs))
