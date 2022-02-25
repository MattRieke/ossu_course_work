Problem A.5: Writeup
1. compare_cow_transport_algorithms() resulted in a greedy trip count of 6 trips, while brute_force had a trip count of 5 trips. Greedy took approximately 0.000126 seconds and brute_force took approximately 0.508614 seconds. Greedy ran faster than brute_force because it only has to evaluate one valid solution, whereas brute_force must evaluate all possible solutions.

2. The greedy algorithm does not return the optimal solution. The number of trips returned by the greedy algorithm can be greater than the brute_force solution. It optimizes to load the heaviest possible cow first and does not optimize to minimize the wasted space on a trip. As a result the wasted space across multiple trips can result in needing additional trips.

3. The brute fore algorithm returns the optimal solution. By enumerating all possible solutions and then finding a solution with the minimum number of trips, it is guaranteed to find the optimal solution based on the criteria of minimum number of trips.
