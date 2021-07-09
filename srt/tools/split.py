#!/usr/bin/python3

"""Splits subtitles at a given timestamp."""

import datetime
import logging
import srt
from . import utils

log = logging.getLogger(__name__)


def split(subs, timestamp):
    """
    Splits subtitles at a given timestamp.

    :param subs: :py:class:`Subtitle` objects
    :param datetime.timedelta timestamp: The timestamp to split subtitles at.
    :rtype: :term:`generator` of :py:class:`Subtitle` objects
    """
    # ensures list compatibility
    from types import GeneratorType

    subs = (x for x in subs) if not isinstance(subs, GeneratorType) else subs

    # yield unsplit captions before the timestamp
    idx = 1
    break_subtitle = None
    split_subs = []
    for subtitle in subs:
        if subtitle.start < timestamp and timestamp < subtitle.end:
            yield srt.Subtitle(idx, subtitle.start, timestamp, subtitle.content)
            subtitle.start = timestamp
            split_subs.append(subtitle)
            idx += 1
        elif subtitle.start == timestamp:
            split_subs.append(subtitle)
        elif subtitle.start > timestamp:
            break_subtitle = subtitle
            break
        else:
            yield subtitle
            idx += 1

    # yield split captions (sort to adjust index first)
    split_subs.sort()
    for subtitle in split_subs:
        yield srt.Subtitle(idx, timestamp, subtitle.end, subtitle.content)
        idx += 1

    # yield unsplit captions after the timestamp
    if break_subtitle:
        yield srt.Subtitle(
            idx, break_subtitle.start, break_subtitle.end, break_subtitle.content
        )
        idx += 1

    for subtitle in subs:
        yield srt.Subtitle(idx, subtitle.start, subtitle.end, subtitle.content)
        idx += 1


# Command Line Interface
def parse_args():
    examples = {
        "Split captions at :05": "srt split -i example.srt -t 00:00:5,00",
    }
    parser = utils.basic_parser(description=__doc__, examples=examples)
    parser.add_argument(
        "-t",
        "--timestamp",
        metavar=("TIMESTAMP"),
        type=lambda arg: srt.srt_timestamp_to_timedelta(arg),
        default=datetime.timedelta(0),
        nargs="?",
        help="The timestamp to split captions at.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=args.log_level)
    utils.set_basic_args(args)
    split_subs = split(args.input, args.timestamp)
    output = utils.compose_suggest_on_fail(split_subs, strict=args.strict)
    args.output.write(output)


if __name__ == "__main__":  # pragma: no cover
    main()
