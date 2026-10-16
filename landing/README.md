# JobStream DZ Landing

Static marketing landing page for JobStream DZ.

The page supports three languages with runtime switch:
- French (default)
- English
- Arabic (RTL)

## Files

- `index.html` - page structure
- `styles.css` - layout and visual system
- `script.js` - trilingual content dictionary and language switch behavior
- `assets/` - cropped visual assets derived from `landing.png` reference

## Local preview

From repository root:

```bash
python3 -m http.server 8080
```

Then open:

- `http://localhost:8080/landing/`

## Notes

- Logo source is `../logo.png`.
- Main visual references come from `../landing.png`.
- Telegram CTA points to `https://t.me/jobstream_dz`.
- Selected language is saved in browser local storage.
