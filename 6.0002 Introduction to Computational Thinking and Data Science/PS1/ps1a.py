###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: Matt Rieke
# Collaborators: None
# Time Start: 2022-02-20 01:26 UTC
# Time End: 2022-02-24 0 03:50 UTC


from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cow_dict = {}
    with open(filename) as f:
        for line in f:
            line = line.rstrip()
            comma_pos = line.find(',')
            cow_dict[line[0:comma_pos]] = int(line[comma_pos + 1:])
    return cow_dict

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    working_dict = cows.copy()
    trips = []
    while len(working_dict) > 0:
        trip_result = greedy_build_trip(working_dict, limit)
        trips.append(trip_result[0])
        working_dict = trip_result[1]
    return trips

def greedy_build_trip(cows, limit):
    """
    Builds a single trip of cows that abides with the weight limit. Takes the heaviest
    cow and loads that cow first. Then fills the trip with the next heaviest cow that still
    fits.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (int)

    Returns:
    A tuple with the following items:
    A list of strings, with each string representing a cow name on the current trip
    A dictionary with the remaining cows not yet boarded
    """
    trip = []
    unloaded_cows = cows.copy()
    remaining_cows = cows.copy()
    trip_weight = 0
    while len(remaining_cows) > 0:
        heaviest_cow = max(remaining_cows, key=remaining_cows.get)
        if remaining_cows[heaviest_cow] <= 10 - trip_weight:
            trip.append(heaviest_cow)
            trip_weight += remaining_cows[heaviest_cow]
            del remaining_cows[heaviest_cow]
            del unloaded_cows[heaviest_cow]
        else:
            del remaining_cows[heaviest_cow]
    return (trip,unloaded_cows)

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    set = []
    valid_partitions = []
    cow_names = list(cows.keys())
    shortest_partition_length = len(cows)
    result = []
    for n in range(len(cows)):
        set.append(n)
    for partition in get_partitions(set):
        if check_part(partition, cows, limit):
            valid_partitions.append(partition)
    for partition in valid_partitions:
        if len(partition) <= shortest_partition_length:
            shortest_partition_length = len(partition)
            shortest_partition = partition
    for trip in shortest_partition:
        trip_names = []
        for cow in trip:
            name = cow_names[cow]
            trip_names.append(name)
        result.append(trip_names)
    return result

def check_part(part, dict, limit):
    """
    Evaluates a partition to verify that each list within the partition abides with the
    weight limit for the container.

    Parameters:
    part - a list of lists of integers that enumerate the possible partitions for the dict
    dict - a dictionary with keys cow name (string) and values weight (integer)
    limit - spaceship weight capcity (integer)

    Returns: 
    Boolean - True if all sublists of part have summed dict values <= limit
            - Otherwise False
    """
    values_list = list(dict.values())
    for trip in part:
        trip_weight = 0
        for cow in trip:
            trip_weight += values_list[cow]
        if trip_weight > limit:
            return False
    return True
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    start = time.time()
    print('The number of trips with greedy is: ' + str(len(greedy_cow_transport(load_cows('ps1_cow_data.txt')))))
    end = time.time()
    print('Greedy took ' + str(end-start))
    start = time.time()
    print('The number of trips with brute force is: ' + str(len(brute_force_cow_transport(load_cows('ps1_cow_data.txt')))))
    end = time.time()
    print('Brute force took ' + str(end-start))


if __name__ == '__main__':
    print('The result of greedy load 1: ' + str(greedy_cow_transport(load_cows('ps1_cow_data.txt'))))
    print('The result of greedy load 2: ' + str(greedy_cow_transport(load_cows('ps1_cow_data_2.txt'))))
    print('The result of brute force load 1: ' +str(brute_force_cow_transport(load_cows('ps1_cow_data.txt'))))
    print('The result of brute force load 1: ' +str(brute_force_cow_transport(load_cows('ps1_cow_data_2.txt'))))
    compare_cow_transport_algorithms()
