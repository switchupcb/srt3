import unittest
from . import *
from srt.tools.add import *


class TestToolAdd(unittest.TestCase):
    def setUp(self):
        self.subs = create_blocks
        self.x = list(create_blocks())
        self.y = list(create_blocks(1))

    def tearDown(self):
        pass

    def test_add_caption(self):
        result = add(self.subs(), t("00:00:10,000"), t("00:00:11,000"), "ADD")
        a = list(self.subs())
        a.append(srt.Subtitle(0, t("00:00:10,000"), t("00:00:11,000"), "ADD"))
        self.assertEqual(list(result), sort(a))  # before

        result = add(self.subs(), t("00:00:00,000"), t("00:00:01,000"), "ADD", True)
        a = [
            srt.Subtitle(1, t("00:00:00,000"), t("00:00:01,000"), "ADD"),
            srt.Subtitle(2, t("00:00:12,000"), t("00:00:13,701"), "A"),
            srt.Subtitle(3, t("00:00:13,701"), t("00:00:15,203"), "B"),
            srt.Subtitle(4, t("00:00:15,500"), t("00:00:20,738"), "C"),
            srt.Subtitle(5, t("00:00:17,538"), t("00:00:18,272"), "D"),
            srt.Subtitle(6, t("00:00:18,272"), t("00:00:19,440"), "E"),
        ]
        self.assertEqual(list(result), a)  # before (adjust)

        result = add(self.subs(), t("00:00:15,000"), t("00:00:18,000"), "ADD")
        a = list(self.subs())
        a.append(srt.Subtitle(0, t("00:00:15,000"), t("00:00:18,000"), "ADD"))
        self.assertEqual(list(result), sort(a))  # middle

        result = add(self.subs(), t("00:00:15,000"), t("00:00:16,000"), "ADD", True)
        a = [
            srt.Subtitle(1, t("00:00:11,000"), t("00:00:12,701"), "A"),
            srt.Subtitle(2, t("00:00:12,701"), t("00:00:14,203"), "B"),
            srt.Subtitle(3, t("00:00:14,500"), t("00:00:19,738"), "C"),
            srt.Subtitle(4, t("00:00:15,000"), t("00:00:16,000"), "ADD"),
            srt.Subtitle(5, t("00:00:17,538"), t("00:00:18,272"), "D"),
            srt.Subtitle(6, t("00:00:18,272"), t("00:00:19,440"), "E"),
        ]
        self.assertEqual(list(result), a)  # middle (adjust)

        result = add(self.subs(), t("00:00:25,000"), t("00:00:30,000"), "ADD")
        a = list(self.subs())
        a.append(srt.Subtitle(0, t("00:00:25,000"), t("00:00:30,000"), "ADD"))
        self.assertEqual(list(result), sort(a))  # after


if __name__ == "__main__":
    unittest.main()
