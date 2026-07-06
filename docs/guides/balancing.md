---
title: Balancing and math
description: The formulas behind Panzer Island's stat growth, XP curve, and difficulty tuning, for players who want the numbers behind the design.
---

# Balancing and math

This guide is for players who want to see the actual formulas behind the game's numbers, not just what to do with them. It covers how unit and drone stats grow with level, how the XP curve is shaped, and how the overlevel penalty keeps grinding useful without trivializing content. None of this is required reading to play the game; [Getting Started](index.md) and [Reactive Turns](reactive_turns.md) cover everything you need for that.

---

## Core balancing principles

Everything below is an implementation of a handful of ideas. If a formula further down seems oddly specific, it is in service of one of these:

- **Level parity holds at every level.** A unit at level N fighting a drone at the same level N should be roughly as effective whether N is 1, 10, or 100. A fight should be won or lost on positioning, unit choice, and tactics, not on which arbitrary point of the leveling curve it happens to land on. The [effectiveness metric](#the-effectiveness-metric) and [two-factor stat growth](#two-factor-stat-growth) below exist to guarantee this.

- **A perfect, no-grinding clear is possible, but only for players playing close to optimally.** The campaign is tuned so that a skilled player who never replays a stage for extra XP can still clear it on merit alone. It is not tuned so that an average playthrough clears without effort; skill and preparation are meant to matter.

- **Difficulty rises roughly in a straight line within a chapter and peaks at the boss stage.** Drone count and drone level climb stage to stage rather than in sudden jumps, with each chapter's final stage as the intended high point before the next chapter resets.

- **Each chapter gets harder through complexity, not just volume.** A new chapter's difficulty comes from new enemy drone types (new mechanics to read and react to), not simply more copies of drones the player already knows how to handle. For a player who has fully internalized a chapter's new mechanic, the actual difficulty of clearing it is meant to land in roughly the same place as the chapter before: the harder feel of a new chapter comes from unfamiliarity, not from the fight objectively demanding more. One consequence: the stage right after a boss plays easier than the tough stage before it, but is never trivial, since it is usually the stage that introduces the new chapter's mechanic.

- **Grinding is an intended catch-up mechanism, not an exploit.** Replaying a stage for extra levels is meant to help, not to be a loophole worth patching out. In effect, the amount of grinding a given player needs to clear a chapter, or the whole campaign, is how the game adapts to that player's skill: a highly skilled player can clear in a single pass with no replays, while a less skilled player reaches the same endpoint by spending more attempts and picking up the extra levels along the way. See the [XP curve](#the-xp-curve) and the [overlevel](#the-overlevel-xp-penalty)/[underlevel](#the-underlevel-catch-up-bonus) sections below for how that catch-up is kept meaningful without being a free pass.

**Chapter 1 is the exception to all of this.** As the tutorial chapter, it is deliberately easier than the principles above would otherwise call for, so new players can learn the game's mechanics without also fighting a tuned difficulty curve at the same time.

---

## The effectiveness metric

Every stat growth decision in Panzer Island is checked against one formula:

```
effectiveness(A attacks B) = max(1, A.attack - B.defense) / B.max_hp
```

This is a rough measure of how fast A kills B: higher effectiveness means fewer hits to a kill. Drones have no defense stat, so a unit attacking a drone simplifies to `unit.attack / drone.max_hp`.

What matters for balance is not the absolute value of this number but its *ratio* between two matchups. If Katyusha is twice as effective against guard towers as Maria is at level 1, the design goal is for her to still be roughly twice as effective at level 100. Stat growth is built to hold that ratio constant across the entire level range, unless a design decision explicitly wants it to drift (more on that below).

---

## Two-factor stat growth

Every individual growth rate, how fast a unit's attack rises per level, how fast a drone's HP rises per level, and so on, is **derived**, not hand-set. Two global numbers control everything:

| Factor | Governs |
|---|---|
| `f_offense` | Unit attack growth, drone max HP growth |
| `f_defense` | Drone attack growth, unit max HP growth, unit defense growth |

Each individual rate comes from the same formula:

```
growth_rate = base_stat × factor
```

Which gives every stat the same shape over levels:

```
stat(N) = base × (1 + factor × (N − 1))
```

Current values: `f_offense = 0.11`, `f_defense = 0.11`.

At level N, every stat is a fixed multiple of its level 1 value, and every stat in the same factor group scales by exactly the same multiple. That is the entire trick: because unit attack and drone HP share `f_offense`, the `(1 + factor × (N − 1))` term appears on both sides of the effectiveness ratio and cancels out. Effectiveness holds constant at every level, automatically, without touching individual stat curves by hand.

### Why exactly two groups, not one or four

The grouping is not arbitrary; it falls out of the effectiveness formula itself.

For a unit attacking a drone, effectiveness is `unit.attack(N) / drone.hp(N)`. For this ratio to stay flat as N changes, `unit.attack` and `drone.hp` must grow at the *same* rate. That forces every unit's attack growth and every drone's HP growth onto one shared factor: `f_offense`.

For a drone attacking a unit, effectiveness is `(drone.attack(N) − unit.defense(N)) / unit.hp(N)`. Holding this flat as all three terms grow requires `drone.attack`, `unit.defense`, and `unit.hp` to all share the same growth rate too, otherwise the subtraction and division drift apart independently for every different attack/defense/HP combination in the game. That forces a second shared factor: `f_defense`.

`f_offense` and `f_defense` are otherwise independent of each other, and that gap between them is a real design lever (see below).

### What you can and cannot tune per unit or drone

Because of the grouping above:

- **You cannot** give one drone type a faster HP growth than another, or give one unit a faster attack growth than the others, without breaking the parity the formula guarantees. Every entity within a factor group scales at the identical rate.
- **You can** freely set any entity's *base* stat. A stronger drone has a higher base HP, not a higher growth rate. Base stats are the tool for making one enemy type tougher than another; the factor is the tool for how leveling affects the whole cast at once.
- **You can** choose `f_offense ≠ f_defense` to decide whether leveling favors offense or survivability campaign-wide.

### Flat difficulty vs. asymmetric factors

When `f_offense = f_defense`, every effectiveness ratio in the game stays exactly constant at every level. A level 10 unit fighting a level 10 drone plays out identically, in relative terms, to a level 1 unit fighting a level 1 drone. Only base stats and stage layout drive difficulty. **This is the current setup**, both factors sit at the same value.

Pulling them apart changes the shape of late-game play without touching a single base stat:

- `f_offense > f_defense`: units get disproportionately stronger on offense as they level. Late game trends faster and more aggressive.
- `f_defense > f_offense`: drones get tankier and hit harder relative to unit survivability as levels rise. Late game trends harder.

---

## Grinding and the size of the factor

The factor size controls how much being over or under the stage's intended level actually matters:

- **A factor near 0** makes level almost irrelevant. The game becomes close to purely a positioning and routing skill test, replaying stages for levels barely moves the needle.
- **A high factor** makes level dominate. A sufficiently overleveled player can brute-force a stage that would otherwise require careful play.

The current factor is **0.11** (11% per level) for both `f_offense` and `f_defense`. At that value, stats roughly double by level 10 and reach close to 12 times their level 1 value by level 100. A player three levels above the stage's intended curve is about 36% stronger across every stat governed by that factor, a meaningful edge, but not one that trivializes a stage outright.

The design intent behind that number: a clean, no-grinding playthrough that kills every drone in every stage (maximum available XP) should clear the campaign on its own merits. A player who replays one to three stages for extra XP picks up roughly one to three extra levels, a real catch-up mechanism without making the replay mandatory or making the original difficulty pointless.

**A caveat worth internalizing:** the factor and the XP curve are two separate levers that both affect how much grinding helps, and they need to be read together, not separately. The factor above sets how much *each level* is worth. The XP curve below sets how many levels a stage replay actually *earns*. A steep curve can make the 0.11 factor feel almost irrelevant if a replay only nets a fraction of a level; a shallow curve can make it feel huge if a replay nets two or three levels outright.

---

## The XP curve

The XP required to reach a given level follows a power curve with a flat offset added on top:

```
xp_for_level(L) = floor(A × (L − 1)^B + C × (L − 1))
```

Current values: `A = 50`, `B = 2.0`, `C = 150`. A few reference points from that formula:

| Level | XP required |
|---|---|
| 2 | 200 |
| 10 | 5,400 |
| 50 | 127,400 |
| 100 | 504,900 |

Squaring the level gap (`B = 2.0`) means the threshold steepens continuously: the jump from level 90 to 91 costs vastly more XP than the jump from level 9 to 10. This is deliberate. Kill and damage XP from drones scale with drone level, meaning a stronger, higher-level roster naturally produces more XP income per stage. If the level threshold grew too slowly relative to that income, the result is a runaway curve where a perfect playthrough massively overshoots the intended level for a given stage. An earlier version of this curve (`A = 450`, `B = 1.3`) did exactly that, ending a full campaign clear around level 215 instead of the intended range.

The flat `C` term exists for a narrower reason: it slows down the very first few levels specifically. At low `L`, `C × (L − 1)` is a large share of the threshold; at high `L` the squared `A` term dwarfs it, so it barely changes the long-run shape of the curve. It was added after early playtests showed a unit could reach level 3 off of just two drone kills in the opening stage, faster than the curve was meant to feel.

**Design target:** roughly one to two unit levels gained per stage played straight through, landing in the neighborhood of level 90 to 120 by the campaign's final stage. If you want to check whether a curve change lands correctly, the sanity check is straightforward: fit the actual per-stage XP-income curve your playstyle produces as a power law, then pick a threshold exponent that matches it closely enough that level growth stays close to linear in stage number, rather than accelerating or stalling.

---

## The overlevel XP penalty

Killing or damaging a drone well below your level yields less XP than killing one at or above your level:

```
mult = max(overlevel_factor ^ (unit.level − drone.level), overlevel_floor)
xp   = max(1, floor(base_xp × mult))
```

Current values: `overlevel_factor = 0.9`, `overlevel_floor = 0.2`.

At zero level gap, the multiplier is 1 (no penalty). Each additional level of gap multiplies the reward by another 0.9, so a 10-level gap leaves about 35% of the base XP, and the multiplier reaches its 0.2 floor around a 15-level gap and stays there no matter how far the gap grows past that point.

The floor exists on purpose. Without one, the multiplier decays toward zero as the gap widens, and every kill collapses to the same tiny, fixed trickle regardless of how overleveled the fight actually is. Since replaying a failed stage attempt (keeping surviving units' XP, healing, and trying again) is a legitimate way to make progress on a hard stage, a decay with no floor can turn one extra drone level into the difference between a stage being grindable at all and being a hard wall. This is a single-player, fully offline game where grinding is an intended strategy, not an exploit to close off entirely, so the penalty is tuned to discourage low-level farming without erasing the value of an overleveled attempt at a genuinely hard fight.

---

## The underlevel catch-up bonus

The mirror case also exists: fighting a drone above your level yields more XP than fighting one at or below it.

```
mult = 1 + underlevel_bonus × (drone.level − unit.level)
xp   = floor(base_xp × mult)
```

Current value: `underlevel_bonus = 0.2`. No bonus applies at zero level gap or below; each level the drone sits above the unit adds another flat 20% on top of the base reward, so a unit five levels behind the drones it is fighting earns double the base XP per kill, and one ten levels behind earns triple.

The bonus is additive rather than compounding (`1 + bonus × gap`, not `(1 + bonus)^gap`), so it grows in a straight line as the gap widens instead of accelerating. A unit that falls badly behind, whether from a late-joining teammate, a death penalty, or just an off playthrough, converges back toward the rest of the team over a few fights rather than the gap snowballing in either direction.

This is the same design principle as the overlevel floor, approached from the other side: since a stage's intended drone level is fixed regardless of what level your team actually walks in at, a unit that enters underleveled still needs a realistic way to catch up rather than staying permanently behind for the rest of the campaign.

---

## Level-parity is an assumption, not a guarantee

Everything above guarantees flat effectiveness **only when the acting unit and the target drone are at the same level**. The moment they are not, e.g., a level 8 unit against level 5 drones, effectiveness shifts even with perfectly tuned factors. That is not a flaw; it is the actual difficulty-curve tool used stage by stage:

- Fewer drones in a stage (less available XP) plus units already leveling ahead of the curve means more power carried into later stages, grinding pays off more than usual.
- More drones in a stage means more XP on offer, but also more danger if you engage all of them at the intended level.
- Drones placed above the units' expected level for that point in the campaign create a difficulty spike without changing any global factor at all.

Drone count, drone level, and XP reward are set per stage, independent of the two global factors, and that is where most of the campaign's actual difficulty curve comes from. The factors decide what a level *means*; stage design decides what level you are actually up against.

---

## Setting drone level and roster per stage

The formulas above define what a level is worth. Two more decisions turn that into an actual stage: what level the drones enter at, and how many of them (and which types) to place. Both are set by hand, stage by stage, against a fixed target.

### The baseline playthrough this is tuned against

Every stage is balanced against one specific playthrough: **Normal difficulty**, a single clean run through the whole campaign, one attempt per stage, no replaying a stage for extra XP, no retrying after a bad attempt. The imagined player behind that run is skilled: they read the route preview, spread damage across units, use limit breaks well, and generally play in line with the priority order a careful player would follow (a valuable limit break when one is available, otherwise a free kill, and so on down a sensible list). They are not assumed to find the single numerically optimal line through a stage, only a solid, well-informed one.

That is a deliberately narrower bar than "perfect play." A stage tuned around theoretical optimal clears would be tuned too hard for the player actually sitting down with the game once. Balancing against a skilled-but-not-optimal, one-and-done run is what keeps the "one unit in yellow" target below actually meaning something rather than describing a fight only a min-maxed run would survive.

### Drone level: matching the carry floor

Each stage's `drone_default_level` is set to match the lowest level among your three units as carried over from clearing the previous stage exactly, not simply at or above it. Leaving it above the floor lets a small excess persist and compound: drone kill and damage XP scale with drone level (see the overlevel penalty above), so an over-leveled roster feeds a little extra XP back into the team, which then raises the next stage's floor too, and the whole campaign's levels quietly creep upward stage after stage. Matching the floor exactly keeps the campaign converging on the intended curve of roughly one to two levels gained per stage.

Boss stages (the final stage of each chapter) are the deliberate exception. Their drone level is set above the plain carry floor on purpose, since the finale of a chapter is meant to be its hardest fight, not a fight scaled to the same difficulty as everything before it.

### Roster size: tuned to a single target outcome

Once level is fixed, the number and mix of drones placed in a stage is tuned against one specific target: that baseline player, clearing the stage on their one and only attempt, should end it with exactly one unit down in the yellow HP band, roughly 25% to 50% of max HP, not higher and not lower.

- If a clean first attempt would leave every unit above 50% HP, that reads as too easy, and a drone gets added to the stage before it ships.
- Boss stages are again the exception: they are allowed to demand more than the one-unit-in-yellow target, since they are meant to hit harder than a normal stage.
- Small changes matter more than expected. Adding a single drone, or even just moving one drone to a different tile in the same sector, can be the difference between a sector clearing without a scratch and landing a unit in the yellow band. Roster and placement changes are checked one at a time for exactly this reason.

### A note on Challenge Mode

[Challenge Mode](challenge-mode.md) starts every stage from a fixed level and loadout instead of your campaign save, with no XP gain and no carried-over limit gauge. Every one of those fixed starting points is checked ahead of time and proven clearable, so a Challenge Mode stage that feels tight is never actually unclearable; it is asking you to play tighter than your first campaign clear did.

---

## Summary of current values

| Value | Current setting |
|---|---|
| `f_offense` | 0.11 |
| `f_defense` | 0.11 |
| XP curve `A` | 50 |
| XP curve `B` | 2.0 |
| Overlevel penalty factor | 0.9 per level of gap |
| Overlevel penalty floor | 0.2 |
| Target level range at campaign end | ~90-120 |

These numbers will keep moving as the campaign grows past its current chapter count, this page reflects the values as of the last full balancing pass, not a permanent contract.
