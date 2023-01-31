"""
file: ice_maze.py
This file contains an application that uses a graph to escape an ice maze
author: Athina Stewart
"""

import sys

FIRST_LINE = ""
GRID_HEIGHT = ""
GRID_WIDTH = ""
ESCAPE_ROW = ""
LINES = []
NO_PATH = []
ROCK_LOCATIONS = []


class Vertex:
    __slots__ = "name", "prev", "neighbours", "visited"

    def __init__(self, name=list) -> None:
        """
        Create a new vertex and optionally link it to an existing one.
        :param: name: the value to be stored in the new vertex
        :param: prev: the vertex linked to this one
        :param: neighbours: the value to be stored in the new node
        :param: visited: boolean value to record if a vertex has been visited
        """
        self.name = name
        self.prev = None
        self.neighbours = []
        self.visited = False

    def __repr__(self):
        """
        Return a string representation of the vertex
        :return: string representation of the vertex
        """
        return f"[{self.name[0]}, {self.name[1]}]"

    def __str__(self):
        """
        Return a string representation of the contents of
        this vertex.
        :return: string representation of the vertex
        """
        return f"[{self.name[0]}, {self.name[1]}]"

    def add_vertex_neighbour(self, Vertex):
        """
        Add a neighbour to an existing vertex
        """
        self.neighbours.append(Vertex)


class Solve:

    __slots__ = "start", "end"

    def __init__(self, start, end):
        """
        Create a new graph
        param start: the starting vertex
        param end: the ending node
        """
        self.start = start
        self.end = end
        check = False

    def check_exit(self):
        """
        This checks whether there is a rock in the exit. If this is true,
        the ice maze cannot be escaped and the program will end
        """
        check = False
        for rock in ROCK_LOCATIONS:
            if self.end.name == rock:
                check = True
        if check:
            print("There is a rock in exit of the ice maze and so there is no "
                  "escape.\nGood Bye!")
            exit()

    def search(self):
        """
        This method builds and searches the graph for the shortest path
        between the starting vertex and end vertex
        :return: the shortest path between start and end squares or a path
                    that begins at the start but does not end at the end
                    square
        """
        self.check_exit()
        self.start.visited = True
        queue = [self.start]
        current_node_list = []

        while queue:
            current_node = queue[0]
            if current_node.name == self.end.name:
                # if the current node is the exit node then the loop breaks
                # because a path has been found
                queue.clear()
                break
            current_node_list.append(current_node)
            queue = queue[1:]
            find_neighbours(current_node)
            for vertex in current_node.neighbours:
                for element in current_node_list:
                    if vertex.name == element.name:
                        vertex.visited = True
                if not vertex.visited:
                    if len(queue) == 0 and current_node.neighbours:
                        # if the current vertex has no neighbours then there
                        # are no more unvisited nodes and the nothing else will
                        # be added to the queue
                        queue.append(vertex)
                    for element in queue:
                        if vertex.name == element.name:
                            check = True
                            # a marker to tell if the element is already in the queue
                            # so that it won't be added again
                        if check is False:
                            queue.append(vertex)
                            check = True
                    check = False
                    vertex.visited = True
                    vertex.prev = current_node
        return self.build_path(current_node)

    def build_path(self, current_node):
        """
        This method returns the path in reverse order. If there is only one
        vertex in the path (if the starting square is at the escape), then the
        vertex is added to the path twice to account for the appropriate number
        of steps to escape (which would be 1). If the current path ends at any
        other square than the end square, it is added to a NO_PATH array
        :param: current_node: the vertex that has a connection between the start
                            and an end square
        :return: returns the shortest path between start and end node or does not
                return anything if there is no path. Instead, the start square
                is recorded in a no path array
        """
        temp_end = self.end
        self.end = current_node
        shortest_route = []
        while self.end:
            shortest_route.append(self.end)
            self.end = self.end.prev
        shortest_route.reverse()
        if current_node.name != temp_end.name:
            # if the current node is not the exit node then this means that
            # a path has not been found and the loop ended because the
            # current node had no more neighbours
            NO_PATH.append(shortest_route[0])
            return
        elif len(shortest_route) == 1 and shortest_route[0].name \
                == temp_end.name:
            temp_list = []
            temp_list.append(temp_end)
            temp_list.append(temp_end)
            shortest_route = temp_list
        return shortest_route


def find_Rock_Locations():
    global ROCK_LOCATIONS
    """
    This method returns the location of the rocks in the ice maze
    :return: rock locations
    """
    global GRID_WIDTH
    x = 0
    y = 0
    new_lines_list = []
    for line in LINES:
        new_line = line.replace(" ", "")
        new_lines_list.append(new_line)

    for element in new_lines_list:
        for item in element:
            if item == '*':
                ROCK_LOCATIONS.append([x % int(GRID_WIDTH), y])
            x = x + 1
        y = y + 1
    return ROCK_LOCATIONS


def find_right_neighbour(node=list):
    """
    This method returns the right neighbour of a vertex
    :param: vertex of which right neighbour will be found
    :return: right neighbour of vertex
    """
    global GRID_WIDTH
    beginning = []
    for element in node.name:
        beginning.append(element)
    for rock in ROCK_LOCATIONS:
        checker = False
        if rock[1] == beginning[1]:
            # first check if there is a rock in the row
            while beginning != rock:
                # check to make sure the starting point is not a rock
                x_coordinate = beginning[0]
                if beginning[0] < int(GRID_WIDTH) - 1:
                    x_coordinate = int(x_coordinate + 1)
                beginning[0] = x_coordinate
                for other_rock in ROCK_LOCATIONS:
                    # if there is more than one rock in the row, check to make
                    # the new beginning square is also not a rock
                    if beginning == other_rock:
                        checker = True
                if checker:
                    # if rock is in the line then the neighbour will be one
                    # space before the rock
                    x_coordinate = beginning[0]
                    x_coordinate = int(x_coordinate - 1)
                    beginning[0] = x_coordinate
                    if beginning == node.name:
                        return
                    else:
                        return Vertex(beginning)
                if beginning[0] == int(GRID_WIDTH) - 1:
                    if beginning == node.name:
                        return
                    else:
                        return Vertex(beginning)
        if rock == ROCK_LOCATIONS[(len(ROCK_LOCATIONS) - 1)]:  # if no rock is in the line
            x_coordinate = beginning[0]
            while x_coordinate < int(GRID_WIDTH) - 1:
                x_coordinate = int(x_coordinate + 1)
                beginning[0] = x_coordinate
            if beginning == node.name:
                return
            else:
                return Vertex(beginning)


def find_bottom_neighbour(node=list):
    """
    This method returns the bottom neighbour of a vertex
    :param: vertex of which bottom neighbour will be found
    :return: bottom neighbour of vertex
    """
    # the logic for finding the bottom, left and top neighbours mirrors
    # the logic for finding the right neighbour
    global GRID_WIDTH
    beginning = []
    for element in node.name:
        beginning.append(element)
    for rock in ROCK_LOCATIONS:
        checker = False
        if rock[0] == beginning[0]:
            # first check if there is a rock in the column
            while beginning != rock:
                y_coordinate = beginning[1]
                if beginning[1] < int(GRID_HEIGHT) - 1:
                    y_coordinate = int(y_coordinate + 1)
                beginning[1] = y_coordinate
                for other_rock in ROCK_LOCATIONS:
                    if beginning == other_rock:
                        checker = True
                if checker:
                    y_coordinate = beginning[1]
                    y_coordinate = int(y_coordinate - 1)
                    beginning[1] = y_coordinate
                    if beginning == node.name:
                        return
                    else:
                        return Vertex(beginning)
                if beginning[1] == int(GRID_HEIGHT) - 1:
                    if beginning == node.name:
                        return
                    else:
                        return Vertex(beginning)
        if rock == ROCK_LOCATIONS[(len(ROCK_LOCATIONS) - 1)]:  # if no rock is in the line
            y_coordinate = beginning[1]
            while y_coordinate < int(GRID_HEIGHT) - 1:
                y_coordinate = int(y_coordinate + 1)
                beginning[1] = y_coordinate
            if beginning == node.name:
                return
            else:
                return Vertex(beginning)


def find_left_neighbour(node=list):
    """
    This method returns the left neighbour of a vertex
    :param: vertex of which left neighbour will be found
    :return: left neighbour of vertex
    """
    beginning = []
    for element in node.name:
        beginning.append(element)
    # if rock is in the line then the neighbour will be one space before the rock
    for rock in ROCK_LOCATIONS:
        checker = False
        if rock[1] == beginning[1]:
            while beginning != rock:
                x_coordinate = beginning[0]
                if beginning[0] > 0:
                    x_coordinate = int(x_coordinate - 1)
                beginning[0] = x_coordinate
                for other_rock in ROCK_LOCATIONS:
                    if beginning == other_rock:
                        checker = True
                if checker:
                    x_coordinate = beginning[0]
                    x_coordinate = int(x_coordinate + 1)
                    beginning[0] = x_coordinate
                    if beginning == node.name:
                        return
                    else:
                        return Vertex(beginning)
                if beginning[0] == 0:
                    if beginning == node.name:
                        return
                    else:
                        return Vertex(beginning)
        if rock == ROCK_LOCATIONS[(len(ROCK_LOCATIONS) - 1)]:  # if no rock is in the line
            x_coordinate = beginning[0]
            while x_coordinate > 0:
                x_coordinate = int(x_coordinate - 1)
                beginning[0] = x_coordinate
            if beginning == node.name:
                return
            else:
                return Vertex(beginning)


def find_top_neighbour(node=list):
    """
    This method returns the top neighbour of a vertex
    :param: vertex of which top neighbour will be found
    :return: top neighbour of vertex
    """
    beginning = []
    for element in node.name:
        beginning.append(element)
    # if rock is in the line then the neighbour will be one space before the rock
    for rock in ROCK_LOCATIONS:
        checker = False
        if rock[0] == beginning[0]:
            while beginning != rock:
                y_coordinate = beginning[1]
                if beginning[1] > 0:
                    y_coordinate = int(y_coordinate - 1)
                beginning[1] = y_coordinate
                for other_rock in ROCK_LOCATIONS:
                    if beginning == other_rock:
                        checker = True
                if checker:
                    y_coordinate = beginning[1]
                    y_coordinate = int(y_coordinate + 1)
                    beginning[1] = y_coordinate
                    if beginning == node.name:
                        return
                    else:
                        return Vertex(beginning)
                if beginning[1] == 0:
                    if beginning == node.name:
                        return
                    else:
                        return Vertex(beginning)
        if rock == ROCK_LOCATIONS[(len(ROCK_LOCATIONS) - 1)]:  # if no rock is in the line
            y_coordinate = beginning[1]
            while y_coordinate > 0:
                y_coordinate = int(y_coordinate - 1)
                beginning[1] = y_coordinate
            if beginning == node.name:
                return
            else:
                return Vertex(beginning)


def find_neighbours(Vertex):
    """
    This method returns the neighbours of a given vertex in all direction
    :param: vertex of which neighbours will be found
    :return: neighbours of vertex in clockwise direction
    """
    a = find_right_neighbour(Vertex)
    b = find_bottom_neighbour(Vertex)
    c = find_left_neighbour(Vertex)
    d = find_top_neighbour(Vertex)
    neighbours = [a, b, c, d]
    for element in neighbours:
        if element != Vertex and element is not None:
            Vertex.add_vertex_neighbour(element)
    return Vertex


def read_file(file):
    """
    This method reads in the ice maze file and stores each line in an array
    :return: None
    """
    global GRID_WIDTH
    global GRID_HEIGHT
    global ESCAPE_ROW
    global LINES
    """
    This method reads in the mobile file and stores each line in an array
    :return: None
    """
    global FIRST_LINE
    LINES = []
    try:
        with open(file) as f:
            FIRST_LINE = f.readline()
            for line in f:
                if line == '\n':
                    break
                LINES.append(line.strip())
        GRID_HEIGHT = FIRST_LINE[0]
        GRID_WIDTH = FIRST_LINE[2]
        ESCAPE_ROW = FIRST_LINE[4]
        return LINES
    except IOError:
        print("File not found: ")
        exit()


def check_all_squares():
    """
    This method finds the shortest path among all squares in the maze
    and the end square (it is assumed that rock locations cannot be
    starting squares)
    :param: vertex of which right neighbour will be found
    :return: right neighbour of vertex
    """
    read_file(sys.argv[1])
    end = [int(GRID_WIDTH) - 1, int(ESCAPE_ROW)]
    solutions = []
    rock_locations = find_Rock_Locations()
    for i in range(int(GRID_WIDTH)):
        for j in range(int(GRID_HEIGHT)):
            checker = False
            for rock in rock_locations:
                # check to avoid using a rock location as a starting square
                if [i, j] == rock:
                    checker = True
            if not checker:
                path = (Solve(Vertex([i, j]), Vertex(end)).search())
                if path is not None:
                    solutions.append(path)
    print_results(solutions)


def print_results(solutions):
    """
    This method prints out the squares in the order of the number of moves
    it took to get from that square to the end square. The squares for which
    no path was found are represented in a NO_PATH array
    """
    solutions_count = []
    solutions_frequency = []
    if len(solutions) == 0:
        print(f"No path: {NO_PATH}")
    else:
        for solution in solutions:
            solutions_count.append([solution[0], (len(solution) - 1)])
            solutions_frequency.append((len(solution) - 1))
        start_square_and_count = [["" for x in range(1)] for y in
                                  range(max(solutions_frequency))]
        for i in range(len(start_square_and_count)):
            start_square_and_count[i].remove("")
        for i in range(max(solutions_frequency) + 1):
            for solution in solutions_count:
                if solution[1] == i:
                    start_square_and_count[i-1].append(solution[0])

        for i in range(max(solutions_frequency)):
            print(f"{i+1}: {start_square_and_count[i]}")
        print(f"No path: {NO_PATH}")


def main() -> None:
    """
    This is the main method
    """
    global GRID_WIDTH
    global GRID_HEIGHT
    global ESCAPE_ROW
    if len(sys.argv) != 2:
        print("Usage: python mobile <ice-maze-file>")
        exit()
    else:
        check_all_squares()


if __name__ == '__main__':
    main()
