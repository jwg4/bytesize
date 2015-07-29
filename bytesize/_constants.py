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

""" Constants used by the bytesize package.

    Categories of constants:
     * Rounding methods
     * Size units, e.g., Ki, Mi
"""

class RoundingMethod(object):
    """ Class to generate rounding method enumeration. """
    # pylint: disable=too-few-public-methods

    def __init__(self, doc):
        """ Initializer.

            :param str doc: explanation of the rounding method
        """
        self._doc = doc

    doc = property(lambda s: s._doc, doc="explanation of rounding method")

    def __str__(self):
        return self.doc
    __repr__ = __str__

class RoundingMethods(object):
    """ Static class for accessing rounding methods. """
    # pylint: disable=too-few-public-methods

    ROUND_DOWN = RoundingMethod("Round down.")
    ROUND_HALF_DOWN = RoundingMethod("Round to nearest, down on a tie.")
    ROUND_HALF_UP = RoundingMethod("Round to nearest, up on a tie.")
    ROUND_UP = RoundingMethod("Round up.")

class Unit(object):
    """ Class to encapsulate unit information. """
    # pylint: disable=too-few-public-methods

    def __init__(self, factor, prefix, abbr):
        self._factor = factor
        self._prefix = prefix
        self._abbr = abbr

    factor = property(lambda s: s._factor, doc="numeric multiple of bytes")
    abbr = property(
       lambda s: s._abbr,
       doc="abbreviation for unit, precedes 'B'"
    )
    prefix = property(lambda s: s._prefix, doc="prefix for 'bytes'")

    def __str__(self):
        return self.abbr + "B"
    __repr__ = __str__

B = Unit(1, "", "")
""" The universal unit, bytes. """

class DecimalUnits(object):
    """ Class to store decimal unit constants. """
    # pylint: disable=invalid-name
    # pylint: disable=too-few-public-methods

    FACTOR = 10 ** 3

    KB = Unit(FACTOR ** 1, "kilo", "k")
    MB = Unit(FACTOR ** 2, "mega", "M")
    GB = Unit(FACTOR ** 3, "giga", "G")
    TB = Unit(FACTOR ** 4, "tera", "T")
    PB = Unit(FACTOR ** 5, "peta", "P")
    EB = Unit(FACTOR ** 6, "exa", "E")
    ZB = Unit(FACTOR ** 7, "zetta", "Z")
    YB = Unit(FACTOR ** 8, "yotta", "Y")

    UNITS = [KB, MB, GB, TB, PB, EB, ZB, YB]

class BinaryUnits(object):
    """ Class to store binary unit constants. """
    # pylint: disable=too-few-public-methods

    FACTOR = 2 ** 10

    KiB = Unit(FACTOR ** 1, "kibi", "Ki")
    MiB = Unit(FACTOR ** 2, "mebi", "Mi")
    GiB = Unit(FACTOR ** 3, "gibi", "Gi")
    TiB = Unit(FACTOR ** 4, "tebi", "Ti")
    PiB = Unit(FACTOR ** 5, "pebi", "Pi")
    EiB = Unit(FACTOR ** 6, "exbi", "Ei")
    ZiB = Unit(FACTOR ** 7, "zebi", "Zi")
    YiB = Unit(FACTOR ** 8, "yobi", "Yi")

    UNITS = [KiB, MiB, GiB, TiB, PiB, EiB, ZiB, YiB]