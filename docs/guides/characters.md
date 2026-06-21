---
title: Your units
description: Stats, skills, and limit breaks for Katyusha, Nadeshiko, and Maria in Panzer Island.
---

# Your units

Panzer Island gives you three units. They are not interchangeable: each has a distinct role, movement type, and limit break. Understanding what each unit does well, and where it is weak, is more useful than memorizing numbers.

---

## How to read this page

**HP, Attack, Defense** are base level 1 values from the game data. They scale as units level up. Use the slider to preview values at higher levels.

**Range** is the unit's normal attack range and does not scale.

**Movement** shows which tile types the unit can traverse.

**Limit break.** Each unit has a Limit Gauge that charges by +10 whenever they deal or take damage. When full, the player can trigger the unit's Limit Break instead of a normal action. The gauge resets after triggering and recharges from the next damage event. There is no per-stage cap: a unit that keeps absorbing fire can use their Limit Break more than once per stage.

**Skill tracks.** At levels 4, 7, 14, and 17 the player picks one stack of either track, up to a cap of 2 stacks per track. By level 17 each track has exactly 2 stacks. Stacking one track early forces the other to fill in later.

---

<div class="drone-level-selector">
  <label for="unit-level">Unit level: <strong id="unit-level-display">1</strong></label>
  <input type="range" id="unit-level" min="1" max="100" value="1" step="1">
</div>

HP, Attack, and Defense update to match the selected level. Range does not scale.

---

## Katyusha

<div class="unit-card">
  <img src="../assets/portraits/katyusha_neutral.webp" class="unit-card__portrait" alt="Katyusha">
  <img src="../assets/units/katyusha.png" class="unit-card__sprite" alt="Katyusha tank unit">
  <div class="unit-card__body">
    <p class="unit-card__name">Katyusha</p>
    <p class="unit-card__role">Tank pilot AI</p>
    <p>An AI character who controls a battle tank. High HP, high attack, terrain cover. Her limit break, Iron Curtain, blocks incoming fire and counter-attacks drones that shoot at her while it is active.</p>
  </div>
</div>

| HP | Attack | Defense | Range | Movement |
|----|--------|---------|-------|----------|
| <span class="unit-stat" data-base="150" data-rate="16.5">150</span> | <span class="unit-stat" data-base="25" data-rate="2.75">25</span> | <span class="unit-stat" data-base="13" data-rate="1.43">13</span> | 1 | Ground |

**Role:** Frontline. Takes hits, holds ground, and pushes through defended positions.

**Strengths:** Highest HP and defense of the three units. Gains cover bonuses from terrain. Her limit break turns fire into a counter-attack, making her actively dangerous to shoot at.

**Weaknesses:** Short attack range (1). Interceptors fly over terrain and close distance quickly; Katyusha has no way to avoid their approach.

**Cannot do:** Fire at range 2 or beyond. Cross water or fly. Move quickly across large maps. Katyusha is your frontline; she is not a flexible unit. If she needs to reach a target, she walks through whatever is in the way.

### Limit break: Iron Curtain

> *"Understood. Executing maximum force protocol."*

Katyusha activates a counter-shield. While active, incoming damage is blocked and she counter-attacks up to N unique drones that fire on her. Drones that fire beyond the reflect cap still deal damage normally. The shield is not invulnerability; it is a threat multiplier against clusters.

| Track | Effect per stack | Max stacks |
|-------|-----------------|------------|
| **Curtain Capacity** | Reflect cap +2 (base cap: 2, fully stacked: 6) | 2 |
| **Curtain Reflect** | Counter damage +50% of base attack per stack (0 stacks: blocks only; 1 stack: 150%; 2 stacks: 200%) | 2 |

Best used when pushing through a cluster of guard towers or a tight patrol group. Count how many drones will react before triggering; drones beyond the cap still hit.

---

## Nadeshiko

<div class="unit-card">
  <img src="../assets/portraits/nadeshiko_neutral.webp" class="unit-card__portrait" alt="Nadeshiko">
  <img src="../assets/units/nadeshiko.png" class="unit-card__sprite" alt="Nadeshiko helicopter unit">
  <div class="unit-card__body">
    <p class="unit-card__name">Nadeshiko</p>
    <p class="unit-card__role">Helicopter pilot AI</p>
    <p>An AI character who pilots a reconnaissance helicopter. Flies over any terrain. Her limit break, Storm Run, sends her dashing in a straight line, dealing damage to every drone along the path.</p>
  </div>
</div>

| HP | Attack | Defense | Range | Movement |
|----|--------|---------|-------|----------|
| <span class="unit-stat" data-base="120" data-rate="13.2">120</span> | <span class="unit-stat" data-base="30" data-rate="3.3">30</span> | <span class="unit-stat" data-base="10" data-rate="1.1">10</span> | 2 | Air |

**Role:** Scout and fast striker. Reaches places the other units cannot, and eliminates high-value targets with her limit break.

**Strengths:** Flies over all terrain, including water, mountains, and forest. Highest base attack of the three units. Can approach from angles that ground and water units cannot reach.

**Weaknesses:** Lowest HP and defense. She cannot absorb fire. One bad route into drone range can end a stage. Interceptors fly too and will pursue her regardless of terrain.

**Cannot do:** Take hits. Nadeshiko is not a unit you route through active drone fire. Even a single guard tower hit is significant at her HP and defense values. If she ends up in range of multiple firing drones, she will not survive it. She is for flanking clean routes, not for trading fire.

### Limit break: Storm Run

> *"Okay okay okay, hold on, I've got this!"*

Nadeshiko dashes in a straight line to a target cell within placement range, damaging every drone adjacent (Chebyshev 1) to any cell on the path. She can walk into position first if the target is outside placement range. Drone reactions resolve after the dash completes, not during it.

| Track | Effect per stack | Max stacks |
|-------|-----------------|------------|
| **Storm Range** | Placement range +1 cell | 2 |
| **Storm Damage** | Damage multiplier +×1 per stack | 2 |

Best used to eliminate a high-priority target deep in enemy territory, or to clear a line of drones in a single action that Katyusha could not reach cleanly.

---

## Maria

<div class="unit-card">
  <img src="../assets/portraits/maria_neutral.webp" class="unit-card__portrait" alt="Maria">
  <img src="../assets/units/maria.png" class="unit-card__sprite" alt="Maria warship unit">
  <div class="unit-card__body">
    <p class="unit-card__name">Maria</p>
    <p class="unit-card__role">Warship AI</p>
    <p>An AI character who commands a warship. Long-range, water-bound, and devastating against stationary targets. Her limit break, Broadside, fires a 3x3 barrage that suppresses drone counterfire while it lands.</p>
  </div>
</div>

| HP | Attack | Defense | Range | Movement |
|----|--------|---------|-------|----------|
| <span class="unit-stat" data-base="135" data-rate="14.85">135</span> | <span class="unit-stat" data-base="27" data-rate="2.97">27</span> | <span class="unit-stat" data-base="11" data-rate="1.21">11</span> | 3 | Water |

**Role:** Long-range support. Fires from a stable position and clears fortified clusters with her limit break.

**Strengths:** Longest attack range of the three units. Can engage guard towers and artillery from outside their range. Her Broadside limit break suppresses drone counterfire while it lands.

**Weaknesses:** Water-bound. She cannot move on land and is absent on stages without coastal or river access. Cannot close distance; most effective from a fixed firing position.

**Cannot do:** Move on land. At all. Maria is completely absent from land-only stages. On stages that do have water, she cannot follow Katyusha and Nadeshiko into the interior. Plan her firing positions around water access, not around where the threats are. The threats need to be in her range from a water tile, or she cannot engage them.

### Limit break: Broadside

> *"I'm sorry. But this has to end."*

Maria fires a 3x3 barrage centered on a target cell within placement range. Every drone in the barrage area takes damage but does not counterattack. She stays in place; she can reposition first if the aim point is outside range.

| Track | Effect per stack | Max stacks |
|-------|-----------------|------------|
| **Broadside Range** | Placement range +1 cell | 2 |
| **Broadside Damage** | Damage multiplier +×1 per stack | 2 |

Best used to clear a packed formation or break a defensive position that is too costly to attack directly. The suppression is the reason to trigger it: Broadside lets Maria deal heavy damage to a cluster without any drone in that cluster firing back.

---

## Unit interactions

The three units work best when their actions are coordinated rather than independent.

A common pattern: Katyusha advances into a cluster, triggering drone reactions and charging her limit gauge. With Iron Curtain active she counter-attacks the drones that fire on her. After her turn resolves, Nadeshiko flanks from an unexpected angle or uses Storm Run to finish isolated targets. Maria provides fire support from outside drone range, targeting anything with high HP or a relay node.

The same logic applies in reverse. If Katyusha needs to push through a fortified zone, use Nadeshiko or Maria to draw drone attention first, reducing how many drones react to Katyusha's advance.

See [Reactive Turns](reactive_turns.md) for a full explanation of how passive fire and reflex responses affect all three units simultaneously.

<script>
(function () {
  function applyLevel(level) {
    document.getElementById("unit-level-display").textContent = level;
    document.querySelectorAll(".unit-stat[data-base]").forEach(function (el) {
      var base = parseFloat(el.dataset.base);
      var rate = parseFloat(el.dataset.rate);
      el.textContent = base + Math.trunc(rate * (level - 1));
    });
  }

  function init() {
    var slider = document.getElementById("unit-level");
    if (!slider) return;
    slider.addEventListener("input", function () {
      applyLevel(parseInt(this.value, 10));
    });
    applyLevel(parseInt(slider.value, 10));
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  /* Re-run after Material for MkDocs instant navigation swaps the page */
  if (typeof document$ !== "undefined") {
    document$.subscribe(init);
  }
})();
</script>
