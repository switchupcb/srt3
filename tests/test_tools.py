#!/usr/bin/python3

import os
import subprocess
import sys
import tempfile
from shlex import quote


sample_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "files")


if os.name == "nt":
    # shlex.quote quotes incorrectly on Windows
    quote = lambda x: windows_ebic_quote(x)


def windows_ebic_quote(data):
    """100% secure"""
    data = data.replace('"', '""')
    return '"' + data + '"'


def run_srt_util(cmd, shell=False, encoding="utf-8-sig"):
    extra_env = {}

    env = {"PYTHONPATH": ".", "SystemRoot": r"C:\Windows"}
    env.update(extra_env)

    raw_out = subprocess.check_output(cmd, shell=shell, env=env)
    return raw_out.decode(encoding)


def assert_supports_all_io_methods(cmd, exclude_output=False, exclude_stdin=False):
    cmd.insert(0, sys.executable)
    cmd.insert(1, "srt/tools/_srt.py")
    in_file = os.path.join(sample_dir, "ascii.srt")
    in_file_gb = os.path.join(sample_dir, "gb2312.srt")
    fd, out_file = tempfile.mkstemp()

    # This is accessed by filename, not fd
    os.close(fd)

    outputs = []
    cmd_string = " ".join(quote(x) for x in cmd)

    try:
        outputs.append(run_srt_util(cmd + ["-i", in_file]))
        if not exclude_stdin:
            outputs.append(
                run_srt_util("%s < %s" % (cmd_string, quote(in_file)), shell=True)
            )
        if not exclude_output:
            run_srt_util(cmd + ["-i", in_file, "-o", out_file])
            run_srt_util(
                cmd + ["-i", in_file_gb, "-o", out_file, "--encoding", "gb2312"],
                encoding="gb2312",
            )
            if not exclude_stdin:
                run_srt_util(
                    "%s < %s > %s" % (cmd_string, quote(in_file), quote(out_file)),
                    shell=True,
                )
                run_srt_util(
                    "%s < %s > %s"
                    % (
                        cmd_string + " --encoding gb2312",
                        quote(in_file),
                        quote(out_file),
                    ),
                    shell=True,
                    encoding="gb2312",
                )
        assert len(set(outputs)) == 1, repr(outputs)

        if os.name == "nt":
            assert "\r\n" in outputs[0]
        else:
            assert "\r\n" not in outputs[0]
    finally:
        os.remove(out_file)


def test_tools_support():
    matrix = [
        (["add", "-s", "00:00:01,000", "-e", "00:00:02,000", "-c", "test"], False),
        (["deduplicate"], False),
        (["find"], False),
        (["fixed_timeshift", "--seconds", "5"], False),
        (
            [
                "linear_timeshift",
                "--f1",
                "00:00:01,000",
                "--f2",
                "00:00:02,000",
                "--t1",
                "00:00:03,000",
                "--t2",
                "00:00:04,000",
            ],
            False,
        ),
        (["match", "--fm", "lambda x: True"], False),
        (["mux"], False, True),
        (["mux", "-t"], False, True),
        (["normalize"], False),
        (["paste"], False),
    ]

    for args in matrix:
        assert_supports_all_io_methods(*args)
