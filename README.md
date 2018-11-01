# Receptiviti Challenge

## The Problem

A local commuter railroad services a number of towns in
Kiwiland.  Because of monetary concerns, all of the tracks are 'one-way.'
That is, a route from Kaitaia to Invercargill does not imply the existence
of a route from Invercargill to Kaitaia.  In fact, even if both of these
routes do happen to exist, they are distinct and are not necessarily the
same distance!

The purpose of this problem is to help the railroad provide its customers
with information about the routes.  In particular, you will compute the
distance along a certain route, the number of different routes between two
towns, and the shortest route between two towns.

Input:  A directed graph where a node represents a town and an edge
represents a route between two towns.  The weighting of the edge represents
the distance between the two towns.  A given route will never appear more
than once, and for a given route, the starting and ending town will not be
the same town.

Output: For test input 1 through 5, if no such route exists, output 'NO
SUCH ROUTE'.  Otherwise, follow the route as given; do not make any extra
stops!  For example, the first problem means to start at city A, then
travel directly to city B (a distance of 5), then directly to city C (a
distance of 4).

1. The distance of the route A-B-C.
2. The distance of the route A-D.
3. The distance of the route A-D-C.
4. The distance of the route A-E-B-C-D.
5. The distance of the route A-E-D.
6. The number of trips starting at C and ending at C with a maximum of 3
stops.  In the sample data below, there are two such trips: C-D-C (2
stops). and C-E-B-C (3 stops).
7. The number of trips starting at A and ending at C with exactly 4 stops.
In the sample data below, there are three such trips: A to C (via B,C,D); A
to C (via D,C,D); and A to C (via D,E,B).
8. The length of the shortest route (in terms of distance to travel) from A
to C.
9. The length of the shortest route (in terms of distance to travel) from B
to B.
10. The number of different routes from C to C with a distance of less than 30.  In the sample data, the trips are: CDC, CEBC, CEBCDC, CDCEBC, CDEBC,
CEBCEBC, CEBCEBCEBC.

Test Input:

For the test input, the towns are named using the first few letters of the
alphabet from A to D.  A route between two towns (A to B) with a distance
of 5 is represented as AB5.

Graph: AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7

Expected Output:

Output #1: 9

Output #2: 5

Output #3: 13

Output #4: 22

Output #5: NO SUCH ROUTE

Output #6: 2

Output #7: 3

Output #8: 9

Output #9: 9

Output #10: 7

## Usage
Because no input type was defined in the program, all data used in the program is provided as arguments to program.

To see what the arguments are for the program, run the following:
```buildoutcfg
python train_routes.py -h
```

This produces the following:

```buildoutcfg
usage: train_routes.py [-h] --graphdata GRAPHDATA [GRAPHDATA ...] --testcases
                       TESTCASES [TESTCASES ...]

optional arguments:
  -h, --help            show this help message and exit
  --graphdata GRAPHDATA [GRAPHDATA ...]
                        Specify cities and distance as space separated string.
                        E.g. AB5 BC5 CD5
  --testcases TESTCASES [TESTCASES ...]
                        List of test cases to perform. See documentation for
                        formatting.
```

The ```--testcases``` argument is formatted as such: {TestCaseName}:{Args}.

There are five types of test cases:

1. RouteDistance - gets total distance for route. Format: "RouteDistance:A-D-C".
2. RouteShortest - gets shortest distance between two cities. Format: "RouteShortest:A|C"
3. RouteLessThanHops - gets all paths with hops less than or equal to. Format: "RouteLessThanHops:C|C|3"
4. RouteEqualHops - gets all paths with hops equal to specified value. Format: "RouteEqualHops:A|C|4"
5. RouteLessThanDistance - gets all paths with distance less than specified value (from start_city to end_city). 
Format: "RouteLessThanDistance:C|C|30".

Here is what should be run to mirror the test cases provided:

```
python train_routes.py --graphdata AB5 BC4 CD8 DC8 DE6 AD5 CE2 EB3 AE7 --testcases RouteDistance:A-B-C RouteDistance:A-D RouteDistance:A-D-C RouteDistance:A-E-B-C-D RouteDistance:A-E-D RouteLessThanHops:C|C|3 RouteEqualHops:A|C|4 RouteShortest:A|C RouteShortest:B|B RouteLessThanDistance:C|C|30
```

The expect output has been slightly modified to be more verbose. Here is the output from the provided test cases:

```
Running test case #1
A-B-C distance: 9

Running test case #2
A-D distance: 5

Running test case #3
A-D-C distance: 13

Running test case #4
A-E-B-C-D distance: 22

Running test case #5
A-E-D distance: NO SUCH ROUTE

Running test case #6
Paths between C and C with hops less than or equal to 3: 2 (['C-D-C (2 hops)', 'C-E-B-C (3 hops)'])

Running test case #7
Paths between A and C with hops equal to 4: 3 (['A-B-C-D-C (4 hops)', 'A-D-C-D-C (4 hops)', 'A-D-E-B-C (4 hops)'])

Running test case #8
Shortest distance between A and C: 9

Running test case #9
Shortest distance between B and B: 9

Running test case #10
Paths between C and C with distance less than 30: 7 (['C-D-C (16 distance)', 'C-E-B-C (9 distance)', 'C-D-E-B-C (21 distance)', 'C-D-C-E-B-C (25 distance)', 'C-E-B-C-D-C (25 distance)', 'C-E-B-C-E-B-C (18 distance)', 'C-E-B-C-E-B-C-E-B-C (27 distance)'])
```