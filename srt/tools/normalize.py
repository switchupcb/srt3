#!/usr/bin/python3

"""Take a badly formatted SRT file and output a strictly valid one."""

import logging
from . import _cli

log = logging.getLogger(__name__)


def normalize(subs, strict):
    """
    Normalises subtitles.

    :param subs: :py:class:`Subtitle` objects
    :param bool strict: Whether to enable strict mode, see
                        :py:func:`Subtitle.to_srt` for more information
    :returns: A single SRT formatted string, with each input
                        :py:class:`Subtitle` represented as an SRT block
    :rtype: str
    :raises SRTParseError: If parsing fails.
    """
    return _cli.compose_suggest_on_fail(subs, strict)


def main():
    examples = {"Normalise a subtitle": "srt normalize -i bad.srt -o good.srt"}

    args = _cli.basic_parser(
        description=__doc__, examples=examples, hide_no_strict=True
    ).parse_args()
    logging.basicConfig(level=args.log_level)
    _cli.set_basic_args(args)
    output = normalize(args.input, strict=args.strict)
    args.output.write(output)


if __name__ == "__main__":  # pragma: no cover
    main()
