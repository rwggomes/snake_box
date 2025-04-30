import curses
import random
import time
import os

# Constants
DATA_FILE = 'highscore.txt'
INITIAL_SPEED = 120  # milliseconds
SPEED_INCREMENT = 10  # i'm fast as frick boyyyyy

def load_highscore():
    if not os.path.exists(DATA_FILE):
        return 0
    try:
        with open(DATA_FILE, 'r') as f:
            return int(f.read().strip())
    except:
        return 0

def save_highscore(score):
    with open(DATA_FILE, 'w') as f:
        f.write(str(score))

def main(stdscr):
    curses.curs_set(0)              # Hide cursor 
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    sh, sw = stdscr.getmaxyx()

    # Create game window inside a border
    win = curses.newwin(sh-2, sw-2, 1, 1)
    win.keypad(True)

    # Draw border on stdscr
    stdscr.border()
    stdscr.noutrefresh()

    # Initial snake & food
    snk_x = (sw-2) // 4
    snk_y = (sh-2) // 2
    snake = [[snk_y, snk_x],
             [snk_y, snk_x-1],
             [snk_y, snk_x-2]]
    food = [random.randint(1, sh-4), random.randint(1, sw-4)]
    win.addch(food[0], food[1], curses.ACS_PI, curses.color_pair(2))

    key = curses.KEY_RIGHT
    score = 0
    highscore = load_highscore()
    speed = INITIAL_SPEED

    paused = False

    while True:
        # Pontuação e placar
        stdscr.addstr(0, 2, f" Score: {score} ")
        stdscr.addstr(0, sw//2 - 7, f" High Score: {highscore} ")
        stdscr.addstr(0, sw-15, " P = Pause ")
        stdscr.noutrefresh()
        win.timeout(speed)

        next_key = win.getch()
        if next_key == ord('p') or next_key == ord('P'):
            paused = not paused
            if paused:
                stdscr.addstr(sh//2, sw//2-5, " PAUSED ")
                stdscr.noutrefresh()
            else:
                stdscr.addstr(sh//2, sw//2-5, "       ")
            stdscr.noutrefresh()
            continue

        if paused:
            continue

        key = key if next_key == -1 else next_key
        head = snake[0].copy()

        # Move head
        if key == curses.KEY_DOWN:  head[0] += 1
        elif key == curses.KEY_UP:   head[0] -= 1
        elif key == curses.KEY_LEFT: head[1] -= 1
        elif key == curses.KEY_RIGHT:head[1] += 1

        # Collision with wall or self?
        if (head[0] in [0, sh-3] or
            head[1] in [0, sw-3] or
            head in snake):
            msg = f" Game Over! Final Score: {score} "
            stdscr.addstr(sh//2, sw//2 - len(msg)//2, msg, curses.color_pair(2))
            stdscr.noutrefresh()
            curses.doupdate()
            time.sleep(2)
            break

        snake.insert(0, head)

        # Ate food?
        if head == food:
            score += 1
            speed = max(20, speed - SPEED_INCREMENT)
            # New food
            while True:
                nf = [random.randint(1, sh-4), random.randint(1, sw-4)]
                if nf not in snake:
                    food = nf
                    break
            win.addch(food[0], food[1], curses.ACS_PI, curses.color_pair(2))
        else:
            tail = snake.pop()
            win.addch(tail[0], tail[1], ' ')

        # Draw snake head
        win.addch(head[0], head[1], curses.ACS_CKBOARD, curses.color_pair(1))

        curses.doupdate()

    # Update highscore if beaten
    if score > highscore:
        save_highscore(score)
        stdscr.addstr(sh//2 + 1, sw//2 - 6, " New High Score! ", curses.A_BLINK)
        stdscr.noutrefresh()
        curses.doupdate()
        time.sleep(2)

if __name__ == '__main__':
    curses.wrapper(main)
