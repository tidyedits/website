# Website handoff (as of 2026-11-14)

Everything Claude Code needs to keep working on tidyedits.com. Rules and the page map are in
`../CLAUDE.md`; this file is the status. Update it when things change.

## What's live

| When | PR | What |
|---|---|---|
| 2026-10-21 | first commits | Site launched on GitHub Pages, GoDaddy DNS pointed at it, quote form via FormSubmit (activated) |
| 2026-10-22 | #1 | "Give $25, get $25" referral band, `?ref=Name` link, "Referred by" quote field |
| 2026-10-22 | #2, #3 | Scroll animation, then full-screen 3D scroll film homepage (three.js) |
| 2026-10-23 | #4 | Polish, "all types of cleaning" copy, spray-bottle favicon |
| 2026-10-23 | #6 | Digital business card at `/card/` (+ vCard, QR) |
| 2026-10-25 | #8 | `/thank-you/` booking confirmation; quote form redirects there |
| 2026-10-25 | #9 | Crew clock-in at `/crew/` |
| 2026-10-26 | #10 | Logo/favicon + schema so Google can show the logo in search |
| 2026-10-26 | #11 | 8 service pages, 8 town pages, 4 checklists, hubs, `/plan/` "Plan your clean" lead magnet, answer-first Q&As (replaced #5) |
| 2026-10-27 | #12 | Titles/descriptions trimmed to fit Google |
| 2026-10-28 | #14, #15 | Homepage briefly swapped to a basic page, then the 3D homepage put back. Basic version is in history at commit `731d082` if ever wanted again |
| 2026-10-28 | #16 | 24 s premium brand film on the homepage (`assets/film/`) |
| 2026-11-14 | (this PR) | Hero video (marble kitchen pull-back) + the 3D scroll film remade as real video in the same house (`assets/hero/`, `assets/scroll/`). three.js removed. 3D version is in history before this PR if ever wanted again |

## Open pull requests (waiting for Yessi to tap Merge)

- **#7 `/review` customer review page** (branch `claude/project-thread-kclur1`). Stars + review form to FormSubmit, opt-in to show on site. `GOOGLE_REVIEW_URL = ""` in `review/index.html`: paste Yessi's Google review link there when she sends it. After merge: link it from the homepage footer. Old branch, may need updating from main first.
- **#13 Phone speed + holiday checklist** (branch `claude/project-thread-iifq8y`). three.js loads after page load, lighter idle 3D loop, async fonts, small logo, contrast fix, new `/guides/holiday-cleaning-checklist/`, "Text" button on the phone call bar. Lighthouse mobile was 46 before. Old branch, probably needs updating from main (sitemap/footer conflicts). After merge: ping IndexNow with the new guide URL.
- **#17 `/office` login door page** (branch `claude/project-thread-mlx39s`). Branded page with "Sign in to the Office" (the private Office app on claude.ai) + crew clock-in link, "Office login" in the footer, noindex.

## Open to-dos (most need Yessi)

1. **Enforce HTTPS** in repo Settings > Pages (one checkbox, Yessi). Right now `http://` doesn't redirect to `https://`.
2. **Google Search Console**: Yessi adds a URL-prefix property for `https://tidyedits.com/` with the "HTML tag" method and sends the tag; Claude adds the meta tag to every page (no DNS change). Then submit the sitemap and request indexing. Bing Webmaster can import from it after.
3. **Google Analytics (GA4)**: needs Yessi's `G-` measurement ID. Not set up.
4. **Google review link** for the `/review` page (from the Google Business Profile app, "Ask for reviews").
5. **Website AI chat**: a Cloudflare Worker using free Workers AI (Groq backup) is drafted but not deployed. Needs Yessi's free Cloudflare account. Key never goes in site code.
6. **Real photos**: no job photos on the site yet. When Yessi sends before/after photos, add a proof/gallery section (and a before/after slider idea from the original plan).
7. **Directory links**: add each listing URL (Yelp, Nextdoor, Google Business, etc.) to the schema `sameAs` list in `index.html` as they go live.
8. Testimonials strip on the homepage once opted-in reviews come in from `/review`.

## Decisions Yessi has made

- 2026-11-14: she tried the kitchen hero video + video scroll film as the top of the page (#21, #22), then asked to go back to the original 3D homepage and keep the scroll video as its own section lower down (`#watch`). Keep the 3D homepage (she also flipped to a basic page and back on 2026-10-28; if she asks again, show a phone screenshot of each and ask once which).
- Stay free: no paid AI, no paid site builders. FormSubmit for forms.
- No street address, no PO box. "Milton, MA" only.
- She likes big, full-screen, motion-heavy design (not small widgets), but always in the neutral palette.

## Lessons from past work

- Test with `python3 -m http.server` (not `file://`) and Playwright; `html` has smooth scrolling, so wait ~800 ms after scrolling before screenshots.
- Stub `formsubmit.co` in Playwright to test forms offline.
- Lighthouse works via `npm i lighthouse` with Chromium; headless WebGL inflates blocking time, judge LCP/FCP instead.
- For web video: light denoise + CRF ~27, 30 fps keeps files 2-4 MB.
- Higgsfield free-trial (unlimited) generations only work in Claude chat / Cowork / ChatGPT, not Claude Code. Have Yessi generate there and send the files.
- This PC has no Python; a tiny Node static server with Range support works for testing video seeking.
- The app preview pane freezes animations when it is hidden, so the scroll film looks stuck there. Test with headless Chrome over the DevTools protocol (Node 22+ has WebSocket built in): real phone emulation, live reduced-motion flips, and blocking the film URL.
- Scroll film engine (2026-11-14 review against the 10k-websites skill + design skills): film fetched whole as a Blob, frame-rate independent easing, one seek in flight (uses `video.seeking`), loop rests off screen, reduced motion honored live both ways, poster carries the section if the film fails. On desktop the film sits on the right 74% with a solid text side so words pass contrast in light and dark.
- Old Google favicon/snippet = not recrawled yet; the fix is Search Console "Request indexing", not code.
- Yessi's short messages can change direction fast; act quickly, keep both versions, confirm live in one line.
