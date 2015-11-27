import numpy as np
import math
import random

def next_number(n):
    if n%2 == 0:
        return n/2
    return n*3 + 1

def next_odd_number(n):
    while not n%2:
        n/=2
    n = n*3 + 1
    while not n%2:
        n/=2
    return n

def regular_chain(n):
    while n!=1:
        yield n
        n = next_number(n)

def odd_chain(n):
    while n!=1:
        yield n
        n = next_odd_number(n)

# all even numbers eventually map to odd numbers
# all numbers = 0 mod 3 map to numbers = 1 mod 3
# all numbers = 2 mod 3 map to numbers = 1 mod 3
# all odd numbers = 1 mod 3 map to numbers = 1 mod 3
# all even numbers = 1 mod 3 map to numbers = 2 mod 3
# all numbers = 0 mod 3 eventually map to an odd number = 1 mod 3

# so what are the properties of odd numbers congruent to 1 mod 3
# can we say that within these numbers, they always map to
# something

def pick_number(property = lambda n: True, start = 1, end = 10**10):
    number = int(random.uniform(start, end))
    while not property(number):
        number = int(random.uniform(start, end))
    return number

# hypothesis: there is some pattern when it comes to
# modulo some number n, what the next_num or next_odd_num is modulo n

# pick a number congruent to 1 or 5 mod 6, 

def run_tests(modulo, condition):
    results = np.zeros((modulo, modulo))
    results_2 = np.zeros((modulo, modulo))
    results_3 = np.zeros((modulo, modulo))
    def todo(begin, step, odd):
        results[begin, odd] += 1
        results_2[begin, step] += 1
        results_3[step, odd] += 1
    in_some_modulus(modulo, todo, condition)
    output = []
    for result in results, results_2, results_3:
        output.append(find_entropy(result))
        output.append(find_entropy(np.transpose(result)))
    return output

def in_some_modulus(modulo, todo, condition):
    for i in range(100*modulo*modulo):
        n = pick_number(condition)
        begin = n%modulo
        step = next_number(n)%modulo
        odd = next_odd_number(n)%modulo
        todo(begin, step, odd)

def find_entropy(results):
    total = np.sum(results)
    p_x = np.sum(results, 0)/float(total)
    p_xy = results/float(total)
    entropy = 0.0
    for i, j in np.transpose(np.nonzero(results > 0.5)):
        entropy += p_xy[i,j] * math.log(p_x[j]/p_xy[i,j], 2)
    return entropy

base_modulo = 9
loop_start_modulo = 3
loop_end_modulo = 23
num_tests = 6

all_results = []
for base_congruency in range(base_modulo):
    condition = lambda n: n%base_modulo == base_congruency
    results = np.zeros((num_tests, loop_end_modulo - loop_start_modulo))
    for modulo in range(loop_start_modulo, loop_end_modulo):
        for i,t in enumerate(run_tests(modulo, condition)):
            results[i, modulo-loop_start_modulo] = t
    all_results.append(results)

already_tested = set()

for i in range(base_modulo):
    for j in range(i+1, base_modulo):
        prelim = np.absolute(all_results[i] - all_results[j])
        print i,j,np.sum(prelim)
