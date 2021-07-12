# Contributing

## License

By contributing code to [srt3](https://github.com/switchupcb/srt), you agree to license your contribution under the [MIT License](https://github.com/switchupcb/srt/blob/develop/LICENSE).

## Documentation

[Detailed API documentation](https://srt3.readthedocs.io/en/latest/api.html) is available here. Documentation is auto-generated from comments using [sphinx](https://www.sphinx-doc.org/en/master/).

## Pull Requests

The **stable** branch will always be stable. Submit against the current [**develop**](https://github.com/switchupcb/srt/tree/develop) branch.

### Process

When you create a pull request, be sure to include its goal along with a detailed description of the code involved. A pull request can be merged by a contributor once two other developers (contributor or otherwise) have reviewed the pull request's code.

### Tools

If you are adding an srt tool, you can use the following commit as a guide: [srt tools: add srt add](https://github.com/switchupcb/srt3/commit/1ee1f649c9a09acc649bd48c076ec6f92e8ce78e)

This library uses [argparse](https://docs.python.org/3/library/argparse) to program its Command Line Interface (CLI) and follows [UNIX Program Argument Syntax Conventions](https://www.gnu.org/software/libc/manual/html_node/Argument-Syntax.html). View the [tools table](https://github.com/switchupcb/srt/tree/develop/srt/tools) to see existing default arguments that should **NOT** be used in new tools.

### Style

This library uses the [black](https://black.readthedocs.io/en/stable/) code style.

```
pip install black
cd srt3
cd ..
black srt3
```

### Testing

You are required to test your code using [tox](https://tox.readthedocs.org). You can view the `tox.ini` file for each test that is used (via _[testenv: test]_).

```
pip install tox
cd srt3
tox
```

_Tests use the [pytest](https://docs.pytest.org/en/6.2.x/contents.html) framework._

### Checklist

Before a **pull request**:

1. Ensure any unnecessary files, code and/or dependencies are removed.
2. Adhere to the style guide.
3. Adhere to the testing protocol.
4. Add comments for the auto-generated documentation.
5. Update the README where necessary.

## Roadmap

While srt3 does not have an official roadmap, here are cool features you could add or improve:

**srt3/# -** Simplify code and implement commented features remnant from legacy srt.

**srt3/coverage -** Legacy tools from srt1 don't actually have 100% coverage and don't fully support pytype.

**srt3/srt/tools -** Tools that can be used in the Command Line Interface and srt3 library.

**srt3/srt/tools/tool/transcribe -** A transcription tool that automates audio-video transcription.

**srt3/gui -** A graphical user interface that allows users to use the tools present in the library but **not** in the installed package.
