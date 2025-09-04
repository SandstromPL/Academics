states = ['I'] * 4  # Represents C1 to C4 states as I, M, E, S

while True:
    try:
        line = input().strip()
        if not line:
            continue
        a, b, c = line.split()
        a = int(a)
        a_idx = a - 1  # Convert to 0-based index

        current_state = states[a_idx]

        if b == 'R':
            if current_state == 'I':
                other_caches = [i for i in range(4) if i != a_idx]
                other_had_valid = any(states[i] in ['M', 'E', 'S'] for i in other_caches)

                for i in other_caches:
                    if states[i] in ['M', 'E']:
                        states[i] = 'S'

                if other_had_valid:
                    states[a_idx] = 'S'
                else:
                    states[a_idx] = 'E'
        elif b == 'W':
            if current_state == 'M':
                pass  # No change
            elif current_state == 'E':
                states[a_idx] = 'M'
            elif current_state == 'S':
                other_caches = [i for i in range(4) if i != a_idx]
                for i in other_caches:
                    if states[i] in ['M', 'E', 'S']:
                        states[i] = 'I'
                states[a_idx] = 'M'
            elif current_state == 'I':
                other_caches = [i for i in range(4) if i != a_idx]
                for i in other_caches:
                    if states[i] in ['M', 'E', 'S']:
                        states[i] = 'I'
                states[a_idx] = 'M'

        print(f"C1:{states[0]} C2:{states[1]} C3:{states[2]} C4:{states[3]}")

        if c == '0':
            break
    except EOFError:
        break