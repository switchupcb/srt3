import unittest
from . import *
from srt.tools.split import *


class TestToolSplit(unittest.TestCase):
    def setUp(self):
        self.subs = create_blocks
        self.x = list(create_blocks())
        self.y = list(create_blocks(1))

    def tearDown(self):
        pass

    def test_split(self):
        result = split(self.subs(), self.x[0].start)
        self.assertEqual(list(result), self.x)

        result = split(self.subs(), t("00:00:12,000"))
        a = [
            srt.Subtitle(1, t("00:00:11,000"), t("00:00:12,000"), "A"),
            srt.Subtitle(2, t("00:00:12,000"), t("00:00:12,701"), "A"),
            srt.Subtitle(3, t("00:00:12,701"), t("00:00:14,203"), "B"),
            srt.Subtitle(4, t("00:00:14,500"), t("00:00:19,738"), "C"),
            srt.Subtitle(5, t("00:00:16,538"), t("00:00:17,272"), "D"),
            srt.Subtitle(6, t("00:00:17,272"), t("00:00:18,440"), "E"),
        ]
        self.assertEqual(list(result), a)  # before

        result = split(self.subs(), t("00:00:16,538"))
        a = [
            srt.Subtitle(1, t("00:00:11,000"), t("00:00:12,701"), "A"),
            srt.Subtitle(2, t("00:00:12,701"), t("00:00:14,203"), "B"),
            srt.Subtitle(3, t("00:00:14,500"), t("00:00:16,538"), "C"),
            srt.Subtitle(4, t("00:00:16,538"), t("00:00:17,272"), "D"),
            srt.Subtitle(5, t("00:00:16,538"), t("00:00:19,738"), "C"),
            srt.Subtitle(6, t("00:00:17,272"), t("00:00:18,440"), "E"),
        ]
        self.assertEqual(list(result), a)  # middle

        result = split(self.subs(), t("00:00:17,500"))
        a = [
            srt.Subtitle(1, t("00:00:11,000"), t("00:00:12,701"), "A"),
            srt.Subtitle(2, t("00:00:12,701"), t("00:00:14,203"), "B"),
            srt.Subtitle(3, t("00:00:14,500"), t("00:00:17,500"), "C"),
            srt.Subtitle(4, t("00:00:16,538"), t("00:00:17,272"), "D"),
            srt.Subtitle(5, t("00:00:17,272"), t("00:00:17,500"), "E"),
            srt.Subtitle(6, t("00:00:17,500"), t("00:00:18,440"), "E"),
            srt.Subtitle(7, t("00:00:17,500"), t("00:00:19,738"), "C"),
        ]
        self.assertEqual(list(result), a)  # append


if __name__ == "__main__":
    unittest.main()
