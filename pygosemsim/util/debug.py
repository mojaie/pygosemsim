#
# (C) 2014-2017 Seiji Matsuoka
# Licensed under the MIT License (MIT)
# http://opensource.org/licenses/MIT
#

import os
import sys
import cProfile
import pstats
import linecache
import tracemalloc
from itertools import chain
from collections import deque


def profile(func):
    """ Decorator
    Execute cProfile
    """
    def _f(*args, **kwargs):
        print("\n<<<---")
        pr = cProfile.Profile()
        pr.enable()
        res = func(*args, **kwargs)
        p = pstats.Stats(pr)
        p.strip_dirs().sort_stats('cumtime').print_stats(20)
        print("\n--->>>")
        return res
    return _f


def total_size(obj, verbose=False):
    """ Returns approximate memory size"""
    seen = set()

    def sizeof(o):
        if id(o) in seen:
            return 0
        seen.add(id(o))
        s = sys.getsizeof(o, default=0)
        if verbose:
            print(s, type(o), repr(o))
        if isinstance(o, (tuple, list, set, frozenset, deque)):
            s += sum(map(sizeof, iter(o)))
        elif isinstance(o, dict):
            s += sum(map(sizeof, chain.from_iterable(o.items())))
        elif "__dict__" in dir(o):
            s += sum(map(sizeof, chain.from_iterable(o.__dict__.items())))
        return s

    return sizeof(obj)


def malloc(func):
    """ Decorator
    Execute tracemalloc
    """
    def _f(*args, **kwargs):
        print("\n<<<---")
        tracemalloc.start()
        res = func(*args, **kwargs)
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        print("[ Top 10 ]")
        for i, stat in enumerate(top_stats[:10]):
            frame = stat.traceback[0]
            filename = os.sep.join(frame.filename.split(os.sep)[-2:])
            print("#%s: %s:%s: %.1f KiB"
                  % (i, filename, frame.lineno, stat.size / 1024))
            print(linecache.getline(frame.filename, frame.lineno).strip())
            # print(stat)
        print("--->>>\n")
        return res
    return _f


def malloc_diff(func):
    """ Decorator
    Execute tracemalloc
    """
    def _f(*args, **kwargs):
        print("\n<<<---")
        tracemalloc.start()
        snapshot1 = tracemalloc.take_snapshot()
        res = func(*args, **kwargs)
        snapshot2 = tracemalloc.take_snapshot()
        top_stats = snapshot2.compare_to(snapshot1, 'lineno')
        print("[ Top 10 differences]")
        for stat in top_stats[:10]:
            print(stat)
        print("--->>>\n")
        return res
    return _f


def mute(func):
    """ Decorator
    Make stdout silent
    """
    def _f(*args, **kwargs):
        sys.stdout = open(os.devnull, 'w')
        res = func(*args, **kwargs)
        sys.stdout.close()
        sys.stdout = sys.__stdout__
        return res
    return _f
