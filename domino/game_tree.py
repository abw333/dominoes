import copy
import os

class Node:
    def __init__(self, game=None, children=None, result=None,
                 parent_node=None, parent_move=None):
        if children is None:
            children = {}

        self.game = game
        self.children = children
        self.result = result
        self.parent_node = parent_node
        self.parent_move = parent_move

    def num_leaf_nodes(self):
        if not self.children:
            return 1

        return sum(child.num_leaf_nodes() for child in self.children.values())

def bfs_step(nodes):
    new_nodes = []

    def make_move(node, game, move):
        node.children[move] = Node(result=game.make_move(*move),
                                   parent_node=node, parent_move=move)
        if node.children[move].result is None:
            node.children[move].game = game
            new_nodes.append(node.children[move])

    for node in nodes:
        moves = node.game.valid_moves()
        for move in moves[:-1]:
            new_game = copy.deepcopy(node.game)
            make_move(node, new_game, move)

        make_move(node, node.game, moves[-1])

        node.game = None

    return new_nodes

def bfs(node):
    pid = os.getpid()
    nodes = [node]
    depth = 0

    while nodes:
        nodes = bfs_step(nodes)

        depth += 1
        print('Process {}, Depth {}: {} active games'.format(
                pid, depth, len(nodes)))

    return node
