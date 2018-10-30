import math


def get_graph(input):
    arcs = input.split(',')
    directed_graph = {}
    for arc in arcs:
        # Ensure correct formatting of route
        if len(arc) < 3:
            raise Exception("Invalid route input: '%s'" % arc)

        arc = arc.strip()
        start_city = arc[0]
        end_city = arc[1]
        distance = int(arc[2:])

        # Ensure non-cyclical routes
        if start_city == end_city:
            raise Exception("Start and end cities are the same for route: '%s" % arc)

        if start_city not in directed_graph:
            directed_graph[start_city] = {}

        # Ensure that we only have one route between two cities in one direction
        if end_city in directed_graph[start_city]:
            raise Exception('Two routes between same cities: %s -> %s' % (start_city, end_city))

        directed_graph[start_city][end_city] = distance

    return directed_graph


def get_distance_for_route(route, graph):
    cities = route.split('-')
    num_cities_in_route = len(cities)
    total_route_length = 0
    try:
        for i in range(num_cities_in_route - 1):
            start_city = cities[i]
            end_city = cities[i + 1]
            total_route_length += graph[start_city][end_city]
        return total_route_length
    except:
        return 'NO SUCH ROUTE'


def get_min_distance(distances, unvisited_nodes):
    min_value = None
    node = None
    for city, distance in distances.items():
        if city not in unvisited_nodes:
            continue
        if min_value is None:
            node = city
            min_value = distance
        elif distance < min_value:
            node = city
            min_value = distance
    return node


def find_shortest_path_between_cities(start_city, end_city, graph):
    """
    Runtime: O(n^2)
    Space: O(n)

    Where 'n' is the number of cities in the graph.

    This implements Dijkstra's algorithm.

    We are ignoring creation of the route, as it was not specified in the question. However this could be added
    by including a 'previous' dictionary and reverse walking it to construct the path.
    """
    all_nodes = graph.keys()

    unvisited_nodes = set()
    distances = {}
    for node in all_nodes:
        distances[node] = math.inf
        unvisited_nodes.add(node)

    distances[start_city] = 0

    while len(unvisited_nodes) > 0:
        node = get_min_distance(distances, unvisited_nodes)

        # We are ending because we are only interested in the shortest path from start -> end.
        # Any other path will have a higher cost to reach this city.
        if start_city != end_city:
            if node == end_city:
                return distances[end_city]

        unvisited_nodes.remove(node)

        for neighbour_node in graph[node].keys():
            new_distance = distances[node] + graph[node][neighbour_node]
            if new_distance < distances[neighbour_node]:
                distances[neighbour_node] = new_distance

    if start_city == end_city:
        loop_city_distances = {}
        for city, distance in distances.items():
            if city != start_city and distance != math.inf:
                city_distance = find_shortest_path_between_cities(city, start_city, graph)
                loop_city_distances[city] = city_distance

        min_distance = math.inf
        for loop_city, distance in loop_city_distances.items():
            if distances[loop_city] + distance < min_distance:
                min_distance = distances[loop_city] + distance
        return min_distance
    return distances[end_city]


if __name__ == '__main__':
    graph = get_graph('AB5,BC4,CD8,DC8,DE6,AD5,CE2,EB3,AE7')
    print(find_shortest_path_between_cities('B', 'B', graph))
