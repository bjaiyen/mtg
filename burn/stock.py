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
4 Eidolon of the Great Revel
4 Goblin Guide
4 Lava Spike
4 Lightning Bolt
2 Lightning Helix
4 Monastery Swiftspear
4 Rift Bolt
4 Searing Blaze
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

HORIZON_LANDS= set([
    'Fiery Islet',
    'Sunbaked Canyon',
])

ONE_CMC = set([
    'Goblin Guide',
    'Lava Spike',
    'Lightning Bolt',
    'Monastery Swiftspear',
    'Rift Bolt',
    'Skewer the Critics',
])

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
n_1_land_hand = 0
n_t1_creature_hand = 0
n_all_horizon_lands_hand = 0
n_1_land_hand_next_land_t = collections.defaultdict(int)
# Assuming we always go first.
print("iterations = ", ITERATIONS)
for n in range(ITERATIONS):
    random.shuffle(deck)
    hand = deck[:7]
    n_lands = sum(c in LANDS for c in hand)
    n_horizon_lands = sum(c in HORIZON_LANDS for c in hand)
    n_one_cmc = sum(c in ONE_CMC for c in hand)
    # Mulligan 7 card hand if no lands, no 1 cmc cards, 1 land and fewer than 4
    # 1 cmc cards, or 4 or more lands.
    if (n_lands == 0 or
        n_one_cmc == 0 or
        n_one_cmc == 1 and 'Skewer the Critics' in hand or
        n_lands == 1 and n_one_cmc < 4 or
        n_lands > 3):
        random.shuffle(deck)
        hand = deck[:7]
        n_lands = sum(c in LANDS for c in hand)
        n_horizon_lands = sum(c in HORIZON_LANDS for c in hand)
        n_one_cmc = sum(c in ONE_CMC for c in hand)
        # Mulligan 6 card hand if no lands, no 1 cmc cards, 1 land and fewer
        # than 3 1 cmc cards, or 4 or more lands.
        if (n_lands == 0 or
            n_one_cmc == 0 or
            n_one_cmc == 1 and 'Skewer the Critics' in hand or
            n_lands == 1 and n_one_cmc < 3 or
            n_lands > 3):
            pass
        else:
            n_6_card_hand += 1
            if n_lands == n_horizon_lands:
                n_all_horizon_lands_hand += 1
            if 'Goblin Guide' in hand or 'Monastery Swiftspear' in hand:
                n_t1_creature_hand += 1
            if n_lands ==1:
                n_1_land_hand += 1
                for t in range(3):
                    if deck[7+t] in LANDS:
                        n_1_land_hand_next_land_t[t] += 1
                        break
    else:
        n_7_card_hand += 1
        if n_lands == n_horizon_lands:
            n_all_horizon_lands_hand += 1
        if 'Goblin Guide' in hand or 'Monastery Swiftspear' in hand:
            n_t1_creature_hand += 1
        if n_lands == 1:
            n_1_land_hand += 1
            for t in range(3):
                if deck[7+t] in LANDS:
                    n_1_land_hand_next_land_t[t] += 1
                    break

print("P(7_card) =", n_7_card_hand / ITERATIONS)
print("P(6_card) =", n_6_card_hand / ITERATIONS)
n_7_6_card_hands = n_7_card_hand + n_6_card_hand
print("P(all_horizon_lands|7_6_card) =", n_all_horizon_lands_hand / n_7_6_card_hands)
print("P(turn_1_creature|7_6_card) =", n_t1_creature_hand /  n_7_6_card_hands)
print("P(1_land|7_6_card_hand) =", n_1_land_hand / n_7_6_card_hands)
print("P(next_land_t2|7_6_card,1_land) =", n_1_land_hand_next_land_t[0] / n_1_land_hand)
print("P(next_land_t3|7_6_card,1_land) =", n_1_land_hand_next_land_t[1] / n_1_land_hand)
print("P(next_land_t4|7_6_card,1_land) =", n_1_land_hand_next_land_t[2] / n_1_land_hand)
