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

""" Configuration of the bytesize package. """

class StrConfig(object):
    """ Configuration for __str__ method.

        If max_places is set to None, all non-zero digits after the
        decimal point will be shown.  Otherwise, max_places digits will
        be shown.

        If strip is True and there is a fractional quantity, trailing
        zeros are removed up to (and including) the decimal point.

        min_value sets the smallest value allowed.
        If min_value is 10, then single digits on the lhs of
        the decimal will be avoided if possible. In that case,
        9216 KiB is preferred to 9 MiB. However, 1 B has no alternative.
        If min_value is 1, however, 9 MiB is preferred.
        If min_value is 0.1, then 0.75 GiB is preferred to 768 MiB,
        but 0.05 GiB is still displayed as 51.2 MiB.

        The default for strip is False, so that precision is always shown
        to max_places.
    """
    # pylint: disable=too-few-public-methods

    _FMT_STR = ", ".join([
       "binary_units=%(binary_units)s",
       "max_places=%(max_places)s",
       "min_value=%(strip)s",
       "strip=%(strip)s"
    ])

    def __init__(
       self,
       max_places=2,
       strip=False,
       min_value=1,
       binary_units=True
    ):
        """ Initializer.

            :param max_places: number of decimal places to use, default is 2
            :type max_places: an integer type or NoneType
            :param bool strip: True if trailing zeros are to be stripped.
            :param min_value: Lower bound for value, default is 1.
            :type min_value: A precise numeric type: int or Decimal
            :param bool binary_units: binary units if True, else SI
        """
        self._max_places = max_places
        self._strip = strip
        self._min_value = min_value
        self._binary_units = binary_units

    def __str__(self):
        values = {
           'binary_units' : self.binary_units,
           'max_places' : self.max_places,
           'min_value' : self.min_value,
           'strip' : self.strip
        }
        return "StrConfig(%s)" % (self._FMT_STR % values)
    __repr__ = __str__

    # pylint: disable=protected-access
    max_places = property(lambda s: s._max_places)
    min_value = property(lambda s: s._min_value)
    strip = property(lambda s: s._strip)
    binary_units = property(lambda s: s._binary_units)

class Defaults(object):
    """ Configuration defaults. """
    # pylint: disable=too-few-public-methods

    STR_CONFIG = StrConfig(2, False, 1, True)
    """ Default configuration for string display. """
