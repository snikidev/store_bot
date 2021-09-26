def escape_markdown_chars(text):
    return (
        text.replace("_", "\\_")
        .replace("-", "\\-")
        .replace("~", "\\~")
        .replace("`", "\\`")
        .replace(".", "\\.")
    )
