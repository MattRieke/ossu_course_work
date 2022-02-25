Problem A.5: Writeup

1. What were your results from compare_cow_transport_algorithms? Which algorithm runs faster? Why?
1. compare_cow_transport_algorithms() resulted in a greedy trip count of 6 trips, while brute_force had a trip count of 5 trips. Greedy took approximately 0.000126 seconds and brute_force took approximately 0.508614 seconds. Greedy ran faster than brute_force because it only has to evaluate one valid solution, whereas brute_force must evaluate all possible solutions.

2. Does the greedy algorithm return the optimal solution? Why/why not?
2. The greedy algorithm does not return the optimal solution. The number of trips returned by the greedy algorithm can be greater than the brute_force solution. It optimizes to load the heaviest possible cow first and does not optimize to minimize the wasted space on a trip. As a result the wasted space across multiple trips can result in needing additional trips.

3. Does the brute force algorithm return the optimal solution? Why/why not?
3. The brute fore algorithm returns the optimal solution. By enumerating all possible solutions and then finding a solution with the minimum number of trips, it is guaranteed to find the optimal solution based on the criteria of minimum number of trips.

Problem B.2: Writeup

1. Explain why it would be difficult to use a brute force algorithm to solve this problem if there were 30 different egg weights. You do not need to implement a brute force algorithm in order to answer this.
1. It would be difficult to use a brute force algorithm to solve this problem if there were 30 different egg weights, because the number of partitions of size n is already very large and adding a large number of potential options to slot into the various partitions makes the potential scenarios to analyze incredibly large.

2. If you were to implement a greedy algorithm for finding the minimum number of eggs needed, what would the objective function be? What would the constraints be? What strategy would your greedy algorithm follow to pick which coins to take? You do not need to implement a greedy algorithm in order to answer this.
2. A greedy algorithm would have an objective function of filling the weight capacity of the spaceship with the fewest number of eggs. The constraints would be the maximum weight only since each egg can be used as many times as possible. The greedy algorithm would follow a strategy of adding the heaviest egg that is less than or equal to the remaining weight capacity.

3. Will a greedy algorithm always return the optimal solution to this problem? Explain why it is optimal or give an example of when it will not return the optimal solution. Again, you do not need to implement a greedy algorithm in order to answer this.
3. A greedy algorithm will not always return the optimal solution to this problem. An example of when the greedy solution would not work would be for any even number greater than 4 where the possible egg weights are (n/2 + 1, n/2, and 1). In this scenario the greedy algorithm would choose the n/2 + 1 egg first, resulting in the need to fill the remaining n/2 - 1 weight with eggs of weight 1. However, it would be more efficient to simply skip the heavier egg and load two of the n/2 eggs. As a result the greedy algorithm is not always optimal.