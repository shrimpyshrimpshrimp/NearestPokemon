import csv
import numpy as np
import matplotlib.pyplot as plt
import time

def getPokemonData():
    pokemon_name_to_stat = {}
    pokemon_stat_to_name = {}
    stats = []

    with open('pokemon_stats.csv', 'r') as f:
        reader = csv.reader(f)

        for row in reader:
            #skip header
            if row[0] == 'name':
                continue

            stat = np.array(row[1:], dtype=float)
            name = row[0]
            
            pokemon_name_to_stat[name] = stat

            #can only put tuple in key of a dict not a numpy array
            key = tuple(stat)
            #checks duplicate
            if key not in pokemon_stat_to_name:
                pokemon_stat_to_name[key] = []
                #only append non-duplicate stats
                stats.append(stat)
            pokemon_stat_to_name[key].append(name)
    
    return pokemon_name_to_stat, pokemon_stat_to_name, stats


def LinearSearch(stats, target_stat):
    mindist = float('inf')
    minp = None

    for s in stats:
        #don't include self in the search
        if np.array_equal(s, target_stat):
            continue

        d = np.linalg.norm(s - target_stat)        
        if d < mindist:
            mindist = d
            minp = s

    return minp

class kdNode:
    def __init__(self, point, left = None, right = None):
        self.point = point
        self.left = left
        self.right = right

def kdBuild(points, level=0):
    if len(points) == 0:
        return None
    
    axis = level % 6
    sorted_points = sorted(points, key=lambda p: p[axis])
    median = len(sorted_points) // 2

    return kdNode(
        point=sorted_points[median],
        left=kdBuild(sorted_points[:median], level+1),
        right=kdBuild(sorted_points[median+1:], level+1)
    )

def kdSearch(root, target):
    minp = None
    mindist = float('inf')

    def search(current, level = 0):
        nonlocal minp, mindist

        if current == None:
            return
        
        #skip self
        if not np.array_equal(current.point, target):
            d = np.linalg.norm(current.point - target)
            if d < mindist:
                minp = current
                mindist = d
        
        axis = level % 6
        if abs(target[axis] - current.point[axis]) < mindist:
            search(current.left, level+1)
            search(current.right, level+1)
        
        elif target[axis] < current.point[axis]:
            search(current.left, level+1)
        else:
            search(current.right, level+1)

    search(root)
    return minp.point

def main():
    pokemon_name_to_stat, pokemon_stat_to_name, stats = getPokemonData()

    input_pokemon = input("Enter the pokemon name: ")

    if input_pokemon not in pokemon_name_to_stat:
        print(f"{input_pokemon} not found")
        return
    
    target_stat = pokemon_name_to_stat[input_pokemon]

    Duplicate_pokemon = list(pokemon_stat_to_name[tuple(target_stat)])
    if input_pokemon in Duplicate_pokemon:
        Duplicate_pokemon.remove(input_pokemon)

    if Duplicate_pokemon:
        print("Duplicates found")
        print("Nearest Pokemon: ", Duplicate_pokemon)
        return

    start = time.time()
    Linear_result = LinearSearch(stats, target_stat)
    end = time.time()
    Linear_time = end-start

    print("Linear Search")
    print(f"Time: {Linear_time} seconds")
    print("Nearest Pokemon: ", pokemon_stat_to_name[tuple(Linear_result)])

    root = kdBuild(stats)
    start = time.time()
    kd_result = kdSearch(root, target_stat)
    end = time.time()
    kd_time = end-start

    print("kd Search")
    print(f"Time: {kd_time} seconds")
    print("Nearest Pokemon: ", pokemon_stat_to_name[tuple(kd_result)])

    return

if __name__ == "__main__":
    main()
