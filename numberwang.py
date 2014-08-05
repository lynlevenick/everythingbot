import random
import subscriber
import time

class Numberwang(subscriber.Subscriber):
	def __init__(self, config):
		self.ignored_users = config["ignored_users"]
		self.mask = 0x07
		self.wangernumbstart = time.time()

	def on_add(self, publisher):
		self.publisher = publisher

	def message(self, kind, *args):
		if kind == 'pubmsg':
			if not args[1].source.nick in self.ignored_users:
				contained_number = any(c.isdigit() for c in args[1].arguments[0])

				if contained_number:
					seed = random.randint(0, 2147483647)

					if self.mask == 0 and (time.time() - self.wangernumbstart) > 90:
						self.mask = 0x07

					if (seed & self.mask) == 0:
						val = (seed >> 4) & 0xF

						if val == 1 or val == 2 or val == 3 or val == 5 or val == 8:
							self.publisher.parent.say("Das Ist Numberwang!")
						elif val == 15:
							self.publisher.parent.say("LET'S PLAY WANGERNUMB!")
							self.mask = 0
							wangernumbstart = time.time()
						else:
							self.publisher.parent.say("That's Numberwang!")
