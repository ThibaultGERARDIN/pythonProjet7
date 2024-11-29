import csv


def get_data():
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


def sac_a_dos(actions, max_budget):
    n = len(actions)
    # Créer une matrice de taille (n+1) x (budget_max+1)
    matrix = [[0 for i in range(max_budget + 1)] for y in range(n + 1)]

    # Remplir la matrice
    for i in range(1, n + 1):
        name, cost, gain = actions[i - 1]
        for b in range(max_budget + 1):
            if cost <= b:
                # On choisit entre prendre l'action ou non
                matrix[i][b] = max(
                    matrix[i - 1][b], matrix[i - 1][b - cost] + gain
                )
            else:
                # On ne peut pas prendre l'action
                matrix[i][b] = matrix[i - 1][b]

    # Retrouver la combinaison optimale
    combination = []
    b = max_budget
    for i in range(n, 0, -1):
        if matrix[i][b] != matrix[i - 1][b]:
            combination.append(actions[i - 1])  # Ajouter l'action
            b -= actions[i - 1][1]  # Réduire le budget disponible

    best_gain = matrix[n][max_budget]
    return combination, best_gain


# Fonction principale
def main():
    max_budget = 700

    actions = get_data()
    best_combination, best_gain = sac_a_dos(actions, max_budget)

    print("Meilleure combinaison d'actions :")
    for action in best_combination:
        print(
            f"- {action[0]} (Coût: {action[1]} euros, Bénéfice: {action[2]:.2f} euros)"
        )

    print(f"\nBénéfice total : {best_gain:.2f} euros")


if __name__ == "__main__":
    main()
