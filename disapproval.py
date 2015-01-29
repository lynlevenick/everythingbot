import commands
import json
import logging

class Disapproval(commands.Commands):
	def __init__(self, config):
		commands.Commands.__init__(self, {
			"!check":      self.check_score,
			"!disapprove": self.disapprove,
			"!highscores": self.check_highscores
		})

		self.allowed_users = config["allowed_users"]

		try:
			with open("scores.json") as f:
				self.scores = json.load(f)
		except IOError as e:
                        logging.warning("Unable to open scores.json; Creating new score file")
			self.scores = {}

			with open("scores.json", "w") as f:
				json.dump(self.scores, f)

	def check_score(self, nick, rest):
		"""Provide a name as an argument to check their score!"""
		if len(rest) > 0:
			if not rest in self.scores:
				self.publisher.parent.say("%s has not received ANY points!" % rest)
			else:
				self.publisher.parent.say("%s has %d points!" % (rest, self.scores[rest]))

	def disapprove(self, nick, rest):
		"""Restricted to a subset of users. Disapproves of a user."""
		if nick in self.allowed_users and len(rest) > 0:
			if not rest in self.scores:
				self.scores[rest] = 1
			else:
				self.scores[rest] += 1

                        logging.info("%s disapproves of %s", nick, rest)

			with open("scores.json", "w") as f:
                                logging.info("Storing back updated scores")
				json.dump(self.scores, f)

			self.publisher.parent.say("%s now has %d points!" % (rest, self.scores[rest]))

	def check_highscores(self, nick, rest):
		"""Checks the disapproval high scores!"""
		topscores = []

		for name, score in self.scores.iteritems():
			topscores.append((score, name))

		topscores = sorted(topscores, key = lambda x: x[0], reverse = True)

		if len(topscores) > 0:
			self.publisher.parent.say("High Scores: %s" % ", ".join(map(lambda x: "%s: %d" % (x[1], x[0]), topscores[:5])))
		else:
			self.publisher.parent.say("Nobody has received any points yet!")
