from handlers.handler_com import HandlerCommands
from handlers.handler_all_text import HandlerAllText

class HandlerMain:

    def __init__(self, bot):
        self.bot = bot
        self.handler_commands = HandlerCommands(bot)
        self.handler_all_text = HandlerAllText(bot)

    def handle(self):
        self.handler_commands.handle()
        self.handler_all_text.handle()