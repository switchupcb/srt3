#!/usr/bin/python3

"""Paste subtitles into other subtitles at a timestamp."""

import datetime
import logging
import srt
from types import GeneratorType
from . import utils


log = logging.getLogger(__name__)


def _tryNextSub(subs):
    try:
        return next(subs)
    except StopIteration:
        return None


def paste(subs, copy, timestamp, space=datetime.timedelta(0), block=False):
    """Paste subtitles into other subtitles at a timestamp.

    :param subs: :py:class:`Subtitle` objects
    :param copy: :py:class: The `Subtitle` objects to be pasted.
    :param datetime.timedelta timestamp: The timestamp to paste at.
    :param datetime.timedelta space: The amount of space to precede the paste.
    :param boolean block: Whether to paste the copied captions as a block
                          and adjust the timestamps of subsequent captions.
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

    # Ensure each block is an iterable
    subs = (x for x in subs) if not isinstance(subs, GeneratorType) else subs
    copy = (x for x in copy) if not isinstance(copy, GeneratorType) else copy

    # Perform the paste operation.
    subtitle = _tryNextSub(subs)
    copied_subtitle = _tryNextSub(copy)
    copied_time = timestamp + space
    idx = 1
    while subtitle is not None or copied_subtitle is not None:
        if subtitle is None:
            yield srt.Subtitle(
                idx,
                copied_subtitle.start + copied_time,
                copied_subtitle.end + copied_time,
                copied_subtitle.content,
            )
            idx += 1
            copied_subtitle = _tryNextSub(copy)

        elif copied_subtitle is None:
            yield srt.Subtitle(
                idx,
                subtitle.start + block_time,
                subtitle.end + block_time,
                subtitle.content,
            )
            idx += 1
            subtitle = _tryNextSub(subs)

        # fmt: off
        # ^ prevents extravagant statement expansion from black
        else:
            subtitle_start = subtitle.start
            subtitle_end = subtitle.end
            if subtitle.start > timestamp:
                subtitle_start += block_time
                subtitle_end += block_time

            copied_subtitle_start = copied_subtitle.start + copied_time
            copied_subtitle_end = copied_subtitle.end + copied_time

            # compare the alterted timestamps of subtitle and copied_subtitle
            if subtitle_start > copied_subtitle_start:
                yield srt.Subtitle(idx, copied_subtitle_start, copied_subtitle_end, copied_subtitle.content)
                idx += 1
                last_copied_subtitle = copied_subtitle
                copied_subtitle = _tryNextSub(copy)
            elif subtitle_start < copied_subtitle_start:
                yield srt.Subtitle(idx, subtitle_start, subtitle_end, subtitle.content)
                idx += 1
                subtitle = _tryNextSub(subs)
            elif subtitle_start == copied_subtitle_start:
                if (subtitle_end > copied_subtitle_end):
                    yield srt.Subtitle(idx, copied_subtitle_start, copied_subtitle_end, copied_subtitle.content)
                    idx += 1
                    last_copied_subtitle = copied_subtitle
                    copied_subtitle = _tryNextSub(copy)
                else:
                    yield srt.Subtitle(idx, subtitle_start, subtitle_end, subtitle.content)
                    idx += 1
                    subtitle = _tryNextSub(subs)
        # fmt: on


# Command Line Interface
def parse_args():
    examples = {
        "Paste captions from :05 - :08 at :10": "srt remove -i example.srt --t1 00:00:5,00 --t2 00:00:8,00 --p 00:00:10,00",
        "Paste captions from :05 - :08 at :10 with :01 space beforehand": "srt remove -i example.srt --t1 00:00:5,00 --t2 00:00:8,00 --p 00:00:10,00 --s 00:00:01,00 ",
        "Paste captions from :05 - :08 at :10 and adjust all subsequent captions": "srt remove -i example.srt --t1 00:00:5,00 --t2 00:00:8,00 --p 00:00:10,00 --b",
    }
    parser = utils.basic_parser(description=__doc__, examples=examples)
    parser.add_argument(
        "--start",
        "--t1",
        metavar=("TIMESTAMP"),
        type=lambda arg: srt.srt_timestamp_to_timedelta(arg),
        default=datetime.timedelta(0),
        nargs="?",
        help="The timestamp to start copying from.",
    )
    parser.add_argument(
        "--end",
        "--t2",
        metavar=("TIMESTAMP"),
        type=lambda arg: srt.srt_timestamp_to_timedelta(arg),
        default=datetime.timedelta(0),
        nargs="?",
        help="The timestamp to stop copying at.",
    )
    parser.add_argument(
        "--p",
        "--paste",
        metavar=("TIMESTAMP"),
        type=lambda arg: srt.srt_timestamp_to_timedelta(arg),
        default=datetime.timedelta(0),
        nargs="?",
        help="The timestamp to paste from.",
    )
    parser.add_argument(
        "--s",
        "--space",
        metavar=("TIMESTAMP"),
        type=lambda arg: srt.srt_timestamp_to_timedelta(arg),
        default=datetime.timedelta(0),
        help="The timestamp to paste from.",
    )
    parser.add_argument(
        "--z",
        "--zero",
        action="store_true",
        help="Start the copied caption block from 00:00.",
    )
    parser.add_argument(
        "--b",
        "--block",
        action="store_true",
        help="Paste copied captions as a block and adjust subsequent captions' timestamps.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=args.log_level)
    utils.set_basic_args(args)
    origin_subs = list(args.input)
    copy_subs = srt.tools.find.find_by_timestamp(
        origin_subs, args.start, args.end, args.zero
    )
    paste_subs = paste(origin_subs, copy_subs, args.paste, args.space, args.block)
    output = utils.compose_suggest_on_fail(paste_subs, strict=args.strict)
    args.output.write(output)


if __name__ == "__main__":  # pragma: no cover
    main()