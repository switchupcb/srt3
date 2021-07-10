import unittest
from . import *
from srt.tools.paste import *


class TestToolPaste(unittest.TestCase):
    def setUp(self):
        self.subs = create_blocks
        self.x = list(create_blocks())
        self.y = list(create_blocks(1))
        self.copied = [
            srt.Subtitle(1, t("00:00:10,000"), t("00:00:11,000"), "ADD"),
            srt.Subtitle(2, t("00:00:14,500"), t("00:00:20,000"), "ADD2"),
            srt.Subtitle(3, t("00:00:25,000"), t("00:00:30,000"), "ADD3"),
        ]

    def tearDown(self):
        pass

    def test_paste(self):
        result = paste([], self.copied, t("00:00:00,000"))
        self.assertEqual(list(result), self.copied)

        result = paste(self.subs(), [], t("00:00:00,000"))
        self.assertEqual(list(result), self.x)

        result = paste(self.subs(), self.copied, t("00:00:00,000"))
        a = [
            srt.Subtitle(1, t("00:00:10,000"), t("00:00:11,000"), "ADD"),
            srt.Subtitle(2, t("00:00:11,000"), t("00:00:12,701"), "A"),
            srt.Subtitle(3, t("00:00:12,701"), t("00:00:14,203"), "B"),
            srt.Subtitle(4, t("00:00:14,500"), t("00:00:19,738"), "C"),
            srt.Subtitle(5, t("00:00:14,500"), t("00:00:20,000"), "ADD2"),
            srt.Subtitle(6, t("00:00:16,538"), t("00:00:17,272"), "D"),
            srt.Subtitle(7, t("00:00:17,272"), t("00:00:18,440"), "E"),
            srt.Subtitle(8, t("00:00:25,000"), t("00:00:30,000"), "ADD3"),
        ]
        self.assertEqual(list(result), a)  # before

        result = paste(self.subs(), self.copied, t("00:00:05,000"))
        a = [
            srt.Subtitle(1, t("00:00:11,000"), t("00:00:12,701"), "A"),
            srt.Subtitle(2, t("00:00:12,701"), t("00:00:14,203"), "B"),
            srt.Subtitle(3, t("00:00:14,500"), t("00:00:19,738"), "C"),
            srt.Subtitle(4, t("00:00:15,000"), t("00:00:16,000"), "ADD"),
            srt.Subtitle(5, t("00:00:16,538"), t("00:00:17,272"), "D"),
            srt.Subtitle(6, t("00:00:17,272"), t("00:00:18,440"), "E"),
            srt.Subtitle(7, t("00:00:19,500"), t("00:00:25,000"), "ADD2"),
            srt.Subtitle(8, t("00:00:30,000"), t("00:00:35,000"), "ADD3"),
        ]
        self.assertEqual(list(result), a)  # middle

        result = paste(self.subs(), self.copied, t("00:00:10,000"))
        a = [
            srt.Subtitle(1, t("00:00:11,000"), t("00:00:12,701"), "A"),
            srt.Subtitle(2, t("00:00:12,701"), t("00:00:14,203"), "B"),
            srt.Subtitle(3, t("00:00:14,500"), t("00:00:19,738"), "C"),
            srt.Subtitle(4, t("00:00:16,538"), t("00:00:17,272"), "D"),
            srt.Subtitle(5, t("00:00:17,272"), t("00:00:18,440"), "E"),
            srt.Subtitle(6, t("00:00:20,000"), t("00:00:21,000"), "ADD"),
            srt.Subtitle(7, t("00:00:24,500"), t("00:00:30,000"), "ADD2"),
            srt.Subtitle(8, t("00:00:35,000"), t("00:00:40,000"), "ADD3"),
        ]
        self.assertEqual(list(result), a)  # after

    def test_paste_space(self):
        result = paste([], self.copied, t("00:00:00,000"), t("00:00:10,000"))
        a = [
            srt.Subtitle(1, t("00:00:20,000"), t("00:00:21,000"), "ADD"),
            srt.Subtitle(2, t("00:00:24,500"), t("00:00:30,000"), "ADD2"),
            srt.Subtitle(3, t("00:00:35,000"), t("00:00:40,000"), "ADD3"),
        ]
        self.assertEqual(list(result), a)

        result = paste(self.subs(), [], t("00:00:00,000"), t("00:00:10,000"))
        self.assertEqual(list(result), self.x)

        result = paste(self.subs(), self.copied, t("00:00:00,000"), t("00:00:10,000"))
        a = [
            srt.Subtitle(1, t("00:00:11,000"), t("00:00:12,701"), "A"),
            srt.Subtitle(2, t("00:00:12,701"), t("00:00:14,203"), "B"),
            srt.Subtitle(3, t("00:00:14,500"), t("00:00:19,738"), "C"),
            srt.Subtitle(4, t("00:00:16,538"), t("00:00:17,272"), "D"),
            srt.Subtitle(5, t("00:00:17,272"), t("00:00:18,440"), "E"),
            srt.Subtitle(6, t("00:00:20,000"), t("00:00:21,000"), "ADD"),
            srt.Subtitle(7, t("00:00:24,500"), t("00:00:30,000"), "ADD2"),
            srt.Subtitle(8, t("00:00:35,000"), t("00:00:40,000"), "ADD3"),
        ]
        self.assertEqual(list(result), a)

    def test_block_paste(self):
        result = paste([], self.copied, t("00:00:00,000"), block=True)
        self.assertEqual(list(result), self.copied)

        result = paste(self.subs(), [], t("00:00:00,000"), t("00:00:10,000"), True)
        a = [
            srt.Subtitle(1, t("00:00:21,000"), t("00:00:22,701"), "A"),
            srt.Subtitle(2, t("00:00:22,701"), t("00:00:24,203"), "B"),
            srt.Subtitle(3, t("00:00:24,500"), t("00:00:29,738"), "C"),
            srt.Subtitle(4, t("00:00:26,538"), t("00:00:27,272"), "D"),
            srt.Subtitle(5, t("00:00:27,272"), t("00:00:28,440"), "E"),
        ]
        self.assertEqual(list(result), a)

        result = paste(self.subs(), self.copied, t("00:00:00,000"), block=True)
        a = [
            srt.Subtitle(1, t("00:00:10,000"), t("00:00:11,000"), "ADD"),
            srt.Subtitle(2, t("00:00:14,500"), t("00:00:20,000"), "ADD2"),
            srt.Subtitle(3, t("00:00:25,000"), t("00:00:30,000"), "ADD3"),
            srt.Subtitle(4, t("00:00:41,000"), t("00:00:42,701"), "A"),
            srt.Subtitle(5, t("00:00:42,701"), t("00:00:44,203"), "B"),
            srt.Subtitle(6, t("00:00:44,500"), t("00:00:49,738"), "C"),
            srt.Subtitle(7, t("00:00:46,538"), t("00:00:47,272"), "D"),
            srt.Subtitle(8, t("00:00:47,272"), t("00:00:48,440"), "E"),
        ]
        self.assertEqual(list(result), a)  # before

        result = paste(self.subs(), self.copied, t("00:00:15,000"), block=True)
        a = [
            srt.Subtitle(1, t("00:00:11,000"), t("00:00:12,701"), "A"),
            srt.Subtitle(2, t("00:00:12,701"), t("00:00:14,203"), "B"),
            srt.Subtitle(3, t("00:00:14,500"), t("00:00:19,738"), "C"),
            srt.Subtitle(4, t("00:00:25,000"), t("00:00:26,000"), "ADD"),
            srt.Subtitle(5, t("00:00:29,500"), t("00:00:35,000"), "ADD2"),
            srt.Subtitle(6, t("00:00:40,000"), t("00:00:45,000"), "ADD3"),
            srt.Subtitle(7, t("00:00:46,538"), t("00:00:47,272"), "D"),
            srt.Subtitle(8, t("00:00:47,272"), t("00:00:48,440"), "E"),
        ]
        self.assertEqual(list(result), a)  # middle

        result = paste(self.subs(), self.copied, t("00:00:20,000"), block=True)
        a = [
            srt.Subtitle(1, t("00:00:11,000"), t("00:00:12,701"), "A"),
            srt.Subtitle(2, t("00:00:12,701"), t("00:00:14,203"), "B"),
            srt.Subtitle(3, t("00:00:14,500"), t("00:00:19,738"), "C"),
            srt.Subtitle(4, t("00:00:16,538"), t("00:00:17,272"), "D"),
            srt.Subtitle(5, t("00:00:17,272"), t("00:00:18,440"), "E"),
            srt.Subtitle(6, t("00:00:30,000"), t("00:00:31,000"), "ADD"),
            srt.Subtitle(7, t("00:00:34,500"), t("00:00:40,000"), "ADD2"),
            srt.Subtitle(8, t("00:00:45,000"), t("00:00:50,000"), "ADD3"),
        ]
        self.assertEqual(list(result), a)  # after

    def test_block_paste_space(self):
        result = paste(
            self.subs(), self.copied, t("00:00:00,000"), t("00:00:10,000"), True
        )
        a = [
            srt.Subtitle(1, t("00:00:20,000"), t("00:00:21,000"), "ADD"),
            srt.Subtitle(2, t("00:00:24,500"), t("00:00:30,000"), "ADD2"),
            srt.Subtitle(3, t("00:00:35,000"), t("00:00:40,000"), "ADD3"),
            srt.Subtitle(4, t("00:00:51,000"), t("00:00:52,701"), "A"),
            srt.Subtitle(5, t("00:00:52,701"), t("00:00:54,203"), "B"),
            srt.Subtitle(6, t("00:00:54,500"), t("00:00:59,738"), "C"),
            srt.Subtitle(7, t("00:00:56,538"), t("00:00:57,272"), "D"),
            srt.Subtitle(8, t("00:00:57,272"), t("00:00:58,440"), "E"),
        ]
        self.assertEqual(list(result), a)  # before

        result = paste(
            self.subs(), self.copied, t("00:00:15,000"), t("00:00:01,000"), True
        )
        a = [
            srt.Subtitle(1, t("00:00:11,000"), t("00:00:12,701"), "A"),
            srt.Subtitle(2, t("00:00:12,701"), t("00:00:14,203"), "B"),
            srt.Subtitle(3, t("00:00:14,500"), t("00:00:19,738"), "C"),
            srt.Subtitle(4, t("00:00:26,000"), t("00:00:27,000"), "ADD"),
            srt.Subtitle(5, t("00:00:30,500"), t("00:00:36,000"), "ADD2"),
            srt.Subtitle(6, t("00:00:41,000"), t("00:00:46,000"), "ADD3"),
            srt.Subtitle(7, t("00:00:47,538"), t("00:00:48,272"), "D"),
            srt.Subtitle(8, t("00:00:48,272"), t("00:00:49,440"), "E"),
        ]
        self.assertEqual(list(result), a)  # middle


if __name__ == "__main__":
    unittest.main()
