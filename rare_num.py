#!/usr/bin/env python3

"""A tool for generating rare numbers"""

import argparse
import itertools
import math
import sys


def rare_last_digit(first):
    """Given a leading digit, first, return all possible last digits of a rare number"""

    if first == 2:
        return (2,)
    elif first == 4:
        return (0,)
    elif first == 6:
        return (0,5)
    elif first == 8:
        return (2,3,7,8)
    else:
        raise ValueError(f"Invalid first digit of rare number: {first}")


def py37_isqrt(n):
    """Return largest integer r such that r^2 <= n"""

    if n < 10000000000000000000000: # trial and error
        return math.floor(math.sqrt(n))
    else:
        # https://stackoverflow.com/a/53983683
        if n > 0:
            x = 1 << (n.bit_length() + 1 >> 1)
            while True:
                y = (x + n // x) >> 1
                if y >= x:
                    return x
                x = y
        elif n == 0:
            return 0
        else:
            raise ValueError("square root not defined for negative numbers")


if sys.version_info.major == 3 and sys.version_info.minor >= 8:
    isqrt = math.isqrt
else:
    isqrt = py37_isqrt


def is_perfect_square(n):
    """Return True if n is a Perfect Square"""

    # These shortcuts actually take longer than just checking with isqrt
    #if n % 10 in (2, 3, 7, 8):
    #    return False
    #if digital_root(n) not in (1, 4, 7, 9):
    #    return False
    sqt = isqrt(n)
    return sqt * sqt == n


def digital_root(n):
    """
    Return the sum of the digits of n, repeated until one digit remains.
    This happens to be the same as n % 9 except in the case where the
    modulus is 0 and n is greater than 0, in which case the result
    is 9.
    """

    if n == 0:
        return 0
    mn = n % 9
    return 9 if mn == 0 else mn


def is_rare(n, rev=None):
    """Return True if n is a Rare Number"""

    # This is a good high-pass filter, but slow
    #if digital_root(n) not in (2, 5, 8, 9):
    #    return False
    if rev is None:
        rev = int(str(n)[::-1])
        # Assume if rev is passed in, this check was done
        if rev >= n:
            return False
    return is_perfect_square(n + rev) and is_perfect_square(n - rev)


def rare_second_digits(first, last):
    """
    Given the first and last digits, return tuples of all possible
    second, second-from-last digits in a rare number
    """

    if first == 2 or (first == 8 and last == 8):
        for n in range(10):
            yield (n, n)
    elif first == 4:
        for a in range(0, 10):
            for b in range((0 if a % 2 == 0 else 1), 10, 2):
                yield (a, b)
    elif first == 6:
        for a in range(0, 10):
            for b in range((1 if a % 2 == 0 else 0), 10, 2):
                yield (a, b)
    elif first == 8:
        if last == 2 or last == 8:
            for a in range(0, 10):
                yield (a, 9-a)
        elif last == 3:
            for a in range (0, 10):
                if a > 6:
                    yield (a, a-7)
                else:
                    yield (a, a+3)
        elif last == 7:
            for a in range(0, 10):
                if a > 1:
                    yield (a, 11-a)
                else:
                    yield (a, 1-a)


def _digit_pairs(filter_func):
    """Generate pairs of digits that meet filter_func's metric"""

    for a, b in itertools.product(range(10), repeat=2):
        if filter_func(a, b):
            yield (a, b)


def rare_numbers(digits):
    """Return all rare numbers of length `digits`"""

    if digits > 1:
        for lead_d in (2,4,6,8):
            for last_d in rare_last_digit(first=lead_d):
                if digits < 4:
                    for mid in ([""] if digits == 2 else "0123456789"):
                        n = int(str(lead_d) + mid + str(last_d))
                        if is_rare(n):
                            yield n
                else:
                    # Further constraints on second and second to
                    # last digits based on first and last.
                    # see http://www.shyamsundergupta.com/rare.htm
                    for mid_lead_d, mid_last_d in rare_second_digits(lead_d, last_d):
                        start = str(lead_d) + str(mid_lead_d)
                        end = str(mid_last_d) + str(last_d)
                        if digits == 4:
                            n = int(start + end)
                            rev = int(str(n)[::-1])
                            if n > rev and is_rare(n, rev=rev):
                                yield n
                        else:
                            # 1 followed by digits in middle piece
                            mid_range = 10 ** (digits - 4)
                            mid = mid_range
                            while mid < 2 * mid_range:
                                # Drop the leading "1" for fast 0-padding
                                n = int(start + str(mid)[1:] + end)
                                # Perform a quich check and if it passes, call is_rare
                                # for the full check
                                rev = int(str(n)[::-1])
                                # All valid results will show check % 11 == 0,
                                # but that test is slower than is_rare
                                #check = n + rev if digits % 2 == 0 else n - rev
                                if n > rev and is_rare(n, rev=rev):
                                    yield n
                                root_n = digital_root(n)
                                # A number with a digital root other than 2, 5, 8 or 9
                                # cannot be a rare number, so we skip forward after 
                                # checking a number that has such a root. It doesn't
                                # matter that we're only incrementing the middle-part
                                # of the final number, since it affects the root the
                                # same no matter what part of the number you increment.
                                if root_n in (2, 5):
                                    mid += 3
                                elif root_n == 9:
                                    mid += 2
                                else:
                                    mid += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose output")
    parser.add_argument('--start', metavar='DIGITS', type=int, default=2, help="Starting number of digits")
    parser.add_argument('--end', metavar='DIGITS', type=int, default=None, help="Ending number of digits (optional)")
    options = parser.parse_args()

    start = options.start
    if start < 1:
        raise ValueError(f"Number of digits must be >= 1, not {start!r}")
    end = options.end

    for digits in itertools.count(start):
        if end and digits > end:
            break
        if options.verbose:
            print(f"{digits} digits...")
        for rare in rare_numbers(digits=digits):
            print(rare)


if __name__ == '__main__':
    main()
