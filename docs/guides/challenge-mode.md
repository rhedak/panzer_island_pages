---
title: Challenge mode
description: How Challenge Mode works in Panzer Island, how scores are calculated, and how to submit a run.
---

# Challenge mode

Challenge Mode is a separate difficulty track for players who have already cleared a stage and want a tighter, score-based version of it. This guide covers how it differs from the main game, how your score is calculated, and how to submit a run.

---

## How it differs from the main game

Challenge Mode replays the same stages with three changes:

- **Fixed unit stats.** Each stage starts your units at a preset level, HP, and skill loadout instead of whatever you have equipped in your main save. Every player faces the same starting point on a given stage.
- **No limit gauge carry-over.** All three units start every Challenge stage at 0% limit gauge. You have to charge it up yourself during the stage, the same way you would mid-run in the main game.
- **No XP gain.** Challenge Mode progress is entirely separate from your main save. Clearing a stage here does not level up your units or unlock skills there, and vice versa.

Your goal on each stage is not just to clear it, but to clear it efficiently: fewer actions, less damage taken, more kills.

---

## How the score is calculated

Each stage clear produces a score from three numbers tracked during the run: total kills, total damage taken, and total actions used.

```
score = 10,000 + (kills × 2,000) − (damage taken × 100) − (actions used × 10)
```

The score cannot go below 0. Every kill is worth a lot; taking damage and spending extra actions both cost you, with damage taken being the steeper penalty of the two.

Each stage also has a **target score**, shown on the result screen alongside yours. Your percentage is your score relative to that target. Reaching 100% or more marks the stage as **bested** and unlocks score submission for that run.

---

## Where the target score comes from

The target for each stage is produced by an internal solver, a script that plays every stage using a fixed set of priority rules (take a valuable limit break if one is available, otherwise take a free kill, otherwise take a free limit-break kill, and so on down a fixed priority list) rather than search or trial and error. It does not "know" the best possible play; it plays a consistent, disciplined line and reports what score that line achieves. That score becomes the stage's target.

This means the target is a reasonable bar, not a theoretical maximum. Beating it by a wide margin on a stage you know well is entirely possible.

---

## Submitting a run

When you best a stage (100% or higher), a **Submit Score** button appears on the result screen. Pressing it opens this page in your browser with your run's data attached.

<div id="challenge-submission" style="display:none;">

### Your run

<p id="challenge-submission-summary"></p>

<textarea id="challenge-submission-data" readonly rows="8" style="width:100%; font-family: monospace; font-size: 0.8em;"></textarea>

<p>
<button id="challenge-copy-btn" class="md-button">Copy run data</button>
<a id="challenge-mailto-btn" class="md-button md-button--primary" href="#">Email this run</a>
</p>

<p><small>The email opens with a subject line already filled in. Paste the copied run data into the body before sending.</small></p>

</div>

If you did not arrive here from the game's Submit Score button, or just want to send feedback about Challenge Mode in general, email **[panzerisland@proton.me](mailto:panzerisland@proton.me)** directly. Include the chapter, stage, and your score.

There is no public leaderboard yet. Submitted runs are read manually and may inform target score tuning in future updates.

<script>
(function () {
  function b64DecodeUnicode(str) {
    return decodeURIComponent(
      atob(str)
        .split("")
        .map(function (c) {
          return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
        })
        .join("")
    );
  }

  var params = new URLSearchParams(window.location.search);
  var data = params.get("data");
  if (!data) {
    return;
  }

  var payload;
  try {
    payload = JSON.parse(b64DecodeUnicode(data));
  } catch (e) {
    return;
  }

  var section = document.getElementById("challenge-submission");
  var summary = document.getElementById("challenge-submission-summary");
  var textarea = document.getElementById("challenge-submission-data");
  var copyBtn = document.getElementById("challenge-copy-btn");
  var mailtoBtn = document.getElementById("challenge-mailto-btn");
  if (!section || !summary || !textarea || !copyBtn || !mailtoBtn) {
    return;
  }

  var pretty = JSON.stringify(payload, null, 2);
  var chapter = payload.chapter;
  var stage = payload.stage;

  summary.textContent = "Chapter " + chapter + ", Stage " + stage + ".";
  textarea.value = pretty;

  var subject = encodeURIComponent(
    "Challenge Mode submission: Chapter " + chapter + " Stage " + stage
  );
  var body = encodeURIComponent(
    "Chapter " + chapter + ", Stage " + stage + "\n\nPaste your copied run data below:\n\n"
  );
  mailtoBtn.href = "mailto:panzerisland@proton.me?subject=" + subject + "&body=" + body;

  copyBtn.addEventListener("click", function () {
    textarea.select();
    navigator.clipboard.writeText(textarea.value).then(function () {
      copyBtn.textContent = "Copied";
      setTimeout(function () {
        copyBtn.textContent = "Copy run data";
      }, 1500);
    });
  });

  section.style.display = "block";
})();
</script>
