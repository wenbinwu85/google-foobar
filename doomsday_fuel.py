"""
Doomsday Fuel
=============

Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. 
It starts as raw ore, then during processing, begins randomly changing between forms, eventually 
reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, 
not all of which are useful as fuel. 

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting 
the end state of a given ore sample. You have carefully studied the different structures that the ore 
can take and which transitions it undergoes. It appears that, while random, the probability of each 
structure transforming is fixed. That is, each time the ore is in 1 state, it has the same 
probabilities of entering the next state (which might be the same state).  You have recorded the 
observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that 
the ore can become, but you haven't seen all of them.

Write a function solution(m) that takes an array of array of nonnegative ints representing how many 
times that state has gone to the next state and return an array of ints for each terminal state 
giving the exact probabilities of each terminal state, represented as the numerator for each state, 
then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. 
It is guaranteed that no matter which state the ore is in, there is a path from that state to a 
terminal state. That is, the processing will always eventually end in a stable state. The ore starts 
in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long 
as the fraction is simplified regularly. 

For example, consider the matrix m:
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:
solution.solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
Output:
    [7, 6, 8, 21]

Input:
solution.solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])

Output:
    [0, 3, 2, 9, 14]
"""


from fractions import Fraction
from functools import reduce


def solution(m):
    if len(m) == 1:
        return [1, 1]

    def matrix_identity(size):
        identity = [[] for _ in range(size)]
        for i in range(size):
            for j in range(size):
                if i == j:
                    identity[i].append(1)
                else:
                    identity[i].append(0)
        return identity

    def matrix_subtract(m, n):
        for i in range(len(m)):
            for j in range(len(m[0])):
                m[i][j] -= n[i][j]
        return m

    def matrix_multiply(m, n):
        mn = [[0 for _ in range(len(n[0]))] for _ in range(len(m))]
        columns = [c for c in zip(*n)]
        for i, row in enumerate(m):
            for j, col in enumerate(columns):
                mn[i][j] = sum([x * y for x, y in zip(row, col)])
        return mn

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def lcm(a, b):
        return abs(a*b) / gcd(a, b)

    def get_sub_matrices(m):
        minors = []
        for i in range(len(m)):
            for j in range(len(m[0])):
                temp = [[col for col in row] for row in m]
                temp.pop(i)
                for idx, row in enumerate(temp):
                    row.pop(j)
                    temp[idx] = row
                minors.append(temp)
        return minors

    def get_sub_matrix(m, j):
        minor = [[col for col in row] for row in m]
        minor.pop(0)
        for idx, row in enumerate(minor):
            row.pop(j)
            minor[idx] = row
        return minor

    def get_determinant(m):
        if len(m) == 2:
            return m[0][0] * m[1][1] - m[0][1] * m[1][0]

        determinant = 0
        for idx, val in enumerate(m[0]):
            minor = get_sub_matrix(m, idx)
            determinant += get_determinant(minor) * val * pow(-1, idx)
        return determinant

    def get_adjugate(m):
        if len(m) == 2:
            adjugate = m
            adjugate[0][0], adjugate[1][1] = adjugate[1][1], adjugate[0][0]
            adjugate[0][1] = adjugate[0][1] * -1
            adjugate[1][0] = adjugate[1][0] * -1
            return adjugate

        subs = get_sub_matrices(m)
        minors = [get_determinant(sub) for sub in subs]

        size = len(m[0])
        cofactors = [minors[i:i+size] for i in range(0, len(minors), size)]
        for i in range(len(cofactors)):
            for j in range(len(cofactors[0])):
                cofactors[i][j] = cofactors[i][j] * pow(-1, i+j)

        cofactor_transpose = list(map(list, zip(*cofactors)))
        return cofactor_transpose

    def matrix_inverse(m):
        adjugate = get_adjugate(m)
        determinant = get_determinant(m)
        for i in range(len(adjugate)):
            for j in range(len(adjugate[0])):
                adjugate[i][j] = adjugate[i][j]/determinant
        return adjugate

    non_terms = []
    terms = []

    # modify matrix
    for idx, row in enumerate(m):
        row_sum = sum(row)
        if row_sum > 0:
            m[idx] = [Fraction(i, row_sum) for i in row]
            non_terms.append(idx)
        elif row_sum == 0:
            m[idx][idx] = 1
            terms.append(idx)

    # sort matrix rows
    n = []
    for i in non_terms:
        n.append(m[i])
    for i in terms:
        n.append(m[i])

    # sort matrix columns
    p = []
    for i in n:
        non_term_vals = [i[j] for j in non_terms]
        term_vals = [i[j] for j in terms]
        p.append(non_term_vals + term_vals)

    identity = matrix_identity(len(non_terms))
    i_sub_p = matrix_subtract(identity, p)
    i_sub_p_inverse = matrix_inverse(i_sub_p)
    q = [p[i][len(non_terms):] for i in range(len(non_terms))]
    r = matrix_multiply(i_sub_p_inverse, q)

    probabilities = [Fraction(val).limit_denominator() for val in r[0]]
    numerators = [i.numerator for i in probabilities]
    denominators = [i.denominator for i in probabilities]
    least_common_multiple = reduce(lcm, set(denominators))

    for idx, denom in enumerate(denominators):
        numerators[idx] = least_common_multiple / denom * numerators[idx]

    return numerators + [least_common_multiple]

assert (
    solution([
        [0, 2, 1, 0, 0],
        [0, 0, 0, 3, 4],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]) == [7, 6, 8, 21]
)

assert (
    solution([
        [0, 1, 0, 0, 0, 1],
        [4, 0, 0, 3, 2, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]) == [0, 3, 2, 9, 14]
)

assert (
    solution([
        [1, 2, 3, 0, 0, 0],
        [4, 5, 6, 0, 0, 0],
        [7, 8, 9, 1, 0, 0],
        [0, 0, 0, 0, 1, 2],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]) == [1, 2, 3]
)

assert (
    solution([
        [0]
    ]) == [1, 1]
)

assert (
    solution([
        [0, 0, 12, 0, 15, 0, 0, 0, 1, 8],
        [0, 0, 60, 0, 0, 7, 13, 0, 0, 0],
        [0, 15, 0, 8, 7, 0, 0, 1, 9, 0],
        [23, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [37, 35, 0, 0, 0, 0, 3, 21, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]) == [1, 2, 3, 4, 5, 15]
)

assert (
    solution([
        [0, 7, 0, 17, 0, 1, 0, 5, 0, 2],
        [0, 0, 29, 0, 28, 0, 3, 0, 16, 0],
        [0, 3, 0, 0, 0, 1, 0, 0, 0, 0],
        [48, 0, 3, 0, 0, 0, 17, 0, 0, 0],
        [0, 6, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]) == [4, 5, 5, 4, 2, 20]
)

assert (
    solution([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]) == [1, 1, 1, 1, 1, 5]
)

assert (
    solution([
        [1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]) == [2, 1, 1, 1, 1, 6]
)

assert (
    solution([
        [0, 86, 61, 189, 0, 18, 12, 33, 66, 39],
        [0, 0, 2, 0, 0, 1, 0, 0, 0, 0],
        [15, 187, 0, 0, 18, 23, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]) == [6, 44, 4, 11, 22, 13, 100]
)

assert (
    solution([
        [0, 0, 0, 0, 3, 5, 0, 0, 0, 2],
        [0, 0, 4, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 4, 4, 0, 0, 0, 1, 1],
        [13, 0, 0, 0, 0, 0, 2, 0, 0, 0],
        [0, 1, 8, 7, 0, 0, 0, 1, 3, 0],
        [1, 7, 0, 0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]) == [1, 1, 1, 2, 5]
)
