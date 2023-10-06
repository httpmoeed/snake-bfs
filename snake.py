"""Snake, classic arcade game.

Exercises

1. How do you make the snake faster or slower?
2. How can you make the snake go around the edges?
3. How would you move the food?
4. Change the snake to respond to mouse clicks.
"""

from random import randrange
from turtle import *
from collections import deque
from freegames import square, vector

food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)

#this is a comment
def change(x, y):
    """Change snake direction."""
    aim.x = x
    aim.y = y


def inside(head):
    """Return True if head inside boundaries."""
    return -200 < head.x < 190 and -200 < head.y < 190


def bfs_search(start, target):
    queue = deque([(start, [])])
    visited = set()

    while queue:
        current, path = queue.popleft()
        if current == target:
            return path
        if current in visited:
            continue
        visited.add(current)
        for direction in [(0, 10), (0, -10), (10, 0), (-10, 0)]:
            next_pos = vector(current.x + direction[0], current.y + direction[1])
            if inside(next_pos) and next_pos not in snake:
                queue.append((next_pos, path + [direction]))


def move():
    """Move snake toward food using BFS."""
    head = snake[-1].copy()

    # Use BFS to find the shortest path to the food
    path_to_food = bfs_search(head, food)

    if path_to_food:
        aim.x, aim.y = path_to_food[0]

    head.move(aim)

    if not inside(head) or head in snake:
        update()
        head = snake[-1].copy()

    snake.append(head)

    if head == food:
        print('Snake:', len(snake))
        food.x = randrange(-15, 15) * 10
        food.y = randrange(-15, 15) * 10
    else:
        snake.pop(0)

    clear()

    for body in snake:
        square(body.x, body.y, 9, 'black')

    square(food.x, food.y, 9, 'green')
    update()
    ontimer(move, 100)


def move_food():
    food.x = randrange(-15, 15) * 10
    food.y = randrange(-15, 15) * 10
    ontimer(move_food, 1000)


def on_click(x, y):
    change(x - snake[-1].x, y - snake[-1].y)


setup(420, 420, 370, 0)
move_food()
hideturtle()
tracer(False)
listen()    
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')

onscreenclick(on_click)
move()
done()