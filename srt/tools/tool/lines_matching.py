#!/usr/bin/python3

"""Filter subtitles that match or don't match a particular pattern."""

from .. import utils
import importlib
import logging

log = logging.getLogger(__name__)


def strip_to_matching_lines_only(subtitles, imports, func_str, invert, per_sub):
    """
    Sets all non-mtching subtitle content empty.

    :param subtitles: :py:class:`Subtitle` objects
    :param imports: Modules to import in the function context.
    :param func_str: A function to use to match lines.
    :param bool invert: Whether to only match lines that return False.
    :param per_sub:  Match the content of each subtitle, not each content-line.
    :rtype: :term:`generator` of :py:class:`Subtitle` objects
    """
    for import_name in imports:
        real_import = importlib.import_module(import_name)
        globals()[import_name] = real_import

    raw_func = eval(func_str)  # pylint: disable-msg=eval-used

    if invert:
        func = lambda line: not raw_func(line)
    else:
        func = raw_func

    for subtitle in subtitles:
        if per_sub:
            if not func(subtitle.content):
                subtitle.content = ""
        else:
            subtitle.content = "\n".join(
                line for line in subtitle.content.splitlines() if func(line)
            )

        yield subtitle


def parse_args():
    examples = {
        "Only include Chinese lines": "srt lines_matching -m hanzidentifier -f hanzidentifier.has_chinese",
        "Exclude all lines which only contain numbers": "srt lines_matching -v -f 'lambda x: x.isdigit()'",
    }
    parser = utils.basic_parser(description=__doc__, examples=examples)
    parser.add_argument(
        "-f", "--func", help="a function to use to match lines", required=True
    )
    parser.add_argument(
        "-m",
        "--module",
        help="modules to import in the function context",
        action="append",
        default=[],
    )
    parser.add_argument(
        "-s",
        "--per-subtitle",
        help="match the content of each subtitle, not each line",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--invert",
        help="invert matching -- only match lines returning False",
        action="store_true",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=args.log_level)
    utils.set_basic_args(args)
    matching_subtitles_only = strip_to_matching_lines_only(
        args.input, args.module, args.func, args.invert, args.per_subtitle
    )
    output = utils.compose_suggest_on_fail(matching_subtitles_only, strict=args.strict)
    args.output.write(output)


if __name__ == "__main__":  # pragma: no cover
    main()
