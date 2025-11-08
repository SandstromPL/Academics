import copy

states = ['S1', 'S2', 'S3', 'S4', 'G']
actions = {
    'S1': ['a1', 'a2'],
    'S2': ['a1', 'a2'],
    'S3': ['a1', 'a2'],
    'S4': ['a1'],
    'G': []
}

transitions = {
    'S1': {
        'a1': [('S2', 0.8), ('S3', 0.2)],
        'a2': [('S3', 0.7), ('S4', 0.3)]
    },
    'S2': {
        'a1': [('S1', 0.5), ('S3', 0.4), ('G', 0.1)],
        'a2': [('S3', 0.9), ('S4', 0.1)]
    },
    'S3': {
        'a1': [('S2', 0.6), ('G', 0.4)],
        'a2': [('S4', 1.0)]
    },
    'S4': {
        'a1': [('G', 1.0)]
    },
    'G': {}
}

reward = -2
gamma = 0.9

def policy_evaluation(policy, V, theta=1e-6):
    while True:
        delta = 0
        for s in states:
            if s == 'G':
                continue
            v = V[s]
            action = policy[s]
            expected_value = 0
            for next_s, prob in transitions[s][action]:
                expected_value += prob * (reward + gamma * V[next_s])
            V[s] = expected_value
            delta = max(delta, abs(v - V[s]))
        if delta < theta:
            break

def policy_improvement(policy, V):
    policy_stable = True
    for s in states:
        if s == 'G':
            continue
        old_action = policy[s]
        min_value = float('inf')
        best_action = None
        for a in actions[s]:
            expected_value = 0
            for next_s, prob in transitions[s][a]:
                expected_value += prob * (reward + gamma * V[next_s])
            if expected_value < min_value:
                min_value = expected_value
                best_action = a
        policy[s] = best_action
        if old_action != best_action:
            policy_stable = False
    return policy_stable

def policy_iteration():
    policy = {s: 'a1' for s in states if s != 'G'}
    policy['G'] = None

    V = {s: 0 for s in states}

    iterations = 0
    while True:
        iterations += 1
        policy_evaluation(policy, V)
        stable = policy_improvement(policy, V)
        if stable:
            break

    return policy, V, iterations

if __name__ == '__main__':
    final_policy, final_V, iters = policy_iteration()
    print("Final Policy:")
    for s in ['S1', 'S2', 'S3', 'S4']:
        print(f"π({s}) = {final_policy[s]}")
    print("\nFinal Value Function:")
    for s in ['S1', 'S2', 'S3', 'S4', 'G']:
        print(f"V({s}) = {final_V[s]:.4f}")
    print(f"\nNumber of iterations: {iters}")
