# Phalom prototype source

`phalom_src.html` is the source of the clickable prototype. It has no build dependencies beyond Python 3.

- `fetch_fonts.py` downloads Noto Sans Lao, Noto Serif Lao and Fraunces from Google Fonts and writes them as base64 into `fonts/fonts.css`, so the prototype works without internet. `fonts/sym.css` holds the kip sign (₭) glyph. All fonts are under the SIL Open Font License.
- `build.py <output.html>` inserts the fonts and writes a complete offline page. Run it from this folder:

```
python3 build.py ../exports/phalom_prototype.html
```

## UI and motion rules

Every change to the prototype must keep these:

- Touch targets are at least 44×44 px. Small visual pills sit inside a 44px button.
- Hover styles live only inside `@media (hover:hover)`.
- Only `transform` and `opacity` are animated. No `transition: all`, and never width, height, top or left.
- Press feedback takes 120ms (scale and opacity). Modals, the toast and the demo sheet enter in 280–300ms and exit in 200ms.
- User-driven motion uses CSS transitions on persistent nodes, so it can be interrupted. `render()` patches the DOM in place instead of replacing it.
- Under `prefers-reduced-motion: reduce`, nothing moves; elements crossfade with opacity only.

It also writes `phalom_artifact.html`, the same page without the `<html>` wrapper, for publishing as a claude.ai artifact. That file is not committed.

# Version Log

| Timestamp | Version | Author | Change |
|---|---|---|---|
| 2026-10-12 (Asia/Bangkok) | 0.1 | Claude Code | First version: Mekong design, light theme by default, P0 features and the presenter demo panel. |
| 2026-10-12 (Asia/Bangkok) | 0.2 | Claude Code | Bank-style payment slip, today's total and settlement status, in-place DOM patching, motion and touch-target rules. |
