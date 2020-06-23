#!/usr/bin/env python3
import collections
import random
import re

ITERATIONS = 100000

DECKLIST = """
2 Bloodstained Mire
1 Fiery Islet
4 Inspiring Vantage
3 Mountain
2 Sacred Foundry
4 Sunbaked Canyon
4 Wooded Foothills
4 Boros Charm
4 Chandra's Incinerator
4 Eidolon of the Great Revel
4 Goblin Guide
4 Lava Spike
4 Lightning Bolt
2 Lightning Helix
4 Rift Bolt
4 Seal of Fire
4 Skewer the Critics
2 Skullcrack
"""

LANDS = set([
    'Bloodstained Mire',
    'Fiery Islet',
    'Inspiring Vantage',
    'Mountain',
    'Sacred Foundry',
    'Sunbaked Canyon',
    'Wooded Foothills',
])

ONE_CMC = set([
    'Goblin Guide',
    'Lava Spike',
    'Lightning Bolt',
    'Rift Bolt',
    'Seal of Fire',
    'Skewer the Critics',
])
NO_DELAY_BURN = ONE_CMC - set(['Goblin Guide', 'Rift Bolt'])

deck = []
for line in DECKLIST.splitlines():
    line = line.strip()
    if not line: continue
    match = re.search(r'(\d) (.+)', line)
    n_card, card_name = match.group(1), match.group(2)
    deck.extend([card_name for n in range(int(n_card))])
#print("deck =", deck)
random.shuffle(deck)
print("len(deck) =", len(deck))
print("sample_hand =", deck[:7])

n_7_card_hand = 0
n_6_card_hand = 0

n_t1_creature_hand = 0
n_t1_delayed_spell_hand = 0
n_t2_incinerator_hand = 0
n_t3_incinerator_hand = 0

def UpdateStats(deck):
    global n_t1_creature_hand
    global n_t1_delayed_spell_hand, n_t2_incinerator_hand, n_t3_incinerator_hand

    t1_hand = deck[:7]
    if 'Goblin Guide' in t1_hand:
        n_t1_creature_hand += 1

    t2_hand = deck[:8]
    t2_n_lands = sum(c in LANDS for c in t2_hand)
    t3_hand = deck[:9]
    t3_n_lands = sum(c in LANDS for c in t3_hand)

    # Assuming we play optimally to cast incinerator
    needed_spells = None
    if 'Rift Bolt' in t1_hand:
        n_t1_delayed_spell_hand += 1
        needed_spells = NO_DELAY_BURN
    elif 'Seal of Fire' in t1_hand:
        n_t1_delayed_spell_hand += 1
        needed_spells = (
            ONE_CMC - set(['Goblin Guide', 'Rift Bolt', 'Seal of Fire']))
    if ("Chandra's Incinerator" in t2_hand and
        needed_spells and
        sum(c in needed_spells for c in t2_hand) > 0 and
        t2_n_lands > 1):
        n_t2_incinerator_hand += 1
    else:
        if 'Rift Bolt' in t2_hand:
            needed_spells = NO_DELAY_BURN
        elif 'Seal of Fire' in t2_hand:
            needed_spells = (
                ONE_CMC - set(['Goblin Guide', 'Rift Bolt', 'Seal of Fire']))
        if ("Chandra's Incinerator" in t3_hand and
            ((needed_spells and
              sum(c in needed_spells for c in t3_hand) > 0 and
              t3_n_lands > 1) or
             (sum(c in NO_DELAY_BURN for c in t3_hand) > 1 and
              sum(c in NO_DELAY_BURN for c in t3_hand) != sum(c == 'Skewer the Critics' for c in t3_hand) and
              sum(c in NO_DELAY_BURN for c in t3_hand) != sum(c == 'Seal of Fire' for c in t3_hand) and
              t3_n_lands > 2))):
            n_t3_incinerator_hand += 1

# Assuming we always go first
print("iterations = ", ITERATIONS)
for n in range(ITERATIONS):
    random.shuffle(deck)
    hand = deck[:7]
    n_lands = sum(c in LANDS for c in hand)
    n_one_cmc = sum(c in ONE_CMC for c in hand)

    # Mulligan
    if (n_lands == 0 or
        n_one_cmc == 0 or
        n_one_cmc == 1 and 'Skewer the Critics' in hand or
        n_lands == 1 and n_one_cmc < 4 or
        n_lands > 3):
        random.shuffle(deck)
        hand = deck[:7]
        n_lands = sum(c in LANDS for c in hand)
        n_one_cmc = sum(c in ONE_CMC for c in hand)

        # Mulligan
        if (n_lands == 0 or
            n_one_cmc == 0 or
            n_one_cmc == 1 and 'Skewer the Critics' in hand or
            n_lands == 1 and n_one_cmc < 3 or
            n_lands > 3):
            pass
        else:
            n_6_card_hand += 1
            UpdateStats(deck)
    else:
        n_7_card_hand += 1
        UpdateStats(deck)

print("P(7_card) =", n_7_card_hand / ITERATIONS)
print("P(6_card) =", n_6_card_hand / ITERATIONS)
n_7_6_card_hand = n_7_card_hand + n_6_card_hand
print("P(7_6_card) =", n_7_6_card_hand / ITERATIONS)
print("P(turn_1_creature|7_6_card) =", n_t1_creature_hand /  n_7_6_card_hand)
print("P(turn_1_delayed_spell|7_6_card) =", n_t1_delayed_spell_hand /  n_7_6_card_hand)
print("P(turn_2_incinerator|7_6_card) =", n_t2_incinerator_hand / n_7_6_card_hand)
print("P(turn_3_incinerator|7_6_card) =", n_t3_incinerator_hand / n_7_6_card_hand)
