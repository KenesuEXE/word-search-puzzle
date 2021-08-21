import argparse
import copy
import random
import string
import time

def print_grid(grid, word_list):
    """Print grid to console"""

    for row in grid:
        print(' '.join(row))

    print("\n📝 Your words are:")
    for word in word_list:
        print(word)


def reveal_answer(revealed_grid):
    """Print revealed grid to console"""

    input("\n📝 Press ENTER to reveal answers \n")
    for row in revealed_grid:
        print(' '.join(row))
    print("\n")


def pick_words(word_count, word_maxlength):
    """Pick random words"""

    # Load text file of all English words
    all_words = open('words_alpha.txt', 'r').readlines()
    word_list = []

    # Choose random word and check if below length limit
    while len(word_list) < word_count:
        picked_word = random.choice(all_words)
        if len(picked_word) <= word_maxlength:
            word_list.append(picked_word.strip().upper())

    return word_list


def create_puzzle(grid_size, word_list):
    """Generate word search puzzle"""

    # Create grid of NxN size with underscores as blank
    grid = [ [ '_' for _ in range(grid_size) ] for _ in range(grid_size) ]

    orientations = ["horizontal", "vertical", "diagonal_up", "diagonal_down"]

    for word in word_list:

        # Check if word can possibly fit in grid
        if len(word) > grid_size:
            raise Exception("All words must be equal or shorter than the grid size.")

        # Store timeout to end program when taking too long
        timeout = time.time()+10

        word_length = len(word)
        is_placed = False

        while not is_placed:

            # Check if loop is taking too long to avoid program running indefinitely
            if time.time() > timeout:
                raise Exception("Program took too long to generate grid. Try lowering word count/length or increasing grid size.")

            # Set orientation
            orientation = random.choice(orientations)
            is_reversed = True if random.random() > 0.5 else False

            if orientation == "horizontal":
                step_x = 1
                step_y = 0
            if orientation == "vertical":
                step_x = 0
                step_y = 1
            if orientation == "diagonal_up":
                step_x = 1
                step_y = -1
            if orientation == "diagonal_down":
                step_x = 1
                step_y = 1
            if is_reversed:
                step_x *= -1
                step_y *= -1

            # Set random start position
            start_x = random.randrange(grid_size)
            start_y = random.randrange(grid_size)

            # Compute end position
            end_x = start_x + word_length*step_x
            end_y = start_y + word_length*step_y

            # Check if word is outside of grid
            # If outside, restart to set new orientation
            if end_x < 0 or end_x > grid_size: continue
            if end_y < 0 or end_y > grid_size: continue

            # Check if letters don't overlap other letters
            can_fit = True
            for i in range(word_length):
                letter = word[i]

                position_x = start_x + i*step_x
                position_y = start_y + i*step_y

                letter_at_position = grid[position_x][position_y]

                # Check if position is blank or has the same letter
                if letter_at_position == '_' or letter_at_position == letter:
                    continue  # Check next letter
                else:
                    can_fit = False
                    break  # Cannot place word
 
            if not can_fit:
                continue  # Restart and choose another orientation
            else:  # Word can be placed
                # Actually place word on grid
                for i in range(word_length):
                    letter = word[i]
 
                    position_x = start_x + i*step_x
                    position_y = start_y + i*step_y

                    grid[position_x][position_y] = letter

            is_placed = True  # Current word done. Go for next word

    # Save unfilled grid for answer reveal
    revealed_grid = copy.deepcopy(grid)

    # Fill grid blanks with random letters
    for x in range(grid_size):
        for y in range(grid_size):
            if grid[x][y] == '_':
                grid[x][y] = random.choice(string.ascii_uppercase)

    grids = {"filled_grid": grid, "revealed_grid": revealed_grid}
    return grids


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', "--grid_size", type=int, default=20)
    parser.add_argument('-wc', "--word_count", type=int, default=20)
    parser.add_argument('-wl', "--word_maxlength", type=int, default=20)
    args = parser.parse_args()

    # Pick random words
    word_list = pick_words(args.word_count, args.word_maxlength)

    # Generate word search puzzle
    grids = create_puzzle(args.grid_size, word_list)

    # Print grid to console
    print_grid(grids["filled_grid"], word_list)

    # Print revealed grid to console
    reveal_answer(grids["revealed_grid"])


if __name__ == '__main__':
    print("\n📝 Word Search Puzzle Generator by KenesuEXE\n")
    main()