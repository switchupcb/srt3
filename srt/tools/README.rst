srt tools contains tools written to process SRT files. All tools use
the Python srt3_ library internally.

.. _srt3: https://github.com/switchupcb/srt

Library Usage
-------------
You can use the srt tools module in your python projects. Check the `Detailed
API documentation`_ for more information.

Command Line Interface Usage
----------------------------

You can call ``srt`` directly to see a list of all available utilities.

.. code::

    srt [tool_name] [args ...]

Arbitrary actions can be done with *srt match*, for example:

.. code::

    # Strip HTML
    srt match -m re -fp 'lambda sub: re.sub("<[^<]+?>", "", sub)'

    # Only keep Chinese subtitles
    srt match -m hanzidentifier -fm hanzidentifier.has_chinese

    # Do Both
    srt match -m re -m hanzidentifier -fm hanzidentifier.has_chinese -fp 'lambda sub: re.sub("<[^<]+?>", "", sub)'

Tools
-----

.. list-table::
   :widths: 25 50 20
   :header-rows: 1
   :align: center

   * - Tool
     - Description
     - Arguments (--)
   * - ADD
     - Add a subtitle with the option to move subsequent captions.
     - start -s, end -e, content -c, adjust -a
   * - DEDUPLICATE
     - Remove subtitles with duplicate content.
     - ms -t
   * - FIND
     - Find subtitles by timestamp in sequential or non-sequential order. Placing timestamps non-sequentially finds subtitles up to start and after end.
     - start -s, end -e, adjust -a
   * - FIXED TIMESHIFT
     - Shift subtitles by a fixed amount of time.
     - seconds -s
   * - LINEAR TIMESHIFT
     - Shift the linear rate of each subtitle. Useful for videos that have been sped up or slowed.
     - from-start --f1, from-end --f2, to-start --t1, to-end --t2
   * - MATCH
     - Match subtitle-content using a provided conditional function. Process lines that are matched. Lines that aren't matched are removed.
     - module -m, match -fm, process -fp, lines -l
   * - MUX
     - Multiplex_ multiple subtitles together into one. Useful for creating bilingual subtitles. Supports merging subtitles with similar start/end times to the same time.
     - ms, width -w, top-and-bottom -t, no-time-matching --nt
   * - NORMALIZE
     - Clean SRT Files and standardize them. Removes invalid newlines, normalizes timestamps, and fixes subtitle indexing with compliant data.
     -
   * - PASTE
     - Paste subtitles into/before other subtitles at a given timestamp. Add space that precedes the copied subtitles.
     - t1, t2, paste -p, space -s, block -b, zero -z
   * - SPLIT
     - Split subtitles at a given timestamp.
     - timestamp -t

Default Arguments
-----------------
.. list-table::
  :widths: 25 50 20
  :header-rows: 1
  :align: center

  * - Argument (--)
    - Description
    - Option
  * - input
    - The file to process (default: stdin).
    - -i
  * - output
    - The file to write to (default: stdout).
    - -o
  * - inplace
    - Modify the file in place.
    - -q
  * - encoding
    - The encoding to read/write files in (default: utf8).
    -
  * - ignore-parsing-errors
    - Attempt to continue when there are parsing errors.
    - -x
  * - no-strict
    - Allow blank lines in output. Your media player may explode!
    -
  * - debug
    - Enable debug logging.
    -
  * - help
    - The default option for help (--help does NOT apply).
    - -h

.. _`Multiplex`: https://en.wikipedia.org/wiki/Multiplexing
.. _`Detailed API documentation`: http://srt3.readthedocs.org/en/latest/api.html
