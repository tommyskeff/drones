import tkinter as tk
import math

SCALE = 50
OFFSET = 10
DRONE_RADIUS = 5
HEXAGON_RATIO = math.sqrt(3) / 2
HEXAGON_OFFSETS = [
    [-HEXAGON_RATIO, -1 / 2], [0, -1],
    [HEXAGON_RATIO, -1 / 2], [HEXAGON_RATIO, 1 / 2],
    [0, 1], [-HEXAGON_RATIO, 1 / 2]
]


def create_window():
    window = tk.Tk()
    window.title("Game of Drones")
    window.geometry("500x420")
    window.resizable(0, 0)

    canvas = tk.Canvas(width = 500, height = 420, bg = "white")
    canvas.pack()

    return window, canvas


def render_line(canvas: tk.Canvas, x0: int, y0: int, x1: int, y1: int):
    canvas.create_line(x0, y0, x1, y1, fill="black", width = "3")


def render_text(canvas: tk.Canvas, x: int, y: int, text: str, size: int = 10, colour: str = "black"):
    canvas.create_text(x, y, text=text, fill = colour, font = ("Helvetica", size))


def render_circle(canvas: tk.Canvas, x: int, y: int, r: int, colour: str):
    canvas.create_oval(x - r, y - r, x + r, y + r, fill = colour, outline = "")


def render_drone(canvas: tk.Canvas, edge_placements: list, hexagon: int, direction: int, drone: int):
    # drone {0: red, 1: blue}
    [x, y] = edge_placements[hexagon][direction]
    render_circle(canvas, x, y, DRONE_RADIUS, "blue" if drone else "red")


def render_hexagon(canvas: tk.Canvas, x: int, y: int) -> list:
    offsets, points = list(map(lambda point: list(map(lambda n: n * SCALE, point)), HEXAGON_OFFSETS)), []
    for i in range(6):
        x0, y0 = offsets[i]
        x1, y1 = offsets[(i + 1) % len(offsets)]

        x0, x1 = list(map(lambda n: n + x, [x0, x1]))
        y0, y1 = list(map(lambda n: n + y, [y0, y1]))

        points.append([round((x0 + x1) / 2), round((y0 + y1) / 2)])
        render_line(canvas, x0, y0, x1, y1)

    return points


def render_board(canvas: tk.Canvas):
    hexagon_edges, placements, edge_coordinates = [], [], []
    for i in range(25):
        x, y = i % 5, i // 5
        xp = HEXAGON_RATIO if y % 2 else 0
        x1, y1 = (2 * x + 1) * HEXAGON_RATIO + xp, (y + 1) * (3 / 2) - (1 / 2)
        x1, y1 = list(map(lambda n: n * SCALE + OFFSET, [x1, y1]))
        render_text(canvas, x1, y1, i, 20)

        indexes, edge_placements = [], []
        for [x2, y2] in render_hexagon(canvas, x1, y1):
            index, found = len(edge_coordinates), False
            for j, [x3, y3] in enumerate(edge_coordinates):
                if x2 == x3 and y2 == y3:
                    index, found = j, True
                    
            if not found:
                edge_coordinates.append([x2, y2])

            indexes.append(index)
            midpoint = list(map(lambda n: n[0] + (n[1] - n[0]) * 2 / 3, [[x1, x2], [y1, y2]]))
            edge_placements.append(midpoint)
            render_circle(canvas, x2, y2, 8, "white")
            render_text(canvas, x2, y2, index, 10, "green")

        hexagon_edges.append(indexes)
        placements.append(edge_placements)
    
    return hexagon_edges, placements

                
window, canvas = create_window()
hexagon_edges, edge_placements = render_board(canvas)

render_drone(canvas, edge_placements, 0, 1, 0)
render_drone(canvas, edge_placements, 24, 0, 1)
        
window.mainloop()