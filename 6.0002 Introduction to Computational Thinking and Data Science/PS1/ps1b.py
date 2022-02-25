###########################
# 6.0002 Problem Set 1b: Space Change
# Name: Matt Rieke
# Collaborators: None
# Time Start: 2022-02-24 03:52 UTC
# Time End: 2022-02-24 05:02 UTC
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    if target_weight in memo:
        return memo[target_weight]
    if target_weight == 0:
        return 0
    elif target_weight == 1:
        return 1
    for egg in egg_weights:
        if egg <= target_weight:
            result = 1 + dp_make_weight(egg_weights, (target_weight - egg), memo)
    memo[target_weight] = result
    return result

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()