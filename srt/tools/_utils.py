#!/usr/bin/python3


def tryNext(subs):
    """Finds the next subtitle in an iterator otherwise returns None."""
    try:
        return next(subs)
    except StopIteration:
        return None
