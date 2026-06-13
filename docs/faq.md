---
title: FAQ
description: Answers to common questions about Panzer Island.
---

# FAQ

---

## Gameplay

### Why can Maria not move there?

Maria is water-bound. She can only move on water tiles and is absent from stages without coastal or river access. This is a permanent constraint, not a bug. On water-heavy stages she is your strongest unit; on land-only stages you operate without her.

### Why can Katyusha not hit that drone?

Katyusha's attack range is 1. She can only attack drones on immediately adjacent cells. For longer reach, use Nadeshiko (range 2) or Maria (range 3).

### What does the number on the route preview mean?

It is the estimated total incoming damage if you take that path, accounting for every drone that will react along the route. The number turns red when the predicted damage would reduce your unit to low HP or destroy them.

### How does passive fire work?

At the end of every action, any drone that did not already fire during the action fires at the closest non-acting unit in its range. Your units are not safe just because they are not the one moving. See [Reactive Turns](guides/reactive_turns.md) for the full breakdown.

### A drone seems to be hitting from further than its listed range. Why?

A relay node is probably nearby. Relay nodes increase the attack range of every drone within their radius by 1. Destroying the relay node immediately reverts all boosted ranges.

### What does the orange outline on a drone mean during the route preview?

The drone is in detection range of your planned route and will alert and react if you move there. Drones with the orange outline will fire if you commit to that path.

---

## Progression

### Do levels and skill picks carry over between chapters?

Yes. Unit levels, XP, and skill choices persist across the entire playthrough. Nothing resets between stages or chapters. Only starting a new game resets progression.

### Can I change my skill choices after picking?

No. Skill picks are permanent within a run. If you want to try a different build, start a new game.

### What happens when a unit is destroyed mid-stage?

The unit is gone for the rest of that stage. They return afterward but at reduced HP (damaged state) and lose 50% of the XP they earned in that stage. A damaged unit can be repaired on the world map before the next stage. If a damaged unit is destroyed again before being repaired, they are permanently lost for the run.

### How do I earn XP faster?

Defeat drones and deal damage. You earn XP for damage dealt even if another unit lands the killing blow. Replaying an earlier stage to level up is a valid strategy if you are stuck on a difficult one.

---

## Story

### What are memory fragments?

Memory fragments are collectible objects found on stages: abandoned terminals, black boxes, and similar. When a unit picks one up, they recover a partial memory tied to that location. The unit's memory triggers a fragment of Erika's memory, shown as a short visual scene between stages. Fragments are optional but needed to unlock the full story.

### Does Panzer Island have multiple endings?

Yes, three endings. Which ending you reach depends on choices made during the campaign. The endings are part of Chapters 2-6 (full game).

### Who is Erika?

Erika is the scientist the player accompanies. She wakes at the start of Chapter 1 with most of her memory gone and is gradually piecing together what happened on the island. Her three AI units know more than they are permitted to say.

### What is ORACLE?

ORACLE is referenced in recovered logs and technical documentation found on the island. What it is and what it did becomes clearer as you collect memory fragments across the campaign.

---

## Demo and purchase

### What is included in the free demo?

Chapter 1: ten stages, roughly one to two hours of play. Available on Steam, itch.io, and Android. The demo ends at the ferry crossing to the main island.

### What is the difference between the Steam demo and full game entries?

Steam lists the Chapter 1 demo and the full game as separate store entries. The demo does not unlock the full game. Google Play and itch.io ship as a single app with Chapter 1 free and Chapters 2 onward unlocked by a one-time in-app purchase.

### Is there a New Game Plus or chapter select?

Not in the current version. Each run starts from Chapter 1.

---

## Technical

### Does the game work offline?

Yes. Panzer Island has no online features and runs fully offline on all platforms.

### The dev blog mentions a solver and AI playtester. Can I access it?

The solver is an internal development and balancing tool. It is not distributed as part of the game or publicly available.

### Is there an undo button?

On Easy difficulty, every action creates a checkpoint. You can step back through the current stage's history and restore to any prior state. On other difficulties there is no undo.
