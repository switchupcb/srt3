#!/usr/bin/python3

"""Merge multiple subtitles together into one."""

import datetime
import logging
from . import _cli


log = logging.getLogger(__name__)


def deduplicate(orig_subs, acceptable_diff):
    r"""
    Removes subtitles with duplicated content.

    :param orig_subs: :py:class:`Subtitle` objects
    :param datetime.timedelta acceptable_diff: The amount of milliseconds
                                    a subtitle start time must be to shift.
    :rtype: :term:`generator` of :py:class:`Subtitle` objects
    """
    indices_to_remove = set()

    # If we only store the subtitle itself and compare that, it's possible that
    # we'll not only remove the duplicate, but also the _original_ subtitle if
    # they have the same sub index/times/etc.
    #
    # As such, we need to also store the index in the original subs list that
    # this entry belongs to for each subtitle prior to sorting.
    sorted_subs = sorted(
        enumerate(orig_subs), key=lambda sub: (sub[1].content, sub[1].start)
    )

    for subs in _cli.sliding_window(sorted_subs, width=2, inclusive=False):
        cur_idx, cur_sub = subs[0]
        next_idx, next_sub = subs[1]

        if cur_sub.content == next_sub.content and (
            not acceptable_diff or cur_sub.start + acceptable_diff >= next_sub.start
        ):
            log.debug(
                "Marking l%d/s%d for removal, duplicate of l%d/s%d",
                next_idx,
                next_sub.index,
                cur_idx,
                cur_sub.index,
            )
            indices_to_remove.add(next_idx)

    offset = 0
    for idx in indices_to_remove:
        del orig_subs[idx - offset]
        offset += 1


def set_args():
    examples = {
        "Remove duplicated subtitles within 5 seconds of each other": "srt deduplicate -i duplicated.srt",
        "Remove duplicated subtitles within 500 milliseconds of each other": "srt deduplicate -t 500 -i duplicated.srt",
        "Remove duplicated subtitles regardless of temporal proximity": "srt deduplicate -t 0 -i duplicated.srt",
    }
    parser = _cli.basic_parser(
        description=__doc__,
        examples=examples,
    )
    parser.add_argument(
        "--ms",
        "-t",
        metavar="MILLISECONDS",
        default=datetime.timedelta(milliseconds=5000),
        type=lambda ms: datetime.timedelta(milliseconds=int(ms)),
        help="how many milliseconds distance a subtitle start time must be"
        "within of another to be considered a duplicate "
        "(default: 5000ms)",
    )

    return parser.parse_args()


def main():
    args = set_args()
    logging.basicConfig(level=args.log_level)
    _cli.set_basic_args(args)

    subs = list(args.input)
    deduplicate(subs, args.ms)
    output = _cli.compose_suggest_on_fail(subs, strict=args.strict)
    args.output.write(output)


if __name__ == "__main__":  # pragma: no cover
    main()
