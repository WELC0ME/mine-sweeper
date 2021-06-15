import time
import pyautogui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor
import sys


def click(x, y, button='left'):
    pyautogui.click(x, y, button)


class Group:

    def __init__(self, dots, number):
        self.dots = dots
        self.number = number

    def __sub__(self, other):
        return Group(self.dots - other.dots, self.number - other.number)

    def __eq__(self, other):
        v1 = sorted(list(self.dots))
        v2 = sorted(list(other.dots))
        return v1 == v2 and self.number == other.number

    def __and__(self, other):
        dots = self.dots & other.dots
        number = self.number - (len(other.dots) - len(dots))
        if number > other.number or number > self.number or number <= 0:
            return False

        return Group(dots, number)

    def __repr__(self):
        return '(' + str(self.dots) + ' ' + str(self.number) + ')'

    def copy(self):
        return Group(self.dots, self.number)


click(186, 1064)
time.sleep(2)
app = QApplication([])
screen = app.primaryScreen()

left_top_position = (195, 142)
cell_size = (51, 51)
board_size = (30, 16)

board = [[9 for _ in range(board_size[0])] for _ in range(board_size[1])]

while any([9 in row for row in board]):

    screen_shoot = screen.grabWindow(QApplication.desktop().winId(),
                                     x=left_top_position[0],
                                     y=left_top_position[1],
                                     width=board_size[0] * cell_size[0],
                                     height=board_size[1] * cell_size[1]).toImage()
    for k in range(0, board_size[1] * cell_size[1], cell_size[1]):
        for i in range(0, board_size[0] * cell_size[0], cell_size[0]):
            p = QColor(screen_shoot.pixel(i + 25, k + 43)).getRgb()[:-1]
            if board[k // cell_size[1]][i // cell_size[1]] == 9:
                if len(set(p)) == 1:
                    if QColor(screen_shoot.pixel(i + 2, k + 2)).getRgb()[0] < 150:
                        board[k // cell_size[1]][i // cell_size[1]] = 9
                    else:  # if QColor(screen_shoot.pixel(i + 2, k + 2)).getRgb()[:-1] == (193, 193, 193):
                        board[k // cell_size[1]][i // cell_size[1]] = 0
                    continue
                if p == (0, 0, 129):
                    board[k // cell_size[1]][i // cell_size[1]] = 1
                elif p == (0, 129, 0):
                    board[k // cell_size[1]][i // cell_size[1]] = 2
                elif p == (128, 103, 1):
                    board[k // cell_size[1]][i // cell_size[1]] = 3
                else:
                    print(i // 51, k // 51, p)
                    sys.exit(1)
    for i in board:
        print(i)
    sys.exit(1)
    groups = []
    for i in range(len(board)):
        for k in range(len(board[i])):
            if 1 <= board[i][k] <= 7:
                tmp = []
                flag_counter = 0
                for j in range(-1, 2):
                    for m in range(-1, 2):
                        if (j != 0 or m != 0) and 0 <= i + j < len(board) and 0 <= k + m < len(board[0]):
                            if board[i + j][k + m] == 9:
                                tmp.append((i + j) * 30 + k + m)
                            elif board[i + j][k + m] == -1:
                                flag_counter += 1
                if len(tmp) > 0:
                    groups.append(Group(set(tmp[:]), board[i][k] - flag_counter))

    change = True
    while change:
        change = False
        for i in range(len(groups)):
            for k in range(i + 1, len(groups)):
                if groups[i] == groups[k]:
                    groups.remove(groups[k])
                    break

                if groups[i].dots > groups[k].dots and groups[i].number >= groups[k].number:
                    groups[i] = groups[i] - groups[k]
                    change = True
                elif groups[k].dots > groups[i].dots and groups[k].number >= groups[i].number:
                    groups[k] = groups[k] - groups[i]
                    change = True
                elif len(groups[i].dots & groups[k].dots) > 0:
                    continue
                    # TODO
                    # обдумать пересечение групп
                    if groups[i].number > groups[k].number:
                        d = groups[i] & groups[k]
                    else:
                        d = groups[k] & groups[i]
                    if d:
                        groups.append(d)
                        groups[i] = groups[i] - d
                        groups[k] = groups[k] - d
                        change = True
    clicked = False
    for counter in range(len(groups)):
        if groups[counter].number == len(groups[counter].dots):
            for h in list(groups[counter].dots):
                click(left_top_position[0] + (h % 30) * cell_size[0] + cell_size[0] // 2,
                      left_top_position[1] + (h // 30) * cell_size[1] + cell_size[1] // 2,
                      btn='right')
                clicked = True
        elif groups[counter].number == 0:
            for h in list(groups[counter].dots):
                click(left_top_position[0] + (h % 30) * cell_size[0] + cell_size[0] // 2,
                      left_top_position[1] + (h // 30) * cell_size[1] + cell_size[1] // 2)
                clicked = True
    if not clicked:
        for i in range(len(board)):
            for k in range(len(board[i])):
                if board[i][k] == 9:
                    click(left_top_position[0] + k * cell_size[0] + cell_size[0] // 2,
                          left_top_position[1] + i * cell_size[1] + cell_size[1] // 2)
                    clicked = True
                    break
            if clicked:
                break
    time.sleep(0.04)
