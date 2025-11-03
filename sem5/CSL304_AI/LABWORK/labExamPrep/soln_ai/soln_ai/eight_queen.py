import random
import numpy as np

def attackers(state):
    pairs = 0
    for i in range(0, len(state)):
        for j in range(i+1, len(state)):
            if state[i] == state[j]:
                pairs += 1
    for i in range(0, len(state)):
        diag_num = 0
        for j in range(i+1, len(state)):
            if state[j] == state[i]-diag_num:
                pairs += 1
            if state[j] == state[i]+diag_num:
                pairs += 1
            diag_num += 1
    return pairs

def simulated_annealing(initial_state, n_iterations, temp):
    best = initial_state
    best_attack = attackers(initial_state)
    curr, curr_attack = initial_state, best_attack

    for i in range(n_iterations):
        candidate = curr

        move = random.randint(1, 2)

        if move == 1:
            candidate[random.randint(0, len(curr)-1)] = random.randint(1, 8)
        else:
            num_1 = random.randint(0, len(curr)-1)
            num_2 = random.randint(0, len(curr)-1)

            temp = candidate[num_1]
            candidate[num_1] = candidate[num_2]
            candidate[num_2] = temp

        candidate_attack = attackers(candidate)

        if candidate_attack < best_attack:
            best, best_attack = candidate, candidate_attack
            print('>%d f(%s) = %.5f' % (i, best, best_attack))

        diff = candidate_attack - curr_attack
        t = temp/float(i+1)
        metropolis = np.exp(-diff/t)

        if diff < 0 or random.random() < metropolis:
            curr, curr_attack = candidate, candidate_attack
    return [best, best_attack]

initial = [2, 7, 4, 8, 1, 3, 6, 5]
#initial = [3, 7, 6, 6, 8, 6, 1, 8]
print(attackers(initial))
soln = simulated_annealing(initial, 1000, 10000)

print(soln[0], attackers(soln[0]))
