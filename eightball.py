import commands
import random

REPLIES = [
	"Signs point to yes.",
	"Yes.",
	"Reply hazy, try again.",
	"Without a doubt",
	"Sources say no.",
	"As I see it, yes",
	"Rely on it.",
	"Ask again later.",
	"Outlook isn't good.",
	"Decidedly so.",
	"Better not to say now.",
	"Doubtful.",
	"Definitely.",
	"It's certain.",
	"Can't see now.",
	"Most likely.",
	"Try again.",
	"I say no.",
	"Outlook looks good.",
	"Don't count on it."
]

class Eightball(commands.Commands):
	def __init__(self, config):
		commands.Commands.__init__(self, {
			'!8ball': self.do_8ball
		})
		self.ignored_users = config["ignored_users"]

	def do_8ball(self, nick, rest):
		"""Test your luck!"""
		if not nick in self.ignored_users:
			self.publisher.parent.say(random.choice(REPLIES))
