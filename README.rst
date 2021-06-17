|travis| |lgtm| |coveralls| |libraries|

.. |travis| image:: https://travis-ci.com/switchupcb/srt.svg?branch=develop
  :target: https://travis-ci.com/switchupcb/srt
  :alt: Tests

.. |lgtm| image:: https://img.shields.io/lgtm/grade/python/github/switchupcb/srt.svg?label=code%20quality
  :target: https://lgtm.com/projects/g/switchupcb/srt/overview/
  :alt: LGTM

.. |coveralls| image:: https://img.shields.io/coveralls/switchupcb/srt/develop.svg?label=test%20coverage
  :target: https://coveralls.io/github/switchupcb/srt?branch=develop
  :alt: Coverage

.. |libraries| image:: https://img.shields.io/librariesio/github/switchupcb/srt.svg?label=dependencies
  :target: https://libraries.io/github/switchupcb/srt
  :alt: Dependencies

srt3 is a simple yet featureful Python library for parsing, modifying, and
composing `SRT files`_. Take a look at the quickstart_ for a basic overview of
the library. `Detailed API documentation`_ is also available.

Want to see some examples of its use? Take a look at the `tools shipped with
the library`_.

Why choose this library?
------------------------

- Parses broken SRT files other libraries can't and fixes them
- Support for Asian-style SRT formats (ie. "fullwidth" SRT format)
- Extremely lightweight with a `Well Documented API`_
- Includes tools that allow you to perform tasks using the library
- No Dependencies outside of the Standard Library
- High quality test suite using Hypothesis_
- `~30% faster than pysrt on typical workloads`_
- 100% Unicode Compliant
- Portable — runs on Windows, OSX, and Linux
- Released under a highly permissive license (MIT)

.. _quickstart: http://srt3.readthedocs.org/en/latest/quickstart.html
.. _`SRT files`: https://en.wikipedia.org/wiki/SubRip#SubRip_text_file_format
.. _Hypothesis: https://github.com/DRMacIver/hypothesis
.. _`Well Documented API`: http://srt3.readthedocs.org/en/latest/index.html
.. _`~30% faster than pysrt on typical workloads`: https://paste.pound-python.org/raw/8nQKbDW0ROWvS7bOeAb3/

Usage
-----

Tools
=====

There are a number of `tools shipped with the library`_ to manipulate, process,
and fix SRT files. Here's an example using `hanzidentifier`_ to strip out
non-Chinese lines:

.. code::

    $ cat pe.srt
    1
    00:00:33,843 --> 00:00:38,097
    Only 3% of the water on our planet is fresh.
    地球上只有3%的水是淡水

    2
    00:00:40,641 --> 00:00:44,687
    Yet, these precious waters are rich with surprise.
    可是这些珍贵的淡水中却充满了惊奇

    $ srt lines_matching -m hanzidentifier -f hanzidentifier.has_chinese -i pe.srt
    1
    00:00:33,843 --> 00:00:38,097
    地球上只有3%的水是淡水

    2
    00:00:40,641 --> 00:00:44,687
    可是这些珍贵的淡水中却充满了惊奇


These tools are easy to chain together. For example, you have a subtitle
containing Chinese and English, and another containing French. You only want Chinese
French. The Chinese and English subtitle is also 5 seconds late. That's easy enough
to sort out:

.. code::

   $ srt lines_matching -m hanzidentifier -f hanzidentifier.has_chinese -i chs+eng.srt |
   >     srt fixed_timeshift --seconds -5 |
   >     srt mux --input - --input fra.srt

See the srt/tools/ directory for more information.

.. _hanzidentifier: https://github.com/tsroten/hanzidentifier

Library
=======

`Detailed API documentation`_ is available, but here are the basics:

.. code:: python

    >>> # list() is needed as srt.parse creates a generator
    >>> subs = list(srt.parse('''\
    ... 1
    ... 00:00:33,843 --> 00:00:38,097
    ... 地球上只有3%的水是淡水
    ...
    ... 2
    ... 00:00:40,641 --> 00:00:44,687
    ... 可是这些珍贵的淡水中却充满了惊奇
    ...
    ... 3
    ... 00:00:57,908 --> 00:01:03,414
    ... 所有陆地生命归根结底都依赖於淡水
    ...
    ... '''))
    >>> subs
    [Subtitle(index=1, start=datetime.timedelta(0, 33, 843000), end=datetime.timedelta(0, 38, 97000), content='地球上只有3%的水是淡水', proprietary=''),
     Subtitle(index=2, start=datetime.timedelta(0, 40, 641000), end=datetime.timedelta(0, 44, 687000), content='可是这些珍贵的淡水中却充满了惊奇', proprietary=''),
     Subtitle(index=3, start=datetime.timedelta(0, 57, 908000), end=datetime.timedelta(0, 63, 414000), content='所有陆地生命归根结底都依赖於淡水', proprietary='')]
    >>> print(srt.compose(subs))
    1
    00:00:33,843 --> 00:00:38,097
    地球上只有3%的水是淡水

    2
    00:00:40,641 --> 00:00:44,687
    可是这些珍贵的淡水中却充满了惊奇

    3
    00:00:57,908 --> 00:01:03,414
    所有陆地生命归根结底都依赖於淡水

Installation
------------

To install the latest stable version from PyPi:

.. code::

    pip install -U srt

To install the latest development version directly from GitHub:

.. code::

    pip install -U git+https://github.com/switchupcb/srt.git@develop

.. _`Detailed API documentation`: http://srt3.readthedocs.org/en/latest/api.html
.. _`tools shipped with the library`: https://github.com/switchupcb/srt/tree/develop/srt/tools
