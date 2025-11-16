import matplotlib.pyplot as plt
from copy import deepcopy

def wiring_cost(chip_1, chip_2):
    return max(0, chip_2[2]-(chip_1[2]+chip_1[0][0]), chip_1[2]-(chip_2[2]+chip_2[0][0])) + abs(chip_1[1]-chip_2[1])

def overlap_blocks(chip_1, chip_2):
    w1, h1 = chip_1[0]
    w2, h2 = chip_2[0]
    y1, y2 = chip_1[1], chip_2[1]
    x1, x2 = chip_1[2], chip_2[2]

    x_overlap = max(0, min(x1+w1-1, x2+w2-1) - max(x1, x2) + 1)
    y_overlap = max(0, min(y1+h1-1, y2+h2-1) - max(y1, y2) + 1)

    return x_overlap * y_overlap

def cost_calc(chips, connections):
    cost = 0
    for i in connections:
        cost += wiring_cost(chips[i[0]], chips[i[1]])
    for i in range(len(chips)):
        for j in range(i+1, len(chips)):
            cost += overlap_blocks(chips[i], chips[j])
    return cost

def gradient_descent_track(chips, connections, width):
    """Run integer descent, return final score and score history"""
    improved = True
    history = [cost_calc(chips, connections)]
    while improved:
        improved = False
        for ci in chips:
            current_score = cost_calc(chips, connections)
            best_score = current_score
            old_x = ci[2]
            best_x = old_x

            # try left
            if old_x - 1 >= 0:
                ci[2] = old_x - 1
                score_left = cost_calc(chips, connections)
                if score_left < best_score:
                    best_score = score_left
                    best_x = ci[2]

            # try right
            if old_x + ci[0][0] < width:
                ci[2] = old_x + 1
                score_right = cost_calc(chips, connections)
                if score_right < best_score:
                    best_score = score_right
                    best_x = ci[2]

            ci[2] = old_x  # reset

            if best_score < current_score:
                ci[2] = best_x
                improved = True
                history.append(best_score)

    return cost_calc(chips, connections), history

connections = [[0, 1], [1, 5], [1, 2], [2, 4], [3, 4], [4, 5], [0, 5], [6, 3], [6, 1], [7, 4]]
chips = [[[2, 4], 0, 0], [[2, 5], 1, 1], [[1, 3], 0, 1], [[2, 5], 4, 2], [[2, 4], 3, 3], [[1, 4], 2, 2], [[2, 5], 5, 0], [[1, 3], 6, 4]]
height = 10
width = 10

chips_copy = deepcopy(chips)
final_score, history = gradient_descent_track(chips_copy, connections, width)

print(f"Width of grid matrix: {width}")
print("Optimal configuration: ")
print("(Here dimensions are in format of width x height)")
for i in range(len(chips)):
    print(f"Chip {i+1}: Dimensions: {chips[i][0][0]}x{chips[i][0][1]}, Row: {chips[i][1]}, Final x-coordinate: {chips[i][2]}")
print("Score history:", history)
print(f"Optimal score: {final_score}")


# Plot
plt.figure(figsize=(6,4))
plt.plot(history, marker="o")
plt.title("Conflict Score During Integer Descent")
plt.xlabel("Step")
plt.ylabel("Conflict Score")
plt.grid(True)
plt.show()

