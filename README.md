# journal-scene-reel (논문-도해영상)

Turn a journal paper / issue (.docx / .hwpx) into a cinematic 16:9 **scene-reel**
"도해" video with spoken narration — Chinese(中文) / Korean toggle — and export a
ready-to-upload **MP4**.

- `templates/scene-reel.template.html` — the player (cover → overview → per-paper scenes → closing).
- `scripts/extract_docx.py` — pull text from the manuscript.
- `scripts/clova_voice.py` — synthesize narration (NAVER CLOVA) and embed it.
- `scripts/render_video.py` — static per-scene headless capture → MP4 (fast).
- `scripts/render_mp4.mjs` — **real-time** headless render → MP4 (animated; auto-detects
  the scene-reel *and* the mind-map "film" player). Node 18+ / Chrome / ffmpeg, no npm install.

See `SKILL.md` for the full workflow. Films/reels are authored as UTF-8 (templates carry
`<meta charset="utf-8">`); the renderer also serves UTF-8 to avoid Korean/CJK mojibake.
