import unittest


class TestImportSRT(unittest.TestCase):
    def test_import(self):
        try:
            # import the srt package as a whole.
            print("srt package")
            import srt

            print([module for module in dir(srt) if not module.startswith("__")])

            print("\nsrt module")
            print([member for member in dir(srt.srt) if not member.startswith("__")])

            print("\ntools module")
            print([member for member in dir(srt.tools) if not member.startswith("__")])

            print("\nremove module")
            print(
                [
                    member
                    for member in dir(srt.tools.find)
                    if not member.startswith("__")
                ]
            )
        except AttributeError:
            self.fail("AttributeError raised during package import.")

        try:
            # only import the srt.py (module) from the srt package.
            print("\nonly srt module")
            from srt import srt as module

            print([member for member in dir(module) if not member.startswith("__")])

            # only import the tools package from the srt package.
            print("\nonly tools package")
            from srt import tools

            print([member for member in dir(tools) if not member.startswith("__")])

            # only import the remove module from the tools package in the srt package.
            print("\nonly remove module")
            from srt.tools import find

            print([member for member in dir(find) if not member.startswith("__")])

        except AttributeError:
            self.fail("AttributeError raised during module import.")
