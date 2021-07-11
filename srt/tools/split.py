#!/usr/bin/python3

"""Split subtitles at a given timestamp."""

import datetime
import logging
import srt
from types import GeneratorType
from . import _utils
from . import _cli

log = logging.getLogger(__name__)


def split(subs, timestamp):
    """
    Splits subtitles at a given timestamp.

    :param subs: :py:class:`Subtitle` objects
    :param datetime.timedelta timestamp: The timestamp to split subtitles at.
    :rtype: :term:`generator` of :py:class:`Subtitle` objects
    """
    # ensures list compatibility
    subs = (x for x in subs) if not isinstance(subs, GeneratorType) else subs

    # Split subtitles at timestamp.
    added_split_subs = False
    idx = 1
    subtitle = _utils.tryNext(subs)
    split_subs = []
    while subtitle is not None:
        start = subtitle.start
        end = subtitle.end

        if start < timestamp and timestamp < end:
            yield srt.Subtitle(idx, start, timestamp, subtitle.content)
            idx += 1
            split_subs.append(srt.Subtitle(idx, timestamp, end, subtitle.content))
        elif not added_split_subs and timestamp < start:
            added_split_subs = True
            split_subs.sort()
            for sub in split_subs:
                yield srt.Subtitle(idx, timestamp, sub.end, sub.content)
                idx += 1
            yield srt.Subtitle(idx, start, end, subtitle.content)
            idx += 1
        else:
            yield srt.Subtitle(idx, start, end, subtitle.content)
            idx += 1

        subtitle = _utils.tryNext(subs)

    if not added_split_subs:
        split_subs.sort()
        for sub in split_subs:
            yield srt.Subtitle(idx, timestamp, sub.end, sub.content)
            idx += 1


# Command Line Interface
def set_args():
    examples = {
        "Split subtitles at :05": "srt split -i example.srt -t 00:00:5,00",
    }
    parser = _cli.basic_parser(description=__doc__, examples=examples)
    parser.add_argument(
        "-t",
        "--timestamp",
        metavar=("TIMESTAMP"),
        type=lambda arg: srt.srt_timestamp_to_timedelta(arg),
        default=datetime.timedelta(0),
        nargs="?",
        help="The timestamp to split subtitles at.",
    )
    return parser.parse_args()


def main():
    args = set_args()
    logging.basicConfig(level=args.log_level)
    _cli.set_basic_args(args)
    split_subs = split(args.input, args.timestamp)
    output = _cli.compose_suggest_on_fail(split_subs, strict=args.strict)
    args.output.write(output)


if __name__ == "__main__":  # pragma: no cover
    main()
