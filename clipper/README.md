# Live-stream clipper (Twitch -> vertical captioned clip)

Three steps, run from a folder that has a `work/` directory:

1. `python record_live.py <twitch_channel> <seconds> work/live.mp4` - records the live stream (skips ad segments).
2. `python analyze.py work/live.mp4` - loudness per second + word-level transcript -> `work/analysis.json`.
3. `python render.py work/live.mp4 <start_s> <end_s> out.mp4 "Title text"` - 1080x1920, facecam on top, gameplay below, burned-in captions.

Needs: `pip install yt-dlp faster-whisper numpy`, and `ffmpeg` on PATH.

Notes:
- The crop boxes in `render.py` (facecam / gameplay regions) are set for one streamer's layout; adjust per stream.
- In the cloud environment `gta6-clipper`, Twitch video servers must be on the allowed-hosts list; they differ per stream.
