#!/usr/bin/python3

"""Filter and/or process subtitles' content that match a particular pattern."""

import importlib
import logging
from . import _cli

log = logging.getLogger(__name__)


def _true(param):
    """Always returns true for matching functionality."""
    return True


def _pass(param):
    """Always returns the given parameter for process functionality."""
    return param


def match(subtitles, imports, func_match, func_process, lines):
    """
    Passes each matching subtitle-content to a function.

    :param subtitles: :py:class:`Subtitle` objects
    :param imports: Modules to import in the context of the function.
    :param str func_match: The function used to match lines.
    :param str func_process: The function used to process subtitle content.
    :param bool invert: Whether to only match lines that return False.
    :param per_line: Whether to apply functions to each line of content
                     (as opposed to the whole content string).
    :rtype: :term:`generator` of :py:class:`Subtitle` objects
    """
    for import_name in imports:
        real_import = importlib.import_module(import_name)
        globals()[import_name] = real_import

    # fmt: off
    # Evaluate the each function
    match_func = eval(func_match) if func_match else _true # nosec pylint: disable-msg=eval-used
    process_func = eval(func_process) if func_process else _pass # nosec pylint: disable-msg=eval-used
    # fmt: on

    # Match and process each subtitle (or subtitle-line).
    for subtitle in subtitles:
        if lines:
            matched_lines = [
                line for line in subtitle.content.splitlines() if match_func(line)
            ]
            processed_lines = [process_func(line) for line in matched_lines]
            subtitle.content = "\n".join(processed_lines)
        else:
            if match_func(subtitle.content):
                subtitle.content = process_func(subtitle.content)
            else:
                subtitle.content = ""

        yield subtitle


def set_args():
    examples = {
        "Only include Chinese lines": "srt match -m hanzidentifier -fm hanzidentifier.has_chinese",
        "Exclude all lines which only contain numbers": "srt match -fm 'lambda x: not x.isdigit()'",
        "Strip HTML-like symbols from a subtitle": """srt match -m re -fp 'lambda sub: re.sub("<[^<]+?>", "", sub)'""",
    }
    parser = _cli.basic_parser(description=__doc__, examples=examples)
    parser.add_argument("--match", "--fm", help="The function used to match lines.")
    parser.add_argument("--process", "--fp", help="The function used to process lines.")
    parser.add_argument(
        "--module",
        "-m",
        help="modules to import in the function context",
        action="append",
        default=[],
    )
    parser.add_argument(
        "--lines",
        "-l",
        help="Match the content of each subtitle-line, not each subtitle-content.",
        action="store_true",
    )
    return parser.parse_args()


def main():
    args = set_args()
    logging.basicConfig(level=args.log_level)
    _cli.set_basic_args(args)
    matched_subs = match(args.input, args.module, args.match, args.process, args.lines)
    output = _cli.compose_suggest_on_fail(matched_subs, strict=args.strict)
    args.output.write(output)


if __name__ == "__main__":  # pragma: no cover
    main()
