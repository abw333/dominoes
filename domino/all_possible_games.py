import common
import domino
import game_tree
import multiprocessing
import random

FIXED_MOVES = 5
SERIAL_DEPTH = 3

def run_bfs(node):
    node.bfs()
    return node

with common.stopwatch('Initializing random game'):
    game = domino.Game(skinny_board=True)

    for i in range(FIXED_MOVES):
        moves = game.valid_moves()
        move = random.choice(moves)
        game.make_move(*move)

    root = game_tree.Node(game=game)
    nodes = [root]

with common.stopwatch('Computation of all possible games'):
    for i in range(SERIAL_DEPTH):
        nodes = game_tree.bfs_step(nodes)

    with multiprocessing.Pool(len(nodes)) as pool:
        searched_nodes = pool.map(run_bfs, nodes)

    for i, node in enumerate(nodes):
        node.parent_node.children[node.parent_move] = searched_nodes[i]

with common.stopwatch('Counting all possible games'):
    print(root.num_leaf_nodes())
