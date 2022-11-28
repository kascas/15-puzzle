import math
import time


class Node:
    end_state = None
    width, height = 0, 0
    factor = 1.0

    def __init__(self, table: list, x: int = 0, y: int = 0, depth: int = 0, parent=None, direct=None) -> None:
        for i in range(len(table)):
            if i not in table:
                raise Exception('table\'s elements are not correct')
        self._table = table
        self._depth = depth
        self._parent = parent
        self._direct = direct
        self._x, self._y = x, y
        self._f = self._F()

    def __repr__(self):
        return str(self._table) + ' -> ' + str(self._f)

    def generate_nodes(self):
        table_list = []
        if self._x > 0:
            table_list.append(Node(self._move('l'), self._x - 1, self._y, self._depth + 1, self, 'l'))
        if self._x < self.width - 1:
            table_list.append(Node(self._move('r'), self._x + 1, self._y, self._depth + 1, self, 'r'))
        if self._y > 0:
            table_list.append(Node(self._move('u'), self._x, self._y - 1, self._depth + 1, self, 'u'))
        if self._y < self.height - 1:
            table_list.append(Node(self._move('d'), self._x, self._y + 1, self._depth + 1, self, 'd'))
        return table_list

    def _move(self, direction):
        new_table = self._table.copy()
        if direction == 'u':
            new_table[self._x + self._y * self.width], new_table[self._x + (self._y - 1) * self.width] = \
                new_table[self._x + (self._y - 1) * self.width], new_table[self._x + self._y * self.width]
        if direction == 'd':
            new_table[self._x + self._y * self.width], new_table[self._x + (self._y + 1) * self.width] = \
                new_table[self._x + (self._y + 1) * self.width], new_table[self._x + self._y * self.width]
        if direction == 'l':
            new_table[self._x + self._y * self.width], new_table[(self._x - 1) + self._y * self.width] = \
                new_table[(self._x - 1) + self._y * self.width], new_table[self._x + self._y * self.width]
        if direction == 'r':
            new_table[self._x + self._y * self.width], new_table[(self._x + 1) + self._y * self.width] = \
                new_table[(self._x + 1) + self._y * self.width], new_table[self._x + self._y * self.width]
        return new_table

    def _H(self, end_state):
        return Manhattan_distance(self._table, end_state)

    def _G(self):
        return self._depth

    def _F(self):
        return self.factor * self._H(end_state) + self._G()


def Manhattan_distance(a: list, b: list):
    # check length of two list
    a_len, b_len = len(a), len(b)
    if a_len != b_len:
        raise Exception('len(a) is not equal to len(b)')
    # Manhattan Distance
    a_index = [a.index(i) for i in range(1, a_len)]
    b_index = [b.index(i) for i in range(1, a_len)]
    total = 0
    for i in range(1, a_len):
        a_i_x, a_i_y = a_index[i - 1] % math.sqrt(a_len), a_index[i - 1] // math.sqrt(a_len)
        b_i_x, b_i_y = b_index[i - 1] % math.sqrt(a_len), b_index[i - 1] // math.sqrt(a_len)
        d = int(abs(a_i_x - b_i_x) + abs(a_i_y - b_i_y))
        total += d
    return total


def find_best_path(start_state, end_state):
    blank_pos = start_state.index(0)
    blank_x, blank_y = blank_pos % Node.width, blank_pos // Node.width
    Node.end_state = end_state
    root_node = Node(start_state, blank_x, blank_y, 0)
    opened_dict, closed_dict = {}, {}
    opened_dict[str(start_state)] = root_node
    start = time.perf_counter()
    while(1):
        if len(opened_dict) == 0:
            raise Exception('>>> No result <<<')
        f_dict = {opened_dict[table]._f: table for table in opened_dict}
        min_key = f_dict[min(f_dict.keys())]
        selected_node = opened_dict.pop(str(min_key))
        closed_dict[str(min_key)] = selected_node
        if selected_node._table == end_state:
            end = time.perf_counter()
            print('\ntime: {:.4f} s'.format(end - start))
            return selected_node
        new_nodes = selected_node.generate_nodes()
        for node in new_nodes:
            node_table = node._table
            node_key = str(node_table)
            # if node_key in opened_dict:
            #     if node._f>=opened_dict[node_key]._f:
            #         opened_dict[node_key]=node
            # if node_key not in opened_dict and node_key not in closed_dict:
            #     opened_dict[node_key] = node

            if node_key not in opened_dict and node_key not in closed_dict:
                opened_dict[node_key] = node
            else:
                if (node_key in opened_dict and node._f >= opened_dict[node_key]._f) or (node_key in closed_dict and node._f >= closed_dict[node_key]._f):
                    continue
                opened_dict[node_key] = node
                if node_key in closed_dict.keys():
                    closed_dict.pop(node_key)
        print('\ropen_list: {}, close_list: {}'.format(len(opened_dict),len(closed_dict)),end='')


if __name__ == '__main__':
    start_state = [11, 9, 4, 15, 1, 3, 0, 12, 7, 5, 8, 6, 13, 2, 10, 14]
    # start_state = [0, 15, 8, 3, 12, 11, 7, 4, 14, 10, 6, 5, 9, 13, 2, 1]
    # start_state = [0, 15, 8, 13, 12, 11, 3, 7, 14, 9, 6, 2, 4, 10, 5, 1]
    end_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]

    Node.factor = 1
    Node.width, Node.height = 4, 4

    final_node = find_best_path(start_state, end_state)
    path_list = []
    while(1):
        if final_node._direct == None:
            break
        path_list.insert(0, final_node._direct)
        final_node = final_node._parent
    print('path:', '-'.join(path_list), '\npath_len:', len(path_list))
