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


class Language(object):
    """A simplest i18n library compatible with GetText."""

    def __init__(self):
        """Set up message dictionaries."""

        # Determine locale code.
        langenv = os.getenv('LANG')
        force = main.config.get('misc', 'language')
        if force != 'auto': langenv = force

        # Get lang and country variables.
        lang = re.search('^([a-z]+)', langenv).group(1)
        if '_' in langenv: country = re.search('_([A-Z]+)', langenv).group(1)
        else: country = False

        # Set .po file path.
        path = main.potpath
        longpath = '%s/%s_%s.po' % (path, lang, country)
        shortpath = '%s/%s.po' % (path, lang)
        if os.path.exists(longpath): popath = longpath
        elif os.path.exists(shortpath): popath = shortpath
        else: popath = False

        # Print trace.
        if popath: main.log.info('loading language: %s' % popath)
        else: main.log.info('loading language: default')

        # Init dictionary and temps.
        self.messages = {}
        lastid = False
        laststr = False

        # Walk over .po file and append messages to dictionary.
        if popath:
            po = open(popath).read().splitlines()
            for line in po:

                if re.search('msgid ".*"', line):
                    lastid = re.search('msgid "(.*)"', line).group(1)

                if re.search('msgstr ".*"', line):
                    laststr = re.search('msgstr "(.*)"', line).group(1)

                if lastid and laststr:
                    self.messages[lastid] = laststr
                    lastid = False
                    laststr = False


    def gettext(self, msgid):
        """Return translated string for given id.
        @msgid: Message id string."""

        if self.messages.has_key(msgid): return self.messages[msgid]
        else: return msgid
