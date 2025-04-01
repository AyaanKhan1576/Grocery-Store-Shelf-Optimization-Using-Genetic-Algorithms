#%%
# Name: Ayaan Khan
# Roll Number: 22i-0832
# Section: CS-K
# AI Assignment 02
# Question: 02

import random
import pandas as pd
from copy import deepcopy

shelves = {
    "S1": {"name": "Checkout Display", "capacity": 8, "attributes": {"high_visibility"}},
    "S2": {"name": "Lower Shelf", "capacity": 25, "attributes": {"lower"}},
    "S3": {"name": "Eye-Level Shelf", "capacity": 15, "attributes": {"eye_level", "high_visibility"}},
    "S4": {"name": "General Aisle Shelf", "capacity": 20, "attributes": set()},
    "S5": {"name": "Upper Shelf", "capacity": 12, "attributes": {"upper"}},
    "R1": {"name": "Primary Refrigerator", "capacity": 20, "attributes": {"refrigerated"}},
    "R2": {"name": "Secondary Refrigerator", "capacity": 15, "attributes": {"refrigerated"}},
    "H1": {"name": "Hazardous Item Zone", "capacity": 10, "attributes": {"hazardous"}},
    "L1": {"name": "Locked Display", "capacity": 5, "attributes": {"secured", "high_visibility"}}
}

products = [
    {"id": "P1",  "name": "Milk",                 "weight": 5,  "category": "Dairy",     "attributes": {"perishable", "high_demand"}},
    {"id": "P2",  "name": "Rice Bag",             "weight": 10, "category": "Grain",     "attributes": {"heavy"}},
    {"id": "P3",  "name": "Frozen Nuggets",       "weight": 5,  "category": "Frozen",    "attributes": {"perishable"}},
    {"id": "P4",  "name": "Cereal",               "weight": 3,  "category": "Breakfast", "attributes": {"high_demand"}},
    {"id": "P5",  "name": "Pasta",                "weight": 2,  "category": "Pasta",     "attributes": set(), "complementary": {"P6"}},
    {"id": "P6",  "name": "Pasta Sauce",          "weight": 3,  "category": "Pasta",     "attributes": set(), "complementary": {"P5"}},
    {"id": "P7",  "name": "Detergent",            "weight": 4,  "category": "Cleaning",  "attributes": {"hazardous"}},
    {"id": "P8",  "name": "Glass Cleaner",        "weight": 5,  "category": "Cleaning",  "attributes": {"hazardous"}},
    {"id": "P9",  "name": "Yogurt",               "weight": 2,  "category": "Dairy",     "attributes": {"perishable", "high_demand"}},
    {"id": "P10", "name": "Chips",                "weight": 1,  "category": "Snacks",    "attributes": {"high_demand", "discounted"}},
    {"id": "P11", "name": "Frozen Vegetables",    "weight": 4,  "category": "Frozen",    "attributes": {"perishable"}},
    {"id": "P12", "name": "Cookies",              "weight": 2,  "category": "Snacks",    "attributes": {"discounted"}},
    {"id": "P13", "name": "Lettuce",              "weight": 1,  "category": "Produce",   "attributes": {"perishable"}},
    {"id": "P14", "name": "Tomato",               "weight": 1,  "category": "Produce",   "attributes": {"perishable", "high_demand"}},
    {"id": "P15", "name": "Luxury Perfume",       "weight": 0.5,"category": "Luxury",    "attributes": {"expensive", "high_theft"}},
    {"id": "P16", "name": "Buy-One-Get-One Cereal","weight": 2,  "category": "Breakfast", "attributes": {"promotional", "discounted", "high_demand"}},
    {"id": "P18", "name": "Bulk Beans",           "weight": 12, "category": "Grain",     "attributes": {"heavy"}},
    {"id": "P19", "name": "Fresh Juice",          "weight": 3,  "category": "Beverage",  "attributes": {"perishable", "high_demand"}},
    {"id": "P20", "name": "Ice Cream",            "weight": 4,  "category": "Frozen",    "attributes": {"perishable", "discounted"}},
    {"id": "P21", "name": "Bread",                "weight": 2,  "category": "Bakery",    "attributes": {"high_demand"}},
    {"id": "P22", "name": "Organic Apples",       "weight": 3,  "category": "Produce",   "attributes": {"perishable", "discounted"}},
    {"id": "P23", "name": "Granola Bars",         "weight": 2,  "category": "Snacks",    "attributes": {"high_demand", "promotional"}},
    {"id": "P24", "name": "Soda",                 "weight": 2,  "category": "Beverage",  "attributes": {"high_demand"}},  # non-perishable beverage
    {"id": "P25", "name": "Cheese",               "weight": 3,  "category": "Dairy",     "attributes": {"perishable"}},
    {"id": "P26", "name": "Spaghetti",            "weight": 1.5,"category": "Pasta",     "attributes": set(), "complementary": {"P27"}},
    {"id": "P27", "name": "Tomato Sauce",         "weight": 2.5,"category": "Pasta",     "attributes": set(), "complementary": {"P26"}}
]

NUM_PRODUCTS = len(products)
POPULATION_SIZE = 50
GENERATIONS = 150
TOURNAMENT_SIZE = 3
MUTATION_RATE = 0.1
shelf_ids = list(shelves.keys())

def initialize_population():
    population = []
    for _ in range(POPULATION_SIZE):
        chromosome = [random.choice(shelf_ids) for _ in range(NUM_PRODUCTS)]
        population.append(chromosome)
    return population

def fitness(chromosome):
    penalty = 0

    # 1. Shelf Capacity Constraint
    shelf_load = {sid: 0 for sid in shelf_ids}
    for gene, product in zip(chromosome, products):
        shelf_load[gene] += product["weight"]
    for sid, total_weight in shelf_load.items():
        capacity = shelves[sid]["capacity"]
        if total_weight > capacity:
            penalty += (total_weight - capacity) * 10  

    # 2. Product-Level Constraints
    refrigerated_shelves = {sid for sid in shelf_ids if "refrigerated" in shelves[sid]["attributes"]}
    high_visibility_shelves = {"S1", "S3", "L1"}

    for gene, product in zip(chromosome, products):
        prod_attrs = product["attributes"]
        assigned_shelf = gene
        shelf_attr = shelves[assigned_shelf]["attributes"]

        # Perishable goods on refrigerated shelf.
        if "perishable" in prod_attrs and assigned_shelf not in refrigerated_shelves:
            penalty += 50

        # Hazardous items in hazardous zone 
        if "hazardous" in prod_attrs and assigned_shelf != "H1":
            penalty += 50

        # Heavy items on lower shelf (S2)
        if "heavy" in prod_attrs and assigned_shelf != "S2":
            penalty += 30

        # High-demand (if not perishable or hazardous) in high-visibility
        if "high_demand" in prod_attrs and "perishable" not in prod_attrs and "hazardous" not in prod_attrs:
            if assigned_shelf not in high_visibility_shelves:
                penalty += 20

        # Discounted items (if non-perishable) in high-visibility
        if "discounted" in prod_attrs and "perishable" not in prod_attrs:
            if assigned_shelf not in high_visibility_shelves:
                penalty += 20

        # Promotional items (if non-perishable) in high-visibility
        if "promotional" in prod_attrs and "perishable" not in prod_attrs:
            if assigned_shelf not in high_visibility_shelves:
                penalty += 20

        # Expensive items in the secure zone
        if ("expensive" in prod_attrs or "high_theft" in prod_attrs) and assigned_shelf != "L1":
            penalty += 50

        # Discourage farther shelves if general have space
        if "lower" in shelf_attr or "upper" in shelf_attr:
            penalty += 15

    # 3. Refrigeration Efficiency:
    used_refrigerators = set()
    for gene, product in zip(chromosome, products):
        if "perishable" in product["attributes"] and gene in refrigerated_shelves:
            used_refrigerators.add(gene)
    if len(used_refrigerators) > 1:
        penalty += (len(used_refrigerators) - 1) * 30

    # 4. Complementary Products:
    for idx, product in enumerate(products):
        if "complementary" in product:
            for comp in product["complementary"]:
                comp_idx = next((i for i, p in enumerate(products) if p["id"] == comp), None)
                if comp_idx is not None and chromosome[idx] != chromosome[comp_idx]:
                    penalty += 15

    # 5. Category Segmentation:
    for idx, product in enumerate(products):
        same_category = False
        for jdx, other in enumerate(products):
            if idx != jdx and product["category"] == other["category"]:
                if chromosome[idx] == chromosome[jdx]:
                    same_category = True
                    break
        if not same_category:
            penalty += 5

    return penalty

def tournament_selection(population):
    tournament = random.sample(population, TOURNAMENT_SIZE)
    tournament.sort(key=lambda chromo: fitness(chromo))
    return tournament[0]

def crossover(parent1, parent2):
    point = random.randint(1, NUM_PRODUCTS - 2)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(chromosome):
    for i in range(NUM_PRODUCTS):
        if random.random() < MUTATION_RATE:
            chromosome[i] = random.choice(shelf_ids)
    return chromosome

def genetic_alg():
    population = initialize_population()
    best_solution = None
    best_fitness = float("inf")
    
    for gen in range(GENERATIONS):
        new_population = []
        while len(new_population) < POPULATION_SIZE:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            new_population.extend([child1, child2])
        
        population = new_population[:POPULATION_SIZE]
        for chromo in population:
            f = fitness(chromo)
            if f < best_fitness:
                best_fitness = f
                best_solution = chromo

        # TO TEST WORKING
        # print(f"Generation {gen}: Best Fitness = {best_fitness}")
    
    return best_solution, best_fitness

def main():
    best_solution, best_fit = genetic_alg()

    allocation = {sid: [] for sid in shelf_ids}
    for gene, product in zip(best_solution, products):
        allocation[gene].append(product)

    rows = []
    for sid in shelf_ids:
        shelf_info = shelves[sid]
        prods = allocation[sid]
        prod_ids = ", ".join(p["id"] for p in prods)
        prod_names = ", ".join(p["name"] for p in prods)
        total_weight = sum(p["weight"] for p in prods)
        rows.append({
            "Shelf ID": sid,
            "Shelf Name": shelf_info["name"],
            "Capacity (kg)": shelf_info["capacity"],
            "Assigned Product IDs": prod_ids,
            "Assigned Product Names": prod_names,
            "Total Weight (kg)": total_weight
        })

    df_allocation = pd.DataFrame(rows)

    excel_filename = "optimized_shelf_allocation.xlsx"
    df_allocation.to_excel(excel_filename, index=False)

    print("Optimized Shelf Allocation (Fitness Score = {}):".format(best_fit))
    print(df_allocation)
    print("\nThe allocation has also been saved to '{}'.".format(excel_filename))

main()


# %%
