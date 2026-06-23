---
date: 2026-06-23
title: "Dev Log: 2026-06-23"
description: "The challenges of making a Godot 4 game work across PC, web, and Android screen sizes."
authors:
  - rhedak
---

**Dev Log: 2026-06-23**  
*“Why Godot hates me personally and every screen manufacturer is in on it”*

---

### Cross-Platform Viewport Scaling: A Tragedy in Three Acts

I ship one humble Godot 4 game to **Steam** (PC/Mac/Linux), **itch.io** (web), and **Google Play** (Android). That’s three platforms, each with its own unique way of saying “lol no” to the concept of a consistent screen.

It’s like trying to fit the same pair of pants on a giraffe, a raccoon, and a sentient toaster.

---

### The Three Targets and Their Personality Disorders

| Target       | Container                          | Key Personality Flaw |
|--------------|------------------------------------|----------------------|
| Steam (desktop) | OS window, user-resizable         | “I can be any size I want, you can’t stop me” |
| itch.io (web)   | Responsive iframe in browser page | Gaslighting champion |
| Google Play (Android) | Device screen + hardware nonsense | “What if we put corners *and* holes in it?” |

---

### Godot Stretch Modes: The Knobs of Madness

Godot gives me two magical dials:

- **`window/stretch/mode`**: Decides if the game world is a fixed kingdom or stretches like a yoga influencer.
  - `"viewport"`: Fixed 1280x720 coordinate space. Everything outside gets letterboxed or clipped.
  - `"canvas_items"`: Everything scales like it’s on a diet. No clipping, just beautiful proportional chaos.
  - `"disabled"`: Pure anarchy.

- **`window/stretch/aspect`**: What to do when reality doesn’t match my beautiful 16:9 dreams.
  - `"expand"`: Let the player see more map. (My hero)
  - `"keep"`: Black bars forever.
  - `"ignore"`: Just distort everything like a funhouse mirror.

I mostly run `"viewport"` + `"expand"` because I like my players to see extra battlefield instead of fancy black bars.

---

### Desktop: The Only Sane One

On Steam, it just… works. Players resize the window like civilized humans and my dynamic UI shrugs and adapts. The worldmap doesn’t throw a tantrum. 

For once, something didn’t try to ruin my day. I almost cried.

---

### Web: The Iframe Trap (A Horror Story)

Here’s how itch.io works, apparently designed by a committee that hates solo developers:

I set my embed size to 1280x720. Cool. Then itch.io slaps `width: 100%` on the container like it’s 2009 and responsive design just got invented. Suddenly the browser says “actually it’s whatever size I feel like today.”

Inside the game, `window.innerWidth` helpfully reports the *entire browser window*, not my embed. It’s like asking how big your pizza is and getting the dimensions of the delivery guy’s car.

Then there’s `canvas_resize_policy`:

- 0 = Tiny pixel gremlin in the corner
- 1 = Fixed size, black bars galore
- 2 = “I will consume the entire screen like a digital black hole”

I need 2. Of course I do.

The combination of Adaptive + viewport + expand worked *everywhere* except the worldmap, which was still hardcoded like it was 2018 and I’d never heard of scaling. Cue 188 pixels of beautiful empty blue space staring at players like “yes, I am the void.”

After several failed attempts that involved me yelling at Retina displays, I surrendered and used **feature tag overrides** like a proper adult:

```ini
window/stretch/mode.web="canvas_items"
```

Web gets to live in proportional scaling land. Everything else keeps the dynamic viewport. Peace was restored (for now).

---

### Android: A Satirical Rant About Rounded Corners and Humanity’s Mistakes

**Oh, Android.** Sweet summer child of hardware fragmentation.

You know what the world needed in 2026? More **rounded corners**. Because sharp 90-degree angles were clearly oppressing us. And while we’re at it, let’s shove a camera notch right in the middle of the UI. Maybe two notches. Maybe a whole *hole punch*. Perhaps we’ll make the phone fold in half for no reason.

The OS very kindly gives me a “safe area inset” so my UI doesn’t get eaten by the designer’s fever dream. Does Godot automatically respect it? **Haha. No.** Of course not.

So now I have a sacred constant:

```gdscript
const SAFE_EDGE := 20  # pixels of therapy
```

Every button, every panel, every “yes I’m sure I want to end my turn” lives in constant fear of being swallowed by a lovingly rounded bezel. The worldmap at least centers itself like a good boy. The rest of the HUD gets manually nudged away from the edges like I’m herding particularly stubborn cats.

I also have aspect ratios ranging from “normal human” to “this phone is 90% taller than it is wide, enjoy your new vertical shooter.” Thankfully `"viewport" + "expand"` just shows more map instead of panicking. Small mercies.

**To the phone manufacturers**: I see you. I see your rounded corners. I hope your design team steps on a Lego every morning for the rest of their lives.

---

### Summary: Emergency Debugging Cheatsheet

| Symptom                            | Likely Cause                              | Where to Cry |
|------------------------------------|-------------------------------------------|--------------|
| Web: empty blue void below grid   | viewport mode + hardcoded worldmap        | `project.godot` + `world_map.gd` |
| Web: game is a sad little postage stamp | canvas_resize_policy = 0                 | `export_presets.cfg` |
| Web: massive black bars           | Window overrides fighting DPR             | Remove the overrides |
| Android: UI gets nommed by corners| SAFE_EDGE not applied to new element      | `hud.gd` |
| Desktop: black bars everywhere    | Someone set aspect to "keep"              | Check `project.godot` immediately |

---

**Final Note:** If the screen layout breaks again, the correct first step is to make a very strong coffee and whisper “I chose this career” to myself. Then check the feature tag overrides.

See you next time the industry decides to invent new ways to torment solo devs.