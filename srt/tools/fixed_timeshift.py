#!/usr/bin/python3

"""Shifts subtitles by a fixed number of seconds."""

import datetime
import logging
from . import _cli

log = logging.getLogger(__name__)


def timeshift(subtitles, seconds_to_shift):
    """
    Performs a fixed timeshift on given subtitles.

    :param subtitles: :py:class:`Subtitle` objects
    :param float seconds_to_shift: The amount of seconds to shift.
    :rtype: :term:`generator` of :py:class:`Subtitle` objects
    """
    td_to_shift = datetime.timedelta(seconds=seconds_to_shift)
    for subtitle in subtitles:
        subtitle.start += td_to_shift
        subtitle.end += td_to_shift
        yield subtitle


def set_args():
    examples = {
        "Make all subtitles 5 seconds later": "srt fixed_timeshift -s 5",
        "Make all subtitles 5 seconds earlier": "srt fixed_timeshift --seconds -5",
    }

    parser = _cli.basic_parser(description=__doc__, examples=examples)
    parser.add_argument(
        "--seconds",
        "-s",
        type=float,
        required=True,
        help="The amount of seconds to shift subtitiles by.",
    )
    return parser.parse_args()


def main():
    args = set_args()
    logging.basicConfig(level=args.log_level)
    _cli.set_basic_args(args)
    corrected_subs = timeshift(args.input, args.seconds)
    output = _cli.compose_suggest_on_fail(corrected_subs, strict=args.strict)
    args.output.write(output)


if __name__ == "__main__":  # pragma: no cover
    main()
