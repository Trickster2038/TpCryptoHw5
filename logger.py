'''
Class implements functions
of simply-configurable console logger
'''

class Logger:
	state = 1

	@staticmethod
	def log(p_text):
		if Logger.state == 1:
			print('> log: ' + p_text)

	@staticmethod
	def config(p_state):
		Logger.state = p_state