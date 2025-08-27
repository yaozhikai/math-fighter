#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Boxing Math Game v2 — Two-Digit Subtraction with Borrowing

Updates in this version:
- If attack <= defense: auto "Avoid!" or "Perfect Defense!" (random) and skip math, next round.
- Attacks now use randomized names and damage range 11–49 (integers).
- Defense roll (0–50) is *biased toward lower values* to reduce perfect dodges; high defense is rarer.
- Math prompts are engineered to more often require BORROWING in the tens place.
  We ensure at least one of:
    (attack % 10) < (defense % 10)  -> borrow in "actual damage" calc
    (life_before % 10) < (actual_damage % 10) -> borrow in "remaining life" calc
  If not satisfied, we reroll a limited number of times to seek a borrow-friendly case.
"""

import random
from typing import Tuple, List

# --- Configurable ranges ---
ATTACK_RANGE = (11, 49)      # inclusive
DEFENSE_RANGE = (0, 50)      # inclusive; distribution is weighted toward low values
LIFE_RANGE = (80, 120)       # inclusive
MAX_ATTEMPTS = 3
MAX_REROLLS_FOR_BORROW = 12  # attempt up to 12 times to get a borrow scenario

# Cool attack names (randomly chosen each turn)
ATTACK_NAMES: List[str] = [
    "Comet Cross", "Dragon Hook", "Phantom Jab", "Thunder Uppercut", "Shadow Step",
    "Cyclone Smash", "Blazing Elbow", "Nebula Feint", "Meteor Rush", "Vortex Swing",
    "Falcon Strike", "Aurora Burst", "Riptide Punch", "Sonic Boom", "Iron Hammer"
]


def weighted_defense_roll(low: int, high: int) -> int:
    """
    Roll defense in [low, high] with decreasing probability for larger values.
    Weights proportional to (high + 1 - d)^2 so higher defense is rarer.
    """
    values = list(range(low, high + 1))
    # Weight high numbers less: weight(d) = (high+1 - d)^2
    weights = [(high + 1 - d) ** 2 for d in values]
    return random.choices(values, weights=weights, k=1)[0]


def ask_int_with_attempts(prompt: str, correct_value: int, max_attempts: int = MAX_ATTEMPTS) -> None:
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
            print(f"❌ Please enter a whole number. Attempts left: {max_attempts - attempts}")
            continue

        if val == correct_value:
            print("✅ Correct!")
            return
        else:
            attempts += 1
            hint = ""
            if attempts < max_attempts:
                hint = " (too high)" if val > correct_value else " (too low)"
            print(f"❌ Not quite{hint}. Attempts left: {max_attempts - attempts}")
    print(f"📘 The correct answer is: {correct_value}\n")


def roll_attack() -> Tuple[str, int]:
    """Return (attack_name, base_damage)."""
    name = random.choice(ATTACK_NAMES)
    dmg = random.randint(*ATTACK_RANGE)
    return name, dmg


def roll_defense() -> int:
    """Defense is 0–50 but *biased* to be smaller numbers on average."""
    return weighted_defense_roll(*DEFENSE_RANGE)


def ensure_borrow_case(base: int, defense: int, life_before: int) -> Tuple[int, int]:
    """
    Try to make at least one subtraction require borrowing in the ones place:
      A) actual_damage = base - defense, want base%10 < defense%10 (when base > defense)
      B) remaining = life_before - actual_damage, want life_before%10 < actual_damage%10
    We'll reroll base/defense pairs a few times to find a borrow case, unless base<=defense.
    """
    if base <= defense:
        return base, defense  # no need, will be auto-avoid

    for _ in range(MAX_REROLLS_FOR_BORROW):
        # If either subtraction causes a borrow, accept it
        actual_damage = base - defense
        if (base % 10) < (defense % 10) or (life_before % 10) < (actual_damage % 10):
            return base, defense
        # Otherwise try a small tweak: reroll either base or defense (biased defense again)
        # Randomly decide which to reroll for variety
        if random.random() < 0.5:
            base = random.randint(*ATTACK_RANGE)
        else:
            defense = roll_defense()

        if base <= defense:
            return base, defense  # will be auto-avoid; acceptable

    return base, defense  # fall back if we couldn't force a borrow case


def prompt_enter(msg: str = "Press Enter to continue...") -> None:
    input(msg)


def print_status(p1_name: str, p1_hp: int, p2_name: str, p2_hp: int) -> None:
    print(f"🔹 {p1_name}: {p1_hp} HP | 🔸 {p2_name}: {p2_hp} HP\n")


def main():
    print("🥊 Boxing Math Game — Two-Digit Subtraction (with Borrowing) v2\n")
    print("Type 'quit' or 'exit' at any input to end the game.\n")

    user1 = input("Enter Player 1 name: ").strip() or "Player 1"
    user2 = input("Enter Player 2 name: ").strip() or "Player 2"

    # Random life points
    p1_hp = random.randint(*LIFE_RANGE)
    p2_hp = random.randint(*LIFE_RANGE)

    print(f"\n{user1} and {user2} step into the ring!")
    print(f"{user1} starts with {p1_hp} HP.")
    print(f"{user2} starts with {p2_hp} HP.\n")

    attacker, defender = (user1, user2)
    round_no = 1

    while p1_hp > 0 and p2_hp > 0:
        print(f"===== 🏁 Round {round_no} =====")
        print_status(user1, p1_hp, user2, p2_hp)

        # Snapshot defender HP for math prompt
        life_before = p1_hp if defender == user1 else p2_hp

        # Roll attack + defense with borrowing preference
        atk_name, base_dmg = roll_attack()
        defense = roll_defense()
        base_dmg, defense = ensure_borrow_case(base_dmg, defense, life_before)

        # Announce attack & defense
        print(f"💥 {attacker} uses {atk_name}! Base damage roll: {base_dmg}")
        prompt_enter(f"🛡️  {defender}, press Enter to roll your defense (0–50, high values rarer)...")
        print(f"🛡️  {defender} defense roll: {defense}")

        # Auto-avoid if defense >= attack
        if defense >= base_dmg:
            print(random.choice(["✨ Avoid!", "🛡️  Perfect Defense!", "💫 Slick Dodge!", "🌀 Clean Evade!"]))
            # Switch turns
            attacker, defender = defender, attacker
            round_no += 1
            print()
            continue

        # Compute actual damage
        actual_damage = base_dmg - defense
        # Ask math questions (with borrowing preference fulfilled when possible)
        ask_int_with_attempts(
            prompt=f"❓ What is the ACTUAL damage? (base {base_dmg} - defense {defense}, not below 0): ",
            correct_value=actual_damage,
        )

        expected_remaining = max(0, life_before - actual_damage)
        ask_int_with_attempts(
            prompt=f"❓ What is {defender}'s REMAINING life? ({life_before} - {actual_damage}, not below 0): ",
            correct_value=expected_remaining,
        )

        # Apply damage
        if defender == user1:
            p1_hp = expected_remaining
        else:
            p2_hp = expected_remaining

        print(f"📣 {attacker} hit {defender} for {actual_damage}. {defender} now has {expected_remaining} HP.\n")

        # Check end condition
        if p1_hp <= 0 or p2_hp <= 0:
            break

        # Swap roles
        attacker, defender = defender, attacker
        round_no += 1

    # Game over
    print("===== 🏁 Match Over =====")
    if p1_hp <= 0 and p2_hp <= 0:
        print("It's a draw! Both boxers are down!")
    elif p1_hp <= 0:
        print(f"🏆 Winner: {user2}! {user1} has been defeated.")
    else:
        print(f"🏆 Winner: {user1}! {user2} has been defeated.")
    print("\nThanks for playing! Keep practicing those subtraction skills!")

if __name__ == "__main__":
    main()