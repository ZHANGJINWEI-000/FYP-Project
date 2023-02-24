class action:
    def __init__(self, setup_dialog, change_game_status):
        self.list = None
        self.index = 0

        self.setup_dialog = setup_dialog
        self.change_game_status = change_game_status

    def get_list(self, list):
        if list and len(list) > 0:
            self.list = list
            self.change_game_status("action")

    def process(self):
        z = self.list[self.index]
        print(z)
        type = z["type"]
        content = z["content"]

        if type == "text":
            self.setup_dialog(content)

    def finish(self):
        self.index += 1
        if not self.index < len(self.list):
            self.quit()