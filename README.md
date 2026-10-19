<div align="center">

# Liu Zhongjing in Watercolour

**Fourteen short explainer films on the thought of Liu Zhongjing (劉仲敬), painted entirely in code: a procedural watercolour engine in Python, WebGL compositing in the browser, and a headless Chrome frame renderer.**

<img src="docs/images/series-grid.jpg" width="100%" alt="Title frames of the fourteen films, painted in procedural watercolour">

</div>

The ideas and the quotations are Liu Zhongjing's. No image or video generation model, photograph or stock footage is used for the picture. Companion series: [Liu Zhongjing's History, in Maps](https://github.com/ChanMeng666/lzj-history-maps).

## The films

### Roots 《根》
<!-- FILM: liu-zhongjing-roots · 16:9 · 1:46 — Chan uploads the video here in GitHub's web editor -->
▶ Watch on YouTube: https://youtu.be/p-LRdBfJyuI

### Four Seasons 《四季》
<!-- FILM: liu-zhongjing-four-seasons · 16:9 · 1:46 — Chan uploads the video here in GitHub's web editor -->
▶ Watch on YouTube: https://youtu.be/en5LAyvK8Kw

### Keeping the Seed 《守先待後》
<!-- FILM: liu-zhongjing-keeping-the-seed · 16:9 · 1:38 — Chan uploads the video here in GitHub's web editor -->
▶ Watch on YouTube: https://youtu.be/98k0f22QKtc

### The Basin 《窪地》
<!-- FILM: liu-zhongjing-the-basin · 16:9 · 2:30 — Chan uploads the video here in GitHub's web editor -->
▶ Watch on YouTube: https://youtu.be/PXzgyn3u4bA

### Scattered Sand 《散沙》
<!-- FILM: liu-zhongjing-scattered-sand · 16:9 · 2:34 — Chan uploads the video here in GitHub's web editor -->
▶ Watch on YouTube: https://youtu.be/zKfOdkfVyLY

### Invention 《發明》
<!-- FILM: liu-zhongjing-invention · 16:9 · 2:59 — Chan uploads the video here in GitHub's web editor -->
▶ Watch on YouTube: https://youtu.be/kNxHbWrHNOs

### The Footpath 《小路》
<!-- FILM: liu-zhongjing-the-footpath · 16:9 · 2:48 — Chan uploads the video here in GitHub's web editor -->
▶ Watch on YouTube: https://youtu.be/ZKPJGwkNdsk

### Blood Reward 《血酬》
<!-- FILM: liu-zhongjing-blood-reward · 16:9 · 2:34 — Chan uploads the video here in GitHub's web editor -->
▶ Watch on YouTube: https://youtu.be/uo0T_Bdtbew

### The Black Box 《黑匣子》
<!-- FILM: liu-zhongjing-the-black-box · 16:9 · 2:47 — Chan uploads the video here in GitHub's web editor -->
▶ Watch on YouTube: https://youtu.be/iBLGHhoRL5g

### The Carrot 《胡蘿蔔》
<!-- FILM: liu-zhongjing-the-carrot · 16:9 · 2:47 — Chan uploads the video here in GitHub's web editor -->
▶ Watch on YouTube: https://youtu.be/Bir_XTmdCfw

### Mould 《霉菌》
<!-- FILM: liu-zhongjing-mould · 16:9 · 2:46 — Chan uploads the video here in GitHub's web editor -->
▶ Watch on YouTube: https://youtu.be/nCmURADzMoY

### The Ladder 《梯子》
<!-- FILM: liu-zhongjing-the-ladder · 16:9 · 2:39 — Chan uploads the video here in GitHub's web editor -->
▶ Watch on YouTube: https://youtu.be/hNqoy6IL4b4

### The Clan 《宗族》
<!-- FILM: liu-zhongjing-the-clan · 16:9 · 2:42 — Chan uploads the video here in GitHub's web editor -->
▶ Watch on YouTube: https://youtu.be/V81DCtHuvAs

### The Station 《車站》
<!-- FILM: liu-zhongjing-the-station · 16:9 · 2:41 — Chan uploads the video here in GitHub's web editor -->
▶ Watch on YouTube: https://youtu.be/uRqo56M73dk

## How it's made

- **Painted by code.** `engine/wc.py` glazes transparent pigment onto transmittance maps (a simplified Kubelka–Munk mix), with paper grain, granulation, edge pooling, wet-in-wet bleeds, backruns and tremoring pen lines. Each scene in `scenes/film*.py` is saved as depth layers, growth maps and sprites (Python, numpy, OpenCV).
- **Animated in the browser.** `web/lib/engine.js` composites the layers in WebGL 2 with a parallax camera, growth masks and an ink-bleed transition; `fx.js` adds lamps, snow, fire and fireworks; `type.js` sets Traditional Chinese captions that bleed in character by character. Every frame is a pure function of time.
- **Rendered frame by frame.** `render.mjs` runs parallel headless Chrome workers (playwright-core), captures each frame and encodes with ffmpeg.
- **Scored in code.** `audio/score*.py` write each score to the scene boundaries and play it from recorded instrument samples, normalised to −16 LUFS.
- **Quotations are sourced.** Every captioned quotation is verbatim and carries its source on screen; sources are listed in `docs/STORYBOARD*.md`.

## Make your own

Needs Python 3 (numpy, opencv-python, scipy, soundfile, soxr, opencc), Node 18+, Google Chrome and ffmpeg. The painted assets are committed; the instrument sample libraries are not: point `LZJ_INSTRUMENTS` at your own copy (see `audio/lib/sampler.py`).

```bash
npm install
python engine/build.py film4           # optional: repaint one film's scenes
python audio/score2.py film4           # score for films 4-10 (score.py: 1-3, score_film11..14.py: 11-14)
node render.mjs film4 --stills 12,48   # check single frames
node render.mjs film4 --workers 6      # out/film4.mp4
```

## Licence

- **Code:** MIT ([LICENSE](LICENSE)).
- **Films, scores, paintings and images made by Chan Meng:** CC BY 4.0 ([LICENSE-MEDIA.md](LICENSE-MEDIA.md)).
- **Excluded:** the quoted text, which is Liu Zhongjing's and credited to him; fonts (LXGW WenKai TC, Noto Serif TC: SIL OFL 1.1); the Lemo-Opuscar sampler helpers (MIT, © 2026 LemoLab); instrument samples (their own licences, not redistributed); npm libraries (their licences). Full list: [NOTICE.md](NOTICE.md).

More detail: [docs/overview.md](docs/overview.md)
