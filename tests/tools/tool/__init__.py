from srt import srt
from srt import srt_timestamp_to_timedelta as t


def create_blocks(setting=0):
    """Creates a generator of subtitles for testing purposes"""
    subs = []
    if setting == 0:
        subs.append(srt.Subtitle(1, t("00:00:11,000"), t("00:00:12,701"), "A"))
        subs.append(srt.Subtitle(2, t("00:00:12,701"), t("00:00:14,203"), "B"))
        subs.append(srt.Subtitle(3, t("00:00:14,500"), t("00:00:19,738"), "C"))
        subs.append(srt.Subtitle(4, t("00:00:16,538"), t("00:00:17,272"), "D"))
        subs.append(srt.Subtitle(5, t("00:00:17,272"), t("00:00:18,440"), "E"))
    elif setting == 1:
        subs.append(srt.Subtitle(1, t("00:00:1,000"), t("00:00:10,000"), "A"))
        subs.append(srt.Subtitle(2, t("00:00:2,000"), t("00:00:08,000"), "B"))
        subs.append(srt.Subtitle(3, t("00:00:3,000"), t("00:00:05,000"), "C"))
        subs.append(srt.Subtitle(4, t("00:00:3,500"), t("00:00:04,500"), "D"))
        subs.append(srt.Subtitle(5, t("00:00:6,000"), t("00:00:08,000"), "E"))
        subs.append(srt.Subtitle(6, t("00:00:9,000"), t("00:00:10,000"), "F"))

    for subtitle in subs:
        yield subtitle


def sort(subs):
    return list(srt.sort_and_reindex(subs))
