try:
	import pymysql

	pymysql.install_as_MySQLdb()
except ImportError:
	# pymysql not installed; log a warning rather than silently swallowing all exceptions
	import logging

	logging.getLogger(__name__).warning("pymysql not installed; MySQL specific backends may fail")