import math
import argparse
import re

TEST_CASE_TYPES = {
    'RouteDistance': re.compile("^[A-Z](-[A-Z])+$"),
    'RouteShortest': re.compile("^[A-Z]\|[A-Z]$"),
    'RouteLessThanHops': re.compile("^[A-Z]\|[A-Z]\|[0-9]+$"),
    'RouteEqualHops': re.compile("^[A-Z]\|[A-Z]\|[0-9]+$"),
    'RouteLessThanDistance': re.compile("^[A-Z]\|[A-Z]\|[0-9]+$")
}


class TestCase:
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.args = kwargs['args']


class TrainRoutes:
    def __init__(self, **kwargs):
        self.graph_data = kwargs['graph_data']
        if isinstance(self.graph_data, str):
            self.graph_data = self.graph_data.split(',')
        self.test_case_data = kwargs['test_case_data']
        if isinstance(self.test_case_data, str):
            self.test_case_data = self.test_case_data.split(',')

        self.graph = {}
        self.parse_graph()

        self.test_cases = []
        self.parse_testcases()

    def parse_graph(self):
        arcs = self.graph_data
        self.graph = {}
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

            if start_city not in self.graph:
                self.graph[start_city] = {}

            # Ensure that we only have one route between two cities in one direction
            if end_city in self.graph[start_city]:
                raise Exception('Two routes between same cities: %s -> %s' % (start_city, end_city))

            self.graph[start_city][end_city] = distance

    def parse_testcases(self):
        for test_case in self.test_case_data:
            test_case_name, test_case_args = test_case.split(':')

            if test_case_name not in TEST_CASE_TYPES:
                raise Exception('Unknown test case: %s' % test_case)

            arg_pattern = TEST_CASE_TYPES[test_case_name]

            if not arg_pattern.match(test_case_args):
                raise Exception("Invalid arguments for test case: %s" % test_case)

            self.test_cases.append(TestCase(name=test_case_name, args=test_case_args))

    def get_distance_for_route(self, route):
        """
        Gets the distance for travelling a route.

        :param route:
        :return:
        """
        cities = route.split('-')
        num_cities_in_route = len(cities)
        total_route_length = 0
        try:
            for i in range(num_cities_in_route - 1):
                start_city = cities[i]
                end_city = cities[i + 1]
                total_route_length += self.graph[start_city][end_city]
            return '%s distance: %d' % (route, total_route_length)
        except:
            return '%s distance: NO SUCH ROUTE' % route

    @staticmethod
    def get_min_distance(distances, unvisited_nodes):
        """
        Get node with the minimum distance (that has yet to be visited) in the distances dictionary.

        :param distances:
        :param unvisited_nodes:
        :return:
        """
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

    def find_shortest_path_between_cities(self, start_city, end_city):
        """
        Runtime: O(n^2) (this can be improved to O(E + n lg n) by using a priority queue)
        Space: O(n)

        Where 'n' is the number of cities in the graph.

        This implements Dijkstra's algorithm.

        We are ignoring creation of the route, as it was not specified in the question. However this could be added
        by including a 'previous' dictionary and reverse walking it to construct the path.
        """
        all_nodes = self.graph.keys()

        unvisited_nodes = set()
        distances = {}
        for node in all_nodes:
            distances[node] = math.inf
            unvisited_nodes.add(node)

        distances[start_city] = 0

        while len(unvisited_nodes) > 0:
            node = TrainRoutes.get_min_distance(distances, unvisited_nodes)

            # We are ending because we are only interested in the shortest path from start -> end.
            # Any other path will have a higher cost to reach this city.
            if start_city != end_city:
                if node == end_city:
                    return distances[end_city]

            unvisited_nodes.remove(node)

            for neighbour_node in self.graph[node].keys():
                new_distance = distances[node] + self.graph[node][neighbour_node]
                if new_distance < distances[neighbour_node]:
                    distances[neighbour_node] = new_distance

        if start_city == end_city:
            # Special case when we start and end on same city, as Dijkstra's does not solve this.
            # We apply Dijkstra's algo to all the end points, and then determine the combined minimum path
            # to reach the start city again.
            loop_city_distances = {}
            for city, distance in distances.items():
                if city != start_city and distance != math.inf:
                    city_distance = self.find_shortest_path_between_cities(city, start_city)
                    loop_city_distances[city] = city_distance

            min_distance = math.inf
            for loop_city, distance in loop_city_distances.items():
                if distances[loop_city] + distance < min_distance:
                    min_distance = distances[loop_city] + distance
            return min_distance
        return distances[end_city]

    def trips_hop_constraint_bfs(self, start_node, end_node, hops, equal=False):
        """
        Perform breadth first search to find all available paths.

        :param start_node: City to start at.
        :param end_node: City to end at.
        :param hops: Maximum number of hops allowed between cities (depending on what :param equal is set to)
        :param equal: Set this to true if we want exact hop matching. False if we want less than or equal to.
        :return:
        """
        queue = [(start_node, 0, [])]
        paths = []
        while queue:
            node, depth, traceback = queue.pop(0)

            # We do not need to parse anymore as any further city addition will break our max_hops constraint
            if depth > hops:
                continue

            path = traceback + [node]
            if len(path) > 2 and path[-1] == end_node:
                if equal:
                    if depth == hops:
                        paths.append('-'.join(path) + (' (%d hops)' % depth))
                else:
                    paths.append('-'.join(path) + (' (%d hops)' % depth))

            for neighbour in self.graph[node].keys():
                queue.append((neighbour, depth + 1, traceback + [node]))

        return paths

    def trips_distance_constraint_bfs(self, start_node, end_node, max_distance):
        """
        Perform breadth first search to find all available paths.

        :param start_node: City to start at.
        :param end_node: City to end at.
        :param max_distance: Maximum distance allowed on route.
        :return:
        """
        queue = [(start_node, 0, [])]
        paths = []
        while queue:
            node, distance, traceback = queue.pop(0)

            # We do not need to parse anymore as any further city addition will break our max_hops constraint
            if distance >= max_distance:
                continue

            path = traceback + [node]
            if len(path) > 2 and path[-1] == end_node:
                paths.append('-'.join(path) + (' (%d distance)' % distance))

            for neighbour in self.graph[node].keys():
                queue.append((neighbour, distance + self.graph[node][neighbour], traceback + [node]))

        return paths

    def run_test_cases(self):
        """
        Runs all test cases specified by self.test_cases.

        :return:
        """
        count = 1
        for test_case in self.test_cases:
            print("Running test case #%d" % count)
            if test_case.name == 'RouteDistance':
                print(self.get_distance_for_route(test_case.args))
            elif test_case.name == 'RouteShortest':
                args = test_case.args.split('|')
                shortest_distance = self.find_shortest_path_between_cities(args[0], args[1])
                print("Shortest distance between %s and %s: %d" % (args[0], args[1], shortest_distance))
            elif test_case.name == 'RouteLessThanHops':
                args = test_case.args.split('|')
                paths = self.trips_hop_constraint_bfs(args[0], args[1], int(args[2]))
                print('Paths between %s and %s with hops less than or equal to %d: %d (%s)' % (
                    args[0], args[1], int(args[2]), len(paths), paths
                ))
            elif test_case.name == 'RouteEqualHops':
                args = test_case.args.split('|')
                paths = self.trips_hop_constraint_bfs(args[0], args[1], int(args[2]), equal=True)
                print('Paths between %s and %s with hops equal to %d: %d (%s)' % (
                    args[0], args[1], int(args[2]), len(paths), paths
                ))
            elif test_case.name == 'RouteLessThanDistance':
                args = test_case.args.split('|')
                paths = self.trips_distance_constraint_bfs(args[0], args[1], int(args[2]))
                print('Paths between %s and %s with distance less than %d: %d (%s)' % (
                    args[0], args[1], int(args[2]), len(paths), paths
                ))
            else:
                raise Exception('Unknown test case: %s' % test_case.name)
            count += 1
            print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--graphdata',
                        nargs='+',
                        help='Specify cities and distance as space separated string. E.g. AB5 BC5 CD5',
                        required=True)
    parser.add_argument('--testcases',
                        nargs='+',
                        help='List of test cases to perform. See documentation for formatting.',
                        required=True)

    args = parser.parse_args()

    x = TrainRoutes(graph_data=args.graphdata,
                    test_case_data=args.testcases)
    x.run_test_cases()
