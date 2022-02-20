from ps1a import *

#
# test code
#

def test_load_cows():
    """
    Unit test for load_cows
    """
    failure = False
    data_1 ={
        'Maggie':3,
        'Herman':7,
        'Betsy':9,
        'Oreo':6,
        'Moo Moo':3,
        'Milkshake':2,
        'Millie':5,
        'Lola':2,
        'Florence':2,
        'Henrietta':9
    }
    data_2 ={
        'Miss Moo-dy':3,
        'Milkshake':4,
        'Lotus':10,
        'Miss Bella':2,
        'Horns':9,
        'Betsy':5,
        'Rose':3,
        'Dottie':6
    }
    if data_1 != load_cows('ps1_cow_data.txt'):
        print("FAILURE: load_cows()")
        print("Data Set 1 Failed")
        failure = True
    if data_2 != load_cows('ps1_cow_data_2.txt'):
        if failure == True:
            print("Data Set 2 Failed")
        else:
            print("FAILURE: load_cows()")
            print("Data Set 2 Failed")
        failure = True
    if not failure:
        print("SUCCESS: load_cows()")

def test_greedy_cow_transport():
    """
    Unit test for greedy_cow_transport()
    """
    failure = False
    data_1 = [
        ['Betsy'],
        ['Henrietta'],
        ['Herman', 'Maggie'],
        ['Oreo','Moo Moo'],
        ['Millie', 'Milkshake', 'Lola'],
        ['Florence']
    ]
    data_2 = [
        ['Lotus'],
        ['Horns'],
        ['Dottie', 'Milkshake'],
        ['Betsy', 'Miss Moo-dy', 'Miss Bella'],
        ['Rose']
    ]
    if data_1 != greedy_cow_transport(load_cows('ps1_cow_data.txt')):
        print("FAILURE: greedy_cow_transport()")
        print("Data Set 1 Failed")
        failure = True
    if data_2 != greedy_cow_transport(load_cows('ps1_cow_data_2.txt')):
        if failure == True:
            print("Data Set 2 Failed")
        else:
            print("FAILURE: greedy_cow_transport()")
            print("Data Set 2 Failed")
        failure = True
    if not failure:
        print("SUCCESS: greedy_cow_transport()")

test_load_cows()
test_greedy_cow_transport()