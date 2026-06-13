# Site roadmap

Suggested additions and improvements, grouped by area. Items are roughly in priority order within each section.

---

## Guides

The guide section covers the basics but has clear gaps for players who want more depth or are stuck.

### Missing pages

**Drone reference** (`docs/guides/drones.md`)
A one-page reference for every drone type: patrol, guard tower, sentinel, interceptor, artillery, cruiser, spotter, relay node, repair drone, detonator variants. For each: what it does, how it reacts, what unit type counters it best, and what to watch out for. This is the most-requested type of reference in any strategy game and there is currently nothing like it on the site.

**Stage objectives guide** (`docs/guides/objectives.md`)
Explains each objective type the game uses: extract, destroy all, destroy type, collect, escort, hold. What counts as success, what fails the sector, and basic tactics for each. New players frequently misunderstand the `extract` objective (it does not require destroying all drones) and the `escort` failure condition (escorted unit dies = sector over).

**Chapter 1 stage tips** (`docs/guides/chapter-1.md`)
A light per-stage tip page, not a full walkthrough. One or two sentences per stage: what the stage is trying to teach, which unit to lead with, and the one thing players tend to get wrong. Useful for players stuck on a specific stage without spoiling the approach entirely.

**Skill build guide** (`docs/guides/skill-builds.md`)
Goes beyond the unit reference page to suggest concrete builds for different playstyles. Aggressive Katyusha, evasive Nadeshiko, stationary artillery Maria, and team synergy builds (e.g. Safe Harbor Maria + Last Stand Katyusha). A page for players who have reached level 4-5 and are not sure which branch to take.

**Advanced tactics** (`docs/guides/advanced.md`)
A bridge between Getting Started and the Reactive Turns deep dive. Topics: reading the route preview for multi-step routes, deliberate damage spreading, using limit breaks defensively (not just offensively), sector transition positioning, and when not to kill a drone. The deep dive explains the engine; this page explains how to play around it.

### Improvements to existing pages

- **Getting started:** add a section on what to do when stuck (replay for XP, check the skill tree, consider approaching from a different angle). Currently the page explains the system but not the recovery loop.
- **Your units:** add a section on what each unit cannot do, clearly stated. Maria's water-only movement trips up new players repeatedly. Nadeshiko's fragility is mentioned but not emphasized enough.
- **Guides index:** currently a plain list. A short note on which guide to read first and which to return to after Chapter 1 would help.

---

## FAQ

A `docs/faq.md` page covering questions that appear in player feedback. Suggested entries:

- Why can Maria not move here? (water requirement)
- Do skill choices carry over between chapters? (yes, permanently)
- What happens if a unit dies? (carries through, does not return mid-stage)
- What is the difference between the Steam demo and the full game?
- Is there a New Game Plus or chapter replay?
- What are memory fragments?
- Does the game have multiple endings? (yes, three)
- Can I change my skill picks? (no, they are permanent)
- The solver / AI playtest is mentioned in the dev blog, can I use it?

The FAQ does not need to be comprehensive on launch but even eight to ten entries cut a significant share of repeat support questions.

---

## Story and characters

The landing page sells the story but gives players nowhere to go if they want to know more without being spoiled. Two options:

**Characters page** (`docs/story/characters.md`)
Brief non-spoiler profiles for each speaking character: Erika, Katyusha, Nadeshiko, Maria, Drona, Wilhelm. What the player knows at the start of Chapter 1. Could include character portrait images once those are cleared for public use.

**Lore overview** (`docs/story/index.md`)
One page covering Panzer Island as a setting: what the island is, what the drones are, and what the player is walking into. No plot spoilers past Chapter 1. Useful for players who want context before starting, and for press and streamers writing coverage.

These two pages could live under a `Story` nav section alongside the existing guides.

---

## Blog

The blog has two posts. Suggested future articles:

**Development updates** (ongoing)
Short posts when a chapter is released, a major mechanic ships, or a significant update deploys. These do not need to be long. A 200-word "Chapter 2 is now live" post with a link is better than silence between major releases.

**Patch notes** (per update)
A brief post per notable update: what changed, what was fixed, what was added. Players who follow the game via RSS or the blog need a record of this. These can be short.

**How the reactive turn system was designed**
A design-focused post explaining the choices behind the step-by-step reaction model rather than end-turn. Why it was chosen, what it took to balance, where it surprised us. The AI article establishes that we publish honest dev articles; this is the natural companion piece on the core mechanic.

**Chapter 2 preview / release post**
When Chapter 2 is ready, a post introducing the new setting, new drone types, and any new mechanics. Gives press and streamers something to reference.

**Music and audio in Panzer Island**
A short post on Patrick de Arteaga's CC music tracks, how they were selected, and the custom Python SFX synthesizer. The AI article mentions audio briefly; there is a full story there.

---

## Press and distribution

**Credits page** (`docs/credits.md` or a section in press)
Lists Patrick de Arteaga for music (with link), GUT testing framework, any other third-party assets or tools used. Good practice, and some music licenses require attribution in documentation.

**Platform-specific tips** (press kit or separate page)
For press and streamers: where to find review keys, which platform is best for capture (itch.io / PC), and whether there is a presskit.io entry. The current press kit has a contact email but no workflow for key requests.

---

## Guide visuals (asset pipeline)

The sister repo's `tank_tactics_tools/lib/guide_render.py` generates annotated mock-stage PNG images using the game's own terrain tiles, unit sprites, drone sprites, and prop assets. Each image is a `SceneDef` (grid layout + unit/drone/prop placement) combined with annotation calls (attack range diamonds, movement path lines, reaction arrows, labels, callout numbers, title banner, legend box). Output is a named PNG that the sync manifest copies to `docs/guides/guide_assets/`.

Eleven scenes already exist and cover the reactive turn system guide. The scenes below are missing and block the new guide pages planned above. Each entry names the scene, describes what it should show, which new guide page uses it, and which renderer primitives cover the work (so the scope is clear before writing code).

**Add these to `guide_render.py` and register in `_SCENES`:**

---

### Drone reference page (`docs/guides/drones.md`)

**`scene_drone_overview`**
A wide grid with one representative sprite of each core drone type arranged in two rows, each labeled with its name and type tags (GROUND/AIR/STATIC). No attack annotations; purely a visual roster. Use the `label()` primitive with name + type tag on each cell.

**`scene_sentinel_chain`**
Shows the sentinel chain-reaction mechanic: a sentinel in idle state with a nearby guard tower that fires at a unit. The sentinel's activation arc triggers from the guard tower's shot. Use `detection_band` on the sentinel, a reaction `arrow` from the guard tower to the unit, and a second `arrow` from the sentinel to indicate it has now activated. The title banner: "SENTINEL CHAIN REACTION."

**`scene_interceptor_pursuit`**
An interceptor with a ghost trail showing its last two positions (same ghost-cell style as `scene_idle_drift`) closing in on Nadeshiko. The interceptor attack range diamond shown at the final position. Key annotation: "CLOSES DISTANCE BEFORE FIRING" label. Demonstrates why Nadeshiko is particularly vulnerable to interceptors.

**`scene_artillery_charge`**
An artillery drone with two states side by side on the same canvas: left half shows it detecting a unit (detection band + label "CHARGE: 0"), right half shows it one turn later with the charge indicator label "CHARGE: 1 — FIRES NEXT." Use a vertical dividing line (thin grey rect) to split the two states. The full charged state shows the attack range diamond at full radius.

**`scene_relay_node_buff`**
A relay node in the center with two guard towers within its buff radius. The towers' extended attack range shown as a wider diamond with a label "WITH RELAY NODE" next to a second diamond at normal size labeled "WITHOUT." Uses `highlight_diamond` at two radii. The relay node itself gets a callout circle. Title: "RELAY NODE — EXTENDED RANGE."

**`scene_spotter_mark`**
A spotter in range of Katyusha with a mark indicator on her cell (orange callout circle + label "MARKED"). An incoming drone attack arrow with label showing amplified damage "+50% DMG." A second scenario on the right: spotter destroyed, damage label at normal value. Title: "SPOTTER MARK."

**`scene_repair_drone_heal`**
A repair drone adjacent to two damaged drones (partial HP indicator via label e.g. "HP: 8/20"). An arrow from the repair drone to each wounded drone labeled "+4 HP." One unit outside the repair radius with label "OUT OF RANGE." Title: "REPAIR DRONE."

**`scene_detonator_rush`**
A detonator with a path of three ghost cells (same drift style as `scene_idle_drift`) rushing toward Katyusha. An explosion-zone highlight (3x3 or diamond) centered on Katyusha's cell labeled "AoE ON CONTACT." A label on the detonator: "1 HIT = DESTROYED." Title: "DETONATOR."

---

### Objectives guide (`docs/guides/objectives.md`)

**`scene_objective_extract`**
A small 8x5 grid with Katyusha and the extract zone highlighted in a distinct color (green fill using `highlight_cells`) labeled "EXTRACT ZONE." A drone between the unit and the zone. Route path shown with the movement arrow threading around the drone. Emphasizes: drones do not need to be destroyed. Title: "EXTRACT."

**`scene_objective_collect`**
A grid with two memory fragment props placed on the map (use `callout_number` on each: 1 and 2). Katyusha near fragment 1 with a collection arrow. Fragment 2 further away with a dashed path. Label: "COLLECT BOTH TO CLEAR." Title: "COLLECT."

**`scene_objective_escort`**
A non-combat unit (use the `katyusha` sprite with a distinct label "ESCORT UNIT") flanked by Nadeshiko and Maria as guards. A route path leading to an exit zone. A drone near the escort unit with a red warning border. Label: "IF ESCORT UNIT DIES — SECTOR FAILS." Title: "ESCORT."

---

### Advanced tactics guide (`docs/guides/advanced.md`)

**`scene_damage_spreading`**
Two side-by-side scenarios (split canvas like `scene_artillery_charge`): left shows all three units bunched up, with passive fire arrows hitting all of them and labels "KATYUSHA: -12 HP, NADESHIKO: -9 HP, MARIA: -9 HP." Right shows units spread out with only the acting unit drawing fire. Title: "SPREAD THE DAMAGE."

**`scene_sector_hp_carry`**
Three unit sprites with HP labels below them (e.g. "HP: 34/60, HP: 18/40, HP: 55/70") and a thick horizontal arrow pointing right labeled "SECTOR TRANSITION — HP CARRIES." Below the arrow, same three units with identical HP values. A second set to the right showing a destroyed unit slot with a red X. Label: "DESTROYED UNITS DO NOT RETURN." Title: "SECTOR TRANSITIONS."

**`scene_limit_gauge_build`**
Katyusha with a gauge bar (thin horizontal rect, partially filled in yellow) labeled "LIMIT GAUGE: 60%." Two arrows pointing at her: one from a drone (incoming fire, +gauge) and one pointing away to a drone (outgoing attack, +gauge). Callout showing the gauge at full: "LIMIT BREAK READY." Title: "BUILDING THE LIMIT GAUGE."

---

### How to add a new scene

1. Add a `scene_NAME(renderer: GuideRenderer) -> str` function in `guide_render.py`.
2. Register it in `_SCENES` at the bottom of the file.
3. Run `uv run tt2d-generate-guide-assets --scenes NAME` from the sister repo to test output.
4. Run `uv run tt2d-generate-guide-assets` (all scenes) to regenerate the full set.
5. Run `uv run python sync_assets.py --sync` in this repo to pull the new PNG.
6. Reference it in the guide Markdown as `![Alt text](guide_assets/scene_NAME.png)`.

The `--scenes` flag accepts multiple names separated by spaces, so partial regeneration is fast during iteration.

---

**404 page** (`docs/404.md`)
MkDocs supports a custom 404. A simple branded page is better than the GitHub Pages default.

**RSS for the blog**
The Material blog plugin generates a feed by default. Worth verifying it is enabled and linking to it in the footer so players can follow updates in their feed reader. Add `feed_length` and `feed_tiers` config if not already set.

**Search quality**
The search index includes all pages. Worth checking that the drone names and mechanic terms (Iron Curtain, Storm Run, Broadside, Spotter, Relay Node) return the right pages. If search results are weak, add `search.boost` annotations to key pages.

---

## Navigation

Current nav: Home, Guides (4 pages), Press Kit, Blog.

Suggested nav as the site grows:

```
Home
Guides
  Getting Started
  Your Units
  Reactive Turns
  Drones           ← new
  Objectives       ← new
  Advanced         ← new
  Chapter 1 Tips   ← new
Story              ← new section
  Characters
  Lore
FAQ                ← new
Press Kit
Blog
```

Adding Story and FAQ as top-level nav items is reasonable once those pages exist. They are the two areas most likely to bring in organic search traffic beyond the existing guide terms.
