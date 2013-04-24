#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


def full_name(char=None):

    types = {
        'c':'unsigned char',
        'C':'unsigned char*',
        'ć':'signed char',
        'Ć':'signed char*',
        'i':'unsigned int',
        'I':'unsigned int*',
        'í':'signed int',
        'Í':'signed int*',
        'l':'unsigned long',
        'L':'unsigned long*',
        'ĺ':'signed long',
        'Ĺ':'signed long*',
        'f':'float',
        'F':'float*',
        'd':'double',
        'D':'double*',
        'P':'long long int'}

    if not char: return types
    return types[char]


def python_char(char):

    types = {
        'c':'c',
        'C':'s',
        'i':'i',
        'I':'i',
        'l':'l',
        'L':'i',
        'f':'f',
        'F':'i',
        'd':'d',
        'D':'i',
        'P':'L'}

    return types[char]
