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

    def get_parent(self):
        return self._parent

    def set_parent(self, parent):
        self._parent = parent

    def get_table(self):
        return self._table

    def set_table(self, table):
        self._table = table

    def get_depth(self):
        return self._depth

    def set_depth(self, depth):
        self._depth = depth

    def reset_f(self):
        self._F()

    def get_f(self):
        return self._f

    def get_direction(self):
        return self._direct

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

    def compare_node(self, node):
        if self.get_table() == node.get_table():
            return True
        else:
            return False

    def compare_table(self, table):
        if self.get_table() == table:
            return True
        else:
            return False

    def _H(self, end_state):
        return Manhattan_distance(self.get_table(), end_state)

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
    start = time.perf_counter()
    blank_pos = start_state.index(0)
    blank_x, blank_y = blank_pos % Node.width, blank_pos // Node.width
    Node.end_state = end_state
    root_node = Node(start_state, blank_x, blank_y, 0)
    opened_dict, closed_dict = {}, {}
    opened_dict[str(start_state)] = root_node
    while(1):
        if len(opened_dict) == 0:
            raise Exception('>>> No result <<<')
        f_dict = {opened_dict[table].get_f(): table for table in opened_dict}
        min_key = f_dict[min(f_dict.keys())]
        selected_node = opened_dict.pop(str(min_key))
        closed_dict[str(min_key)] = selected_node
        if selected_node.compare_table(end_state):
            end = time.perf_counter()
            print('time: {:.4f} s'.format(end - start))
            return selected_node
        new_nodes = selected_node.generate_nodes()
        for node in new_nodes:
            node_table = node.get_table()
            node_key = str(node_table)
            # if node_key in opened_dict:
            #     if node.get_f()>=opened_dict[node_key].get_f():
            #         opened_dict[node_key]=node
            # if node_key not in opened_dict and node_key not in closed_dict:
            #     opened_dict[node_key] = node

            if node_key not in opened_dict and node_key not in closed_dict:
                opened_dict[node_key] = node
            else:
                if (node_key in opened_dict and node.get_f() >= opened_dict[node_key].get_f()) or (node_key in closed_dict and node.get_f() >= closed_dict[node_key].get_f()):
                    continue
                opened_dict[node_key] = node
                if node_key in closed_dict.keys():
                    closed_dict.pop(node_key)


if __name__ == '__main__':
    start_state = [11, 9, 4, 15, 1, 3, 0, 12, 7, 5, 8, 6, 13, 2, 10, 14]
    end_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]

    # start_state = [2, 8, 3, 1, 0, 4, 7, 6, 5]
    # end_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]

    Node.factor = 1.5
    Node.width, Node.height = 4, 4

    final_node = find_best_path(start_state, end_state)
    path_list = []
    while(1):
        if final_node.get_direction() == None:
            break
        path_list.insert(0, final_node.get_direction())
        final_node = final_node.get_parent()
    print('path:', '-'.join(path_list), '\npath_len:', len(path_list))
