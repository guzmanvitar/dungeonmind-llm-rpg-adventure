"""Utily python functions for the project"""

import random


def weighted_random_stat():
    """Generate a random stat with weighted probabilities."""
    return random.choices([8, 9, 10, 11, 12], weights=[1, 2, 4, 2, 1])[0]
