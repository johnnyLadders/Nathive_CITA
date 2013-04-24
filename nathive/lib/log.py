#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import os
import re
import time
import inspect
import traceback
import functools


class Log(object):

    def __init__(self):

        self.logfile = False
        versions = (main.version, main.phase, main.level)
        print '\nNathive Project %s %s [%s]' % versions


    def echo(self, msg, mark):

        msg = msg.replace(main.home, '~')
        print '(%s) %s' % (mark, msg)


    def info(self, *msg):

        msg = [str(x) for x in msg]
        msg = ', '.join(msg)
        self.echo(msg, '?')


    def debug(self, *msg):

        if not main.options.debug: return

        if not self.logfile:
            now = time.strftime('%H%M%S', time.localtime())
            logpath = os.path.join(main.path, 'log')
            if not os.path.exists(logpath): os.mkdir(logpath)
            path = os.path.join(logpath, now + '.log')
            self.echo('creating debug log in: %s' % path, '@')
            self.logfile = open(path, 'a')

        msg = [repr(x)[:100] for x in msg]
        msg = [x.strip("'") for x in msg]
        msg = ', '.join(msg)
        self.logfile.write(msg + '\n')
        self.logfile.flush()


    def end(self):

        if self.logfile: self.logfile.close()
        self.info('thanks for being libre, see you soon')
        print ''


    def allow_tracking(self, instance):
        """Decorate each method of the instance given to send a function and
        arguments entry to the debug log.
        @instance: The instance to be decorated."""

        # Stop if debug mode is disabled.
        if not main.options.debug: return

        # Get arguments of the init method of instance.
        args, vargs, keys, local = inspect.getargvalues(inspect.stack()[1][0])
        args.remove('self')
        args = [local[x] for x in args]

        # Get short instance name.
        instance_name = re.search('\.([^\. ]+) ', repr(instance)).group(1)

        # Send init entry to the log.
        deep = len(traceback.extract_stack()) - 2
        addr = '%s %s' % (' '*deep, hex(id(instance)))
        main.log.debug(addr, '%s.__init__' % instance_name, *args)

        # Get names of instance scope.
        names = dir(instance)
        names = [x for x in names if not x.startswith('_')]

        # For each name get attribute, test if is method, and decorate.
        for name in names:
            oldattr = getattr(instance, name)
            if not callable(oldattr): continue
            newattr = functools.partial(self.decorator, instance, oldattr)
            setattr(instance, name, newattr)


    def decorator(self, *args):
        """Decorate (replace) a method sending an entry to the debug log.
        @*args: Arguments of the original method call."""

        instance = args[0]
        function = args[1]
        args = args[2:]
        name = re.search('method ([^ ]+)', repr(function)).group(1)

        deep = len(traceback.extract_stack())
        addr = '%s %s' % (' '*deep, hex(id(instance)))
        main.log.debug(addr, name, *args)

        return function(*args)
