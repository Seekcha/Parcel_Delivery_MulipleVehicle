# --------------------------------------------------------------
# Course:     Master IA and Robotics                          |
# --------------------------------------------------------------
# Members:     Seekcha Sungkur                                |
#              Munish Dawoonah                                |
#              Ferio Rasambatra                               |
# Course:      Metaheuristics:                                |
#              Evolutionary and Bio-Inspired Algorithms       |
# Assignment:  Solving a Complex Problem using Metaheuristics |
#              [ASSIGNMENT - 4]                               |
# Title:
# Date:        OCTOBER  25, 2020                              |
# --------------------------------------------------------------

# !pip3 install -U googlemaps
# https://github.com/chncyhn/simulated-annealing-tsp/blob/master/anneal.py
#

import math
import time
import json
import random
import datetime
from decimal import Decimal

import googlemaps
import collections

# Calling the distance matrix API
gmaps = googlemaps.Client(key='AIzaSyBx0n2ciqzWa6er_BjaDJvXZ6eYr1jKmN0 ')
print("Maximum number of vehicle = 6")
numVehicles = int(input("VEHICLES NUMBERS : "))


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)


# -------------------------------------------------------------------------------------
################################# SimulatedAnneling ##################################
# -------------------------------------------------------------------------------------
def SimulatedAnneling():
    time1 = time.localtime()  # get struct_time
    hour1 = time.strftime("%H:%M:%S", time1)
    h1 = int(time.localtime().tm_hour)  # get hour
    mn1 = int(time.localtime().tm_min)  # get minute
    s1 = int(time.localtime().tm_sec)  # get second
    duration1 = int((h1 * 3600) + (mn1 * 60) + s1)  # convert to seconds

    # function using the data in the API
    def get_distance_between_coords(origin, destination):
        # getting the current datetime
        now = datetime.datetime.now()

        # calling the function of the API
        ans = gmaps.directions(origin, destination, mode="driving", departure_time=now)

        # loading the data in a JSON file
        jsn = json.loads(json.dumps(ans))
        # returning the specific data found in Json > legs > distance > value
        # return distance and time
        return jsn[0]['legs'][0]['distance']['value'], jsn[0]['legs'][0]['duration']['value']

    # Loading JSON file
    locs = None
    with open('data.json') as json_file:
        locs = json.load(json_file)

    n = len(locs['locations'])
    # From dry cleaning services to the first delivery place
    distance_matrix = [[0] * n for i in range(n)]

    # "Dry Cleaning Services, Destination"

    # #i is the value of the start destination
    # #j is the value of the end destination

    for i in range(0, len(locs['locations'])):
        for j in range(0, len(locs['locations'])):
            # adding Json data obtained in get_distance_between_coords in distance_matrix
            distance_matrix[i][j] = get_distance_between_coords(locs['locations'][i]['coords'],
                                                                locs['locations'][j]['coords'])

    print(distance_matrix)

    def convert(seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return "%d:%02d:%02d" % (hour, minutes, seconds)

    # maxSteps size of tabu search

    def simulatedAnnealing(Nitems, maxDuration, maxSteps, T, numVehicles):
        simAneal_list = [i for i in range(len(Nitems))]  # indexes of locations available to select randomly

        # returns random neighbour
        def getRandomNeighbour(n):
            index = random.randint(0, n - 1)
            return index

        # Get new neighbours from list of locations not used yet
        def randomize_new_neighbours(neighboursPerSteps):
            ans = []
            n = neighboursPerSteps
            if len(simAneal_list) < neighboursPerSteps: n = len(simAneal_list)
            for i in range(n):
                ans.append(simAneal_list[getRandomNeighbour(n)])
            return ans

        # defining the conditional probability (whether or not to accept a bad value_
        def conditionalProbability(cst, newCst, temp):
            if newCst > cst:
                e = 1
            else:
                e = math.exp(- (abs(newCst - cst)) / temp)
            return e

        # User defined metric to evaluate neighbour
        def cost_function(current_loc, next_loc):
            try:
                distance_increment = Nitems[current_loc][next_loc][0]
                duration_increment = Nitems[current_loc][next_loc][1]
                return (distance_increment / duration_increment), next_loc
            except:
                return 0, next_loc

        # Evaluate best neighbour from random choices
        def calculate_cost_functions(current_loc, new_neighbours):
            ans = []
            for i in range(len(new_neighbours)):
                ans.append(cost_function(current_loc, new_neighbours[i]))
            return ans

        def get_best_neighbour(current_loc):
            random_neighbour_values = calculate_cost_functions(current_loc, randomize_new_neighbours(2))

            # get index of best neighbour from random choices made
            if len(random_neighbour_values) != 0:
                best_neighbour_index = random_neighbour_values.index(max(random_neighbour_values))
            # returns global location index of best neighbour
            return random_neighbour_values[best_neighbour_index][1]

        def get_best_neighbours(current_loc):
            ans = []
            for i in range(maxSteps):
                ans.append(get_best_neighbour(current_loc))
            return ans

        # counts how many elementts in a list
        def mode_filter(neighbour_indexes):
            data = collections.Counter(neighbour_indexes)
            # returns element and frequency of occurence /returns elememnt and frequency of occurence
            return data.most_common(1)[0][0]  # returns item'[0]' with frequency of occurence'[1]'

        # #Code for Simulated annealing

        # getting first change and value
        n = 0
        route = [[] for i in range(numVehicles)]
        route_distance = [0] * numVehicles
        route_duration = [0] * numVehicles
        current_loc_index = [0] * numVehicles
        return_distance = [0] * numVehicles
        return_duration = [0] * numVehicles
        previous_return_distance = [0] * numVehicles
        previous_return_duration = [0] * numVehicles


        for v in range(numVehicles):
            # adding current distance to Route
            route[v].append(current_loc_index[v])

        # remove current distance to SimAneal_list
        simAneal_list.remove(current_loc_index[0])

        # The number of times the experiment repeats
        for i in range(len(simAneal_list)):
            for v in range(numVehicles):
                best_neighbour_index = mode_filter(get_best_neighbours(current_loc_index[v]))
                best_neighbour_distance = Nitems[current_loc_index[v]][best_neighbour_index][0]
                best_neighbour_duration = Nitems[current_loc_index[v]][best_neighbour_index][1]

                return_distance[v] = Nitems[0][best_neighbour_index][0]
                return_duration[v] = Nitems[0][best_neighbour_index][1]

                m = best_neighbour_duration + return_duration[v] - previous_return_duration[v]

                # Duration not exceed the maximum duration
                if (route_duration[v] + m) < maxDuration:
                    # returning the absolute value
                    currentChange = abs(best_neighbour_duration - previous_return_distance[v])

                    if conditionalProbability(n, currentChange, T) > random.random():
                        route_distance[v] += (
                                best_neighbour_distance + return_distance[v] - previous_return_distance[v])
                        route_duration[v] += (
                                best_neighbour_duration + return_duration[v] - previous_return_duration[v])

                        previous_return_distance[v] = return_distance[v]
                        previous_return_duration[v] = return_duration[v]

                        current_loc_index[v] = best_neighbour_index
                        route[v].append(current_loc_index[v])
                        simAneal_list.remove(current_loc_index[v])  # remove location from tabulist
                        n += 1

                T *= (1 - (T / maxSteps))

        for v in range(numVehicles):
            route[v].append(0)
        return route, route_distance, route_duration

    # getting time for the Simulated Annealing algorithm to run
    # getting time for the simulatedAnnealing Search algorithm to run
    time2 = time.localtime()  # get struct_time
    hour2 = time.strftime("%H:%M:%S", time2)
    h2 = int(time.localtime().tm_hour)  # get hours
    mn2 = int(time.localtime().tm_min)  # get minutes
    s2 = int(time.localtime().tm_sec)  # get seconds
    duration2 = int((h2 * 3600) + (mn2 * 60) + s2)  # convert to seconds
    duration = duration2 - duration1
    elapsed = convert(duration)
    ans = simulatedAnnealing(distance_matrix, 10000, 100, 6, numVehicles)
    print("PROCESSING TIMES :")
    print(" |>Begin at =", hour1)
    print(" |>End at = ", hour2)
    print(" |>Time for Simulated Annealing algorithm to run = ", elapsed)

    for v in range(numVehicles):
        print("\nVEHICLE %d :" % (v + 1))
        print(" |>Optimal route = ", end="")
        for i in range(len(ans[0][v]) - 1):
            print(locs['locations'][ans[0][v][i]]['name'], end="")
            print(' ---> ', end="")
        print(locs['locations'][ans[0][v][0]]['name'])
        km = float(ans[1][v] / 1000)
        print(" |>Total route distance = ", km, "kilometers")
        print(" |>Total route duration = ", convert(ans[2][v]), "\n")


# ---------------------------------------------------------------------------------
################################# TABU ##################################
# ---------------------------------------------------------------------------------
def TabuSearch():
    time1 = time.localtime()  # get struct_time
    hour1 = time.strftime("%H:%M:%S", time1)
    h1 = int(time.localtime().tm_hour)  # get hour
    mn1 = int(time.localtime().tm_min)  # get minute
    s1 = int(time.localtime().tm_sec)  # get second
    duration1 = int((h1 * 3600) + (mn1 * 60) + s1)  # convert to seconds

    # function using the data in the API
    def get_distance_between_coords(origin, destination):
        # getting the current datetime
        now = datetime.datetime.now()

        # calling the function of the API
        ans = gmaps.directions(origin, destination, mode="driving", departure_time=now)

        # loading the data in a JSON file
        jsn = json.loads(json.dumps(ans))
        # returning the specific data found in Json > legs > distance > value
        # return distance and time
        return jsn[0]['legs'][0]['distance']['value'], jsn[0]['legs'][0]['duration']['value']

    # Loading JSON file
    locs = None
    with open('data.json') as json_file:
        locs = json.load(json_file)

    n = len(locs['locations'])
    # From dry cleaning services to the first delivery place
    distance_matrix = [[0] * n for i in range(n)]

    # "Dry Cleaning Services, Destination"

    # #i is the value of the start destination
    # #j is the value of the end destination

    for i in range(0, len(locs['locations'])):
        for j in range(0, len(locs['locations'])):
            # adding Json data obtained in get_distance_between_coords in distance_matrix
            distance_matrix[i][j] = get_distance_between_coords(locs['locations'][i]['coords'],
                                                                locs['locations'][j]['coords'])

    print(distance_matrix)

    def tabuSearch(items, maxDuration, maxSteps, neighboursPerSteps, numVehicles):
        tabu_list = [i for i in range(len(items))]  # indexes of locations available to select randomly

        # Random number generator
        def get_random_neighbour_index(n):
            index = random.randint(0, n - 1)
            return index

        # Get new neighbours from list of locations not used yet
        def randomize_new_neighbours(neighboursPerSteps):
            ans = []
            n = neighboursPerSteps
            if len(tabu_list) < neighboursPerSteps: n = len(tabu_list)
            for i in range(n):
                ans.append(tabu_list[get_random_neighbour_index(n)])
            return ans

        # User defined metric to evaluate neighbour
        def cost_function(current_loc, next_loc):
            try:
                distance_increment = items[current_loc][next_loc][0]
                duration_increment = items[current_loc][next_loc][1]
                return (distance_increment / duration_increment), next_loc
            except:
                return 0, next_loc

        # Evaluate best neighbour from random choices
        def calculate_cost_functions(current_loc, new_neighbours):
            ans = []
            for i in range(len(new_neighbours)):
                ans.append(cost_function(current_loc, new_neighbours[i]))

            return ans

        def get_best_neighbour(current_loc):

            random_neighbour_values = calculate_cost_functions(current_loc,
                                                               randomize_new_neighbours(neighboursPerSteps))

            # get index of best neighbour from random choices made
            if len(random_neighbour_values) != 0:
                best_neighbour_index = random_neighbour_values.index(max(random_neighbour_values))
                # returns global location index of best neighbour
                return random_neighbour_values[best_neighbour_index][1]

        def get_best_neighbours(current_loc):
            ans = []
            for i in range(maxSteps):
                ans.append(get_best_neighbour(current_loc))
            return ans

        def mode_filter(neighbour_indexes):
            data = collections.Counter(neighbour_indexes)
            return data.most_common(1)[0][0]  # returns item'[0]' with frequency of occurence'[1]'

        # Initial setup
        n = 0

        route = [[] for i in range(numVehicles)]
        route_distance = [0] * numVehicles
        route_duration = [0] * numVehicles
        current_loc_index = [0] * numVehicles
        return_distance = [0] * numVehicles
        return_duration = [0] * numVehicles
        previous_return_distance = [0] * numVehicles
        previous_return_duration = [0] * numVehicles

        tabu_list.remove(current_loc_index[0])
        for v in range(numVehicles):
            route[v].append(current_loc_index[v])

        for i in range(len(tabu_list)):
            for v in range(numVehicles):
                best_neighbour_index = mode_filter(get_best_neighbours(current_loc_index[v]))
                best_neighbour_distance = items[current_loc_index[v]][best_neighbour_index][0]
                best_neighbour_duration = items[current_loc_index[v]][best_neighbour_index][1]

                return_distance[v] = items[0][best_neighbour_index][0]
                return_duration[v] = items[0][best_neighbour_index][1]
                m = best_neighbour_duration + return_duration[v] - previous_return_duration[v]

                if (route_duration[v] + m) < maxDuration:
                    route_distance[v] += (best_neighbour_distance + return_distance[v] - previous_return_distance[v])
                    route_duration[v] += (best_neighbour_duration + return_duration[v] - previous_return_duration[v])

                    previous_return_distance[v] = return_distance[v]
                    previous_return_duration[v] = return_duration[v]

                    current_loc_index[v] = best_neighbour_index
                    route[v].append(current_loc_index[v])
                    tabu_list.remove(current_loc_index[v])  # remove location from tabulist
                    n += 1

        for v in range(numVehicles):
            route[v].append(0)
        return route, route_distance, route_duration

    # getting time for the Tabu Search algorithm to run

    # getting time for the simulatedAnnealing Search algorithm to run
    time2 = time.localtime()  # get struct_time
    hour2 = time.strftime("%H:%M:%S", time2)
    h2 = int(time.localtime().tm_hour)  # get hours
    mn2 = int(time.localtime().tm_min)  # get minutes
    s2 = int(time.localtime().tm_sec)  # get seconds
    duration2 = int((h2 * 3600) + (mn2 * 60) + s2)  # convert to seconds
    duration = duration2 - duration1
    elapsed = convert(duration)

    print("PROCESSING TIMES :")
    print(" |>Begin at  = ", hour1)
    print(" |>End at    = ", hour2)
    print(" |>Time for Tabu Search algorithm to run = ", elapsed)

    ans = tabuSearch(distance_matrix, 10000, 100, 2, numVehicles)

    for v in range(numVehicles):

        print("\nVEHICLE %d :" % (v + 1))
        print(" |>Optimal route = ", end="")
        for i in range(len(ans[0][v]) - 1):
            print(locs['locations'][ans[0][v][i]]['name'], end="")
            print(' ---> ', end="")
        print(locs['locations'][ans[0][v][0]]['name'])
        km = float(ans[1][v] / 1000)
        print(" |>Total route distance = ", km, "kilometers")
        print(" |>Total route duration = ", convert(ans[2][v]), "\n")


print("-----------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------")
print("TABU SEARCH")
print("....")
start1 = time.time()
st1 = Decimal(start1)
TabuSearch()
end1 = time.time()
en1 = Decimal(end1)
TS = end1 - start1
print("-----------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------")
print("SIMULATED ANNEALING")
print("....")
start = time.time()
st = Decimal(start)
SimulatedAnneling()
end = time.time()
en = Decimal(end)
SA = en - st
print("-----------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------")
print("Comparing the running time for algorithm")

for i in range(1, 10):
    print("\nNumber of time the function ran: ", i)
    print("Time for Tabu Search algorithm to run = ", TS, "s")
    print("Time for Simulated Annealing algorithm to run = ", SA, "s")
i += 1
