import unittest
from . import *
from srt.tools.find import *


class TestToolRemove(unittest.TestCase):
    def setUp(self):
        self.subs = create_blocks
        self.x = list(create_blocks())
        self.y = list(create_blocks(1))

    def tearDown(self):
        pass

    def test_find_sequential(self):
        result = find_by_timestamp([], t("00:00:00,000"), t("00:00:30,000"))
        self.assertEqual(list(result), [])

        result = find_by_timestamp(self.subs(), t("00:00:11,000"), t("00:00:19,738"))
        self.assertEqual(list(result), self.x)

        result = find_by_timestamp(self.subs(), self.x[0].start, self.x[0].end)
        self.assertEqual(list(result), [self.x[0]])

        result = find_by_timestamp(self.subs(), self.x[0].start, t("00:00:14,500"))
        self.assertEqual(list(result), sort([self.x[0], self.x[1]]))

        result = find_by_timestamp(self.subs(), t("00:00:00,000"), t("00:00:17,500"))
        a = [
            srt.Subtitle(1, t("00:00:11,000"), t("00:00:12,701"), "A"),
            srt.Subtitle(2, t("00:00:12,701"), t("00:00:14,203"), "B"),
            srt.Subtitle(3, t("00:00:14,500"), t("00:00:17,500"), "C"),
            srt.Subtitle(4, t("00:00:16,538"), t("00:00:17,272"), "D"),
            srt.Subtitle(5, t("00:00:17,272"), t("00:00:17,500"), "E"),
        ]
        self.assertEqual(list(result), a)  # split

    def test_find_nonsequential(self):
        result = find_by_timestamp([], t("00:00:30,000"), t("00:00:00,000"))
        self.assertEqual(list(result), [])

        result = find_by_timestamp(self.subs(), self.x[0].start, self.x[0].start)
        self.assertEqual(list(result), self.x)  # equivalent

        result = find_by_timestamp(self.subs(), t("00:00:19,738"), t("00:00:11,000"))
        self.assertEqual(list(result), [])

        result = find_by_timestamp(self.subs(), self.x[0].end, self.x[0].start)
        self.assertEqual(
            list(result), sort([self.x[1], self.x[2], self.x[3], self.x[4]])
        )

        result = find_by_timestamp(self.subs(), t("00:00:14,500"), self.x[0].start)
        self.assertEqual(list(result), sort([self.x[2], self.x[3], self.x[4]]))

        result = find_by_timestamp(self.subs(), t("00:00:17,500"), t("00:00:00,000"))
        a = [
            srt.Subtitle(1, t("00:00:17,500"), t("00:00:18,440"), "E"),
            srt.Subtitle(2, t("00:00:17,500"), t("00:00:19,738"), "C"),
        ]
        self.assertEqual(list(result), a)  # split

    def test_find_sequential_adjust(self):
        result = find_by_timestamp(
            self.subs(), self.x[0].start, t("00:00:14,500"), True
        )
        a = [
            srt.Subtitle(1, t("00:00:00,000"), t("00:00:01,701"), "A"),
            srt.Subtitle(2, t("00:00:01,701"), t("00:00:03,203"), "B"),
        ]
        self.assertEqual(list(result), a)  # first subtitle

    def test_find_nonsequential_adjust(self):
        result = find_by_timestamp(
            self.subs(), t("00:00:14,500"), self.x[0].start, True
        )
        a = [
            srt.Subtitle(1, t("00:00:00,000"), t("00:00:05,238"), "C"),
            srt.Subtitle(2, t("00:00:02,038"), t("00:00:02,772"), "D"),
            srt.Subtitle(3, t("00:00:02,772"), t("00:00:03,940"), "E"),
        ]
        self.assertEqual(list(result), a)

        result = find_by_timestamp(
            self.subs(), t("00:00:17,500"), t("00:00:00,000"), True
        )
        a = [
            srt.Subtitle(1, t("00:00:00,000"), t("00:00:00,940"), "E"),
            srt.Subtitle(2, t("00:00:00,000"), t("00:00:02,238"), "C"),
        ]
        self.assertEqual(list(result), a)  # split


if __name__ == "__main__":
    unittest.main()
