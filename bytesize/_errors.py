# Copyright (C) 2015  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): Anne Mulhern <amulhern@redhat.com>

""" Exception types used by the bytesize class. """

import abc

from six import add_metaclass

@add_metaclass(abc.ABCMeta)
class SizeError(Exception):
    """ Generic Size error. """
    pass

class SizeValueError(SizeError):
    """ Raised when a parameter has an unacceptable value.

        May also be raised when the parameter has an unacceptable type.
    """

    _FMT_STR = "value '%s' for parameter %s is unacceptable"

    def __init__(self, value, param, msg=None):
        """ Initializer.

            :param object value: the value
            :param str param: the parameter
            :param str msg: an explanatory message
        """
        # pylint: disable=super-init-not-called
        self._value = value
        self._param = param
        self._msg = msg

    def __str__(self):
        if self._msg:
            fmt_str = self._FMT_STR + ": %s"
            return fmt_str % (self._value, self._param, self._msg)
        else:
            return self._FMT_STR % (self._value, self._param)

@add_metaclass(abc.ABCMeta)
class SizeUnsupportedOpError(SizeError):
    """ Error when executing unsupported operation on Size. """
    pass

@add_metaclass(abc.ABCMeta)
class SizeNonsensicalOpError(SizeUnsupportedOpError):
    """ Error when requesting an operation that doesn't make sense. """
    pass

class SizeNonsensicalBinOpError(SizeNonsensicalOpError):
    """ Error when requesting a binary operation that doesn't make sense. """
    _FMT_STR = "nonsensical operand types for %s: 'Size' and '%s'"

    def __init__(self, operator, other):
        """ Initializer.

            :param str operator: the operator
            :param object other: the other argument
        """
        # pylint: disable=super-init-not-called
        self._operator = operator
        self._other = other

    def __str__(self):
        return self._FMT_STR % (self._operator, type(self._other).__name__)

@add_metaclass(abc.ABCMeta)
class SizeUnrepresentableResultError(SizeUnsupportedOpError):
    """ Error when requesting an operation that yields units that cannot
        be represented with Size, e.g., when multiplying a Size by a Size.
    """
    pass

class SizePowerResultError(SizeUnrepresentableResultError):
    """ Error when requesting an operation that would yield a byte power. """

    def __str__(self):
        return  "requested operation result requires non-unit power of bytes"
