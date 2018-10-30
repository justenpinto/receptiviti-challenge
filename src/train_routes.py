def get_graph(input):
    arcs = input.split(',')
    directed_graph = {}
    for arc in arcs:
        arc = arc.strip()
        start_city = arc[0]
        end_city = arc[1]
        distance = int(arc[2:])

        if start_city == end_city:
            raise Exception('Start and end cities are the same for route: %s' % arc)

        if start_city not in directed_graph:
            directed_graph[start_city] = {}

        # Ensure that we only have on route between two cities in one direction
        if end_city in directed_graph[start_city]:
            raise Exception('Two routes between same cities: %s -> %s' % (start_city, end_city))

        directed_graph[start_city][end_city] = distance

    return directed_graph

if __name__ == '__main__':
    print(get_graph('AA2,AB5, BC4,CD81,BC5'))