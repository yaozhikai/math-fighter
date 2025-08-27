# Boxing Math Game 🎲🥊

A fun **two-player subtraction practice game** wrapped in a boxing theme.
Built in Python, this game makes **two-digit subtraction with borrowing** exciting and interactive — perfect for kids learning math in a playful way.

---

## ✨ Features

* **Two-player mode**: enter short names (max 3 characters each).
* **Boxing mechanics**:

  * Each round, the attacker rolls a named attack (damage **11–49**).
  * Defender rolls defense (**0–50**, weighted toward smaller numbers).
  * Attacks always resolve (no pure “auto-dodge” rounds).
* **Math challenges each turn**:

  1. Calculate **actual damage** = attack – defense
  2. Calculate **remaining HP** = defender’s HP – damage

  * Up to 3 attempts; hints if too high/low; correct answer shown after.
* **Borrowing focus**: subtraction problems are designed to often require borrowing in the ones place.
* **Adaptive difficulty**:

  * Tracks player accuracy.
  * Difficulty level (1–5) adjusts dynamically: higher levels increase borrowing cases and tougher gaps.
* **Rounds & winner**:

  * Default: **8 rounds** (can be changed with `--rounds`).
  * Winner decided by KO or by comparing HP at the end.
* **Colorful output with emojis** for fun and clarity (disable with `--no-color`).

---

## 🚀 Installation

Clone this repo:

```bash
git clone https://github.com/yaozhikai/math-fighter.git
cd math-fighter
```

Run with Python 3.8+:

```bash
python math_fighter.py
```

---

## ⚙️ Command-Line Options

| Option       | Description                           |
| ------------ | ------------------------------------- |
| `--rounds N` | Max number of rounds (default: 8).    |
| `--seed S`   | Set RNG seed (for reproducible runs). |
| `--no-color` | Disable colored output and emojis.    |

---

## 🎮 Example Play

```text
🥊 Boxing Math Game — Two-Digit Subtraction (Borrowing) v3
Type 'quit' or 'exit' at any input to end the game.

Enter Player 1 name (max 3 chars): Kai
Enter Player 2 name (max 3 chars): Vik

Kai and Vik step into the ring!
Kai starts with 108 HP.
Vik starts with 97 HP.

===== 🏁 Round 1 / 5 =====
🔹 Kai: 108 HP | 🔸 Vik: 97 HP

💥 Kai uses Meteor Rush! Base damage roll: 34
🛡️  Vik, press Enter to roll your defense...
🛡️  Vik defense roll: 21

❓ What is the ACTUAL damage? (base 34 - defense 21): 
```

---

## 📜 License

MIT License — free to fork, adapt, and use for your own math practice or teaching projects.

---

👉 This version is **simpler, more accurate, and child-friendly**, while still showing off your adaptive difficulty and boxing theme.