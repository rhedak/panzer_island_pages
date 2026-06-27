---
title: English Writer's Styleguide
description: Writing conventions for panzer_island_pages content.
---

# Panzer Island Pages: English Writer's Styleguide

This guide covers writing conventions for the public-facing website: the landing page,
player guides, dev blog, and press kit. It is distinct from the in-game writing guide
in the sister repo (`docs/localization/styleguide_en.md`), which covers cutscenes and
UI strings. When they conflict, this guide wins for website content.

**English is the only language on this site.** Non-English speakers are expected to use
browser auto-translation. Do not add translation infrastructure or multilingual content.

---

## 1. Proper nouns

These spellings are locked everywhere on the site. Never abbreviate or vary them.

| Term | Spelling | Notes |
|---|---|---|
| Game title | **Panzer Island** | External brand. Never "Tank Tactics 2D" in public-facing text. |
| Developer credit | Solo dev project (no studio name) | Do not invent a studio name. |
| Platforms | Steam, Android, itch.io | Exact capitalization. Not "STEAM" or "Itch". |
| Katyusha | Katyusha | Full name each time. |
| Nadeshiko | Nadeshiko | Full name each time. |
| Maria | Maria | Standard. |
| Erika | Erika | No surname or title in prose. |
| ORACLE / Oracle | **ORACLE** in technical/lore references; **Oracle** in narrative prose | Match context. |
| Panzer Republic | Panzer Republic | Both words capitalized. |
| Nautilus Empire / the Empire | Nautilus Empire / the Empire | Capital E always; "the" lowercase mid-sentence. |
| Godot | Godot | Engine name. Not "GODOT". |

---

## 2. Dialect, spelling, and numbers

Use **American English** spellings.

| Use | Avoid |
|---|---|
| center, theater, fiber | centre, theatre, fibre |
| color, behavior, honor | colour, behaviour, honour |
| recognize, organize, analyze | recognise, organise, analyse |
| -ized / -izing | -ised / -ising |

**Numbers:**
- Spell out one through nine in prose; use numerals for 10 and above.
- Use numerals for all game-specific counts and statistics ("10 stages", "3 endings").
- Percentages use numerals ("25% complete").
- The webnovel (fiction/narrative prose) is exempt from the "numerals for 10+" rule; it uses literary conventions (spelled-out numbers). All other rules apply.

---

## 3. Punctuation and formatting

### 3.1 Em dashes: banned

Do not use em dashes (`—`, U+2014). Use a period, comma, semicolon, or restructured
sentence instead.

### 3.2 Double hyphens

Do not use `--` as a pause substitute. Same rule as em dashes.

### 3.3 Ellipsis

Use **three literal periods** (`...`), no surrounding spaces.
Ellipsis is rare in website prose. Prefer a full stop.

### 3.4 Exclamation marks

Use them sparingly. One per paragraph at most. Dev blog posts may be slightly warmer;
landing page copy should be calm and confident.

### 3.5 Headings

Use **sentence case** for page headings and section headers. Title case only for
proper names embedded in a heading ("Meet the Cast").

### 3.6 Lists

Use a bulleted list when order does not matter. Use a numbered list for
step-by-step instructions only. Do not use lists for single-item "lists."

### 3.7 Horizontal rules

Always follow a `---` horizontal rule with **two blank lines** before the next content.
The first blank line is required for correct Markdown parsing. The second blank line
survives as an empty paragraph when the chapter is copy-pasted into Royal Road or
similar platforms, creating visible spacing there too. The visual breathing room in
the MkDocs-rendered HTML comes from the `hr` margin rule in `extra.css`.

```markdown
---


Next paragraph here.
```

---

## 4. Tone by section

### 4.1 Landing page

Calm, confident, brief. The reader is deciding whether to care. Assume they have ten
seconds.

- Lead with what the game *is*, not what it is *not*.
- One strong sentence per feature. No superlatives ("amazing", "groundbreaking").
- Active voice. Short sentences.

### 4.2 Player guides

Instructional and direct. Second person ("you", "your units").

- Use the exact ability names the game UI shows.
- Prefer imperative sentences for actions ("Select a unit. Tap the target tile.").
- Spell out contractions when in doubt; guide prose can be slightly formal.
- Add a brief "what you will learn" summary at the top of each guide.

### 4.3 Dev blog

Conversational but professional. First person ("I") is fine. Avoid filler phrases
("super excited to share", "thrilled to announce"). State what happened and why it
matters.

- No em dashes.
- One topic per post. Do not pad short updates into long posts.
- Dates in ISO format in front matter (`date: 2026-06-13`).

### 4.4 Press kit

Factual and scannable. Journalists are busy.

- Fact sheet: bullet points, no prose.
- Short description (one paragraph, 50-80 words): what the game is, for whom, on what platforms.
- Long description (up to 200 words): full pitch including tone and story hook.
- Do not editorialize ("critics will love"). Stick to facts.

---

## 5. Page structure

Every page needs front matter with at minimum:

```yaml
---
title: Page Title
description: One-sentence summary for SEO and social previews.
---
```

The `description` field is load-bearing for search engine snippets. Write it as a
standalone sentence that reads well out of context.

---

## 6. Links and images

- Internal links use root-relative paths (`/guides/getting-started/`).
- External links open in the same tab unless it would be disorienting (e.g. a link
  that takes the reader completely off-topic mid-guide).
- Image filenames are lowercase with hyphens (`katyusha-intro-screen.png`).
- Every image needs descriptive alt text.
- Keep images under 500 KB. Prefer WebP for screenshots.

---

## 7. What to avoid

- Marketing superlatives ("revolutionary", "groundbreaking", "the ultimate").
- Spoilers anywhere outside a clearly marked spoiler section.
- Mentioning the internal project name "Tank Tactics 2D" in any public page.
- Character voice (cutscene register) in web prose. Guides and blog posts are not
  part of the narrative.
- Passive voice where active is clearer.

---

## 8. Checklist before publishing

1. Proper nouns match §1 exactly.
2. No em dashes or double hyphens.
3. American English spellings.
4. Front matter has `title` and `description`.
5. Images have alt text and are under 500 KB.
6. Run `./check.sh` to verify the build.
