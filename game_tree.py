import copy
import numpy
import os

class GameNode:
    def __init__(self, game=None, children=None,
                 depth=0, result=None, optimal_move=None,
                 parent_node=None, parent_move=None):
        if children is None:
            children = {}

        self.game = game
        self.children = children
        self.depth = depth
        self.result = result
        self.optimal_move = optimal_move
        self.parent_node = parent_node
        self.parent_move = parent_move

    def leaf_nodes(self):
        if not self.children:
            yield self

        for child in self.children.values():
            for leaf_node in child.leaf_nodes():
                yield leaf_node

    def bfs(self, max_depth=numpy.inf, parent_pointers=False):
        pid = os.getpid()
        nodes = [self]
        depth = self.depth

        while nodes and depth < max_depth:
            new_nodes = []
            depth += 1

            def make_move(node, game, move):
                if parent_pointers:
                    parent_node = node
                    parent_move = move
                else:
                    parent_node = None
                    parent_move = None

                node.children[move] = GameNode(result=game.make_move(*move),
                                               depth=depth,
                                               parent_node=parent_node,
                                               parent_move=parent_move)
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

            nodes = new_nodes

            print('Process {}, Depth {}: {} active games'.format(
                    pid, depth, len(nodes)))

    def minimax(self):
        if self.result is None:
            if self.depth % 2:
                self.optimal_move = min(self.children,
                                        key=lambda move: self.children[move].minimax()[1][2])
            else:
                self.optimal_move = max(self.children,
                                        key=lambda move: self.children[move].minimax()[1][2])

            self.result = self.children[self.optimal_move].result

        return self.optimal_move, self.result
