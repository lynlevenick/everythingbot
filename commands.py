import subscriber

class Commands(subscriber.Subscriber):
	def __init__(self, commands):
		self.commands = commands

	def on_add(self, publisher):
		self.publisher = publisher

	def message(self, kind, *args):
		if kind == "pubmsg":
			command = args[1].arguments[0].split()
			if len(command) > 0:
				command = command[0]

				if command in self.commands:
					self.commands[command](args[1].source.nick, args[1].arguments[0][len(command) + 1:])
				elif command == "!help":
					self.publisher.parent.say("%s:" % self.__module__)

					for name, func in self.commands.iteritems():
						self.publisher.parent.say("    %s: %s" % (name, func.__doc__ or "No docstring available"))
