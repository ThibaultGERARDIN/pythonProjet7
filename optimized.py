import csv
import math


def get_data():
    # Read CSV file and return usable data : action = (name, cost, gain)
    actions = []
    with open("actions.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["Actions #"]
            cost = int(row["Cout par action (en euros)"])
            percentage = row["Benefice (apres 2 ans)"].strip("%")
            gain_percentage = float(percentage) / 100
            gain = round(cost * gain_percentage, 2)
            actions.append((name, cost, gain))
    return actions


def get_data_old(filename):
    # Read CSV file and return usable data : action = (name, cost, gain)
    # => from old dataset
    actions = []
    with open(filename, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["name"]
            cost = float(row["price"])
            percentage = row["profit"]
            gain_percentage = float(percentage) / 100
            gain = round(cost * gain_percentage, 2)
            if cost <= 0:
                pass
            else:
                actions.append((name, cost, gain))
    return actions


def get_best_combination(actions, max_budget):
    n = len(actions)
    # Create a matrix of size (n+1)(max_budget +1) and initialize it at 0
    matrix = [[0 for i in range(max_budget + 1)] for y in range(n + 1)]

    # Fill the matrix while choosing which action is bought
    for i in range(1, n + 1):
        name, cost, gain = actions[i - 1]
        rounded_cost = math.ceil(cost)
        for b in range(max_budget + 1):
            if rounded_cost <= b:
                # Either buy or not the action (maximum gain of the two)
                matrix[i][b] = max(
                    matrix[i - 1][b], matrix[i - 1][b - rounded_cost] + gain
                )
            else:
                # Can't buy the action
                matrix[i][b] = matrix[i - 1][b]

    # Read the matrix in reverse to obtain the combination
    combination = []
    b = max_budget
    for i in range(n, 0, -1):
        if matrix[int(i)][int(b)] != matrix[int(i - 1)][int(b)]:
            combination.append(actions[i - 1])
            b -= actions[i - 1][1]

    best_gain = round(matrix[n][max_budget], 2)
    total_cost = 0
    for action in combination:
        total_cost += action[1]
    return combination, best_gain, total_cost


def main():
    max_budget = 500

    actions = get_data_old("dataset1.csv")
    best_combination, best_gain, total_cost = get_best_combination(
        actions, max_budget
    )

    print("Meilleure combinaison d'actions :")
    for action in best_combination:
        print(
            f"- {action[0]} (Coût: {action[1]} euros,"
            f" Bénéfice: {action[2]} euros)"
        )

    print(f"\nCoût total : {total_cost} euros")
    print(f"\nBénéfice total : {best_gain} euros")


if __name__ == "__main__":
    main()
