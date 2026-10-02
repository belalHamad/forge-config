# forge-config

The wording on the Forge app's **Upgrade to Premium** screen (the paywall).
Edit `remote_config.json` here and phones pick it up with no App Store update.

It can only change paywall text. It can't change prices (those always come from
the App Store), what's unlocked, or any other screen.

## How to edit it (on github.com, no tools needed)

1. Open **`remote_config.json`** in this repo and click the **pencil** (Edit) button.
2. Change the text you want (see the examples below).
3. Click **Commit changes…**, then **Commit changes** again.
4. Wait about a minute and check the commit's mark on the repo's front page:
   - **Green ✓**: the file is fine.
   - **Red ✗**: there's a mistake. Click the ✗, then **Details**; it says exactly what's wrong
     (for example `Unknown field "paywallHedline" — did you mean "paywallHeadline"?`). Fix it and
     commit again. Until it's fixed, phones keep showing the last good version.
5. Wait about **5 minutes** (GitHub's cache), then **fully close Forge** (swipe it away in the app
   switcher) and open it again. Forge only checks for a new version when it starts.
6. Open the paywall (Profile → Upgrade to Forge Premium) to see your change.

## What each line does

| Line | What it changes | Example |
|---|---|---|
| `"paywallHeadline"` | The big title at the top | `"Unlock Forge Premium"` |
| `"paywallSubheadline"` | The smaller line under the title | `"Every premium feature and every template pack."` |
| `"bannerVisible"` | Show the highlighted banner box: `true` or `false` | `false` |
| `"bannerText"` | The banner's text (only shown when `bannerVisible` is `true`) | `"Ramadan Mubarak"` |
| `"anchorPriceText"` | A small grey line under the pack's price | `"Included free with Premium"` |

Use `null` (no quotes) for "nothing": no subheadline, no banner text, no grey line.

## Example: turn on a Ramadan banner

Change these two lines:

```json
  "bannerVisible": true,
  "bannerText": "Ramadan Mubarak — build your Ramadan habits with Premium",
```

## Example: turn it off after Ramadan

Change `bannerVisible` back to `false` (you can leave the text; it won't show):

```json
  "bannerVisible": false,
```

## Rules that keep the file working

- Text goes in **straight double quotes**: `"like this"`.
- Every line ends with a **comma**, except the last line before `}`.
- `true`, `false` and `null` are lowercase and have **no quotes**.
- Don't add new lines or rename them. The app only understands the five above.
- **No price claims** like "Normally $4.99" unless they're true. Apple requires that, and the check
  warns about it.

Made a mess of it? Open the file's **History**, find the last green ✓ version, and copy that back
in. Or just put back the original:

```json
{
  "paywallHeadline": "Unlock Forge Premium",
  "paywallSubheadline": "Every premium feature and every pack, including the Islamic pack. Try it free for 7 days.",
  "bannerVisible": false,
  "bannerText": null,
  "anchorPriceText": null
}
```

## If something goes wrong

Forge never shows an error. If the file is missing, broken, or the phone is offline, the app keeps
the last version it downloaded. If it has never downloaded one, it uses the built-in wording
(the original above).

## Notes for development

- App side: `RemoteConfigService` / `RemoteConfig` in the Forge app repo. It fetches
  `https://raw.githubusercontent.com/belalHamad/forge-config/main/remote_config.json` once per launch.
- The app's model also has `featuredPackID`, but no screen uses it yet. It's left out of this file
  on purpose, and the check rejects it so nobody edits a field that does nothing.
- The check is `.github/scripts/validate_config.py`, run by `.github/workflows/validate.yml` on every
  commit.
