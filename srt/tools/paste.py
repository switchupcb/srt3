#!/usr/bin/python3

"""Paste subtitles into other subtitles at a given timestamp."""

import datetime
import logging
import srt
from types import GeneratorType
from . import _cli
from . import _utils


log = logging.getLogger(__name__)


def paste(subs, copy, timestamp, space=datetime.timedelta(0), block=False):
    """Pastes subtitles into other subtitles at a given timestamp.

    :param subs: :py:class:`Subtitle` objects
    :param copy: The :py:class:`Subtitle` objects to be pasted.
    :param datetime.timedelta timestamp: The timestamp to paste at.
    :param datetime.timedelta space: The amount of space to precede the paste.
    :param boolean block: Whether to paste the copied subtitles as a block
                          and adjust the timestamps of subsequent subtitles.
    :rtype: :term:`generator` of :py:class:`Subtitle` objects
    """
    # In the case of a block paste, determine the block time(span).
    block_time = datetime.timedelta(0)
    if block:
        block_copy = list(copy)
        for subtitle in block_copy:
            if subtitle.end > block_time:
                block_time = subtitle.end
        block_time += space
        copy = (x for x in block_copy)  # regenerate copy

    # Ensure each block is iterable
    subs = (x for x in subs) if not isinstance(subs, GeneratorType) else subs
    copy = (x for x in copy) if not isinstance(copy, GeneratorType) else copy

    # Perform the paste operation.
    idx = 1
    subtitle = _utils.tryNext(subs)
    copied_subtitle = _utils.tryNext(copy)
    copied_time = timestamp + space
    while subtitle is not None or copied_subtitle is not None:
        if subtitle is None:
            yield srt.Subtitle(
                idx,
                copied_subtitle.start + copied_time,
                copied_subtitle.end + copied_time,
                copied_subtitle.content,
            )
            idx += 1
            copied_subtitle = _utils.tryNext(copy)

        elif copied_subtitle is None:
            yield srt.Subtitle(
                idx,
                subtitle.start + block_time,
                subtitle.end + block_time,
                subtitle.content,
            )
            idx += 1
            subtitle = _utils.tryNext(subs)

        # fmt: off
        # ^ prevents extravagant statement expansion from black
        else:
            start = subtitle.start
            subtitle_end = subtitle.end
            if subtitle.start > timestamp:
                start += block_time
                subtitle_end += block_time

            copied_start = copied_subtitle.start + copied_time
            copied_end = copied_subtitle.end + copied_time

            # compare the alterted timestamps of subtitle and copied_subtitle
            if start > copied_start:
                yield srt.Subtitle(idx, copied_start, copied_end, copied_subtitle.content)
                idx += 1
                copied_subtitle = _utils.tryNext(copy)
            elif start < copied_start:
                yield srt.Subtitle(idx, start, subtitle_end, subtitle.content)
                idx += 1
                subtitle = _utils.tryNext(subs)
            elif start == copied_start:
                if (subtitle_end > copied_end):
                    yield srt.Subtitle(idx, copied_start, copied_end, copied_subtitle.content)
                    idx += 1
                    copied_subtitle = _utils.tryNext(copy)
                else:
                    yield srt.Subtitle(idx, start, subtitle_end, subtitle.content)
                    idx += 1
                    subtitle = _utils.tryNext(subs)
        # fmt: on


# Command Line Interface
def set_args():
    examples = {
        "Paste subtitles from :05 - :08 at :10": "srt paste -i example.srt --t1 00:00:5,00 --t2 00:00:8,00 -p 00:00:10,00",
        "Paste subtitles from :05 - :08 at :10 with :01 space beforehand": "srt paste -i example.srt --t1 00:00:5,00 --t2 00:00:8,00 -p 00:00:10,00 -s 00:00:01,00",
        "Paste subtitles from :05 - :08 at :10 and adjust all subsequent subtitles": "srt paste -i example.srt --t1 00:00:5,00 --t2 00:00:8,00 -p 00:00:10,00 -b",
    }
    parser = _cli.basic_parser(description=__doc__, examples=examples)
    parser.add_argument(
        "--t1",
        metavar=("TIMESTAMP"),
        type=lambda arg: srt.srt_timestamp_to_timedelta(arg),
        default=datetime.timedelta(0),
        nargs="?",
        help="The timestamp to start copying from.",
    )
    parser.add_argument(
        "--t2",
        metavar=("TIMESTAMP"),
        type=lambda arg: srt.srt_timestamp_to_timedelta(arg),
        default=datetime.timedelta(0),
        nargs="?",
        help="The timestamp to stop copying at.",
    )
    parser.add_argument(
        "--paste",
        "-p",
        metavar=("TIMESTAMP"),
        type=lambda arg: srt.srt_timestamp_to_timedelta(arg),
        default=datetime.timedelta(0),
        nargs="?",
        help="The timestamp to paste at.",
    )
    parser.add_argument(
        "--space",
        "-s",
        metavar=("TIMESTAMP"),
        type=lambda arg: srt.srt_timestamp_to_timedelta(arg),
        default=datetime.timedelta(0),
        help="The amount of space to place before copied subtitles.",
    )
    parser.add_argument(
        "--block",
        "-b",
        action="store_true",
        help="Paste copied subtitles as a block and adjust subsequent subtitles' timestamps.",
    )
    parser.add_argument(
        "--zero",
        "-z",
        action="store_true",
        help="Start the copied subtitle block from 00:00.",
    )
    return parser.parse_args()


def main():
    args = set_args()
    logging.basicConfig(level=args.log_level)
    _cli.set_basic_args(args)
    origin_subs = list(args.input)
    copy_subs = srt.tools.find.find_by_timestamp(
        origin_subs, args.t1, args.t2, args.zero
    )
    paste_subs = paste(origin_subs, copy_subs, args.paste, args.space, args.block)
    output = _cli.compose_suggest_on_fail(paste_subs, strict=args.strict)
    args.output.write(output)


if __name__ == "__main__":  # pragma: no cover
    main()
