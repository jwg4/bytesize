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

""" Tests for named methods of Size objects. """

from hypothesis import given
from hypothesis import strategies
import unittest

from fractions import Fraction

from bytesize import Size
from bytesize import B
from bytesize import ROUND_DOWN
from bytesize import ROUND_HALF_UP
from bytesize import ROUND_UP
from bytesize import ROUNDING_METHODS

from bytesize._constants import BinaryUnits
from bytesize._constants import DecimalUnits
from bytesize._constants import UNITS

from bytesize._errors import SizeValueError

from tests.utils import SIZE_STRATEGY

class ConversionTestCase(unittest.TestCase):
    """ Test conversion methods. """

    def testException(self):
        """ Test exceptions. """
        with self.assertRaises(SizeValueError):
            Size(0).convertTo(-2)
        with self.assertRaises(SizeValueError):
            Size(0).convertTo(0)

    @given(
       strategies.builds(Size, strategies.integers()),
       strategies.one_of(
           strategies.none(),
           strategies.sampled_from(UNITS()),
           strategies.builds(Size, strategies.integers(min_value=1))
       )
    )
    def testPrecision(self, s, u):
        """ Test precision of conversion. """
        factor = (u and int(u)) or int(B)
        self.assertEqual(s.convertTo(u) * factor, int(s))

class ComponentsTestCase(unittest.TestCase):
    """ Test components method. """

    def testException(self):
        """ Test exceptions. """
        with self.assertRaises(SizeValueError):
            Size(0).components(min_value=-1)
        with self.assertRaises(SizeValueError):
            Size(0).components(min_value=3.2)

    @given(
       strategies.builds(Size, strategies.integers()),
       strategies.integers(min_value=1),
       strategies.booleans()
    )
    def testResults(self, s, min_value, binary_units):
        """ Test component results. """
        (m, u) = s.components(min_value, binary_units)
        self.assertEqual(m * int(u), int(s))
        if u == B:
            return
        if binary_units:
            self.assertIn(u, BinaryUnits.UNITS())
        else:
            self.assertIn(u, DecimalUnits.UNITS())
        self.assertTrue(abs(m) >= min_value)

class RoundingTestCase(unittest.TestCase):
    """ Test rounding methods. """

    @given(
       SIZE_STRATEGY,
       strategies.one_of(
          SIZE_STRATEGY.filter(lambda x: int(x) >= 0),
          strategies.sampled_from(UNITS())
       ),
       strategies.sampled_from(ROUNDING_METHODS())
    )
    def testResults(self, s, unit, rounding):
        """ Test roundTo results. """
        rounded = s.roundTo(unit, rounding)

        if int(unit) == 0:
            self.assertEqual(rounded, Size(0))
            return

        converted = s.convertTo(unit)
        if converted.denominator == 1:
            self.assertEqual(rounded, s)
            return

        factor = int(unit)
        (q, r) = divmod(converted.numerator, converted.denominator)
        ceiling = Size((q + 1) * factor)
        floor = Size(q * factor)
        if rounding is ROUND_UP:
            self.assertEqual(rounded, ceiling)
            return

        if rounding is ROUND_DOWN:
            self.assertEqual(rounded, floor)
            return

        remainder = abs(Fraction(r, converted.denominator))
        half = Fraction(1, 2)
        if remainder > half:
            self.assertEqual(rounded, ceiling)
        elif remainder < half:
            self.assertEqual(rounded, floor)
        else:
            if rounding is ROUND_HALF_UP:
                self.assertEqual(rounded, ceiling)
            else:
                self.assertEqual(rounded, floor)

    def testExceptions(self):
        """ Test raising exceptions when rounding. """
        with self.assertRaises(SizeValueError):
            Size(0).roundTo(Size(-1, B), rounding=ROUND_HALF_UP)
