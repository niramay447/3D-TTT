from random import randint

N = 3
PLAYER = 1
COMPUTER = 2
DIFF = [-1, 0, 1]
winner = 0
moves = 0
curr_move_taker = 0
player_moves_list = []
computer_moves_list = []
lines_of_player = 0
lines_of_computer = 0
started = False
finished = False


def delimiter():
    print("------------------------------$------------------------------")


#this function generates a 3 dimensional cube
#and it initialises all points with 0 value
def gen_cube():
    """
    Generate a cube
    """
    return [[[0 for k in range(N)] for j in range(N)] for i in range(N)]

#tic tac toe board
TIC_TAC_TOE = gen_cube()

#function to print the three planes of the cube
def print_cube(cube):
    for i in range(0, N):
        print("Plane " + str(i + 1) + ": ")
        for j in range(0, N):
            for k in range(0, N):
                print("{:2d}".format(cube[i][j][k]), end="  ")
            print("\n")
        print("\n")


# this function generates a magic cube
def gen_magic_cube():
    """
    Generate magic cube
    """
    cube = gen_cube()
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            for k in range(1, N + 1):
                a = (i - j + k + 1) % N
                if a < 0:
                    a += N
                b = (i - j - k) % N
                if b < 0:
                    b += N
                c = (i + j + k - 2) % N
                if c < 0:
                    c += N
                cube[i - 1][j - 1][k - 1] = a * N * N + b * N + c + 1
    return cube

#magic cube
MAGIC_CUBE = gen_magic_cube()


#this function takes 3 points and returns True if the 3 points are collinear
def points_are_collinear(a, b, c):
    """
    Check if three points are collinear
    """
    ba1 = b[0] - a[0]
    ba2 = b[1] - a[1]
    ba3 = b[2] - a[2]

    ca1 = c[0] - a[0]
    ca2 = c[1] - a[1]
    ca3 = c[2] - a[2]
#condition for three points to be collinear
    if ba2 * ca3 - ca2 * ba3 != 0:
        return False

    if ba1 * ca3 - ca1 * ba3 != 0:
        return False

    if ba1 * ca2 - ba2 * ca1 != 0:
        return False

    return True


#this function takes a point and returns true if the point
#is in the required range of the cube and returns false otherwise
def is_point_in_bounds(p):
    """
    Checks if the point is in the cube
    """
    return (0 <= p[0] < N) and (0 <= p[1] < N) and (0 <= p[2] < N)

#this function takes a tuple and returns the value at that point
#in the cube : 0 if the position is not marked
#1 if the position is marked by the player and 2 if its marked by the computer
def get_value_at_point(p, cube):
    """
    Gives the value at the required point
    """
    return cube[p[0]][p[1]][p[2]]

#this function takes a tuple and returns true if the position
#on the cube is empty
def is_position_empty(p, cube):
    """
    Check is the position in the cube is empty for the given point
    """
    return get_value_at_point(p, cube) == 0



#this function checks if a particular value is present in the cube
#and if it does, it returns the position at which it is present as a tuple

def search_value(value, cube):
    """
    Get the point if the search value is present in the cube
    """
    for i in range(0, N):
        for j in range(0, N):
            for k in range(0, N):
                if cube[i][j][k] == value:
                    return (i, j, k)
    return None


#this function counts the number of lines won by the player
#or the computer at a particular stage in the game
def winning_lines_count(for_who):
    """
    Returns the count of number of winning lines
    """
    count = 0
    moves_list = player_moves_list if for_who == PLAYER else computer_moves_list
    num_of_moves = len(moves_list)
    for i in range(num_of_moves):
        for j in range(i + 1, num_of_moves):
            for k in range(j + 1, num_of_moves):
                a = moves_list[i]
                b = moves_list[j]
                c = moves_list[k]

                v1 = get_value_at_point(a, MAGIC_CUBE)
                v2 = get_value_at_point(b, MAGIC_CUBE)
                v3 = get_value_at_point(c, MAGIC_CUBE)
                #check if points indeed sum up to the 42 and are collinear
                if v1 + v2 + v3 == 42 and points_are_collinear(a, b, c):
                    count += 1

    return count


#this function helps the computer make a move and
#returns the point that would make a winning line for the computer
def get_winning_line_point(moves_list):
    """
    Gets the point to for a winning line
    """
    num_player_moves = len(moves_list)
    hash_map = dict()
    for i in range(num_player_moves):
        for j in range(i + 1, num_player_moves):
            pt1 = moves_list[i]
            pt2 = moves_list[j]

            v1 = get_value_at_point(pt1, MAGIC_CUBE)
            v2 = get_value_at_point(pt2, MAGIC_CUBE)
            v3 = 42 - v1 - v2

            if v3 >= 1 and v3 <= 27:
                pt3 = search_value(v3, MAGIC_CUBE)
                if points_are_collinear(pt1, pt2, pt3) and is_position_empty(pt3, TIC_TAC_TOE):
                    try:
                        hash_map[pt3] += 1
                    except KeyError:
                        hash_map[pt3] = 1

    if len(hash_map) == 0:
        return (-1, -1, -1)
    else:
        res = (-1, -1, -1)
        max_occurences = 0
        for (k, v) in hash_map.items():
            if v > max_occurences:
                res = k
                max_occurences = v
        return res


#if the computer cannot win a line on the next move
#and if the player win line is not to be blocked,
#this function returns the point that the computer would mark
def computer_optimal_random_move():
    pt = (-1, -1, -1)
    global computer_moves_list

    for move in computer_moves_list:
        plane = move[0]
        row = move[1]
        col = move[2]

        for i in range(0, N):
            for j in range(0, N):
                for k in range(0, N):
                    np = (plane + DIFF[i], row + DIFF[j], col + DIFF[k])

                    if is_point_in_bounds(np) and is_position_empty(np, TIC_TAC_TOE):
                        return np

        for i in range(0, N):
            for j in range(0, N):
                for k in range(0, N):
                    pt = (i, j, k)
                    if is_position_empty(pt, TIC_TAC_TOE):
                        return pt


#this function calculates the computer's move
def get_next_computer_move():
    global computer_moves_list, player_moves_list, N
    num_p_moves = len(player_moves_list)
    num_c_moves = len(computer_moves_list)
    #computer's first move
    if num_c_moves == 0:
        #if middle position (1,1,1) is empty, mark that
        #else mark (0,0,0)
        if is_position_empty((1, 1, 1), TIC_TAC_TOE):
            return (1, 1, 1)
        else:
            return (0, 0, 0)
    #computer's second move
    elif num_c_moves == 1:
        #if player has only had one move
        # mark (0,0,0) if it's empty
        # if (0,0,0) is filled, mark (2,2,2)
        # if (2,2,2) is filled, mark (0,2,0)
        if num_p_moves == 1:
            pt1 = (0, 0, 0)
            pt2 = (N - 1, N - 1, N - 1)
            if is_position_empty(pt1, TIC_TAC_TOE):
                return pt1
            elif is_position_empty(pt2, TIC_TAC_TOE):
                return pt2
            else:
                return (0, N - 1, 0)
        # if the player has had more than one move
        else:
            #check the winning point
            pt = get_winning_line_point(player_moves_list)
            if is_point_in_bounds(pt):
                return pt
            else:
                return computer_optimal_random_move()
    #computer's moves after the second move
    else:
        pt = get_winning_line_point(computer_moves_list)
        if is_point_in_bounds(pt):
            return pt
        else:
            block_player_pt = get_winning_line_point(player_moves_list)
            if is_point_in_bounds(block_player_pt):
                return block_player_pt
            else:
                return computer_optimal_random_move()


#this function starts the game and randomly assigns
#the first move to the player or the computer
def greet():
    global curr_move_taker
    print("Welcome to 3d TicTacToe")
    print("You'll be assigned first or second move randomly, here you go...")
    user = randint(1, 2)
    if user == 1:
        print("You are 1, make the first move")
        curr_move_taker = PLAYER
    else:
        print("You are 2, you go second")
        curr_move_taker = COMPUTER


#this function handles the user's input when the move is taken in
def take_users_move():
    global moves, curr_move_taker, TIC_TAC_TOE, player_moves_list
    while True:
        user_ip = tuple(
            map(lambda x: int(x.strip()),
                input("Type your next move:\t").split(',')))
        if not len(user_ip) == 3:
            print("Invalid input, must have three numbers")
            continue
        if not is_point_in_bounds(user_ip):
            print(
                "Input out of range, individual positions must be from 0 to 2")
            continue
        if not is_position_empty(user_ip, TIC_TAC_TOE):
            print("Position already filled")
            continue
        break

    TIC_TAC_TOE[user_ip[0]][user_ip[1]][user_ip[2]] = PLAYER
    player_moves_list.append(user_ip)
    curr_move_taker = COMPUTER
    moves += 1


#this function prints the player and computer moves made so far
def show_moves():
  global computer_moves_list, player_moves_list
  print("Computer moves:" + str(computer_moves_list))
  print("Player moves:" + str(player_moves_list))


#this function shows the options that the user has
#and takes the input calls the required functions
def show_menu():
    while True:
        print("\n1.Show magic cube")
        print("2. Show game stats")
        print("3. Show tic-tac-toe cube")
        print("4. Take your turn")
        print("5. Show computer and User Moves")

        user_choice = None
        while True:
            try:
                user_choice = int(input("Please enter a number: "))
                break
            except ValueError:
                print("That was not a valid number.")
        if (user_choice == 1):
            print_cube(MAGIC_CUBE)
            break
        elif (user_choice == 2):
            show_game_stats()
            break
        elif user_choice == 3:
            print_cube(TIC_TAC_TOE)
        elif user_choice == 4:
            take_users_move()
            break
        elif user_choice == 5:
            show_moves()
            break
        else:
            print("Please enter either 1, 2, or 3")


#this function prints the game stats
def show_game_stats():
    global moves, PLAYER, COMPUTER
    delimiter()
    print("Game stats ->")
    print("Total moves: " + str(moves))
    print("Player winning lines: " + str(winning_lines_count(PLAYER)))
    print("Computer winning lines: " + str(winning_lines_count(COMPUTER)))
    delimiter()


#this function drives the entire 3D Tic Tac Toe game
def playTTT():
    global winner, moves, curr_move_taker, started, finished, PLAYER, COMPUTER
    winner = 0
    moves = 0
    curr_move_taker = 0
    started = False
    finished = False

    while True:
        if finished:
            return
        elif not started:
            print("Starting new game...")
            greet()
            started = True

        if started:
            if curr_move_taker == PLAYER:
                show_menu()
            if curr_move_taker == COMPUTER:
                p = get_next_computer_move()
                TIC_TAC_TOE[p[0]][p[1]][p[2]] = COMPUTER
                computer_moves_list.append(p)
                curr_move_taker = PLAYER
                moves += 1
            lines_won_comp = winning_lines_count(COMPUTER)
            lines_won_player = winning_lines_count(PLAYER)

            if lines_won_player >= 10:
                finished = True
                winner = PLAYER
            elif lines_won_comp >= 10:
                finished = True
                winner = COMPUTER

            elif moves == N * N * N:
                finished = True
                winner = 3

        if finished:
            if winner == 3:
                print("It's a draw")
            else:
                print(("Player" if winner == PLAYER else "Computer") + " wins the game")
            return


playTTT()
