from logging.handlers import SysLogHandler
import socket
try:
	import codecs
except ImportError:
	codecs = None

class UTFFixedSysLogHandler(SysLogHandler):
	"""
	A bug-fix sub-class of SysLogHandler that fixes the UTF-8 BOM syslog
	bug that caused UTF syslog entries to not go to the correct
	facility.  This is fixed by over-riding the 'emit' definition
	with one that puts the BOM in the right place (after prio, instead
	of before it).
	
	Based on Python 2.7 version of logging.handlers.SysLogHandler.
	
	Bug Reference: http://bugs.python.org/issue7077
	"""
	
	def emit(self, record):
		"""
		Emit a record.
		
		The record is formatted, and then sent to the syslog server.  If
		exception information is present, it is NOT sent to the server.
		"""
		msg = self.format(record) + '\000'
		"""
		We need to convert record level to lowercase, maybe this will
		change in the future.
		"""
		prio = '<%d>' % self.encodePriority(self.facility,
					self.mapPriority(record.levelname))
		prio = prio.encode('utf-8')
		# Message is a string. Convert to bytes as required by RFC 5424.
		msg = msg.encode('utf-8')
		if codecs:
			msg = codecs.BOM_UTF8 + msg
		msg = prio + msg
		try:
			if self.unixsocket:
				try:
					self.socket.send(msg)
				except socket.error:
					self._connect_unixsocket(self.address)
					self.socket.send(msg)
			elif self.socktype == socket.SOCK_DGRAM:
				self.socket.sendto(msg, self.address)
			else:
				self.socket.sendall(msg)
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			self.handleError(record)
