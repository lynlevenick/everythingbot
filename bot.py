import irc.bot
import publisher
import time

class Bot(irc.bot.SingleServerIRCBot):
	def __init__(self, ircopt):
		irc.bot.SingleServerIRCBot.__init__(self, [(ircopt.server, ircopt.port, ircopt.secret)], ircopt.nickname, ircopt.nickname)
		self.publisher = publisher.Publisher(self)
		self.channel = ircopt.channel
		self.start_time = time.time() + 5
		self.should_process = False
		self.live = True
		self.restart = False

	def on_nicknameinuse(self, conn, event):
		raise Exception("nickname in use")

	def on_welcome(self, conn, event):
		conn.join(self.channel)

	def on_privmsg(self, conn, event):
		if self.should_process:
			self.publisher.message("privmsg", conn, event)

	def on_pubmsg(self, conn, event):
		if self.should_process:
			self.publisher.message("pubmsg", conn, event)

	def on_dccmsg(self, conn, event):
		if self.should_process:
			self.publisher.message("dccmsg", conn, event)

	def on_dccchat(self, conn, event):
		if self.should_process:
			self.publisher.message("dccchat", conn, event)

	def event_loop(self, timeout = 0.1):
		self._connect()

		while self.live:
			self.should_process = time.time() >= self.start_time
			self.ircobj.process_once(timeout)
			self.publisher.message("update")

		self.disconnect()

	def say(self, message):
		if self.connection.socket != None:
			self.connection.privmsg(self.channel, message)
