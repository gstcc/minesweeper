import random

def initMap(r, c, n_of_mines):
    map = [[0 for i in range(r)] for j in range(c)];
    revealed = [['_' for i in range(r)] for j in range(c)];

    for _ in range(n_of_mines):
        random_row = random.randint(0, c - 1)
        random_col = random.randint(0, r - 1)
        map[random_row][random_col] = -1
    
    map = [
        [
            count_neighbours(map, i, j) if map[i][j] != -1 else -1
            for j in range(r)
        ]
        for i in range(c)
    ]
    return map, revealed

def count_neighbours(map, r, c):
    count = 0
    width = len(map[0])
    length = len(map)

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            neighbor_row = r + i
            neighbor_col = c + j
            if 0 <= neighbor_row < length and 0 <= neighbor_col < width and map[neighbor_row][neighbor_col] == -1:
                count += 1
    return count

def reveal_neighbours(map, revealed, row, col):
    if row < 0 or row >= len(map) or col < 0 or col >= len(map[0]) or revealed[row][col]:
        return

    revealed[row][col] = True

    if map[row][col] == 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                reveal_neighbours(map, revealed, row + i, col + j)
    
def reveal(map, revealed, row, col):
    result = [[False if cell == '_' or cell == "f" else True for cell in row] for row in revealed]
    reveal_neighbours(map, result, row, col)
    #All elements that are true in result should  become the corresponding cell in revealed
    revealed = [
        [map[i][j] if result[i][j] and (revealed[i][j]!="f" or revealed[row][col]=="f") else revealed[i][j] for j in range(len(revealed[0]))]
        for i in range(len(revealed))
    ]
    return revealed

def place_flag(map, revealed, row, col):
    if 0 <= row < len(revealed) and 0 <= col < len(revealed[0]) and revealed[row][col] == "_":
        revealed[row][col] = "f"

def check_win(map, revealed):
    for row in range(len(map)):
        for col in range(len(map[0])):
            if map[row][col] != -1 and revealed[row][col] == "_":
                return False
    #All mines have flags, and all cells that are not mines have been revealed
    return True 
def game_lost(map, revealed):
    for row in revealed:
        if -1 in row:
            return True
    
    for row in range(len(revealed)):
        for col in range(len(revealed[0])):
            if map[row][col] != -1 and revealed[row][col] == "_":
                return False  # There are still unrevealed cells, game not over
            
    # All non-mine cells have been revealed, game over
    return True
