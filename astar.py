from bisect import insort
import copy


class Node:
    end_state = None
    width, height = 0, 0
    extend_num = 0

    def __init__(self, table: list, x: int = -1, y: int = -1, depth: int = 0, parent=None, direct=None) -> None:
        self.table = table
        self.depth = depth
        self.parent = parent
        self.direct = direct
        self.f = self.F()
        self.x, self.y = -1, -1
        self.id = '-'.join(map(str, table))
        if Node.width == Node.height == 0:
            Node.width, Node.height = len(table), len(table[0])
        if x != -1 and y != -1:
            self.x, self.y = x, y
        else:
            for i in range(Node.width):
                for j in range(Node.height):
                    if table[i][j] == 0:
                        self.x, self.y = i, j

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.f < other.f

    def extend(self):
        table_list = []
        if self.x > 0:
            table_list.append(Node(self.move('UP'), self.x - 1, self.y, self.depth + 1, self, 'UP'))
        if self.x < self.width - 1:
            table_list.append(Node(self.move('DOWN'), self.x + 1, self.y, self.depth + 1, self, 'DOWN'))
        if self.y > 0:
            table_list.append(Node(self.move('LEFT'), self.x, self.y - 1, self.depth + 1, self, 'LEFT'))
        if self.y < self.height - 1:
            table_list.append(Node(self.move('RIGHT'), self.x, self.y + 1, self.depth + 1, self, 'RIGHT'))
        Node.extend_num += len(table_list)
        return table_list

    def move(self, direct):
        new_table = copy.deepcopy(self.table)
        if direct == 'LEFT':
            new_table[self.x][self.y], new_table[self.x][self.y - 1] = new_table[self.x][self.y - 1], new_table[self.x][self.y]
        elif direct == 'RIGHT':
            new_table[self.x][self.y], new_table[self.x][self.y + 1] = new_table[self.x][self.y + 1], new_table[self.x][self.y]
        elif direct == 'UP':
            new_table[self.x][self.y], new_table[self.x - 1][self.y] = new_table[self.x - 1][self.y], new_table[self.x][self.y]
        elif direct == 'DOWN':
            new_table[self.x][self.y], new_table[self.x + 1][self.y] = new_table[self.x + 1][self.y], new_table[self.x][self.y]
        return new_table

    def F(self):
        return 5*M_dist(self.table, Node.end_state, Node.width, Node.height) + self.depth

    def is_end(self):
        return self.table == Node.end_state


def M_dist(a: list, b: list, width: int, height: int):
    a_dict, total = dict(), 0
    for i in range(width):
        for j in range(height):
            a_dict[a[i][j]] = (i, j)
    for i in range(width):
        for j in range(height):
            ax, ay = a_dict[b[i][j]]
            total += (abs(i - ax) + abs(j - ay))
    return total


def astar(start_state, end_state):
    root = Node(start_state, depth=0)
    Node.end_state = end_state
    opened_list, closed_list = [], []
    opened_dict, closed_dict = dict(), dict()
    # insert root node into open_list
    insort(opened_list, root)
    opened_dict[root.id] = root
    while True:
        # opened_list is empty means NoAnswer
        if len(opened_list) == 0:
            raise Exception('NoAnswer')
        current = opened_list.pop(0)
        opened_dict.pop(current.id)
        insort(closed_list, current)
        closed_dict[current.id] = current
        if current.is_end():
            return current
        nodes = current.extend()
        for node in nodes:
            if node.id not in closed_dict:
                if node.id not in opened_dict:
                    insort(opened_list, node)
                    opened_dict[node.id] = node
                else:
                    index = opened_list.index(node)
                    old = opened_list[index]
                    if node.f < old.f:
                        opened_list.pop(index)
                        insort(opened_list, node)
                        opened_dict[node.id] = node
            else:
                closed_list.remove(node)
                closed_dict.pop(node.id)
                insort(opened_list, node)
                opened_dict[node.id] = node
        print('\ropen_list: {}, close_list: {}, extened: {}'.format(len(opened_list), len(closed_list), Node.extend_num), end='')


def get_path(final_node):
    path_list = []
    while (1):
        if final_node.direct == None:
            path_list.insert(0, [final_node.table, 'INIT'])
            break
        path_list.insert(0, [final_node.table, final_node.direct])
        final_node = final_node.parent
    return path_list


def print_path(path_list):
    print('\n\nNum of Steps:', len(path_list) - 1)
    print('\n\nNum of Extended Nodes:', Node.extend_num)
    for path in path_list:
        p, d = path
        print('\n{:5s} --------------\n'.format(d))
        for i in range(len(start_state)):
            for j in range(len(start_state[0])):
                print('{:4d}'.format(p[i][j]), end='')
            print()
    return


if __name__ == '__main__':
    start_state = [[11, 9, 4, 15], [1, 3, 0, 12], [7, 5, 8, 6], [13, 2, 10, 14]] # ppt
    # start_state = [[2, 5, 4, 8], [1, 7, 0, 3], [10, 6, 15, 14], [9, 13, 12, 11]]  # very hard
    # start_state = [[5, 1, 2, 4], [9, 6, 3, 8], [13, 15, 10, 11], [0, 14, 7, 12]]  # hard
    end_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

    # start_state = [[2, 8, 3], [1, 0, 4], [7, 6, 5]]
    # end_state = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]

    final_node = astar(start_state, end_state)
    path_list = get_path(final_node)
    print_path(path_list)
