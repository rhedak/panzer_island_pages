---
date: 2026-06-13
title: How generative AI supported the making of Panzer Island
description: A detailed account of where AI helped, where it did not, and the line between the two.
authors:
  - dev
---

# How generative AI supported the making of Panzer Island

Panzer Island is a solo project. One developer. A full-length strategy game with a written narrative, three playable characters, a custom toolchain, and a campaign solver that can verify every stage is beatable before a build ships.

I used generative AI throughout. This post describes exactly where, how much, and what I kept out of its hands.

<!-- more -->

---

## The philosophy

The shortest version: human-driven, AI-assisted.

Every design call, balance verdict, and story beat comes from me. Every merged change is one I validated by playing the game on hardware. AI is a power tool that compresses the gap between "I want to try X" and "X is in my hands." It does not decide what X should be.

That distinction matters because the failure mode I was trying to avoid is not "AI wrote bad code." It is "AI made a decision I did not notice." Generators, solvers, and language models are all good at producing something that looks like an answer. The discipline is noticing when the answer does not actually fit, and doing the work to find one that does.

---

## Where AI was used

### 1. Code: Claude as a programming assistant

The largest share of AI involvement was Claude (Anthropic), Grok Build (xAI) and OpenCode Zen, as coding assistants throughout development. This covered:

**Design Document Review.** Before writing any code extensive design documents were created and passed to the AI for review. These include a master Game Design Document (GDD), a balancing document as well as various styleguides. For details see subsection Design Document driven development.

**Tooling.** The four Python tools that carry the most weight in this project were built with heavy AI assistance: the stage editor (Tkinter UI for placing terrain, drones, and objectives), the cutscene editor (locale-aware dialogue authoring), the balance editor (unit and drone growth schemas, XP budget), and the feasibility solver (a Python mirror of the live game engine that can verify whether a stage is clearable). These tools exist so a human can iterate fast. The design decisions they produce are still mine to make.

**Refactors and parsers.** Godot's GDScript is not a language with a long tail of Stack Overflow answers. When I needed to migrate the stage data format, restructure the save schema, or add a new drone behavior while keeping the Python solver in sync, AI handled the mechanical parts. I reviewed every change and ran the test suite.

**Test scaffolding.** The project ships with 400+ GDScript tests and 200+ Python solver tests. Writing test harnesses is work I would have cut corners on without assistance. Having a test suite that catches regressions at the unit level changed how freely I could iterate on the reactive turn engine.

**Design discussions and subagent playtests.** Some of the most useful interactions were not code at all. Describing a proposed mechanic and talking through its implications with a system that had read the whole codebase caught several problems before they became bugs. It is not the same as talking to another developer. It is useful in a different way. For that purpose I designed a subagent playtest system that involved an AI Agent playing the game in a "headless" environment (see subsection subagent playtest system)

What Claude does not do: it does not balance the game. It does not decide which stages are fun, which story beats land, or whether the pacing of Chapter 1 is right. Those required playing the game on hardware, over and over, until the answer was obvious.

### 2. Character portraits: Google Gemini

I cannot draw. The 196 character portrait images in the game (Erika, Katyusha, Nadeshiko, Maria, Wilhelm, Drona, and the greyscale alpha unit variants, each in nine emotional states) were generated with Google Gemini against a tightly specified prompt set.

The prompts are documented in full at `docs/assets/portraits.md` in the game repository. Each character has a base prompt describing their visual identity in precise terms: hair color and style, clothing, color palette, posture, emotional register. Each emotional variant adds specific expression and body language tags. For example, Katyusha's "Angry" variant specifies "flat intense glare, furrowed brow, sharp eyes, tight pressed lips, arms raised, hands balled to fists," distinct from Maria's "Angry" which reads "intense red glow in eyes, sharp dangerous smirk, hand resting firmly on hip, tense authoritative stance." The difference in register matches the difference in character.

The generation workflow was:
1. Generate a full-body reference image first, to anchor the character's proportions and outfit.
2. Use that image as a character reference at 60% strength on subsequent generation passes, to prevent outfit and hair drift between expressions.
3. Post-process every output with Python tooling: bust crop to a consistent 55-65% framing, format conversion, batch rename.

This is not "AI made the art." It is closer to: I wrote a detailed brief, iterated on the brief until the output matched my intent, and then automated the production pipeline. The characters look like who they are supposed to be because the prompts specify exactly what that means. Getting there took revision.

A few things that did not work and required explicit solutions: maintaining consistent skin tone across emotional variants (required explicit palette specification), keeping Drona's red-to-pink gradient hair stable (required "Vivid red roots bleeding into pink tips" in every prompt), and preventing the alpha unit greyscale variants from losing the red targeting reticle detail (required explicit emphasis). Each problem had a specific fix; none had a general fix.

### 3. What I did not use AI for

Three areas where AI was explicitly not used, and why.

**In-game sprites.** Every unit sprite (Katyusha, Nadeshiko, Maria, and their animated frames), every drone sprite, every terrain tile, every UI icon, every prop, the world map, the boot splash, and the studio logo are generated programmatically with Python and matplotlib. Reproducibly, from source code, via `./generate.sh`. Note AI helped draft the code for the assets and I refined it.

This was a deliberate choice. Direct AI image generation produces outputs I cannot fully control or regenerate deterministically. Programmatic generation produces outputs I can version-control, tweak pixel by pixel, and rebuild from scratch if the spec changes. When Katyusha's color palette needed to shift, I changed two constants in `palette.py` and regenerated. When a new drone type was added, I wrote the drawing code for it. The art is simple, deliberately GBA-era in aesthetic. That constraint and the code-driven approach fit each other.

**Sound effects.** All SFX were generated by a custom Python `wave`-package synthesizer from JSON parameter files. The parameter files were designed using sfxr-compatible browser tools, then saved as data. The synthesizer is hand-written. No AI audio generation was used. The output is retro and intentionally lo-fi. Note that the AI helped draft the code for the sfx system and I refined it.

**Music.** The 11 in-game chiptune tracks are licensed Creative Commons compositions by Patrick de Arteaga. Human-composed, not generated.

**Story and narrative.** The narrative, the characters, the stage-by-stage plot beats, the locked cutscene exchanges, and the structure of the six-chapter arc are mine. This was the area where I was most careful not to let AI become the author. AI helped with prose checking (does this line match the character's voice profile? does this paragraph contain an em dash?) but not with deciding what the story says or what the characters mean to each other. The game has things it is trying to say. Those things came from me.

---

### Design document driven development

Before a line of code was written, the design existed as documents.

The process was: write a detailed design document, pass it to an AI coding assistant for review, then implement. The key documents included the Game Design Document (GDD) and the story document, alongside several supporting specifications. Both were completed to a high level of detail before development started: the GDD specifies the reactive turn system, all unit stats and skill trees, enemy drone types and behaviors, stage structure, the business model, and platform targets. The story document specifies all six named characters, the full six-chapter narrative arc with per-stage plot beats, the character voice system (how each character speaks, what sentence shapes they use, what they are and are not allowed to say), and dozens of locked dialogue exchanges that cannot be changed without cascading consequences.

Passing this material to an AI before implementation had a specific effect: the design had to be unambiguous to survive review. Vague designs produce vague AI questions that expose the vagueness. A rule like "drones react when you move" turned into a concrete question about edge cases (what counts as a reaction, what happens when multiple drones react to the same step, how pursuit interacts with passive fire) that I had to resolve before the first commit. The process of making the design legible to an AI is largely the process of making it legible to a developer, including a future version of yourself.

The styleguides followed the same pattern. The English writer's styleguide for the game specifies proper noun spellings, American vs. British dialect preference, the ellipsis format, the em dash ban, exclamation mark allocation by character, contraction frequency by character, and sentence shape profiles for each of the six speaking characters. It was written before the cutscenes were authored, and reviewed by AI before any dialogue was written. When a new cutscene line was drafted, checking it against the styleguide was a first-pass review the AI could run mechanically, flagging a misplaced exclamation mark or a Katyusha line with too many contractions before a human read it.

The documents that were in place before development began, with a brief summary of each:

**Game Design Document (GDD).** The primary specification. Covers the reactive turn system rules in full, all three unit stat blocks and skill trees, every drone type and its exact behavior, sector and chapter structure, objective types, the business model, and platform targets. The most intensively AI-reviewed document: the reactive fire rules in particular required several passes to resolve edge cases around multi-drone reaction order and the interaction between pursuit and passive fire, all before the first commit.

**story.md.** Narrative specification. Defines all six named characters with biographical backgrounds and relationships; the full six-chapter arc with per-stage plot beats; per-character voice profiles covering sentence shape, vocabulary constraints, and contraction frequency; and dozens of locked dialogue exchanges. Locked means that specific line cannot be rewritten without cascading consequences in adjacent scenes. AI review of this document before cutscene authoring surfaced several timeline continuity gaps that were resolved in the document, not in the code.

**visual_styleguide.md.** Visual identity per chapter. Assigns a palette family, terrain theme (clean, tainted, dead, or chapter-specific), composition vocabulary, and prop leitmotifs to each chapter. Cross-chapter rules include: every stage must contain navigable water, because Maria is a ship and removing water removes her from that stage, which is a mechanical event requiring a narrative justification; each indoor stage has exactly one saturated color point against an otherwise desaturated palette; and the only greyscale elements on screen are Alpha-unit appearances, making Alpha sightings a recognizable visual beat without dialogue. These rules were written and reviewed before any terrain sprites were generated.

**tech_stack.md.** Engine selection and project structure. Evaluates Godot 4 against the project's requirements (2D pixel art, anime portrait cutscenes, one-click export to Steam and Android, solo developer overhead) and defines the folder layout, key script responsibilities, and Python toolchain organization. Writing this early gave the AI assistant a precise map of where each new file belonged, rather than allowing structure to accumulate ad-hoc across the project.

**balancing.md.** Balance mathematics and drone placement contracts. Derives a two-factor growth system where all unit attack rates and drone HP rates share one global growth factor, and all drone attack, unit defense, and unit HP rates share a second. This algebraic coupling guarantees that effectiveness ratios are preserved at all levels, preventing the stat inflation that typically appears in long strategy campaigns. The document also specifies placement contracts for the three support drone types introduced in Chapter 3 (Spotter, Relay Node, Repair Drone), stating exactly what decision each one must force on the player for its placement to satisfy the design intent.

**chapter_stage_design.md.** Stage authoring checklist. Encodes the canonical 10-stage chapter structure, required objective type mix across a chapter, drone count escalation targets, anti-ground and anti-air coverage requirements per sector, tutorial text obligations for new mechanics, and a named catalog of common drafting errors collected from review passes. This document functions as the verification contract that every chapter is audited against before the feasibility solver is run.

**English writer's styleguide (styleguide_en.md).** Described in the paragraph above. The voice system for all six speaking characters, written before cutscene authoring began.

The constraint this creates is real: you cannot write design documents of this depth quickly. The GDD took time to write and more time to get to a state where review would produce useful feedback. The payoff is that the implementation phase had very few "what does this mechanic actually do?" moments, because those questions were resolved in the documents.

---

### Subagent playtest system

Every stage in Panzer Island needs to be verified as clearable and worth playing before it ships. For a solo developer without a QA team, neither condition is easy to confirm alone. The playtest system has two parts that work in sequence.

**Part 1: the feasibility solver.**

The solver is a parallel implementation of the live game engine in pure Python. Combat math, drone reactions, step-by-step movement, terrain, limit break triggers, XP accrual, level-ups, and stage objectives are all re-implemented so the solver can simulate states without running Godot. The full Chapter 1 campaign (10 stages) runs in roughly one minute.

The agent inside the solver is a greedy priority-ladder planner. It operates on a ranked list of move types: a valuable limit break kill is always preferred over a free kill, which is always preferred over a bait move, and so on down the ladder. At each step the planner generates all candidates for the highest-priority viable move type, picks the best by a tiebreaker (acting unit's HP band, then team minimum HP), and commits. The planner is deterministic given a fixed stage and unit state.

When the solver clears a stage it produces a JSON action log that the live engine can replay as a full visual playthrough inside Godot. When it fails, the failure report is diagnostic data: a stage the solver cannot path through in 60 seconds per sector is almost certainly too hard. The difficulty target is a stage where the solver needs several attempts and produces a solution that looks like it required genuine priority management.

Every time a gameplay mechanic changes in GDScript, the matching Python module must be updated in the same commit. Drift between the two implementations is the only real failure mode: if the solver's model of Iron Curtain diverges from the live engine's model, it finds "solutions" that do not work in the game. A test suite of 200+ Python solver tests checks mechanical parity on each commit.

**Part 2: the AI subagent playtest.**

The solver answers "is this stage clearable?" It does not answer "is the tutorial text accurate?", "does the story beat land?", "is the difficulty progression appropriate?", or "does anything feel wrong as a player experience?" For those questions, the second part of the system uses an AI language model as a structured playtester.

The briefing process for a subagent playtest is documented in the game repository as a step-by-step protocol. The agent receives:

1. A mechanics reference document covering the reactive turn system, all unit stats, all drone types and behaviors, terrain codes, combat formulas, objective types, and cutscene slot order.
2. A story-so-far summary covering every plot beat the player has accumulated up to the stage being tested.
3. The solver's carry-state JSON from the previous stage, establishing the exact unit levels, XP, and skill choices the player would have at this point in a real playthrough.
4. The live stage files read directly from the repository: the grid, drone roster, objectives, tutorial text, and all cutscene files.
5. The solver's action log for this stage, if one exists.

The agent is then asked to play the full experience in order: cutscenes, then gameplay step by step with HP tracking and explicit reasoning, then post-stage cutscenes. Feedback is structured into three categories: mechanics and level design, narrative, and overall verdict.

The solver's action log is included because it creates a specific cross-check: does the tutorial text describe the tactic the solver found? If the tutorial says "center the Broadside on the artillery cluster," does the solver's action log show a Broadside fired at that cell? A discrepancy is not automatically a bug. The greedy planner may find a valid clear that differs from the described approach. But if the tactic the tutorial describes does not work at all, or works only in a way that contradicts the explanation, that is a flag.

After the subagent returns its feedback, the workflow is: apply all text and logic fixes autonomously, hold for human confirmation on anything that touches drone roster, map layout, unit stats, or stage structure, and iterate until the stage gets a clean pass. Then rerun the solver as a final sanity check, confirm all changes with a human, and mark the stage closed.

The system does not replace playing the game. The solver finds clearable paths; it does not find enjoyable ones. The subagent notices mismatches between what the text says and what the mechanics do; it cannot tell you whether a stage feels tense or satisfying. Human playtesting on hardware remains the final bar. The two-part system narrows the surface area that hardware playtesting has to cover.

---

## What this cost

Transparency requires acknowledging the tradeoffs.

The portrait generation workflow produced 196 images that I am broadly happy with, but they required significant iteration to get right. AI image generation is not faster than commissioning an artist if you care about specificity. It is faster than learning to draw from scratch, which was the relevant comparison for this project.

The AI-assisted tooling saved an amount of development time I would estimate at several weeks. The tradeoff is that I sometimes merged code I understood at a high level but had not written line by line. The test suite caught most of the problems that created. A few it did not catch required careful debugging.

The programmatic sprite generation is slower and more limited than an AI image pipeline for producing visual variety. The tradeoff is full control and reproducibility. For a solo project that needs to stay maintainable, that was the right call.

---

## The line

If I had to state the principle in a single sentence: AI generates candidates; I make decisions.

The reactive turn system, the three-unit dynamic, the sector structure, the skill trees, the story of a scientist who caused a catastrophe and has spent a long time not looking at it directly. None of those came from a generator. They came from thinking about what kind of game I wanted to play, and not stopping until the thing in my hands matched it.

The tools helped me get there faster. The getting there was mine to do.
