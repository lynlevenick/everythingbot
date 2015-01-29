import commands
import logging

class Admin(commands.Commands):
	def __init__(self, config):
		commands.Commands.__init__(self, {
			"!die":     self.do_die,
			"!restart": self.do_restart
		})

		self.admins = config["allowed_users"]

	def do_die(self, nick, rest):
		"""Restricted to a subset of users. Kills the entire bot."""
		if nick in self.admins:
                        logging.info("%s commanded a shutdown" % nick)
			self.publisher.parent.say("The bot is going down for maintenance, NOW!")
			self.publisher.parent.live = False

	def do_restart(self, nick, rest):
		"""Restricted to a subset of users. Forces the bot to reconnect."""
		if nick in self.admins:
                        logging.info("%s commanded a restart" % nick)
			self.publisher.parent.say("The bot is restarting, NOW!")
			self.publisher.parent.live = False
			self.publisher.parent.restart = True
