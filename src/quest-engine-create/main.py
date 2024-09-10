import ai.gpt as gpt
import gui.gui as gui


class Main:
    def __init__(self):
        self.gui = gui.Gui(self)
        self.gpt = gpt.Gpt()

    def run(self):
        self.gui.run()


if __name__ == "__main__":
    main = Main()
    main.run()
