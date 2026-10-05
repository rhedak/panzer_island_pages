---
title: Keyboard controls
description: Every keyboard shortcut in Panzer Island on desktop, from selecting units and stepping routes with the arrow keys to confirming popups, plus how to remap any key.
---

# Keyboard controls

On desktop, Panzer Island can be played almost entirely from the keyboard. This guide covers what each key does, how the arrow keys change meaning depending on what you are doing, and how to remap everything in the Options menu. Touch devices have no keyboard shortcuts, so none of this applies on Android.

Every shortcut does exactly what the matching on-screen button does. If a button is hidden or grayed out, its key does nothing. You cannot use a shortcut to do something the interface would not let you do with the mouse.

---

## Default keys

| Key | Action |
|---|---|
| **K** | Select Katyusha |
| **N** | Select Nadeshiko |
| **M** | Select Maria |
| **E** or **Enter** | Execute |
| **Q** | Add to queue |
| **C** | Cancel |
| **Z** | Undo (Easy difficulty) |
| **Backspace** | Remove the last queued action |
| **I** | Open unit details |
| **Arrow keys** | Step a route, browse, or page chapters (see below) |
| **Esc** | Pause menu |
| **F11** | Toggle fullscreen |

Esc, F11, and Enter are fixed. You cannot remap them, and you cannot assign them to another action.

---

## Planning a move with the keyboard

A full move can be done without touching the mouse.

1. Press **K**, **N**, or **M** to select a unit.
2. Press an arrow key to take the first step of the route. Each press moves the route one cell in that direction.
3. Keep pressing arrow keys to extend the route. The route preview updates after every step, so you can watch the predicted damage as you go.
4. Press **E** or **Enter** to execute the route.

To shorten a route, press the arrow key that points back at the previous cell. Stepping back onto the previous waypoint removes the last step. Stepping back off the first step clears the route and leaves the unit selected.

To attack, step the route into a cell that holds a drone. That drone becomes the attack target, the same way it does when you drag a path with the mouse.

Press **C** to cancel a route in progress. If you have a unit selected but have not started a route, **C** deselects it.

Press **I** with a unit selected to open its details panel.

![Route preview: cyan line shows the planned path, orange cells mark danger zones with predicted hit counts](guide_assets/scene_route_preview.png)

---

## The queue

The queue lets you plan actions for several units and run them in one go.

- **Q** adds the current route to the queue.
- **E** or **Enter** runs the queued actions. When a route is waiting for confirmation, **E** confirms that route first.
- **Backspace** removes the most recently queued action.
- **C** cancels the queue before it runs.
- With nothing selected, the **Left** and **Right** arrow keys browse through the queued actions, the same as the **<** and **>** buttons.

---

## Arrow keys by context

The arrow keys do different things depending on what is on screen.

| Situation | Left and Right | Up and Down |
|---|---|---|
| A unit is selected | Step the route one cell | Step the route one cell |
| Nothing selected, queue has actions | Browse queued actions | No effect |
| Undo browser is open | Step through checkpoints | No effect |
| World map | Previous and next chapter | Previous and next mode or difficulty |

On the world map, Left and Right page through chapters exactly like the chapter buttons, including the same locks. A chapter you have not unlocked stays out of reach. Up and Down move through the mode and difficulty selector one row at a time, skipping locked rows and stopping at the ends. Any confirmation dialog that clicking would show appears here too.

---

## Undo

Undo is available on Easy difficulty. See the [FAQ](../faq.md) for how checkpoints work.

1. Press **Z** to open the undo browser.
2. Press **Left** and **Right** to step through earlier checkpoints.
3. Press **Z** again, **E**, or **Enter** to rewind to the checkpoint you picked.
4. Press **C** to leave the browser without changing anything.

While the browser is open, these are the only keys that act. Unit selection and route keys wait until you leave it.

---

## Popups and dialogs

Popups take the same keys, so you can keep your hands on the keyboard.

- **E** or **Enter** presses the popup's OK, Yes, or Continue button.
- **C** closes the popup, the same as Esc. On a yes or no question, **C** answers No.

This covers tutorial popups, confirmation dialogs, level-up choices, memory fragments, and the stage and chapter result screens. Popups that offer several equal choices have no single OK button, so **E** does nothing there. When you type into a text field, such as your player name, the keys type normally and never trigger a shortcut.

---

## Remapping keys

1. Open **Options**.
2. Choose **Controls**.
3. Click the key button next to the action you want to change. It reads "Press a key...".
4. Press the new key.

A few rules apply.

- **Esc** cancels the capture without changing anything.
- **F11**, **Enter**, and modifier keys on their own (Shift, Ctrl, Alt, Meta, Caps Lock) cannot be assigned. The page tells you when a key is refused.
- If the key you press is already used by another action, the two actions **swap** keys. The page names the action that moved, so nothing is ever left without a key by accident.
- **Reset Keys to Defaults** restores every shortcut at once.

Your choices are saved with your other settings.

Keys are stored by physical position, not by the letter printed on the keycap. If you play on a QWERTZ or AZERTY keyboard, the defaults stay under the same fingers as on a QWERTY keyboard, and the Controls page shows the label from your own layout.

---

## Quick reference

1. **K**, **N**, **M** select a unit. **I** opens its details.
2. Arrow keys step the route. Step backward to undo a step.
3. **E** or **Enter** executes. **C** cancels. **Q** queues.
4. **Z** opens undo on Easy. Arrow keys browse. **Z** or **E** confirms.
5. **E** and **C** also answer popups.
6. Remap everything except Esc, F11, and Enter under **Controls** in Options.

---

## Other guides

**[Getting Started](index.md)**
The core ideas you need for Chapter 1: reactive movement, route previews, and spreading damage.

**[Advanced Tactics](advanced.md)**
Reading multi-step routes and planning actions across several units.

**[Challenge Mode](challenge-mode.md)**
A score-based replay of any cleared stage, where fast and precise input pays off.
