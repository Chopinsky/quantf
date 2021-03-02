import copy


# The idea is that the times matrix gives us a graph, and the goal is to travel
# from start (i.e. vertex #0) to end (i.e. vertex #(self.v-1)) within the time
# limit, and going through the most number of the vertices in between. Using the
# Bellman-Ford algo to build the graph, and calculate the path.
class Graph:
    def __init__(self, matrix):
        # save the graph, self.graph[u][v] is the cost to travel from vertex #u
        # to #v.
        self.graph = matrix
        self.v = len(matrix)

        # init the distance table, where self.dist[u][v] is the distance (i.e.
        # the time cost) to travel between vertex #u and #v.
        self.inf = float("Inf")
        self.dist = [[self.inf for _ in range(self.v)] for _ in range(self.v)]

    # calculate the distance from src vertex to all other (reachable) vertices;
    # also check if there is a negative cycle passing through src
    def calc_dist_from_src(self, src):
        # vertex to self is always 0
        self.dist[src][src] = 0

        # relax all edges for self.v-1 times, to find the shortest path from
        # src all to other vertices, since we can have at most self.v-1 edges,
        # the 1 ~ self.v-1 runs should find the shortest path, based on the
        # Bellman-Ford algo we use here
        for _ in range(self.v - 1):
            for u in range(self.v):
                for v in range(self.v):
                    # if a src->u path exists, and src->u + u->v is shorter than src->v (which may not
                    # exist at the moment, hence dist == inf), update to use the shorter path
                    if self.dist[src][u] != self.inf and self.dist[src][u] + self.graph[u][v] < self.dist[src][v]:
                        # this may update src->src, essentially creating a negative weight cycle involving
                        # vertex #src
                        self.dist[src][v] = self.dist[src][u] + self.graph[u][v]

        # check for negative weight cycles: we should have already found the shortest path
        # between src and v based on Bellman-Ford algo, if we can still spot a "shorter" path
        # at the moment, it means a negative weight path exists between src->v, and we can
        # hoop on this loop to gain enough time to free all bunnies
        for u in range(self.v):
            for v in range(self.v):
                if self.dist[src][u] != self.inf and self.dist[src][u] + self.graph[u][v] < self.dist[src][v]:
                    return False

        return True

    # check if the graph contains a negative cycle -- if so, we can keep routing
    # around the negative cycle to gain enough time to rescue all bunnies.
    def build_graph(self):
        for v in range(self.v):
            if not self.calc_dist_from_src(v):
                return False

        return True

    def get_path(self, start, goal, time):
        paths = []
        stack = [(start, [start], time, [[i] for i in range(self.v)])]
        vertices = set(range(self.v))
        done = False

        while len(stack) > 0 and not done:
            # get next vertex for the traverse, cycles will contain vertices that
            # could form a cycle route without gaining more bunnies (i.e. rounding
            # back to the start point, vertex #v)
            (u, path, time_left, cycles) = stack.pop()

            for v in (vertices - set(cycles[u])):
                # save to variables
                u_to_v = self.dist[u][v]
                v_to_door = self.dist[v][goal]
                v_to_u = self.dist[v][u]
                next_cycles = copy.deepcopy(cycles)

                # if the route of u -> v -> u costs 0 time, it's forming a cycle and
                # needs to be excluded from getting into future iterations when we're
                # at either u or v again (for generating future routes)
                if u_to_v + v_to_u == 0:
                    next_cycles[v].append(u)
                    next_cycles[u].append(v)

                # find the time for the route: u -> v -> door, if we have time left
                # when reaching the door, we can escape; otherwise, unusable route,
                # moving on to other open choices.
                time_remain = time_left - u_to_v - v_to_door
                if time_remain >= 0:
                    # hopping on to v, add the vertex to the path leading to the vertex,
                    # and update: append the vertex to generate the path so far
                    next_path = path + [v]

                    # push the tuple into the path candidate queue
                    stack.append((v, next_path, time_left - u_to_v, next_cycles))

                    # if we have reached the goal, this is a possible solution, save it
                    # off
                    if v == goal:
                        # flatten the path, only take 1 vertex each time -- aka the bunny
                        # that is saved, plus start + door (which will be filtered out
                        # later)
                        freed = set(next_path)
                        paths.append(freed)

                        # found the path that will save all bunnies, done, stop
                        if len(freed) == self.v:
                            done = True
                            break

        return paths

    def print(self):
        print(self.dist, self.v)


def rescue_list(times, limit):
    # init the graph from the time matrix
    g = Graph(times)
    max_freed = set([])

    # no bunny in the graph to rescue
    if g.v < 3:
        return []

    if g.build_graph():
        for freed in g.get_path(0, g.v-1, limit):
            # get rescued bunny count
            max_count = len(max_freed)
            curr_count = len(freed)

            # if this route can rescue more bunnies, or the bunnies have smaller
            # IDs, use this route and the bunnies rescued along the way
            if max_count < curr_count or (max_count == curr_count and sum(max_freed) > sum(freed)):
                max_freed = freed
    else:
        # there exists a negative cycle, we can use it to gain enough time to
        # rescue all bunnies, hence result is [0, 1, ..., last_bunny]
        return range(g.v-2)

    # print("solution:", sorted(max_freed - {0, g.v-1}))
    # return list(map(lambda x: x-1, sorted(max_freed - {0, g.v-1})))

    answer = sorted(max_freed - {0, g.v-1})
    for i in range(len(answer)):
        answer[i] -= 1

    return answer


def test():
    tests = [
        [
            [
                [0, 2, 2, 2, -1],
                [9, 0, 2, 2, -1],
                [9, 3, 0, 2, -1],
                [9, 3, 2, 0, -1],
                [9, 3, 2, 2, 0]
            ],
            1,
            [1, 2]
        ],
        [
            [
                [0, 1, 1, 1, 1],
                [1, 0, 1, 1, 1],
                [1, 1, 0, 1, 1],
                [1, 1, 1, 0, 1],
                [1, 1, 1, 1, 0]
            ],
            3,
            [0, 1]
        ]
    ]

    for i in range(len(tests)):
        m, t = tests[i][0], tests[i][1]
        ans = rescue_list(m, t)
        print(f"test {i}:\n\texpected: {tests[i][2]}\n\tfound: {ans}\n")
