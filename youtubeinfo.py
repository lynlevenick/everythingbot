import logging
import re
import subscriber
import traceback
import urllib
import urlparse

# TODO: This file is probably very difficult to have 2/3 compat with due to use of unicode api

url_res = [
	"youtube\\.com/watch\\?\\S*?v=([\\w-]+)",
	"youtu\\.be/([\\w-]+)"
]

def parse_seconds(n):
	hours = n / 3600
	n %= 3600
	minutes = n / 60
	n %= 60
	seconds = n
	buf = ""

	min_fmt = "{:d}:"

	if hours != 0:
		buf += str.format("{:d}:", hours)
		min_fmt = "{:02d}:"
	buf += str.format(min_fmt, minutes)
	buf += str.format("{:02d}", seconds)
	return buf

class Youtubeinfo(subscriber.Subscriber):
	def __init__(self, config):
		self.cache = {}
		self.ignored_users = config["ignored_users"]

	def on_add(self, publisher):
		self.publisher = publisher

	def message(self, kind, *args):
		if kind == 'pubmsg':
			nick = args[1].source.nick
			text = args[1].arguments[0]

			if not nick in self.ignored_users:
				for url_re in url_res:
					for match in re.finditer(url_re, text):
						vid_id = match.group(1)
						title = None
						length_seconds = None

                                                logging.info("Youtube ID=%s found in text" % vid_id)

						if vid_id in self.cache:
                                                        logging.info("Already in cache")
							title = self.cache[vid_id][0]
							length_seconds = self.cache[vid_id][1]
						else:
                                                        logging.info("Not in cache; Hitting youtube.com")

							try:
								resp = urllib.urlopen("http://youtube.com/get_video_info?video_id=%s" % vid_id)
								data_unparsed = resp.read()
								data = urlparse.parse_qs(data_unparsed)
								title = unicode(data["title"][0], "utf-8")
								length_seconds = unicode(parse_seconds(int(data["length_seconds"][0])), "utf-8")
								self.cache[vid_id] = (title, length_seconds)
							except Exception as e:
                                                                # TODO: Python 2/3 compat here
                                                                logging.info("Failed: %s: %s" % (e, traceback.format_exc()))
								self.publisher.parent.say("Linked Youtube video not found.")

						if title and length_seconds:
							self.publisher.parent.say(u"Linked Youtube video: \"%s\" [%s]" % (title, length_seconds))
