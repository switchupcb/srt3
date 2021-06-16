#!/usr/bin/python3

"""Shifts a subtitle by a fixed number of seconds."""

from .. import utils
import datetime
import logging

log = logging.getLogger(__name__)


def scalar_correct_subs(subtitles, seconds_to_shift):
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


def parse_args():
    examples = {
        "Make all subtitles 5 seconds later": "srt fixed_timeshift --seconds 5",
        "Make all subtitles 5 seconds earlier": "srt fixed_timeshift --seconds -5",
    }

    parser = utils.basic_parser(description=__doc__, examples=examples)
    parser.add_argument(
        "--seconds", type=float, required=True, help="how many seconds to shift"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=args.log_level)
    utils.set_basic_args(args)
    corrected_subs = scalar_correct_subs(args.input, args.seconds)
    output = utils.compose_suggest_on_fail(corrected_subs, strict=args.strict)
    args.output.write(output)


if __name__ == "__main__":  # pragma: no cover
    main()
