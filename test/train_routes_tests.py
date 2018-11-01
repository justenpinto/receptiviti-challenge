from src.train_routes import *
import argparse
import unittest


class TrainRouteTests(unittest.TestCase):
    def setUp(self):
        pass

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


if __name__ == '__main__':
    unittest.main()
