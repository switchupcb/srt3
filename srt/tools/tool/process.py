#!/usr/bin/python3

"""Process subtitle text content using arbitrary Python code."""

import importlib
import logging
from .. import utils

log = logging.getLogger(__name__)


def strip_to_matching_lines_only(subtitles, imports, func_str):
    """
    Passes all subtitle content to a function per subtitle.

    :param subtitles: :py:class:`Subtitle` objects
    :param imports: Modules to import in the function context.
    :param func_str: A function used to process subtitle content.
    :rtype: :term:`generator` of :py:class:`Subtitle` objects
    """
    for import_name in imports:
        real_import = importlib.import_module(import_name)
        globals()[import_name] = real_import

    # process and lines_matching should be merged.
    func = eval(func_str)  # nosec pylint: disable-msg=eval-used

    for subtitle in subtitles:
        subtitle.content = func(subtitle.content)
        yield subtitle


def parse_args():
    examples = {
        "Strip HTML-like symbols from a subtitle": """srt process -m re -f 'lambda sub: re.sub("<[^<]+?>", "", sub)'"""
    }

    parser = utils.basic_parser(description=__doc__, examples=examples)
    parser.add_argument(
        "-f", "--func", help="a function to use to process lines", required=True
    )
    parser.add_argument(
        "-m",
        "--module",
        help="modules to import in the function context",
        action="append",
        default=[],
    )
    return parser.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=args.log_level)
    utils.set_basic_args(args)
    processed_subs = strip_to_matching_lines_only(args.input, args.module, args.func)
    output = utils.compose_suggest_on_fail(processed_subs, strict=args.strict)
    args.output.write(output)


if __name__ == "__main__":  # pragma: no cover
    main()
