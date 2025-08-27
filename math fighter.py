#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Boxing Math Game v3 — Two-Digit Subtraction with Borrowing + Round Limit
(Updated: default 8 rounds, adaptive difficulty, no avoid rounds)
"""

import argparse
import random
import sys
from typing import Tuple, List

ATTACK_RANGE = (11, 49)
DEFENSE_RANGE = (0, 50)
LIFE_RANGE = (80, 120)
MAX_ATTEMPTS = 3
MAX_REROLLS_FOR_BORROW = 12

ATTACK_NAMES: List[str] = [
    "Comet Cross", "Dragon Hook", "Phantom Jab", "Thunder Uppercut", "Shadow Step",
    "Cyclone Smash", "Blazing Elbow", "Nebula Feint", "Meteor Rush", "Vortex Swing",
    "Falcon Strike", "Aurora Burst", "Riptide Punch", "Sonic Boom", "Iron Hammer",
    "Starlight Flicker", "Quasar Cut", "Tempest Knuckle", "Glacier Chop", "Solar Slam"
]

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

class Adaptive:
    def __init__(self):
        self.correct = 0
        self.total = 0

    def update(self, is_correct: bool) -> None:
        self.total += 1
        if is_correct:
            self.correct += 1

    @property
    def accuracy(self) -> float:
        return (self.correct / self.total) if self.total else 0.0

    @property
    def level(self) -> int:
        return max(1, min(5, 1 + int(self.accuracy * 4)))

ADAPT = Adaptive()

def weighted_defense_roll(low: int, high: int) -> int:
    values = list(range(low, high + 1))
    weights = [(high + 1 - d) ** 2 for d in values]
    return random.choices(values, weights=weights, k=1)[0]

def ask_int_with_attempts_bool(prompt: str, correct_value: int, max_attempts: int, style: Style) -> bool:
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
            return True
        else:
            attempts += 1
            hint = ""
            if attempts < max_attempts:
                hint = " (too high)" if val > correct_value else " (too low)"
            print(style.wrap(f"❌ Not quite{hint}. Attempts left: {max_attempts - attempts}", style.yellow))
    print(style.wrap(f"📘 The correct answer is: {correct_value}\n", style.blue))
    return False

def roll_attack() -> Tuple[str, int]:
    name = random.choice(ATTACK_NAMES)
    dmg = random.randint(*ATTACK_RANGE)
    return name, dmg

def roll_defense() -> int:
    return weighted_defense_roll(*DEFENSE_RANGE)

def force_borrow_pair(level: int) -> Tuple[int, int]:
    base_tens = random.randint(2, 9)
    gap = random.randint(1 + level, min(9, 2 + 2 * level))
    d_ones = random.randint(gap, 9)
    b_ones = d_ones - gap
    base = base_tens * 10 + b_ones
    d_tens = random.randint(0, base_tens)
    defense = d_tens * 10 + d_ones
    if base <= defense:
        base += 10
    if (base % 10) >= (defense % 10):
        defense = (defense // 10) * 10 + min(9, (base % 10) + 1)
    return base, defense

def ensure_borrow_case(base: int, defense: int, life_before: int) -> Tuple[int, int]:
    if base <= defense:
        return base, defense
    extra = (ADAPT.level - 1) * 4
    for _ in range(MAX_REROLLS_FOR_BORROW + extra):
        actual_damage = base - defense
        if (base % 10) < (defense % 10) or (life_before % 10) < (actual_damage % 10):
            return base, defense
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

def generate_pair(life_before: int) -> Tuple[str, int, int]:
    atk_name, base = roll_attack()
    defense = roll_defense()
    p_force = 0.25 + 0.15 * (ADAPT.level - 1)
    if random.random() < p_force:
        base, defense = force_borrow_pair(ADAPT.level)
    else:
        base, defense = ensure_borrow_case(base, defense, life_before)
    if defense >= base:
        base, defense = force_borrow_pair(ADAPT.level)
    return atk_name, base, defense

def play_game(max_rounds: int, style: Style) -> None:
    print(style.wrap("🥊 Boxing Math Game — Two-Digit Subtraction (Borrowing) v3", style.bold))
    print("Type 'quit' or 'exit' at any input to end the game.\n")

    user1 = input("Enter Player 1 name (max 3 chars): ").strip() or "P1"
    user2 = input("Enter Player 2 name (max 3 chars): ").strip() or "P2"
    user1 = user1[:3]
    user2 = user2[:3]

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
        atk_name, base_dmg, defense = generate_pair(life_before)

        print(f"💥 {attacker} uses {atk_name}! Base damage roll: {base_dmg}")
        prompt_enter(f"🛡️  {defender}, press Enter to roll your defense...")
        print(f"🛡️  {defender} defense roll: {defense}")

        actual_damage = base_dmg - defense

        ok1 = ask_int_with_attempts_bool(
            prompt=f"❓ What is the ACTUAL damage? (base {base_dmg} - defense {defense}): ",
            correct_value=actual_damage,
            max_attempts=MAX_ATTEMPTS,
            style=style,
        )
        ADAPT.update(ok1)

        expected_remaining = max(0, life_before - actual_damage)
        ok2 = ask_int_with_attempts_bool(
            prompt=f"❓ What is {defender}'s REMAINING life? ({life_before} - {actual_damage}): ",
            correct_value=expected_remaining,
            max_attempts=MAX_ATTEMPTS,
            style=style,
        )
        ADAPT.update(ok2)

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
    elif p1_hp <= 0:
        print(f"🏆 Winner: {user2}! {user1} has been defeated.")
    elif p2_hp <= 0:
        print(f"🏆 Winner: {user1}! {user2} has been defeated.")
    else:
        print(style.wrap("🧑‍⚖️ Time! Deciding by remaining life points...", style.bold))
        print(f"Final HP — {user1}: {p1_hp}  |  {user2}: {p2_hp}")
        if p1_hp > p2_hp:
            print(f"🏆 Winner: {user1}!")
        elif p2_hp > p1_hp:
            print(f"🏆 Winner: {user2}!")
        else:
            print("Result: Draw.")

def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Boxing Math Game v3 — subtraction practice (adaptive difficulty; judges by remaining HP)")
    p.add_argument("--rounds", type=int, default=8, help="Max rounds (default: 8)")
    p.add_argument("--seed", type=int, default=None, help="Set RNG seed for reproducible runs")
    p.add_argument("--no-color", action="store_true", help="Disable colored output")
    return p.parse_args(argv)

def main():
    args = parse_args(sys.argv[1:])
    if args.seed is not None:
        random.seed(args.seed)
    style = Style(enable=not args.no_color)
    play_game(max_rounds=args.rounds, style=style)

if __name__ == "__main__":
    main()