#! /usr/bin/python

"""
The Grandest Staircase Of Them All
==================================

With the LAMBCHOP doomsday device finished, Commander Lambda is preparing to debut on the galactic 
stage -- but in order to make a grand entrance, Lambda needs a grand staircase! As the Commander's 
personal assistant, you've been tasked with figuring out how to build the best staircase EVER. 

Lambda has given you an overview of the types of bricks available, plus a budget. You can buy 
different amounts of the different types of bricks (for example, 3 little pink bricks, or 5 blue 
lace bricks). Commander Lambda wants to know how many different types of staircases can be built 
with each amount of bricks, so they can pick the one with the most options. 

Each type of staircase should consist of 2 or more steps.  No two steps are allowed to be at the 
same height - each step must be lower than the previous one. All steps must contain at least one 
brick. A step's height is classified as the total amount of bricks that make up that step.
For example, when N = 3, you have only 1 choice of how to build the staircase, with the first 
step having a height of 2 and the second step having a height of 1: (# indicates a brick)

#
##
21

When N = 4, you still only have 1 staircase choice:

#
#
##
31

But when N = 5, there are two ways you can build a staircase from the given bricks. The two 
staircases can have heights (4, 1) or (3, 2), as shown below:

#
#
#
##
41

#
##
##
32

Write a function called solution(n) that takes a positive integer n and returns the number of 
different staircases that can be built from exactly n bricks. n will always be at least 3 
(so you can have a staircase at all), but no more than 200, because Commander Lambda's not 
made of money!

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:
solution.solution(200)
Output:
    487067745

Input:
solution.solution(3)
Output:
    1
"""


def answer(n):
    # your code here
    memo = [[0 for _ in range(n + 2)] for _ in range(n + 2)]
    return staircase(1, n, memo) - 1

def staircase(h, l, memo):
    if memo[h][l] != 0:
        return memo[h][l]
    if l == 0:
        return 1
    if l < h:
        return 0
    memo[h][l] = staircase(h + 1, l - h, memo) + staircase(h + 1, l, memo)
    return memo[h][l]



def solution(n):
    def _get_steps(x, y):
        s = []
        while x < y:
            s.append(x)
            x += 1
            y -= x
        s.append(x+y)
        return s
    
    count = 0
    for start in range(1, n/2+1):
        steps = _get_steps(start, n - start)
        if len(steps) == 1:
            break
        count += 1
        while len(steps) > 2:
            y = steps.pop()
            x = steps.pop()
            if y-x > x:
                steps.extend(_get_steps(x+1, y-1))
                count += 1
                continue
            if (y-x) % 2:
                count += (y - x - 1) / 2
            else:
                count += (y - x) / 2 - 1
            steps.append(x+y)
            count += 1
    return count
