#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Boxing Math Game — Two-Digit Subtraction Practice

How it works
------------
- Two players enter their names. Each starts with random life between 80 and 120.
- On each turn, the attacker lands a RANDOM attack:
    * Heavy Punch: base damage 30–50
    * Light Punch: base damage 10–30
- The defender presses Enter to roll a RANDOM defense between 0–50
  (50 means a perfect dodge).
- The program asks the player to compute:
    1) Actual damage = max(0, base_damage - defense)
    2) Defender's remaining life = max(0, life_before - actual_damage)
- If the player answers incorrectly, they get up to 3 attempts.
  After 3 wrong attempts, the correct answer is displayed.
- The game ends when a player's life is 0 or below, and the winner is announced.
"""

import random
from typing import Tuple

HEAVY_RANGE = (30, 50)
LIGHT_RANGE = (10, 30)
DEFENSE_RANGE = (0, 50)
LIFE_RANGE = (80, 120)


def ask_int_with_attempts(prompt: str, correct_value: int, max_attempts: int = 3) -> None:
    """
    Ask the user to enter an integer answer up to `max_attempts` times.
    If they fail, display the correct answer.
    Returns None (we don't change game state based on user input — it's for practice).
    """
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
            print(f"❌ That wasn't a whole number. Attempts left: {max_attempts - attempts}")
            continue

        if val == correct_value:
            print("✅ Correct!")
            return
        else:
            attempts += 1
            hint = ""
            if attempts < max_attempts:
                # Offer a directional hint to support learning
                hint = " (too high)" if val > correct_value else " (too low)"
            print(f"❌ Not quite{hint}. Attempts left: {max_attempts - attempts}")
    # After max attempts, reveal the answer
    print(f"📘 The correct answer is: {correct_value}\n")


def roll_attack() -> Tuple[str, int]:
    """Randomly choose an attack type and roll its base damage."""
    attack_type = random.choice(["Heavy Punch", "Light Punch"])
    if attack_type == "Heavy Punch":
        dmg = random.randint(*HEAVY_RANGE)
    else:
        dmg = random.randint(*LIGHT_RANGE)
    return attack_type, dmg


def roll_defense() -> int:
    """Roll the defense value (0–50)."""
    return random.randint(*DEFENSE_RANGE)


def prompt_enter(msg: str = "Press Enter to continue...") -> None:
    input(msg)


def print_status(p1_name: str, p1_hp: int, p2_name: str, p2_hp: int) -> None:
    print(f"🔹 {p1_name}: {p1_hp} HP | 🔸 {p2_name}: {p2_hp} HP\n")


def main():
    print("🥊 Welcome to the Boxing Math Game (Two-Digit Subtraction Practice)!\n")
    print("Type 'quit' or 'exit' at any input to end the game.\n")

    # Get names
    user1 = input("Enter Player 1 name: ").strip() or "Player 1"
    user2 = input("Enter Player 2 name: ").strip() or "Player 2"

    # Random life points
    p1_hp = random.randint(*LIFE_RANGE)
    p2_hp = random.randint(*LIFE_RANGE)

    print(f"\n{user1} and {user2} step into the ring!")
    print(f"{user1} starts with {p1_hp} HP.")
    print(f"{user2} starts with {p2_hp} HP.\n")

    attacker, defender = (user1, user2)
    attacker_hp, defender_hp = (p1_hp, p2_hp)

    round_no = 1
    while p1_hp > 0 and p2_hp > 0:
        print(f"===== 🏁 Round {round_no} =====")
        print_status(user1, p1_hp, user2, p2_hp)

        # Attacker's random attack
        atk_name, base_dmg = roll_attack()
        print(f"💥 {attacker} uses {atk_name}! Base damage roll: {base_dmg}")

        # Defender's defense roll (after pressing Enter)
        prompt_enter(f"🛡️  {defender}, press Enter to roll your defense (0–50)...")
        defense = roll_defense()
        print(f"🛡️  {defender} defense roll: {defense}")

        # Compute actual damage and ask the math questions
        actual_damage = max(0, base_dmg - defense)

        ask_int_with_attempts(
            prompt=f"❓ What is the ACTUAL damage? (base {base_dmg} - defense {defense}, not below 0): ",
            correct_value=actual_damage,
        )

        # Ask to compute the defender's remaining life (use their current HP snapshot)
        if defender == user1:
            life_before = p1_hp
        else:
            life_before = p2_hp

        expected_remaining = max(0, life_before - actual_damage)

        ask_int_with_attempts(
            prompt=f"❓ What is {defender}'s REMAINING life? ({life_before} - {actual_damage}, not below 0): ",
            correct_value=expected_remaining,
        )

        # Apply the damage
        if defender == user1:
            p1_hp = expected_remaining
        else:
            p2_hp = expected_remaining

        print(f"📣 {attacker} attacked {defender} for {actual_damage} damage. {defender} now has {expected_remaining} HP.\n")

        # Check end condition
        if p1_hp <= 0 or p2_hp <= 0:
            break

        # Swap roles
        attacker, defender = (defender, attacker)
        round_no += 1

    # Determine winner
    print("===== 🏁 Match Over =====")
    if p1_hp <= 0 and p2_hp <= 0:
        print("It's a draw! Both boxers are down!")
    elif p1_hp <= 0:
        print(f"🏆 Winner: {user2}! {user1} has been defeated.")
    else:
        print(f"🏆 Winner: {user1}! {user2} has been defeated.")

    print("\nThanks for playing! Keep practicing your subtraction!")

if __name__ == '__main__':
    main()