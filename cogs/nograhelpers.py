import math


def secondstotiming(seconds):
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
        minutes = minutes - hours * 60
        seconds = seconds - minutes * 60 - hours * 60 * 60
        ddisplay = "s" if days != 1 else ""
        hdisplay = "s" if hours != 1 else ""
        mindisplay = "s" if minutes != 1 else ""
        secdisplay = "s" if seconds != 1 else ""
        return f"{days} day{ddisplay}, {hours} hour{hdisplay}, {minutes} minute{mindisplay} and {seconds} second{secdisplay}"
    weeks = math.trunc(days / 7)
    days = days - weeks * 7
    hours = hours - days * 24
    minutes = minutes - hours * 60
    seconds = seconds - minutes * 60 - hours * 60 * 60
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
