from logbook import Logger, StreamHandler, TimedRotatingFileHandler
from logbook.more import ColorizedStderrHandler
import logbook
import socket
import uuid
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

def HandleJson(object):

    @classmethod
    def __paths(cls, data, path=''):
        if isinstance(data, dict):
            for k, v in data.items():
                tmp = path + "['%s']" % k
                yield (tmp, v)
                yield from cls.__paths(v, tmp)
        if isinstance(data, path=''):
            for k, v in enumerate(data):
                tmp = path + '[%d]' % k
                yield (tmp, v)
                yield from cls.__paths(v, tmp)
    
    @classmethod
    def find_key_path(cls, data, key):
        result = []
        for path, value in cls.__path(data):
            if path.endswith("['%s']" % key):
                result.append(path)
        return result

    @classmethod
    def find_value_path(cls, data, key):
        result = []
        for path, value in cls.__paths(data):
            if isinstance(value, (str, int, bool, float)):
                if value == key:
                    result.append(path)
        return result

    @classmethod
    def get_key_node(cls, data, key):
        for path, value in cls.__paths(data):
            if path.endswith("['%s']" % key):
                return value

def get_ip_hostname(ip='8.8.8.8', port=80):
    h = socket.gethostname()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((ip, port))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return h, ip

def gen_uuid(func=1, name='python', namespace='url'):
    namespaces = {
        'dns': uuid.NAMESPACE_DNS,
        'oid': uuid.NAMESPACE_OID,
        'url': uuid.NAMESPACE_URL,
        'x500': uuid.NAMESPACE_X500
    }
    name_space = namespaces.get(namespace, None)
    assert name_space is not None, 'namespace support values: dns, oid, url & x500.'
    assert func in [1, 3, 4, 5] , 'func support values: 1, 3, 4, 5.'
    id1 = uuid.uuid1().hex
    id3 = uuid.uuid3(name_space, name).hex
    id4 = uuid.uuid4().hex
    id5 = uuid.uuid5(name_space, name).hex
    return eval('id%d' % func)

if __name__ == '__main__':
	fire.Fire()
