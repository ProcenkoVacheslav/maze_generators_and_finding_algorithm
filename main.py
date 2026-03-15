from window.window import Window


class RunApp:
    def __init__(self):
        self._app = Window()

    def run_app(self):
        self._app.run()


if __name__ == '__main__':
    runner = RunApp()
    runner.run_app()
