# Tidy Edits website: instructions for Claude

This repo is the live website for **Tidy Edits Cleaning Company** (https://tidyedits.com), a locally owned
cleaning company in Greater Boston. The owner is Yesenia "Yessi" Ventura. She works **from a phone only**,
so keep replies short and plain, and give her one step at a time with a tappable link.

Read `_handoff/README.md` first for the full handoff: what's live, open pull requests and open to-dos.
`_handoff/STARTER-PROMPT.md` has the prompt Yessi pastes to start a session.

## How the site works

- Plain static HTML, CSS and JS. No framework, no npm build for the live pages.
- Hosted free on **GitHub Pages** from the `main` branch, repo root. Anything merged to `main` is live in about 1 to 10 minutes.
- Domain `tidyedits.com` is registered at **GoDaddy**. DNS: 4 GitHub A records on `@`, `www` CNAME to `tidyedits.github.io`. Google email (MX) records live there too. `CNAME` file in the repo must stay `tidyedits.com`.
- GitHub Pages runs Jekyll, so folders starting with `_` (like `_build/` and `_handoff/`) are **not published**. `_config.yml` also keeps `CLAUDE.md` and `README.md` off the public site.
- Quote and plan forms post to **FormSubmit** (`https://formsubmit.co/ajax/info@tidyedits.com`) with a `mailto:` fallback and a `_honey` spam trap. The home quote form sends people to `/thank-you/` after success.

## Page map

| Path | What it is | How to edit |
|---|---|---|
| `index.html` | Homepage: full-screen hero video (plays once, ends on the wide kitchen), then the scroll film (one video scrubbed by scroll, sticky stage, word-by-word headlines; no three.js anymore), brand video, services, referral band ("Give $25, get $25", `?ref=Name`), towns, FAQ, quote form, LocalBusiness/FAQ schema | Edit by hand (one big file) |
| `services/<slug>/`, `areas/<town>/`, `guides/<slug>/`, hub pages, `plan/`, `sitemap.xml`, `assets/site.css` | SEO pages (8 services, 8 towns, 4 checklists) and the "Plan your clean" lead magnet | **Generated.** Edit `_build/content.py` (or `_build/plan.py`, `_build/base.css`) then run `python3 _build/build.py`. Don't hand-edit the output. |
| `card/` | Digital business card + `tidy-edits.vcf` + QR | By hand |
| `thank-you/` | Booking confirmation page (noindex). Used as the Google Ads / Google Business "after booking" page | By hand |
| `crew/` | Crew clock-in page (noindex, blocked in robots.txt) | By hand |
| `assets/hero/` | Hero video, 16x9 + 9x16 + posters (Higgsfield: GPT Image 2.6 still, Seedance 2.5) | Replace files |
| `assets/scroll/` | 25 s scroll film, 16x9 (desktop) + 1x1 (phone, crop follows the action) + posters. Encoded with keyframes every 6 frames (`-g 6 -bf 0`) so scrubbing is smooth both ways. Script: `_handoff/scroll-film-video-script.md` | Replace files, keep `-g 6` |
| `assets/film/` | 24-second muted brand film, 16x9 and 9x16 cuts + posters (see CREDITS.md) | Replace files; keep web size small (CRF ~27) |
| `171a8ac649a60802fab9655b7d0e425c.txt` | IndexNow key. Don't delete. | |
| favicons, `icon-*.png`, `site.webmanifest`, `logo.png` | Spray-bottle favicon and app icons | |

After adding or changing public pages, ping IndexNow (free, no account):
`POST https://api.indexnow.org/indexnow` with `{"host":"tidyedits.com","key":"171a8ac649a60802fab9655b7d0e425c","keyLocation":"https://tidyedits.com/171a8ac649a60802fab9655b7d0e425c.txt","urlList":[...]}`.

## Yessi's standing rules (always follow)

1. **Brand colors: neutrals only.** White, cream, tan, brown, plus the logo's black. No green, blue, lime or other bright accents. Reference tokens: paper `#f6f3ec`, cream `#e7dccb`, tan `#b89a74` (use `#8f7049` for text, it passes contrast), brown `#8a6a4a`, ink `#111312`. Fonts: Bodoni Moda (headings) + Figtree (body).
2. **Design skills on every UI change.** Use UI taste if installed (say so in one line if it isn't), plus pro-design, web-design-guidelines and frontend-design, and the Superpowers skills (brainstorm before creative work, plan multi-step work, verify before saying done).
3. **We do all types of cleaning.** Present services as examples, never a closed list. Use a line like "We take on all types of cleaning jobs, big or small, one-time or recurring."
4. **Address: "Milton, MA" only.** Never put a street address (no 340 Central Ave) or a PO box on the site. Public contact: 857-753-5593, info@tidyedits.com.
5. **No personal name on the card or vCard**, business name only. Emails that need a name use "Yesenia Ventura", never "Yessi".
6. **Never put API keys, passwords, passcodes or tokens in this repo.** It is public. Secrets go in Cloudflare/GitHub secrets, never in page code. No lead lists or customer emails in the repo either.
7. **Free AI first.** If the site needs an AI model (chat, receptionist), use a free API: Cloudflare Workers AI first, Groq as backup (see the `tidyedits/awesome-free-llm-apis` list). Key stays server-side in a Worker. Suggest paid AI only if nothing free can do it, and say why.
8. **Ask Yessi first before:** spending money or signing her up for paid services, deleting things, or changing the domain/DNS at GoDaddy or the Pages settings. Everything else: just do it and tell her what you did.
9. **Honest content only.** Town pages use true local facts. No invented reviews, clients, landmarks or prices. Never show the Google review button only to happy customers (review gating breaks Google policy) and never tie discounts to reviews.
10. **Prices** aren't published on the site. Yessi sends quotes herself.

## How to work

- Branch, open a pull request, and give Yessi the PR link. She merges from her phone (the green "Merge" button). Only merge yourself if she says "merge it".
- Test before saying done: serve with `python3 -m http.server` and check with Playwright at 390px (phone) and 1440px, light and dark mode, no sideways scroll, no console errors. Phone matters most: most visitors are on phones.
- Keep the homepage fast: the scroll film loads after page load; don't add heavy libraries.
- Keep these docs current: when something ships or a to-do changes, update `_handoff/README.md`.
