class IRC():
	def __init__(self, config, secret = ""):
		self.server = config["server"]
		self.port = config["port"]
		self.channel = config["channel"]
		self.nickname = config["nickname"]
		self.secret = secret
