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
            actions.append((name, cost, gain_percentage, gain))
    return actions


def generate_base_combination(sorted_actions, max_budget):
    base_combination = []
    base_combination_cost = 0
    base_combination_gain = 0

    for action in sorted_actions:
        base_combination_cost += action[1]
        if base_combination_cost <= max_budget:
            base_combination.append(action)
            base_combination_gain += action[3]
        else:
            base_combination_cost -= action[1]
            break
    for action in base_combination:
        sorted_actions.remove(action)

    actions_left = sorted_actions
    budget_left = max_budget - base_combination_cost

    return base_combination, actions_left, budget_left, base_combination_gain


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
        total_gain = sum(action[3] for action in combination)

        if total_cost <= max_budget and total_gain > best_gain:
            best_combination = combination
            best_combination_cost = total_cost
            best_gain = total_gain

    return best_combination, best_combination_cost, best_gain


def main():
    max_budget = 500

    actions = get_data()
    sorted_by_percentage = sorted(
        actions, key=lambda tup: tup[2], reverse=True
    )
    base_combination, actions_left, budget_left, base_combination_gain = (
        generate_base_combination(sorted_by_percentage, max_budget)
    )

    best_combination, best_combination_cost, best_gain = get_best_combination(
        actions_left, budget_left
    )
    base_combination.extend(best_combination)
    total_cost = max_budget - budget_left + best_combination_cost
    total_gain = round(base_combination_gain + best_gain, 2)

    print("Meilleure combinaison d'actions :")
    for action in base_combination:
        print(
            f"- {action[0]} (Coût: {action[1]} euros,"
            f" Bénéfice: {action[3]} euros)"
        )

    print(f"\nCoût total : {total_cost} euros")
    print(f"Bénéfice total : {total_gain} euros")


if __name__ == "__main__":
    main()
