import unittest
from . import *
from srt.tools.remove import *


class TestToolRemove(unittest.TestCase):
    def setUp(self):
        self.subs = create_blocks
        self.x = list(create_blocks())
        self.y = list(create_blocks(1))

    def tearDown(self):
        pass

    def test_remove_by_timestamp(self):
        result = remove_by_timestamp([], t("00:00:00,000"), t("00:00:30,000"))
        self.assertEqual(list(result), [])

        result = remove_by_timestamp(self.subs(), self.x[0].start, self.x[0].end)
        self.assertEqual(
            list(result), sort([self.x[1], self.x[2], self.x[3], self.x[4]])
        )

        result = remove_by_timestamp(self.subs(), self.x[0].start, t("00:00:14,500"))
        self.assertEqual(list(result), sort([self.x[2], self.x[3], self.x[4]]))

        result = remove_by_timestamp(self.subs(), t("00:00:11,000"), t("00:00:19,738"))
        self.assertEqual(list(result), [])

        result = remove_by_timestamp(self.subs(), t("00:00:00,000"), t("00:00:30,000"))
        self.assertEqual(list(result), [])

        result = remove_by_timestamp(self.subs(), t("00:00:00,000"), t("00:00:17,500"))
        a = [
            srt.Subtitle(1, t("00:00:17,500"), t("00:00:18,440"), "E"),
            srt.Subtitle(2, t("00:00:17,500"), t("00:00:19,738"), "C"),
        ]
        self.assertEqual(list(result), a)  # split

        # reverse timestamps
        result = remove_by_timestamp([], t("00:00:30,000"), t("00:00:00,000"))
        self.assertEqual(list(result), [])

        result = remove_by_timestamp(self.subs(), t("00:00:30,000"), t("00:00:00,000"))
        self.assertEqual(list(result), self.x)

        result = remove_by_timestamp(self.subs(), t("00:00:14,500"), self.x[0].start)
        self.assertEqual(list(result), sort([self.x[0], self.x[1]]))

        result = remove_by_timestamp(self.subs(), t("00:00:19,738"), t("00:00:11,000"))
        self.assertEqual(list(result), self.x)

        result = remove_by_timestamp(self.subs(), self.x[0].end, self.x[0].start)
        self.assertEqual(list(result), [self.x[0]])

        result = remove_by_timestamp(self.subs(), self.x[0].start, self.x[0].start)
        self.assertEqual(list(result), [])

    def test_remove_by_timestamp_adjust(self):
        result = remove_by_timestamp(
            self.subs(), self.x[0].start, t("00:00:14,500"), True
        )
        a = [
            srt.Subtitle(1, t("00:00:00,000"), t("00:00:05,238"), "C"),
            srt.Subtitle(2, t("00:00:02,038"), t("00:00:02,772"), "D"),
            srt.Subtitle(3, t("00:00:02,772"), t("00:00:03,940"), "E"),
        ]
        self.assertEqual(list(result), a)

        # split
        result = remove_by_timestamp(
            self.subs(), t("00:00:00,000"), t("00:00:17,500"), True
        )
        a = [
            srt.Subtitle(1, t("00:00:00,000"), t("00:00:00,940"), "E"),
            srt.Subtitle(2, t("00:00:00,000"), t("00:00:02,238"), "C"),
        ]
        self.assertEqual(list(result), a)

        # reverse timestamps
        result = remove_by_timestamp(
            self.subs(), t("00:00:30,000"), t("00:00:00,000"), True
        )
        self.assertEqual(list(result), self.x)

        result = remove_by_timestamp(
            self.subs(), t("00:00:14,500"), self.x[0].start, True
        )
        a = [
            srt.Subtitle(1, t("00:00:00,000"), t("00:00:01,701"), "A"),
            srt.Subtitle(2, t("00:00:01,701"), t("00:00:03,203"), "B"),
        ]
        self.assertEqual(list(result), a)


if __name__ == "__main__":
    unittest.main()
