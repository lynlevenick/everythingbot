class Subscriber():
	def __init__(self):
		pass

	def on_add(self, publisher):
		pass

	def on_remove(self):
		pass

	def message(self, kind, *args):
		raise Exception('message unimplemented in subscriber class')
