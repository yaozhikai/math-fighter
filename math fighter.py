#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Boxing Math Game v3 — Two-Digit Subtraction with Borrowing + Round Limit

Key Features
------------
- Two players enter names; each starts with random HP in [80, 120].
- Each round, attacker uses a RANDOM-NAMED attack with base damage in [11, 49].
- Defender "rolls" defense in [0, 50] with a bias toward smaller numbers (big defenses are rarer).
- If defense >= attack: auto "Avoid!" / "Perfect Defense!" (skip math) and go to the next round.
- Otherwise, player answers two subtraction prompts:
    1) Actual damage = max(0, base - defense)
    2) Remaining HP = max(0, life_before - actual_damage)
  * You get up to 3 tries; then the correct answer is revealed.
- Borrowing Focus: the program tries to generate problems that require borrowing
  in the ones place for at least one of the subtractions (within a capped number of rerolls).
- Round Limit: stop after MAX_ROUNDS if no knockout; decide winner by remaining HP
  (optional sudden-death tiebreaker).

CLI Options
-----------
--rounds N             : max rounds (default: 12)
--no-sudden-death      : disable sudden-death on tie after max rounds
--seed S               : set random seed for reproducible gameplay
--no-color             : disable ANSI colors/emojis (plain text)
"""

import argparse
import random
import sys
from typing import Tuple, List

# -------------------- Config Defaults --------------------

ATTACK_RANGE = (11, 49)      # inclusive
DEFENSE_RANGE = (0, 50)      # inclusive
LIFE_RANGE = (80, 120)       # inclusive
MAX_ATTEMPTS = 3
MAX_REROLLS_FOR_BORROW = 12  # attempts to create a borrow-friendly subtraction

ATTACK_NAMES: List[str] = [
    "Comet Cross", "Dragon Hook", "Phantom Jab", "Thunder Uppercut", "Shadow Step",
    "Cyclone Smash", "Blazing Elbow", "Nebula Feint", "Meteor Rush", "Vortex Swing",
    "Falcon Strike", "Aurora Burst", "Riptide Punch", "Sonic Boom", "Iron Hammer",
    "Starlight Flicker", "Quasar Cut", "Tempest Knuckle", "Glacier Chop", "Solar Slam"
]

# -------------------- Coloring Helpers --------------------

class Style:
    def __init__(self, enable: bool):
        self.enable = enable
        self.reset = "\033[0m" if enable else ""
        self.bold = "\033[1m" if enable else ""
        self.green = "\033[32m" if enable else ""
        self.red = "\033[31m" if enable else ""
        self.yellow = "\033[33m" if enable else ""
        self.blue = "\033[34m" if enable else ""

    def wrap(self, text: str, color: str) -> str:
        if not self.enable:
            return text
        return f"{color}{text}{self.reset}"

# -------------------- Core Mechanics --------------------

def weighted_defense_roll(low: int, high: int) -> int:
    """
    Roll defense with decreasing probability for larger values.
    weight(d) = (high + 1 - d)^2  -> high defense is rarer.
    """
    values = list(range(low, high + 1))
    weights = [(high + 1 - d) ** 2 for d in values]
    return random.choices(values, weights=weights, k=1)[0]


def ask_int_with_attempts(prompt: str, correct_value: int, max_attempts: int, style: Style) -> None:
    attempts = 0
    while attempts < max_attempts:
        raw = input(prompt).strip()
        if raw.lower() in {"quit", "exit"}:
            print("Exiting game. Bye!")
            raise SystemExit(0)
        try:
            val = int(raw)
        except ValueError:
            attempts += 1
            print(style.wrap(f"❌ Please enter a whole number. Attempts left: {max_attempts - attempts}", style.red))
            continue

        if val == correct_value:
            print(style.wrap("✅ Correct!", style.green))
            return
        else:
            attempts += 1
            hint = ""
            if attempts < max_attempts:
                hint = " (too high)" if val > correct_value else " (too low)"
            print(style.wrap(f"❌ Not quite{hint}. Attempts left: {max_attempts - attempts}", style.yellow))
    print(style.wrap(f"📘 The correct answer is: {correct_value}\n", style.blue))


def roll_attack() -> Tuple[str, int]:
    name = random.choice(ATTACK_NAMES)
    dmg = random.randint(*ATTACK_RANGE)
    return name, dmg


def roll_defense() -> int:
    return weighted_defense_roll(*DEFENSE_RANGE)


def ensure_borrow_case(base: int, defense: int, life_before: int) -> Tuple[int, int]:
    """
    Encourage at least one borrowing scenario in the ones place:
      A) base%10 < defense%10  (for base > defense)
      B) life_before%10 < (base - defense)%10
    We attempt rerolls a few times unless base <= defense (which will auto-avoid).
    """
    if base <= defense:
        return base, defense

    for _ in range(MAX_REROLLS_FOR_BORROW):
        actual_damage = base - defense
        # If either subtraction forces a borrow, accept
        if (base % 10) < (defense % 10) or (life_before % 10) < (actual_damage % 10):
            return base, defense

        # Otherwise adjust; randomly reroll base or defense
        if random.random() < 0.5:
            base = random.randint(*ATTACK_RANGE)
        else:
            defense = roll_defense()

        if base <= defense:
            return base, defense
    return base, defense


def prompt_enter(msg: str = "Press Enter to continue...") -> None:
    input(msg)


def print_status(p1_name: str, p1_hp: int, p2_name: str, p2_hp: int, style: Style) -> None:
    print(f"{style.wrap('🔹 ' + p1_name + f': {p1_hp} HP', style.blue)} | "
          f"{style.wrap('🔸 ' + p2_name + f': {p2_hp} HP', style.yellow)}\n")


# -------------------- Game Loop --------------------

def play_game(max_rounds: int, sudden_death: bool, style: Style) -> None:
    print(style.wrap("🥊 Boxing Math Game — Two-Digit Subtraction (Borrowing) v3", style.bold))
    print("Type 'quit' or 'exit' at any input to end the game.\n")

    user1 = input("Enter Player 1 name: ").strip() or "Player 1"
    user2 = input("Enter Player 2 name: ").strip() or "Player 2"

    p1_hp = random.randint(*LIFE_RANGE)
    p2_hp = random.randint(*LIFE_RANGE)

    print(f"\n{user1} and {user2} step into the ring!")
    print(f"{user1} starts with {p1_hp} HP.")
    print(f"{user2} starts with {p2_hp} HP.\n")

    attacker, defender = user1, user2
    round_no = 1

    while p1_hp > 0 and p2_hp > 0 and round_no <= max_rounds:
        print(style.wrap(f"===== 🏁 Round {round_no} / {max_rounds} =====", style.bold))
        print_status(user1, p1_hp, user2, p2_hp, style)

        life_before = p1_hp if defender == user1 else p2_hp

        atk_name, base_dmg = roll_attack()
        defense = roll_defense()
        base_dmg, defense = ensure_borrow_case(base_dmg, defense, life_before)

        print(f"💥 {attacker} uses {atk_name}! Base damage roll: {base_dmg}")
        prompt_enter(f"🛡️  {defender}, press Enter to roll your defense (0–50; big numbers rarer)...")
        print(f"🛡️  {defender} defense roll: {defense}")

        if defense >= base_dmg:
            print(random.choice([
                style.wrap("✨ Avoid!", style.green),
                style.wrap("🛡️  Perfect Defense!", style.green),
                style.wrap("💫 Slick Dodge!", style.green),
                style.wrap("🌀 Clean Evade!", style.green),
            ]))
            attacker, defender = defender, attacker
            round_no += 1
            print()
            continue

        actual_damage = base_dmg - defense

        ask_int_with_attempts(
            prompt=f"❓ What is the ACTUAL damage? (base {base_dmg} - defense {defense}, not below 0): ",
            correct_value=actual_damage,
            max_attempts=MAX_ATTEMPTS,
            style=style,
        )

        expected_remaining = max(0, life_before - actual_damage)
        ask_int_with_attempts(
            prompt=f"❓ What is {defender}'s REMAINING life? ({life_before} - {actual_damage}, not below 0): ",
            correct_value=expected_remaining,
            max_attempts=MAX_ATTEMPTS,
            style=style,
        )

        if defender == user1:
            p1_hp = expected_remaining
        else:
            p2_hp = expected_remaining

        print(style.wrap(f"📣 {attacker} hit {defender} for {actual_damage}. {defender} now has {expected_remaining} HP.\n", style.blue))

        if p1_hp <= 0 or p2_hp <= 0:
            break

        attacker, defender = defender, attacker
        round_no += 1

    print(style.wrap("===== 🏁 Match Over =====", style.bold))
    if p1_hp <= 0 and p2_hp <= 0:
        print("It's a draw! Both boxers are down!")
        return
    elif p1_hp <= 0:
        print(f"🏆 Winner: {user2}! {user1} has been defeated.")
        return
    elif p2_hp <= 0:
        print(f"🏆 Winner: {user1}! {user2} has been defeated.")
        return

    # Judges' decision if we hit the round limit without KO
    print(style.wrap("🧑‍⚖️ Time! Going to the judges' decision...", style.bold))
    print(f"Final HP — {user1}: {p1_hp}  |  {user2}: {p2_hp}")
    if p1_hp > p2_hp:
        print(f"🏆 Winner by decision: {user1}!")
        return
    elif p2_hp > p1_hp:
        print(f"🏆 Winner by decision: {user2}!")
        return

    # Tie -> optional sudden death
    if sudden_death:
        print(style.wrap("⚖️ It's a tie! Entering SUDDEN DEATH: first damaging hit wins...", style.bold))
        # single sudden death attempt
        life_before = p1_hp if defender == user1 else p2_hp
        atk_name, base_dmg = roll_attack()
        defense = roll_defense()
        base_dmg, defense = ensure_borrow_case(base_dmg, defense, life_before)

        print(f"💥 {attacker} uses {atk_name}! Base damage roll: {base_dmg}")
        prompt_enter(f"🛡️  {defender}, press Enter to roll your defense (0–50; big numbers rarer)...")
        print(f"🛡️  {defender} defense roll: {defense}")

        if defense >= base_dmg:
            print(style.wrap("✨ Avoid! Still a tie. Declaring a draw.", style.yellow))
            print("Result: Draw.")
            return

        actual_damage = base_dmg - defense
        if defender == user1:
            p1_hp = max(0, p1_hp - actual_damage)
        else:
            p2_hp = max(0, p2_hp - actual_damage)

        if p1_hp <= 0 or p2_hp <= 0:
            winner = user2 if p1_hp <= 0 else user1
            print(f"🏆 Sudden-death winner: {winner}!")
        else:
            if p1_hp > p2_hp:
                print(f"🏆 Sudden-death decision: {user1}!")
            elif p2_hp > p1_hp:
                print(f"🏆 Sudden-death decision: {user2}!")
            else:
                print("Result: Draw.")
    else:
        print("Result: Draw.")

# -------------------- Entrypoint --------------------

def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Boxing Math Game v3 — subtraction practice")
    p.add_argument("--rounds", type=int, default=12, help="Max rounds (default: 12)")
    p.add_argument("--no-sudden-death", action="store_true", help="Disable sudden-death on tie after max rounds")
    p.add_argument("--seed", type=int, default=None, help="Set RNG seed for reproducible runs")
    p.add_argument("--no-color", action="store_true", help="Disable colored output")
    return p.parse_args(argv)


def main():
    args = parse_args(sys.argv[1:])
    if args.seed is not None:
        random.seed(args.seed)

    style = Style(enable=not args.no_color)
    play_game(max_rounds=args.rounds, sudden_death=(not args.no_sudden_death), style=style)


if __name__ == "__main__":
    main()