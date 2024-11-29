import csv


def get_data():
    actions = []
    with open("actions.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["Actions #"]
            cost = float(row["Cout par action (en euros)"])
            percentage = row["Benefice (apres 2 ans)"].strip("%")
            gain_percentage = float(percentage) / 100
            gain = round(cost * gain_percentage, 2)
            actions.append((name, cost, gain))
    return actions


def generate_combinations(actions):
    combinations = [[]]
    for action in actions:
        new_combinations = []
        for combination in combinations:
            new_combinations.append(combination + [action])
        combinations.extend(new_combinations)
    return combinations


def get_best_combination(actions, max_budget):
    combinations = generate_combinations(actions)
    best_combination = []
    best_combination_cost = 0
    best_gain = 0

    for combination in combinations:
        total_cost = sum(action[1] for action in combination)
        total_gain = sum(action[2] for action in combination)

        if total_cost <= max_budget and total_gain > best_gain:
            best_combination = combination
            best_combination_cost = total_cost
            best_gain = total_gain

    return best_combination, best_combination_cost, best_gain


def main():
    max_budget = 500

    actions = get_data()
    best_combination, best_combination_cost, best_gain = get_best_combination(
        actions, max_budget
    )

    print("Meilleure combinaison d'actions :")
    for action in best_combination:
        print(
            f"- {action[0]} (Coût: {action[1]} euros,"
            f" Bénéfice: {action[2]} euros)"
        )

    print(f"\nCoût total : {best_combination_cost} euros")
    print(f"Bénéfice total : {best_gain} euros")


if __name__ == "__main__":
    main()
