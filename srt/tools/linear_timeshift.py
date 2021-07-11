#!/usr/bin/python3

"""Perform linear time correction on a subtitle."""

import datetime
import logging
import srt
from . import _cli

log = logging.getLogger(__name__)


def _timedelta_to_milliseconds(delta):
    return delta.days * 86400000 + delta.seconds * 1000 + delta.microseconds / 1000


def _calc_correction(to_start, to_end, from_start, from_end):
    angular = (to_end - to_start) / (from_end - from_start)
    linear = to_end - angular * from_end
    return angular, linear


def _correct_timedelta(bad_delta, angular, linear):
    bad_msecs = _timedelta_to_milliseconds(bad_delta)
    good_msecs = round(bad_msecs * angular + linear)
    good_delta = datetime.timedelta(milliseconds=good_msecs)
    return good_delta


def timeshift(subtitles, angular, linear):
    """
    Performs a linear timeshift on given subtitles.

    :param subtitles: :py:class:`Subtitle` objects
    :param float angular:
    :param float linear:
    :rtype: :term:`generator` of :py:class:`Subtitle` objects
    """
    for subtitle in subtitles:
        subtitle.start = _correct_timedelta(subtitle.start, angular, linear)
        subtitle.end = _correct_timedelta(subtitle.end, angular, linear)
        yield subtitle


def set_args():
    def _srt_timestamp_to_milliseconds(parser, arg):
        try:
            delta = srt.srt_timestamp_to_timedelta(arg)
        except ValueError:
            parser.error("not a valid SRT timestamp: %s" % arg)
        else:
            return _timedelta_to_milliseconds(delta)

    examples = {
        "Stretch out a subtitle so that second 1 is 2, 2 is 4, etc": "srt linear_timeshift --f1 00:00:01,000 --t1 00:00:01,000 --f2 00:00:02,000 --t2 00:00:03,000"
    }

    parser = _cli.basic_parser(description=__doc__, examples=examples)
    parser.add_argument(
        "--from-start",
        "--f1",
        type=lambda arg: _srt_timestamp_to_milliseconds(parser, arg),
        required=True,
        help="The first desynchronised timestamp.",
    )
    parser.add_argument(
        "--from-end",
        "--f2",
        type=lambda arg: _srt_timestamp_to_milliseconds(parser, arg),
        required=True,
        help="The second desynchronised timestamp.",
    )
    parser.add_argument(
        "--to-start",
        "--t1",
        type=lambda arg: _srt_timestamp_to_milliseconds(parser, arg),
        required=True,
        help="The first synchronised timestamp.",
    )
    parser.add_argument(
        "--to-end",
        "--t2",
        type=lambda arg: _srt_timestamp_to_milliseconds(parser, arg),
        required=True,
        help="The second synchronised timestamp.",
    )
    return parser.parse_args()


def main():
    args = set_args()
    logging.basicConfig(level=args.log_level)
    angular, linear = _calc_correction(
        args.to_start, args.to_end, args.from_start, args.from_end
    )
    _cli.set_basic_args(args)
    corrected_subs = timeshift(args.input, angular, linear)
    output = _cli.compose_suggest_on_fail(corrected_subs, strict=args.strict)
    args.output.write(output)


if __name__ == "__main__":  # pragma: no cover
    main()
