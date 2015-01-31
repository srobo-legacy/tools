# luhn.py - functions for performing the Luhn and Luhn mod N algorithms
#
# Copyright (C) 2010 Arthur de Jong
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA

"""
Module for calculation and verifying the checksum of a number
using the Luhn algorithm.

Validation can be done with is_valid() which validates that the
calculated checksum is 0. A valid number can be made by calculating
the check digit and appending it.

>>> is_valid('7894')
False
>>> checksum('7894')
6
>>> calc_check_digit('7894')
'9'
>>> is_valid('78949')
True

An alternative alphabet can be provided to use the Luhn mod N algorithm.
The default alphabet is '0123456789'.

>>> is_valid('1234', alphabet='0123456789abcdef')
False
>>> checksum('1234', alphabet='0123456789abcdef')
14
"""


def checksum(number, alphabet='0123456789'):
    """
    Calculate the Luhn checksum over the provided number. Valid numbers should
    have a checksum of 0.

    :param str number: The number to calculate the checksum of.
    :param str alphabet: The alphabet of digits.
    :returns: The checksum of the number.
    :rtype: int
    """
    n = len(alphabet)
    number = tuple(alphabet.index(i) for i in reversed(str(number)))
    return (sum(number[::2]) +
            sum(sum(divmod(i * 2, n)) for i in number[1::2])) % n


def is_valid(number, alphabet='0123456789'):
    """
    Checks to see if the number provided passes the Luhn checksum.

    :param str number: The number to validate.
    :param str alphabet: The alphabet of digits.
    :returns: True if the number is valid.
    :rtype: bool
    """
    return checksum(number, alphabet) == 0


def calc_check_digit(number, alphabet='0123456789'):
    """
    With the provided number, calculate the extra digit that should be appended
    to make it pass the Luhn checksum.

    :param str number: The number to calculate the check digit of.
    :param str alphabet: The alphabet of digits.
    :returns: The check digit of the number.
    :rtype: int
    """
    ck = checksum(str(number) + alphabet[0], alphabet)
    return alphabet[-ck]
