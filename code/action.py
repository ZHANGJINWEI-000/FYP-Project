class action:
    def __init__(self, game_status, dialog_action, input_action, setup_lex, setup_audio):
        self.type = ["text", "input", "lex", "audio", "close"]
        self.action = [self.dialog, self.input, self.lex, self.audio, self.close]
        self.list = []
        self.index = 0

        self.game_status = game_status
        self.dialog_action = dialog_action
        self.input_action = input_action
        self.setup_lex = setup_lex
        self.setup_audio = setup_audio

    def get_list(self, list):
        if list and len(list) > 0:
            self.list = list
            self.index = 0
            self.game_status.change("implement")

    def process(self):
        if self.index == len(self.list):
            self.quit()
            return

        z = self.list[self.index]
        print(z)
        type = z["type"]
        content = z.get("content", None)

        ti = self.type.index(type)
        if ti >= 0:
            self.action[ti](content)

        self.index += 1
        self.game_status.remove("implement")

    def finish(self):
        if not self.game_status.exist("action"):
            self.index += 1
            if self.index == len(self.list):
                self.quit()

    def quit(self):
        self.game_status.change("map")


    """
    use dialog class show text
    使用dialog顯示文字
    """
    def dialog(self, content = None):
        print(content)
        self.dialog_action("setup", content)

    """
    """
    def input(self, content = None):
        self.input_action("setup")

    """
    """
    def lex(self, content = None):
        self.setup_lex()

    def audio(self, content = None):
        self.setup_audio()

    """
    """
    def close(self, content = None):
        self.game_status.remove(content)