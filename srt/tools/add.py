#!/usr/bin/python3

"""Add a subtitle to subtitles."""

import datetime
import logging
import srt
from types import GeneratorType
from . import _cli
from . import _utils

log = logging.getLogger(__name__)


def add(subs, start, end, content="", adjust=False):
    """
    Adds a subtitle to subtitles in the correct position.

    :param subs: :py:class:`Subtitle` objects
    :param datetime.timedelta start: The timestamp the subtitle starts at.
    :param datetime.timedelta end: The timestamp the subtitle ends at.
    :param boolean adjust: Whether to adjust the timestamps of subsequent subtitles.
    :rtype: :term:`generator` of :py:class:`Subtitle` objects
    """
    if end <= start:
        raise ValueError(
            "The end timestamp can't occur before or at the start timestamp."
        )

    # ensures list compatibility
    subs = (x for x in subs) if not isinstance(subs, GeneratorType) else subs

    # Add the subtitle in the correct position.
    added = False
    idx = 1
    adjust_time = datetime.timedelta(0)
    subtitle = _utils.tryNext(subs)
    while subtitle is not None:
        subtitle_start = subtitle.start

        if not added and (
            (start == subtitle_start and end < subtitle.end) or start < subtitle_start
        ):
            yield srt.Subtitle(
                idx,
                start,
                end,
                content,
            )
            idx += 1
            adjust_time = end - start if adjust else adjust_time
            added = True

        yield srt.Subtitle(
            idx,
            subtitle_start + adjust_time,
            subtitle.end + adjust_time,
            subtitle.content,
        )
        idx += 1
        subtitle = _utils.tryNext(subs)

    if not added:
        yield srt.Subtitle(
            idx,
            start,
            end,
            content,
        )


# Command Line Interface
def set_args():
    examples = {
        "Add a subtitle": 'srt add -i example.srt -s 00:00:5,00 -e 00:00:5,00 -c "srt3 is awesome."',
        "Add a subtitle and adjust subsequent ones": 'srt add -i example.srt -s 00:00:5,00 -e 00:00:5,00 --c "srt3 is awesome." -a',
    }
    parser = _cli.basic_parser(description=__doc__, examples=examples)
    parser.add_argument(
        "--start",
        "-s",
        metavar=("TIMESTAMP"),
        type=lambda arg: srt.srt_timestamp_to_timedelta(arg),
        default=datetime.timedelta(0),
        nargs="?",
        help="The timestamp to start the subtitle at.",
    )
    parser.add_argument(
        "--end",
        "-e",
        metavar=("TIMESTAMP"),
        type=lambda arg: srt.srt_timestamp_to_timedelta(arg),
        default=datetime.timedelta(0),
        nargs="?",
        help="The timestamp to stop the subtitle at.",
    )
    parser.add_argument(
        "-c", "--content", required=True, help="The content of the subtitle."
    )
    parser.add_argument(
        "--adjust",
        "-a",
        action="store_true",
        help="Adjust the timestamps of subsequent subtitles.",
    )
    return parser.parse_args()


def main():
    args = set_args()
    logging.basicConfig(level=args.log_level)
    _cli.set_basic_args(args)
    add_subs = add(args.input, args.start, args.end, args.content, args.adjust)
    output = _cli.compose_suggest_on_fail(add_subs, strict=args.strict)
    args.output.write(output)


if __name__ == "__main__":  # pragma: no cover
    main()
