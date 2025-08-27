# Boxing Math Game 🎲🥊

A fun **two-player subtraction game** with a boxing theme.  
Built in Python, this game helps practice **two-digit subtraction with borrowing** while simulating boxing rounds.

---

## Features

- **Two players**: enter your names (max 3 characters each).
- **Random boxing mechanics**:
  - Each round: attacker rolls a named attack (damage 11–49).
  - Defender rolls defense (0–50, biased toward smaller numbers).
  - If defense ≥ attack → auto dodge!
- **Math challenge**:
  - If not dodged, answer two subtraction problems:
    1. Actual damage = base – defense
    2. Remaining HP = defender’s HP – damage
  - Up to 3 tries each; correct answer revealed after.
- **Borrowing focus**: problems often require borrowing in ones place.
- **Adaptive difficulty**:
  - Tracks your answer accuracy.
  - Adjusts difficulty level (1–5).
  - Higher levels increase borrow probability and gap size.
- **Round limit & winner**:
  - Defaults to 12 rounds.
  - Winner decided by KO, HP left, or sudden-death tie-breaker.
- **Colored terminal output with emojis** (disable with `--no-color`).

---

## Installation

Clone this repo:
```bash
git clone https://github.com/yaozhikai/math-fighter.git
cd math-fighter
```

Run with Python 3.8+:

python math_fighter.py

Command Line Options
## Option	Description
--rounds N	Max number of rounds (default 12).
--no-sudden-death	Disable sudden-death tiebreaker.
--seed S	Set RNG seed (for reproducibility).
--no-color	Disable ANSI colors and emojis.
Example Play
python math_fighter.py --rounds 5 --seed 42


## Sample round:

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
🛡️  Vik, press Enter to roll your defense (0–50; big numbers rarer)...
🛡️  Vik defense roll: 21
❓ What is the ACTUAL damage? (base 34 - defense 21, not below 0):

## License

MIT License.
Feel free to fork and adapt for your own math practice!