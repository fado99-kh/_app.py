# Context for Claude

## About the user
- Based in Canada. Apply Canadian availability when discussing platform monetization, payments, and regional features.
- Writes in Levantine Arabic; reply in Arabic.

## Current project: GTA 6 short-form clips channel
- Goal: build a short-form channel in the style of the Instagram page `gta6.clipsmp4` (short GTA 6 clips with meme-style captions).
- Target platforms: YouTube Shorts, TikTok, Instagram Reels, Facebook Reels.
- Known constraint: Instagram (since April 2026) removes accounts that mainly repost others' content from recommendations, so prefer original gameplay or clips with meaningful added value.
- Still open: whether the user owns GTA 6 and can record their own gameplay, and whether the content will be in Arabic or English.

## Clipping workflow (tested 2026-11-20)
- `clipper/` holds a working Twitch-live -> vertical captioned clip pipeline (see `clipper/README.md`).
- Use the cloud environment `gta6-clipper`; Twitch segment hosts vary per stream and each must be added to its allowed hosts.
- Set `HF_HUB_DISABLE_XET=1` when downloading the Whisper model; pass audio to faster-whisper as a numpy array.

## Monetization findings (checked 2026-11-20, third-party trackers; re-verify before acting)
- Money for clippers comes from pay-per-view campaigns, mostly on Content Rewards (runs on Whop; 10% fee on payouts), not from the page itself.
- OpenClip counted 13 open GTA 6 campaigns on 2026-11-19: per-1K rates $0.35-$2.00 (most $1.00), plus view-share pools (Lacy $12,500, Kai Cenat $10,000, Clix $5,000, YourRAGE $5,000). Each brief names which streamer's streams may be clipped.
- Common rejection reasons: no ad disclosure at start, submitting more than 30 minutes after posting, reusing a clip across campaigns. Avoid isolated story cutscenes (Rockstar takedowns) and licensed radio music.
- Format used by top clip pages: facecam on top + gameplay below, one static white headline ("<event> in GTA 6" + emoji), 9-35 seconds, action in the first second.
- User must create the Whop/Content Rewards and social accounts themselves; Canada payout availability on Whop not yet confirmed.
