import re


def html_to_string_formatter(text):
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", text)
    return cleantext


def escape_markdown_chars(text):
    return (
        text.replace("_", "\\_")
        .replace("-", "\\-")
        .replace("~", "\\~")
        .replace("`", "\\`")
        .replace(".", "\\.")
    )
