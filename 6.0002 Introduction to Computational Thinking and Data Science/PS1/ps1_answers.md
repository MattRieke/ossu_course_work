Problem A.5: Writeup

1. What were your results from compare_cow_transport_algorithms? Which
algorithm runs faster? Why?
1. compare_cow_transport_algorithms() resulted in a greedy trip count of 6 trips, while brute_force had a trip count of 5 trips. Greedy took approximately 0.000126 seconds and brute_force took approximately 0.508614 seconds. Greedy ran faster than brute_force because it only has to evaluate one valid solution, whereas brute_force must evaluate all possible solutions.

2. Does the greedy algorithm return the optimal solution? Why/why not?
2. The greedy algorithm does not return the optimal solution. The number of trips returned by the greedy algorithm can be greater than the brute_force solution. It optimizes to load the heaviest possible cow first and does not optimize to minimize the wasted space on a trip. As a result the wasted space across multiple trips can result in needing additional trips.

3. Does the brute force algorithm return the optimal solution? Why/why not?
3. The brute fore algorithm returns the optimal solution. By enumerating all possible solutions and then finding a solution with the minimum number of trips, it is guaranteed to find the optimal solution based on the criteria of minimum number of trips.

Problem B.2: Writeup

1. Explain why it would be difficult to use a brute force algorithm to solve this problem if there
were 30 different egg weights. You do not need to implement a brute force algorithm in order to
answer this.
2. If you were to implement a greedy algorithm for finding the minimum number of eggs
needed, what would the objective function be? What would the constraints be? What strategy
would your greedy algorithm follow to pick which coins to take? You do not need to implement a
greedy algorithm in order to answer this.
3. Will a greedy algorithm always return the optimal solution to this problem? Explain why it is
optimal or give an example of when it will not return the optimal solution. Again, you do not need
to implement a greedy algorithm in order to answer this.