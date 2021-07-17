"""
Fuel Injection Perfection
=========================

Commander Lambda has asked for your help to refine the automatic quantum antimatter fuel 
injection system for the LAMBCHOP doomsday device. It's a great chance for you to get a 
closer look at the LAMBCHOP -- and maybe sneak in a bit of sabotage while you're at it -- 
so you took the job gladly. 

Quantum antimatter fuel comes in small pellets, which is convenient since the many moving 
parts of the LAMBCHOP each need to be fed fuel one pellet at a time. However, minions dump 
pellets in bulk into the fuel intake. You need to figure out the most efficient way to sort 
and shift the pellets down to a single pellet at a time. 

The fuel control mechanisms have three operations: 

1) Add one fuel pellet
2) Remove one fuel pellet
3) Divide the entire group of fuel pellets by 2 (due to the destructive energy released when a 
quantum antimatter pellet is cut in half, the safety controls will only allow this to happen 
if there is an even number of pellets)

Write a function called solution(n) which takes a positive integer as a string and returns the 
minimum number of operations needed to transform the number of pellets to 1. The fuel intake 
control panel can only display a number up to 309 digits long, so there won't ever be more 
pellets than you can express in that many digits.

For example:
solution(4) returns 2: 4 -> 2 -> 1
solution(15) returns 5: 15 -> 16 -> 8 -> 4 -> 2 -> 1

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases -- 
Input:
solution.solution('15')
Output:
    5

Input:
solution.solution('4')
Output:
    2
"""

from math import log

def solution(n):
    n = int(n)
    op = 0

    output = 'n: ' + str(n)
    while n > 1:
        if n == 3:
            output = output + '-> 3 +2'
            print(output)
            return op + 2
        if n % 2:
            if int(n+1) & int(n) == 0:
                output = output + ' +1 p +' + str(int(log(n+1, 2)))
                print(output)
                return op + 1 + int(log(n+1, 2))
            n -= 1
        else:
            if int(n) & int(n-1) == 0:
                output = output + ' p +' + str(int(log(n+1, 2)))
                print(output)
                return op + int(log(n, 2))
            n /= 2
        op += 1
        output = output + ' op:' + str(op) + '\n' + str(n)
    print(output)
    return op
