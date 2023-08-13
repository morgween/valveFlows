#!/usr/bin/env python3
from graphical_interface.main_menu import MenuWindow
from objects.pipe import Pipe

def main():
    pipes = []
    for i in range(1, 5):
        pipes.append(Pipe(i))

    main_menu = MenuWindow(pipes)
    main_menu.run()




if __name__ == '__main__':
    main()