#!/usr/bin/python3

"""Find subtitles by timestamp."""

import datetime
import logging
import srt
from types import GeneratorType
from . import _cli
from . import _utils


log = logging.getLogger(__name__)


def find_by_timestamp(
    subs,
    timestamp_one=datetime.timedelta(0),
    timestamp_two=datetime.timedelta(0),
    adjust=False,
):
    """
    Finds subtitles from subtitles by timestamp.
    When timestamp one > timestamp two, subtitles up to timestamp two and
    subtitles after timestamp one will be found.

    :param subs: :py:class:`Subtitle` objects
    :param datetime.timedelta timestamp_one: The timestamp to find from.
    :param datetime.timedelta timestamp_two: The timestamp to find to.
    :param boolean adjust: Whether to adjust the timestamps of found subtitles.
    :rtype: :term:`generator` of :py:class:`Subtitle` objects
    """
    # ensure subs is iterable
    subs = (x for x in subs) if not isinstance(subs, GeneratorType) else subs

    # Split the subtitle at the start and end of the block(s).
    subs = srt.tools.split.split(subs, timestamp_one)
    subs = srt.tools.split.split(subs, timestamp_two)

    # edge cases
    subtitle = _utils.tryNext(subs)
    sequential = timestamp_one < timestamp_two
    if subtitle is None or (sequential and timestamp_two <= subtitle.start):
        return

    # Find the subtitles using a generator.
    idx = 1
    adjust_time = timestamp_one if adjust else datetime.timedelta(0)
    while subtitle is not None:
        start = subtitle.start

        if (
            timestamp_one == timestamp_two
            or (sequential and timestamp_one <= start and start < timestamp_two)
            or (not sequential and (start < timestamp_two or timestamp_one <= start))
        ):
            yield srt.Subtitle(
                idx,
                subtitle.start - adjust_time,
                subtitle.end - adjust_time,
                subtitle.content,
            )
            idx += 1

        subtitle = _utils.tryNext(subs)


# Command Line Interface
def set_args():
    examples = {
        "Find subtitles from :05 - :08": "srt find -i example.srt -s 00:00:5,00 -e 00:00:8,00",
        "Find subtitles from :00 - :05 and :08 onwards": "srt find -i example.srt -s 00:00:8,00 -e 00:00:5,00",
        "Find subtitles from :00 - :16 and adjust the timestamps of found subtitles": "srt find -i example.srt -e 00:00:16,00",
        "Find subtitles from :16 onwards and zero the block.": "srt find -i example.srt -s 00:00:16,00 -a",
        "Find every subtitle": "srt find -i example.srt",
    }
    parser = _cli.basic_parser(description=__doc__, examples=examples)
    parser.add_argument(
        "--start",
        "-s",
        metavar=("TIMESTAMP"),
        type=lambda arg: srt.srt_timestamp_to_timedelta(arg),
        default=datetime.timedelta(0),
        nargs="?",
        help="The timestamp to start removing from.",
    )
    parser.add_argument(
        "--end",
        "-e",
        metavar=("TIMESTAMP"),
        type=lambda arg: srt.srt_timestamp_to_timedelta(arg),
        default=datetime.timedelta(0),
        nargs="?",
        help="The timestamp to stop removing at.",
    )
    parser.add_argument(
        "--adjust",
        "-a",
        action="store_true",
        help="Adjust the timestamps of subtitles by placing the first found subtitle at 00:00.",
    )
    return parser.parse_args()


def main():
    args = set_args()
    logging.basicConfig(level=args.log_level)
    _cli.set_basic_args(args)
    found_subs = find_by_timestamp(args.input, args.start, args.end, args.adjust)
    output = _cli.compose_suggest_on_fail(found_subs, strict=args.strict)
    args.output.write(output)


if __name__ == "__main__":  # pragma: no cover
    main()
