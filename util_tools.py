from logbook import Logger, StreamHandler, TimedRotatingFileHandler
from logbook.more import ColorizedStderrHandler
import logbook
import socket
import re
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


class switch(object):


    def __init__(self, value, flag=0):
        '''
        re.S DOTALL
        re.I IGNORECASE
        re.L LOCALE
        re.M MULTILINE
        re.X VERBOSE
        re.U
        '''
        self.value = value
        self.fall = False
        self.flag = flag

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, arg=''):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not arg:
            return True
        elif re.search(arg, self.value, self.flag) is not None:
            self.fall = True
            return True
        else:
            return False


def get_ip_hostname(ip='8.8.8.8', port=80):
    h = socket.gethostname()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((ip, port))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return h, ip

if __name__ == '__main__':
	fire.Fire()
