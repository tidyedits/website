# Tidy Edits store app

The app customers use is **https://tidyedits.com/app/** (source in `../app/`). It already works today:
open it on a phone, then "Add to Home Screen" and it runs like an app, with its own icon, offline screen and no browser bar.

This folder wraps that same app so it can go into the Google Play Store and Apple App Store later.
It is not published on the website (folders starting with `_` are skipped by GitHub Pages).

## How it fits together

- `capacitor.config.json`: a Capacitor shell (`com.tidyedits.app`) that opens tidyedits.com/app. Any change merged to the
  website shows up in the store app too, with no new store release.
- `www/index.html`: the screen shown if the phone has no signal (call / text / try again).
- `../codemagic.yaml` (repo root, where Codemagic looks for it; kept off the public site in `_config.yml`): cloud builds on Codemagic's free tier (Macs in the cloud), so nobody needs a computer.
- Icons: `../app/icons/` (`store-1024.png` is the store listing icon).

Checked 2026-11-16: `npm install` + `npx cap add android` generate the Android project cleanly. Store builds have not run yet
(they need the accounts below).

## Costs (ask Yessi before signing up for any of these)

| What | Cost | Needed for |
|---|---|---|
| Install from the website (PWA) | Free | Works now on iPhone and Android |
| Codemagic | Free tier (500 build minutes a month) | Building the store files in the cloud |
| Google Play Console | $25 one time | Putting it on Google Play |
| Apple Developer Program | $99 a year | Putting it on the App Store |

## Steps once Yessi says yes (phone-friendly)

1. **Google Play** ($25): sign up at https://play.google.com/console/signup with the business Google account.
   Then connect this repo at https://codemagic.io/signup (sign in with GitHub), run `android-play`, upload the `.aab`.
2. **App Store** ($99/yr): enroll at https://developer.apple.com/programs/enroll/ (the Apple Developer app on iPhone can do it).
   Create an App Store Connect API key, add it to Codemagic as "Tidy Edits App Store Connect key", run `ios-app-store`.
   It lands in TestFlight; submit from App Store Connect.
3. Store listing: screenshots of the app at phone size, the 1024 icon, a privacy policy URL, and the description
   "All types of cleaning across Greater Boston. Request a quote with photos, call or text, and save your home details."

## Honest risk: Apple review

Apple sometimes rejects apps that are "just a website in a wrapper" (App Store guideline 4.2, minimum functionality).
Google Play is usually fine with it. Before an Apple submission, add at least one phone-only feature through Capacitor
plugins, for example push notifications for "your cleaner is on the way" and the native camera for job photos.
That raises the odds a lot but is not a guarantee.
