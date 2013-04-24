#!/bin/bash

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


BASE = /usr/
APP = share/nathive
BIN = bin
DOC = share/doc/nathive
LAUNCH = share/applications

LIB = nathive/lib
LIBC = nathive/libc


default: compile


compile:
	@python -B utils/makeplugs.py
	@python -B utils/cybuild.py $(LIB)/core.cy $(LIB)/
	@python utils/extbuild.py $(LIB)/core.c $(LIBC)/
	@find . -name "*.c" -delete
	@python utils/shbuild.py


unpyc:
	find . -name "*.pyc" -delete


clean: unpyc
	rm -rf ./log
	rm -rf ./build
	rm -rf ./utils/deb
	rm -rf ./utils/rpm
	rm -rf ./doc/build
	rm -f  ./cfg/user.cfg
	rm -f  ./cfg/console/history
	find . -name "*~"    -delete
	find . -name "*.c"   -delete
	find . -name "*.pot" -delete
	find . -name "*.deb" -delete
	find . -name "*.rpm" -delete
	find . -name "*.tgz" -delete


source: spaces clean
	find . -name "*.so"  -delete
	find . -name "*.sh"  -delete
	@sed -i 's/appdir =.*/appdir =/' META


tabs:
	python utils/indenter.py -tw .


spaces:
	python utils/indenter.py -sw .


gettext:
	find ./ -name "*.py" | xargs xgettext -o nathive.pot -i
	python utils/updatepo.py


standalone: spaces clean
	python utils/sabuild.py


tarball: source
	python utils/tbbuild.py


docs:
	@rm -rf doc/build
	python -B utils/docbuild.py
	cd doc; make html; cd -
	@rm -rf doc/build/doctrees
	@rm -rf doc/build/html/_sources

root:
ifneq ($(shell whoami), root)
	@echo "\n**** ERROR: You must be root\n"
	@exit 1
endif


dirs:
	mkdir -p $(BASE)$(APP)
	mkdir -p $(BASE)$(BIN)
	mkdir -p $(BASE)$(DOC)
	mkdir -p $(BASE)$(LAUNCH)


install: root dirs unpyc
	# Shared files.
	cp    nathive.py    $(BASE)$(APP)
	cp    AUTHORS       $(BASE)$(APP)
	cp    COPYING       $(BASE)$(APP)
	cp    COPYING-BRIEF $(BASE)$(APP)
	cp    META          $(BASE)$(APP)
	cp -r cfg/          $(BASE)$(APP)
	cp -r img/          $(BASE)$(APP)
	cp -r nathive/      $(BASE)$(APP)
	cp -r palettes/     $(BASE)$(APP)
	cp -r po/           $(BASE)$(APP)
	chmod -R 755        $(BASE)$(APP)
	# Exclude source files.
	find $(BASE)$(APP) -name "*.c" -delete
	# Binary and launcher.
	install -m 755 -T nathive.sh      $(BASE)$(BIN)/nathive
	install -m 644    nathive.desktop $(BASE)$(LAUNCH)
	# Documentation.
	install -m 644 AUTHORS $(BASE)$(DOC)
	install -m 644 COPYING $(BASE)$(DOC)
	install -m 644 README  $(BASE)$(DOC)


uninstall: root
	rm -rf $(BASE)$(APP)
	rm -rf $(BASE)$(DOC)
	rm -f $(BASE)$(BIN)/nathive
	rm -f $(BASE)$(LAUNCH)/nathive.desktop


debinit:
	rm -rf ./utils/deb
	mkdir ./utils/deb
	mkdir ./utils/deb/DEBIAN


deb: BASE = ./utils/deb/usr/
deb: root debinit install
	@python ./utils/debbuild.py


rpminit:
	rm -rf ./utils/rpm
	mkdir ./utils/rpm
	mkdir ./utils/rpm/BUILD
	mkdir ./utils/rpm/SOURCES
	mkdir ./utils/rpm/SOURCES/nathive


rpm: BASE = ./utils/rpm/SOURCES/nathive/usr/
rpm: root rpminit install
	@python ./utils/rpmbuild.py
