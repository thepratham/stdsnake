import random
import curses
from curses import textpad


def print_score(term, score):
    sh, sw = term.getmaxyx()
    score_text = 'Score: {}'.format(score)
    y = 0
    x = sw//2-len(score_text)//2
    term.addstr(y, x, score_text)
    term.refresh()

def create_food(snake, box):
    food = None
    while food is None:
        food = [random.randint(box[0][0]+1, box[1][0]-1),
                random.randint(box[0][1]+1, box[1][1]-1)]
        if food in snake:
            food = None
    return food


def main(term):
    curses.curs_set(0)
    term.nodelay(1)
    term.timeout(150)

    sh, sw = term.getmaxyx()

    box = [[3,3], [sh-3, sw-3]]

    textpad.rectangle(term, box[0][0], box[0][1], box[1][0], box[1][1])

    term.refresh()

    snake = [[sh//2, sw//2+1], [sh//2, sw//2], [sh//2, sw//2-1]]
    direction = curses.KEY_RIGHT

    for y, x in snake:
        term.addstr(y, x, '#')

    food = create_food(snake, box)
    term.addstr(food[0], food[1], '*')

    score = 0
    print_score(term, score)

    while 1:
        key = term.getch()

        if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
            direction = key
        
        head = snake[0]

        if direction == curses.KEY_RIGHT:
            new_head = [head[0], head[1]+1]
        elif direction == curses.KEY_LEFT:
            new_head = [head[0], head[1]-1]
        elif direction == curses.KEY_UP:
            new_head = [head[0]-1, head[1]]
        elif direction == curses.KEY_DOWN:
            new_head = [head[0]+1, head[1]]

        snake.insert(0, new_head)
        term.addstr(new_head[0], new_head[1], '#')

        term.addstr(snake[-1][0], snake[-1][1], ' ')
        
        if snake[0] == food:
            food = create_food(snake, box)
            term.addstr(food[0], food[1], '*')
            score += 1
            print_score(term, score)
        else:
            term.addstr(snake[-1][0], snake[-1][1], ' ')
            snake.pop()

        if (snake[0][0] in [box[0][0], box[1][0]] or 
            snake[0][1]in [box[0][1], box[1][1]]):
            msg = 'Game Over'
            term.addstr(sh//2, sw//2 - len(msg)//2, msg)
            term.nodelay(0)
            term.getch()
            break

        term.refresh()

curses.wrapper(main)
