from graphics import *
from random import *
import sys

# Displays the 16 numbers by converting the raw numbers in everyNumber into text objects

def display(moves, score):
    count = 0
    for i in everyText:
        i.setText(everyNumber[count])
        if everyNumber[count] != 0:
            i.draw(win)
        count += 1
    moves = str(moves)
    movesDisplay = Text(Point(200, 75), "Moves: " + moves)
    scoreText = str(score)
    scoreDisplay = Text(Point(400, 75), "Score: " + scoreText)
    return movesDisplay, scoreDisplay

# Generates a new number before each turn

def generate():
    emptyCells = []

    rand = randint(0, 16)
    if rand == 0:
        newNumber = 4
    else:
        newNumber = 2

    for i in range(0, 16):
        if everyNumber[i] == 0:
            emptyCells.append(i)
    everyNumber[choice(emptyCells)] = newNumber

# Checks if there are no more possible moves, which means the game is over

def gameOver(everyNumber):

    newListA = move(everyNumber.copy(), 0, score)[0]
    newListB = move(everyNumber.copy(), 1, score)[0]
    newListC = move(everyNumber.copy(), 2, score)[0]
    newListD = move(everyNumber.copy(), 3, score)[0]

    if everyNumber == newListA and everyNumber == newListB and everyNumber == newListC and everyNumber == newListD:
        return True

def move(array, direction, score):

    # for direction input: 0 = up, 1 = left, 2 = down, 3 = right

    if direction == 0:
        start = 0
        jump = 1
        step = 4
    elif direction == 1:
        start = 0
        jump = 4
        step = 1
    elif direction == 2:
        start = 12
        jump = 1
        step = -4
    elif direction == 3:
        start = 3
        jump = 4
        step = -1

    # Start is from where it starts to scan across the rows / columns
    # jump is getting from column to colums or row to row,
    # step is moving between elements in each column / row

    # The first for loop runs through all 4 rows or columns
    # The second for loop goes through the last 3 numbers in each row / column,
    # since the first number can never move
    # It checks how far it can move the number,
    # combining numbers as necessary
    # There is also something to prevent a number from combining more than once in ove move,
    # using the list "changed"

    for numbered in range (0, 4):

        # "numbered" means first, second, third, or fourth row or column

        if step < 0:
            signOfStep = -1
        elif step > 0:
            signOfStep = 1

        changed = []
        for i in range(start + numbered * jump + step, start + numbered * jump + 3 * step + signOfStep, step):
            # If there is actually a number in the cell
            if array[i] != 0:
                # Start scanning at one past the cell (heading towards the direction you want to move)
                new = i - step
                # This condition detects when to stop moving, either you've reached the end or there's a number in the way
                while new != start + numbered * jump and array[new] == 0 and new not in changed:
                    new -= step
                trueNew = new
                # You either move the number on top of the cell you stopped at (if you're combining numbers),
                # or at one before it, if you aren't combining
                if array[i] != array[new] or new in changed:
                    new += step
                    # Special case: this is for if you've rached the end of the row / column
                    # Even though you're not combining, you're still moving it on top of the original cell,
                    # called "trueNew"
                    if trueNew == start + numbered * jump and array[trueNew] == 0:
                        new -= step
                # Stuff only happens if you are actually able to move
                if new != i:
                    # If you're combining, you need to log that cell as one that can't combine again in that move
                    # And you're adding the combined numbers to the total score
                    if array[i] == array[new]:
                        changed.append(trueNew)
                        score += array[i] + array[new]
                    array[new] += array[i]
                    array[i] = 0
    return[array, score]

# This is the starting screen for the game (only runs at the beginning)

while True:

    win = GraphWin("2048", 600, 600)
    title = Text(Point(300, 300), "2048")
    title.setStyle("bold")
    title.setSize(32)
    title.draw(win)
    startPrompt = Text(Point(300, 340), "Press \"p\" to start")
    startPrompt.setStyle("bold")
    startPrompt.draw(win)
    key = win.getKey()
    if key == "p":
        win.close()
        break
    else:
        sys.exit()

# This is the main program loop

while True:

    # Initializes the array that holds the value of each cell

    everyNumber = [0, 0, 0, 0,
                   0, 0, 0, 0,
                   0, 0, 0, 0,
                   0, 0, 0, 0]

    # Initializes the text for each cell

    everyText = []

    for i in range(0, 400, 100):
        for j in range(0, 400, 100):
            everyText.append(Text(Point(j + 150, i + 150), 0))

    for i in everyText:
        i.setSize(30)

    win = GraphWin("2048", 600, 600)

    # These draw the horizontal and vertical lines for the game board

    horizontal = Line(Point(100, 100), Point(500, 100))
    vertical = Line(Point(100, 100), Point(100, 500))

    for i in range(0, 600, 100):
        horizontal.draw(win)
        horizontal = horizontal.clone()
        horizontal = Line(Point(100, i + 100), Point(500, i + 100))

    for i in range(0, 600, 100):
        vertical.draw(win)
        vertical = vertical.clone()
        vertical = Line(Point(i + 100, 100), Point(i + 100, 500))

    # Generates the first 2 tiles at the start of the game

    # Decides whether to generate 2 2 , 2 4 , 4 2 , or 4 4

    rand = randint(1, 16)          # Probabilities:

    if rand in range(1, 12):       # 11/16 (69 %)
        combination = [2, 2]
    elif rand in range(12, 14):    # 1/8 (13 %)
        combination = [2, 4]
    elif rand in range(14, 16):    # 1/8 (13 %)
        combination = [4, 2]
    else:
        combination = [4, 4]       # 1/16 (6 %)

    randA = randint(0, 15)
    randB = randint(0, 15)
    while randA == randB:
        randB = randint(0, 15)
    everyNumber[randA] = combination[0]
    everyNumber[randB] = combination[1]

    count = 0
    breakAgain = False
    score = 0

    while True:
        # It doesn't need to generate more numbers for the first turn

        if count > 0:
            generate()
            for i in movecountAndScore:
                i.undraw()

        movecountAndScore = display(count, score)

        for i in movecountAndScore:
            i.setSize(16)
            i.draw(win)

        while True:
            # This makes sure your "move" actually changes something before letting you move on

            oldeveryNumber = everyNumber.copy()

            key = win.getKey()
            if key == "w":
                score = move(everyNumber, 0, score)[1]
            elif key == "a":
                score = move(everyNumber, 1, score)[1]
            elif key == "s":
                score = move(everyNumber, 2, score)[1]
            elif key == "d":
                score = move(everyNumber, 3, score)[1]

            # Also a good spot to slide in the check for gameOver

            if gameOver(everyNumber):
                win.close()
                breakAgain = True
                break

            if everyNumber != oldeveryNumber:
                break

        if breakAgain:
            break

        for i in everyText:
            i.undraw()

        count += 1

    # Prompt to play again

    win = GraphWin("2048", 600, 600)

    endOfGame = Text(Point(300, 300), "Game Over!")
    endOfGame.setStyle("bold")
    endOfGame.setSize(32)
    endOfGame.draw(win)

    countText = str(count)
    endMoves = Text(Point(250, 260), "Moves: " + countText)
    endMoves.draw(win)

    scoreText = str(score)
    endScore = Text(Point(350, 260), "Score: " + scoreText)
    endScore.draw(win)

    playAgain = Text(Point(300, 340), "Press \"p\" to play again")
    playAgain.setStyle("bold")
    playAgain.draw(win)
    while True:
        key = win.getKey()
        if key == "p":
            win.close()
            break
