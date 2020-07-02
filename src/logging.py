from string import Template
import datetime
import sys
import threading


class Logger:

    # [2020-03-06 11:08:42.24][__main__][4450495936] INFO: log string example displayed
    LOG_LEVEL = {
        'error': 'ERROR',
        'info': 'INFO',
        'warn': 'WARNING'
    }

    def __init__(self, name: str):
        # init logger and set name
        self.name = name
        self._reset_msg()
        self.LOG_STRING = Template(self.LOG_STRING.safe_substitute(name=name))
        self.quiet = False
        self.persistent = False
        self.file = None

    def _reset_msg(self):
        # reset log string but keep __name__
        self.LOG_STRING = Template('[$timestamp][{}][$thread] $loglevel: $msg'.format(self.name))

    def mute(self):
        # mute logger
        self.quiet = True

    def unmute(self):
        # unmute logger
        self.quiet = False

    def enable_persistent_logging(self, file: str):
        # each unmuted print while also be stored in given file
        self.persistent = True
        self.file = file

    def disable_persistent_logging(self):
        # logging only to given outfh
        self.persistent = False
        self.file = None

    def _add_timestamp(self):
        # add timestamp to logstring
        self.LOG_STRING = Template(self.LOG_STRING.safe_substitute(
            timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]))

    def _add_thread(self):
        # add thread id to logstring
        self.LOG_STRING = Template(self.LOG_STRING.safe_substitute(thread=threading.get_ident()))

    def _add_message(self, msg: str):
        # add custom message to logstring
        self.LOG_STRING = Template(self.LOG_STRING.safe_substitute(msg=msg))

    def error(self, msg: str, outfh=sys.stderr):
        # add loglevel 'error'
        self.LOG_STRING = Template(self.LOG_STRING.safe_substitute(loglevel=self.LOG_LEVEL['error']))
        self._print(msg=msg, outfh=outfh)

    def info(self, msg: str, outfh=sys.stdout):
        # add loglevel 'info'
        self.LOG_STRING = Template(self.LOG_STRING.safe_substitute(loglevel=self.LOG_LEVEL['info']))
        self._print(msg=msg, outfh=outfh)

    def warn(self, msg: str, outfh=sys.stderr):
        # add loglevel 'warning'
        self.LOG_STRING = Template(self.LOG_STRING.safe_substitute(loglevel=self.LOG_LEVEL['warn']))
        self._print(msg=msg, outfh=outfh)

    def _print(self, msg: str, outfh=sys.stdout):
        # fill logstring template and print to given outfh, flushes after print
        self._add_timestamp()
        self._add_thread()
        self._add_message(msg)
        if not self.quiet:
            outfh.write(self.LOG_STRING.template + '\n')
            if self.persistent:
                with open(self.file, 'w') as f:
                    f.write(self.LOG_STRING.template + '\n')
            outfh.flush()
        self._reset_msg()