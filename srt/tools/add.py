#!/usr/bin/python3

"""Adds a subtitle to subtitles."""

import datetime
import logging
import srt
from . import utils

log = logging.getLogger(__name__)


def add(subs, start, end, content="", adjust=False):
    """
    Adds a subtitle to subtitles in the correct position.

    :param subs: :py:class:`Subtitle` objects
    :param datetime.timedelta start: The timestamp the subtitle starts at.
    :param datetime.timedelta end: The timestamp the subtitle ends at.
    :param boolean adjust: Whether to adjust the timestamps of subsequent captions.
    :rtype: :term:`generator` of :py:class:`Subtitle` objects
    """
    if end <= start:
        raise ValueError(
            "The end timestamp can't occur before or at the start timestamp."
        )

    # ensures list compatibility
    from types import GeneratorType

    subs = (x for x in subs) if not isinstance(subs, GeneratorType) else subs

    # Add subtitles before the added subtitle
    idx = 1
    add_subs = []
    break_sub = None
    for subtitle in subs:
        # determine the correct position
        if subtitle.start < start:
            yield subtitle
            idx += 1
        elif start == subtitle.start:
            add_subs.append(subtitle)
        elif start < subtitle.start:
            break_sub = subtitle
            break

    # add the subtitle to the correct position
    adjust_time = datetime.timedelta(0)
    add_subs_len = len(add_subs)
    if add_subs_len == 0:
        adjust_time = end - start if adjust else adjust_time
        yield srt.Subtitle(idx, start, end, content)
        idx += 1
    else:
        for i in range(add_subs_len):
            subtitle = add_subs[i]

            if i + 1 < add_subs_len and subtitle.end <= end and end < add_subs[i + 1]:
                adjust_time = end - start if adjust else adjust_time
                yield srt.Subtitle(idx, start, end, content)
                idx += 1
            yield srt.Subtitle(
                idx,
                subtitle.start + adjust_time,
                subtitle.end + adjust_time,
                subtitle.content,
            )
            idx += 1

    # Add the remaining subtitles.
    if break_sub:
        yield srt.Subtitle(
            idx,
            break_sub.start + adjust_time,
            break_sub.end + adjust_time,
            break_sub.content,
        )
        idx += 1
        for subtitle in subs:
            yield srt.Subtitle(
                idx,
                subtitle.start + adjust_time,
                subtitle.end + adjust_time,
                subtitle.content,
            )
            idx += 1


# Command Line Interface
def parse_args():
    examples = {
        "Add a caption": "srt add -i example.srt --start 00:00:5,00 --end 00:00:5,00 --content srt3 is awesome.",
    }
    parser = utils.basic_parser(description=__doc__, examples=examples)
    parser.add_argument(
        "--start",
        "--t1",
        metavar=("TIMESTAMP"),
        type=lambda arg: srt.srt_timestamp_to_timedelta(arg),
        default=datetime.timedelta(0),
        nargs="?",
        help="The timestamp to start the subtitle at.",
    )
    parser.add_argument(
        "--end",
        "--t2",
        metavar=("TIMESTAMP"),
        type=lambda arg: srt.srt_timestamp_to_timedelta(arg),
        default=datetime.timedelta(0),
        nargs="?",
        help="The timestamp to stop the subtitle at.",
    )
    parser.add_argument(
        "-c", "--content", help="The content of the subtitle", required=True
    )
    parser.add_argument(
        "--at",
        "--adjust",
        action="store_true",
        help="Adjust the timestamps of non-removed captions",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=args.log_level)
    utils.set_basic_args(args)
    add_subs = add(args.input, args.start, args.end, args.content, args.adjust)
    output = utils.compose_suggest_on_fail(add_subs, strict=args.strict)
    args.output.write(output)


if __name__ == "__main__":  # pragma: no cover
    main()
