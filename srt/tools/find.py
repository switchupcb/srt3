#!/usr/bin/python3

"""Find subtitles by index or timestamp."""

import datetime
import logging
import srt
from . import utils

log = logging.getLogger(__name__)


def find_by_timestamp(
    subs,
    timestamp_one=datetime.timedelta(0),
    timestamp_two=datetime.timedelta(0),
    adjust=False,
):
    """
    Finds captions from subtitles by timestamp.
    When timestamp one > timestamp two, captions up to timestamp two and
    captions after timestamp one will be found.

    :param subs: :py:class:`Subtitle` objects
    :param datetime.timedelta timestamp_one: The timestamp to find from.
    :param datetime.timedelta timestamp_two: The timestamp to find to.
    :param boolean adjust: Whether to adjust the timestamps of found captions.
    :rtype: :term:`generator` of :py:class:`Subtitle` objects
    """
    # ensures list compatibility
    from types import GeneratorType

    subs = (x for x in subs) if not isinstance(subs, GeneratorType) else subs
    adjust_time = timestamp_one if adjust else datetime.timedelta(0)
    idx = 1

    # edge cases
    sequential = timestamp_one < timestamp_two
    try:
        first_subtitle = next(subs)
    except StopIteration:
        return

    if timestamp_one == timestamp_two or (
        not sequential and timestamp_one <= first_subtitle.start
    ):
        yield srt.Subtitle(
            idx,
            first_subtitle.start - adjust_time,
            first_subtitle.end - adjust_time,
            first_subtitle.content,
        )
        idx += 1

        for subtitle in subs:
            yield srt.Subtitle(
                idx,
                subtitle.start - adjust_time,
                subtitle.end - adjust_time,
                subtitle.content,
            )
            idx += 1
        return
    elif sequential and timestamp_two <= first_subtitle.start:
        return

    # Split the caption at the start and end of the block(s).
    subs = srt.tools.split.split(subs, timestamp_one)
    subs = srt.tools.split.split(subs, timestamp_two)

    # Find the captions using a generator.
    if sequential:
        # remove captions before timestamp one
        if first_subtitle.start < timestamp_one:
            for subtitle in subs:
                if timestamp_one <= subtitle.start:
                    yield srt.Subtitle(
                        idx,
                        subtitle.start - adjust_time,
                        subtitle.end - adjust_time,
                        subtitle.content,
                    )
                    idx += 1
                    break
        else:
            yield srt.Subtitle(
                idx,
                first_subtitle.start - adjust_time,
                first_subtitle.end - adjust_time,
                first_subtitle.content,
            )
            idx += 1

        # keep captions after timestamp one but before timestamp two
        for subtitle in subs:
            if timestamp_two <= subtitle.start:
                break
            yield srt.Subtitle(
                idx,
                subtitle.start - adjust_time,
                subtitle.end - adjust_time,
                subtitle.content,
            )
            idx += 1

        # remove captions after timestamp two
        for subtitle in subs:
            pass
    else:
        # keep captions before timestamp two
        if first_subtitle.start < timestamp_two:
            yield srt.Subtitle(
                idx,
                first_subtitle.start - adjust_time,
                first_subtitle.end - adjust_time,
                first_subtitle.content,
            )
            idx += 1

            for subtitle in subs:
                if timestamp_two <= subtitle.start:
                    break
                yield srt.Subtitle(
                    idx,
                    subtitle.start - adjust_time,
                    subtitle.end - adjust_time,
                    subtitle.content,
                )
                idx += 1

        # remove captions after timestamp two but before timestamp one
        for subtitle in subs:
            if timestamp_one <= subtitle.start:
                yield srt.Subtitle(
                    idx,
                    subtitle.start - adjust_time,
                    subtitle.end - adjust_time,
                    subtitle.content,
                )
                idx += 1
                break

        # keep captions after timestamp one
        for subtitle in subs:
            yield srt.Subtitle(
                idx,
                subtitle.start - adjust_time,
                subtitle.end - adjust_time,
                subtitle.content,
            )
            idx += 1


# Command Line Interface
def parse_args():
    examples = {
        "Find captions from :05 - :08": "srt remove -i example.srt --t1 00:00:5,00 --t2 00:00:8,00",
        "Find captions from :00 - :05 and :08 onwards": "srt remove -i example.srt --t1 00:00:8,00 --t2 00:00:5,00",
        "Find captions from :00 - :16 and adjust the timestamps of found captions": "srt remove -i example.srt --t2 00:00:16,00",
        "Find captions from :16 onwards.": "srt remove -i example.srt --t1 00:00:16,00",
        "Find every caption": "srt remove -i example.srt",
    }
    parser = utils.basic_parser(description=__doc__, examples=examples)
    parser.add_argument(
        "--start",
        "--t1",
        metavar=("TIMESTAMP"),
        type=lambda arg: srt.srt_timestamp_to_timedelta(arg),
        default=datetime.timedelta(0),
        nargs="?",
        help="The timestamp to start removing from.",
    )
    parser.add_argument(
        "--end",
        "--t2",
        metavar=("TIMESTAMP"),
        type=lambda arg: srt.srt_timestamp_to_timedelta(arg),
        default=datetime.timedelta(0),
        nargs="?",
        help="The timestamp to stop removing at.",
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
    found_subs = find_by_timestamp(args.input, args.start, args.end, args.adjust)
    output = utils.compose_suggest_on_fail(found_subs, strict=args.strict)
    args.output.write(output)


if __name__ == "__main__":  # pragma: no cover
    main()
