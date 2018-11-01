from src.train_routes import *
import argparse
import math
import unittest


class TrainRouteTests(unittest.TestCase):
    # validate_test_case(test_case)

    def test_validate_test_case_pattern(self):
        self.assertRaises(argparse.ArgumentTypeError, validate_test_case, 'RouteDistance!A-B-C')

    def test_validate_test_case_RouteDistance(self):
        test_case = validate_test_case('RouteDistance:A-B-C')
        self.assertEqual(test_case.name, 'RouteDistance')
        self.assertEqual(test_case.args, 'A-B-C')

    def test_validate_test_case_fail_RouteDistance_InvalidArg(self):
        self.assertRaises(argparse.ArgumentTypeError, validate_test_case, 'RouteDistance:AD-C')

    def test_validate_test_case_RouteShortest(self):
        test_case = validate_test_case('RouteShortest:A|C')
        self.assertEqual(test_case.name, 'RouteShortest')
        self.assertEqual(test_case.args, 'A|C')

    def test_validate_test_case_fail_RouteShortest_InvalidArg(self):
        self.assertRaises(argparse.ArgumentTypeError, validate_test_case, 'RouteShortest:A||C')

    def test_validate_test_case_RouteLessThanHops(self):
        test_case = validate_test_case('RouteLessThanHops:C|C|3')
        self.assertEqual(test_case.name, 'RouteLessThanHops')
        self.assertEqual(test_case.args, 'C|C|3')

    def test_validate_test_case_fail_RouteLessThanHops_InvalidArg(self):
        self.assertRaises(argparse.ArgumentTypeError, validate_test_case, 'RouteLessThanHops:A||C')

    def test_validate_test_case_RouteEqualHops(self):
        test_case = validate_test_case('RouteEqualHops:A|C|4')
        self.assertEqual(test_case.name, 'RouteEqualHops')
        self.assertEqual(test_case.args, 'A|C|4')

    def test_validate_test_case_fail_RouteEqualHops_InvalidArg(self):
        self.assertRaises(argparse.ArgumentTypeError, validate_test_case, 'RouteEqualHops:A||C')

    def test_validate_test_case_RouteLessThanDistance(self):
        test_case = validate_test_case('RouteLessThanDistance:D|F|30')
        self.assertEqual(test_case.name, 'RouteLessThanDistance')
        self.assertEqual(test_case.args, 'D|F|30')

    def test_validate_test_case_fail_RouteLessThanDistance_InvalidArg(self):
        self.assertRaises(argparse.ArgumentTypeError, validate_test_case, 'RouteLessThanDistance:A||C')

    def test_validate_test_case_fail_InvalidName(self):
        self.assertRaises(argparse.ArgumentTypeError, validate_test_case, 'InvalidTestName:A-D-C')

    # validate_routes(route)

    def test_validate_routes_success(self):
        route = validate_routes('AB5')
        self.assertEqual(route, 'AB5')

    def test_validate_routes_fail_InvalidRoute_format(self):
        self.assertRaises(argparse.ArgumentTypeError, validate_routes, 'ABB5')

    def test_validate_routes_fail_InvalidRoute_same_city(self):
        self.assertRaises(argparse.ArgumentTypeError, validate_routes, 'BB5')

    # TrainRoutes

    def test_parse_graph_success(self):
        x = TrainRoutes(['AB1', 'BC2', 'CD3', 'AD4'], [])
        expected_graph = {
            'A': {'B': 1, 'D': 4},
            'B': {'C': 2},
            'C': {'D': 3}
        }
        self.assertEqual(x.graph, expected_graph)

    def test_parse_graph_fail_two_routes_same(self):
        self.assertRaises(Exception, TrainRoutes, ['AB1', 'BC2', 'AB3'], [])

    def test_get_route_distance_success(self):
        x = TrainRoutes(['AB1', 'BC2', 'CD3', 'AD4'], [])
        self.assertEqual(x.get_distance_for_route('A-B-C-D'), 6)

    def test_get_route_distance_no_route(self):
        x = TrainRoutes(['AB1', 'BC2', 'CD3', 'AD4'], [])
        self.assertEqual(x.get_distance_for_route('C-A'), 'NO SUCH ROUTE')

    def test_get_min_distance(self):
        distances = {
            'A': 0,
            'B': math.inf,
            'C': math.inf
        }
        unvisited_nodes = {'A', 'B', 'C'}
        self.assertEqual(TrainRoutes.get_min_distance(distances, unvisited_nodes), 'A')

    def test_get_min_distance_node_visited(self):
        distances = {
            'A': 0,
            'B': 1,
            'C': math.inf
        }
        unvisited_nodes = {'B', 'C'}
        self.assertEqual(TrainRoutes.get_min_distance(distances, unvisited_nodes), 'B')

    def test_find_shortest_path_exception_None_start_city(self):
        x = TrainRoutes(['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7'], [])
        self.assertRaises(Exception, x.find_shortest_path_between_cities, None, 'C')

    def test_find_shortest_path_exception_Blank_start_city(self):
        x = TrainRoutes(['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7'], [])
        self.assertRaises(Exception, x.find_shortest_path_between_cities, '', 'C')

    def test_find_shortest_path_exception_None_end_city(self):
        x = TrainRoutes(['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7'], [])
        self.assertRaises(Exception, x.find_shortest_path_between_cities, 'A', None)

    def test_find_shortest_path_exception_Blank_end_city(self):
        x = TrainRoutes(['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7'], [])
        self.assertRaises(Exception, x.find_shortest_path_between_cities, 'A', '')

    def test_find_shortest_path_success_different_city(self):
        x = TrainRoutes(['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7'], [])
        self.assertEqual(x.find_shortest_path_between_cities('A', 'C'), 9)

    def test_find_shortest_path_success_same_city(self):
        x = TrainRoutes(['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7'], [])
        self.assertEqual(x.find_shortest_path_between_cities('B', 'B'), 9)

    def test_find_shortest_path_no_route(self):
        x = TrainRoutes(['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7'], [])
        self.assertEqual(x.find_shortest_path_between_cities('B', 'A'), math.inf)

    def test_trips_hop_constraint_success_less_than(self):
        x = TrainRoutes(['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7'], [])
        self.assertEqual(len(x.trips_hop_constraint_bfs('C', 'C', 3)), 2)

    def test_trips_hop_constraint_success_equal(self):
        x = TrainRoutes(['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7'], [])
        self.assertEqual(len(x.trips_hop_constraint_bfs('C', 'C', 3, equal=True)), 1)

    def test_trips_hop_constraint_error_None_start_city(self):
        x = TrainRoutes(['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7'], [])
        self.assertRaises(Exception, x.trips_hop_constraint_bfs, None, 'C', 3, equal=True)

    def test_trips_hop_constraint_error_None_end_city(self):
        x = TrainRoutes(['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7'], [])
        self.assertRaises(Exception, x.trips_hop_constraint_bfs, 'A', None, 3, equal=True)

    def test_trips_hop_constraint_error_Blank_start_city(self):
        x = TrainRoutes(['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7'], [])
        self.assertRaises(Exception, x.trips_hop_constraint_bfs, '', 'C', 3, equal=True)

    def test_trips_hop_constraint_error_Blank_end_city(self):
        x = TrainRoutes(['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7'], [])
        self.assertRaises(Exception, x.trips_hop_constraint_bfs, 'A', '', 3, equal=True)

    def test_trips_distance_constraint_success(self):
        x = TrainRoutes(['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7'], [])
        self.assertEqual(len(x.trips_distance_constraint_bfs('C', 'C', 30)), 7)


if __name__ == '__main__':
    unittest.main()
