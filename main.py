#! /usr/bin/env python

import json
import logging

import bot
import options

import loader

def main():
	config = None
	with file("config.json") as f:
		config = json.load(f)

	daemon = bot.Bot(options.IRC(config["IRC"]))
	daemon.publisher.add_subscriber("loader", loader.Loader(config["loader"]))

	daemon.event_loop()
	daemon.publisher.remove_all_subscribers()

	if daemon.restart:
		main()

if __name__ == "__main__":
	logging.basicConfig(filename = "bot.log", level = logging.DEBUG)
	main()
