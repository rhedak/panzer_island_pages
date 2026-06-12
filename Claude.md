# Panzer Island Pages Context

This is the github pages repo associated with the sister repo ../tank_tactics_2d
for the game "Panzer Island".

Note: The internal project name is "Tank Tactics 2D"
But the external game name is "Panzer Island"

For details see also the Claude.md of the sister repo ../tank_tactics_2d

## Site stack

This site uses **MkDocs** with the Material theme, deployed to GitHub Pages via
the `.github/workflows/deploy.yml` GitHub Actions workflow. The build output goes
to `/site/` (gitignored). Push to `main` triggers a deploy.

Local development:
```
uv run mkdocs serve   # hot-reload preview at http://localhost:8000
uv run mkdocs build   # one-off build check
```

## Best Practices for GitHub Pages

- All content lives under `docs/` as Markdown files.
- Every page must have `title` and `description` in front matter.
- Images go in `docs/assets/`, filenames lowercase with hyphens, max 500 KB, prefer WebP.
- Internal links use MkDocs-relative paths (`../guides/foo.md`), not absolute URLs.
- Never commit the `site/` build directory (it is gitignored).
- `mkdocs.yml` is the single source of truth for navigation and site metadata.
- Blog posts live under `docs/blog/posts/` with `date:` in front matter.
- Run `./check.sh` after any structural change to verify the build stays clean.

## Asset sync workflow

Guide Markdown and images are generated in `../tank_tactics_2d` and synced here.
`sync_manifest.toml` is the SSoT for what lives where. When the sister repo updates
guide content, run:

```
uv run python sync_assets.py          # check what is stale
uv run python sync_assets.py --sync   # pull updates in
```

To add a new synced asset, add an entry to `sync_manifest.toml`. The script handles
both individual files (`[[files]]`) and whole directories (`[[dirs]]`).

The sister repo is not available in CI, so the sync check is skipped automatically
on GitHub Actions (the script exits 0 if the sister path does not exist).

## After every code change
Run `./check.sh` to verify the project loads without errors before reporting a task complete.

`check.sh` runs `uv run mkdocs build --strict`. Any warning is treated as an error.

## Language and Styleguide

Adhere to the English styleguide. All pages are English only.
It is assumed that non-English speakers will use auto translation.

Before writing any page content, read `docs/styleguide_en.md`.
Key points: American English, no em dashes, sentence-case headings, every page
needs `title` and `description` front matter.

## misc

- do NOT commit unless asked
- even if you commit do not write a "co-authored" trailer
- no em dashes "—" (U+2014), double hyphens "--", or similar pause-substitutes in prose; 
  hyphens are fine for compound words, prefixes, and ranges, but in running text prefer a period, comma, or restructured sentence instead
- After fixing a bug, if appropriate add a regression guard test
- If you disagree (you don't think they add value) with any instructions I give you feel free to push back once and ask for confirmation
