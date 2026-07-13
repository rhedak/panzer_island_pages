import os


def _relative_webnovel_path(src_uri):
    depth = src_uri.count("/")
    if depth == 0:
        return "webnovel/index.md"
    return "../" * depth + "webnovel/index.md"


def on_page_markdown(markdown, page, config, files):
    src = page.file.src_uri

    # Blog posts are plugin-managed
    if src.startswith("blog/"):
        return markdown

    # Internal reference pages
    if src in ("styleguide_en.md", "404.md"):
        return markdown

    footer_name = "footer_webnovel.md" if src.startswith("webnovel/ch") else "footer.md"
    # noinspection PyTypeChecker
    footer_path = os.path.join(os.path.dirname(config.config_file_path), footer_name)
    try:
        with open(footer_path) as f:
            footer = f.read().strip()
    except FileNotFoundError:
        return markdown

    footer = footer.replace("{{ webnovel_path }}", _relative_webnovel_path(src))
    return markdown + "\n\n---\n\n" + footer + "\n"
