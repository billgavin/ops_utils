from logbook import Logger, StreamHandler, TimedRotatingFileHandler
from logbook.more import ColorizedStderrHandler
import logbook
import sys
import fire
import os


def logger(name='LOGBOOK', log_path='', file_log=False):
	logbook.set_datetime_format('local')
	ColorizedStderrHandler(bubble=True).push_application()
	log_dir = os.path.join('log') if not log_path else log_path
	if not os.path.exists(log_dir):
		os.makedirs(log_dir)
	if file_log:
		TimedRotatingFileHandler(os.path.join(log_dir, '%s.log' % name.lower()), date_format='%Y-%m-%d', bubble=True).push_application()
	return Logger(name)

def abspath(path):
	return os.path.join(os.path.dirname(__file__), path)

def bytes2human(n):
	symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
	prefix = {}
	for i, s in enumerate(symbols):
		prefix[s] = 1 << (i+1) * 10
	for s in reversed(symbols):
		if n >= prefix[s]:
			value = float(n) / prefix[s]
			return '%.2f%s' % (value, s)
	return '%sB' % n
		
def filesize(path):
	assert os.path.isdir(path)
	total_size = 0
	for root, dirs, files in os.walk(path):
		for f in files:
			fpath = os.path.join(root, f)
			if os.path.islink(fpath):
				continue
			total_size += os.path.getsize(fpath)
	return bytes2human(total_size)

if __name__ == '__main__':
	fire.Fire()
