from sys import exit


def digit_size(num):
    return len(str(num))


def print_board(rep):
    print_frame()

    for row in range(board_dimensions[0], 0, -1):
        print(f'{" " * (max_number_size - digit_size(row))}{row}|', *rep[row - 1], '|')

    print_frame()

    line = ' ' * (max_number_size + cell_size + 1)
    for x in range(1, board_dimensions[1] + 1):
        line += str(x) + ' ' * (cell_size + 1 - digit_size(x + 1))
    print(line)


def print_frame():
    print(' ' * max_number_size, '-' * (3 + cell_size * board_dimensions[1] + board_dimensions[1]), sep='')


def get_dimensions():
    while True:
        s = input('Enter your board dimensions (columns, rows):').split()
        try:
            cols = int(s[0])
            rows = int(s[1])
            if cols > 0 and rows > 0:
                return rows, cols
            else:
                print('Invalid dimensions!')
        except (ValueError, IndexError):
            print('Invalid dimensions!')


def get_knight_pos(possible_moves: list[tuple[int, int]] = tuple(), first_time=False):
    if first_time:
        prompt = "Enter the knight's starting position (column, row):"
    else:
        prompt = "Enter your next move:"

    while True:
        s = input(prompt).split()
        try:
            col = int(s[0]) - 1
            row = int(s[1]) - 1
            if is_valid(row, col) and (first_time or (row, col) in possible_moves):
                return row, col
            else:
                print('Invalid position!', end='')
        except (ValueError, IndexError):
            print('Invalid position!', end='')


def get_players_choice():
    while True:
        s = input('Do you want to try the puzzle? (y/n):')
        if len(s) > 0:
            if s.lower() == 'y':
                return True
            elif s.lower() == 'n':
                return False
        print('Invalid option')


def get_mode():
    while True:
        print('Complete searches can take a long time')
        s = input('Do you want to execute a complete search? (y/n):')
        if len(s) > 0:
            if s.lower() == 'y':
                return True
            elif s.lower() == 'n':
                return False
        print('Invalid option')


def generate_board():
    board = []
    line_sample = [''] * board_dimensions[1]
    for x in range(board_dimensions[0]):
        board.append(line_sample.copy())
    return board


def generate_board_rep(knight_pos: tuple[int, int], possible_moves: list[tuple[int, int]],
                       moves: list[tuple[int, int]]):
    result = generate_board()

    for r in range(board_dimensions[0]):
        for c in range(board_dimensions[1]):
            if (r, c) == knight_pos:
                result[r][c] = ' ' * (cell_size - 1) + 'X'
            elif (r, c) in possible_moves:
                result[r][c] = ' ' * (cell_size - 1) + str(num_possible_moves(r, c, moves))
            elif (r, c) in moves:
                result[r][c] = ' ' * (cell_size - 1) + '*'
            else:
                result[r][c] = '_' * cell_size
    return result


def num_possible_moves(knight_row: int, knight_col: int, moves: list[tuple[int, int]]):
    return len(generate_possible_moves(knight_row, knight_col, moves))


def generate_possible_moves(knight_row: int, knight_col: int, moves: list[tuple[int, int]]):
    all_moves = ((knight_row + 1, knight_col + 2), (knight_row + 2, knight_col + 1),
                 (knight_row - 1, knight_col + 2), (knight_row - 2, knight_col + 1),
                 (knight_row + 1, knight_col - 2), (knight_row + 2, knight_col - 1),
                 (knight_row - 1, knight_col - 2), (knight_row - 2, knight_col - 1))

    return [(row, col) for row, col in all_moves if is_possible(row, col, moves)]


def is_valid(row: int, col: int):
    return 0 <= row < board_dimensions[0] and 0 <= col < board_dimensions[1]


def is_possible(row: int, col: int, moves: list[tuple[int, int]]):
    return is_valid(row, col) and (row, col) not in moves


def game_is_over(possible_moves: list[tuple[int, int]]):
    return len(possible_moves) == 0


def visited_all(previous_moves: list[tuple[int, int]]):
    return len(previous_moves) == board_dimensions[0] * board_dimensions[1]


def has_solution(knight_row: int, knight_col: int):
    return get_solution(knight_row, knight_col, [], False) is not None


def get_solution(knight_row: int, knight_col: int, previous_moves: list[tuple[int, int]], complete: bool):
    previous_moves = previous_moves + [(knight_row, knight_col)]
    possible = generate_possible_moves(knight_row, knight_col, previous_moves)

    if game_is_over(possible):
        if visited_all(previous_moves):
            return previous_moves
        else:
            return None

    score_moves = [(move, num_possible_moves(move[0], move[1], previous_moves)) for move in possible]

    if complete:
        # Makes al moves, starting from the best
        moves_to_make = sorted(score_moves, key=lambda item: item[1], reverse=True)
    else:
        # Makes the best and second best moves only
        best_score = 0
        for _move, score in score_moves:
            best_score = max(best_score, score)
        moves_to_make = list(filter(lambda item: item[1] >= best_score - 1, score_moves))
        # print('moves', len(moves_to_make))

    for move, _score in moves_to_make:
        result = get_solution(move[0], move[1], previous_moves, complete)
        if result is not None:
            return result
    return None


def main():
    knight_pos = get_knight_pos(first_time=True)
    if get_players_choice():
        if has_solution(knight_pos[0], knight_pos[1]):
            print('This puzzle has a solution!')
        else:
            print('This might not have a solution!')

        total = 0
        prev_moves = []

        while True:
            prev_moves = prev_moves + [knight_pos]
            possible = generate_possible_moves(knight_pos[0], knight_pos[1], prev_moves)

            rep = generate_board_rep(knight_pos, possible, prev_moves)
            print_board(rep)
            total += 1

            if game_is_over(possible):
                if visited_all(prev_moves):
                    print('What a great tour! Congratulations!')
                else:
                    print('No more possible moves!')
                    print(f'Your knight visited {total} squares!')
                exit()

            knight_pos = get_knight_pos(possible_moves=possible)
    else:
        complete = get_mode()
        if board_dimensions[0] * board_dimensions[1] > 64:
            print('This might take a while')

        solution = get_solution(knight_pos[0], knight_pos[1], [], complete)
        if solution is None:
            print('No solution exists!')
        else:
            print("Here's the solution!")
            rep = generate_board()
            for index, step in enumerate(solution):
                rep[step[0]][step[1]] = ' ' * (cell_size - digit_size(str(index + 1))) + str(index + 1)
            print_board(rep)


board_dimensions = get_dimensions()
cell_size = digit_size(board_dimensions[0] * board_dimensions[1])
max_number_size = digit_size(board_dimensions[0])
main()
