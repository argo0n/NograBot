import math
import ast
import re
NUMBER_REGEX = r"[0-9\.]+"
from simpleeval import simple_eval

def secondstotiming(seconds):  # sourcery no-metrics
    seconds = round(seconds)
    if seconds < 60:
        secdisplay = "s" if seconds != 1 else ""
        return f"{seconds} second{secdisplay}"
    minutes = math.trunc(seconds / 60)
    if minutes < 60:
        seconds = seconds - minutes * 60
        mindisplay = "s" if minutes != 1 else ""
        secdisplay = "s" if seconds != 1 else ""
        return f"{minutes} minute{mindisplay} and {seconds} second{secdisplay}"
    hours = math.trunc(minutes / 60)
    if hours < 24:
        minutes = minutes - hours * 60
        seconds = seconds - minutes * 60 - hours * 60 * 60
        hdisplay = "s" if hours != 1 else ""
        mindisplay = "s" if minutes != 1 else ""
        secdisplay = "s" if seconds != 1 else ""
        return f"{hours} hour{hdisplay}, {minutes} minute{mindisplay} and {seconds} second{secdisplay}"
    days = math.trunc(hours / 24)
    if days < 7:
        hours = hours - days * 24
        minutes = minutes - hours * 60 - days * 24 * 60
        seconds = seconds - minutes * 60 - hours * 60 * 60 - days * 24 * 60 * 60
        ddisplay = "s" if days != 1 else ""
        hdisplay = "s" if hours != 1 else ""
        mindisplay = "s" if minutes != 1 else ""
        secdisplay = "s" if seconds != 1 else ""
        return f"{days} day{ddisplay}, {hours} hour{hdisplay}, {minutes} minute{mindisplay} and {seconds} second{secdisplay}"
    weeks = math.trunc(days / 7)
    days = days - weeks * 7
    hours = hours - weeks*168 - days * 24
    minutes = minutes - hours * 60 - days* 24 * 60 - weeks * 168 * 60
    seconds = seconds - minutes * 60 - hours * 60 * 60 - days * 24 * 60 * 60 - weeks * 168 * 60 * 60
    wdisplay = "s" if weeks != 1 else ""
    ddisplay = "s" if days != 1 else ""
    hdisplay = "s" if hours != 1 else ""
    mindisplay = "s" if minutes != 1 else ""
    secdisplay = "s" if seconds != 1 else ""
    return f"{weeks} week{wdisplay}, {days} day{ddisplay}, {hours} hour{hdisplay}, {minutes} minute{mindisplay} and {seconds} second{secdisplay}"


def durationdisplay(seconds):
    seconds = round(seconds)
    time = []
    if seconds < 60:
        time.append("0")
        time.append(str(seconds))
        return ":".join(time)
    minutes = math.trunc(seconds / 60)
    if minutes < 60:
        seconds = seconds - minutes * 60
        time.append(str(minutes))
        time.append("0" + str(seconds) if seconds < 10 else str(seconds))
    return ":".join(time)

def stringtotime(timing):
    allowedsymbols=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "y", "d", "h", "m", "s"]
    seconds = timing.lower()
    for character in list(seconds):
        if character not in allowedsymbols:
            return None
    if "y" in timing:
        timing = timing.replace("y", "*31536000+")
    if "d" in timing:
        timing = timing.replace("d", "*86400+")
    if "h" in timing:
        timing = timing.replace("h", "*3600+")
    if "m" in timing:
        timing = timing.replace("m", "*60+")
    if "s" in timing:
        timing = timing.replace("s", "*1+")
    timing += "0"
    timing = simple_eval(timing)
    print(timing)
    return timing