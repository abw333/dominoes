import common
import domino
import game_tree
import multiprocessing
import random

FIXED_MOVES = 5
SERIAL_DEPTH = 5
NUM_PROCESSES = 12

def run_bfs(node):
    node.bfs()
    return node

def all_possible_games(fixed_moves=FIXED_MOVES, serial_depth=SERIAL_DEPTH,
                       num_processes=NUM_PROCESSES):
    with common.stopwatch('Initializing random game'):
        game = domino.Game(skinny_board=True)

    with common.stopwatch('Playing {} moves at random'.format(fixed_moves)):
        for i in range(fixed_moves):
            moves = game.valid_moves()
            move = random.choice(moves)
            game.make_move(*move)

    with common.stopwatch('Initializing game tree'):
        root = game_tree.GameNode(game=game)

    with common.stopwatch('Running BFS to depth {} serially'.format(serial_depth)):
        root.bfs(max_depth=serial_depth, parent_pointers=True)
        nodes = list(root.leaf_nodes())

    with common.stopwatch('Running remaining BFS using {} processes'.format(num_processes)):
        with multiprocessing.Pool(num_processes) as pool:
            searched_nodes = pool.map(run_bfs, nodes)

    with common.stopwatch('Combining BFS results'):
        for i, node in enumerate(nodes):
            node.parent_node.children[node.parent_move] = searched_nodes[i]

    with common.stopwatch('Counting all possible games'):
        print(len(list(root.leaf_nodes())))

    return root

if __name__ == '__main__':
    all_possible_games()
