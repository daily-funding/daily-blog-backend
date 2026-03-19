import nh3

ALLOWED_TAGS = {
    "div",
    "figure",
    "figcaption",
    "p",
    "br",
    "span",
    "strong",
    "b",
    "em",
    "i",
    "u",
    "s",
    "blockquote",
    "ul",
    "ol",
    "li",
    "a",
    "img",
    "h1",
    "h2",
    "h3",
    "h4",
    "table",
    "thead",
    "tbody",
    "tr",
    "th",
    "td",
    "hr",
}

ALLOWED_ATTRIBUTES = {
    "*": {"class"},
    "a": {"href", "title", "target"},
    "img": {"src", "alt", "width", "height", "class"},
    "span": {"style"},
    "p": {"style"},
    "h1": {"style"},
    "h2": {"style"},
    "h3": {"style"},
    "h4": {"style"},
    "figure": {"class", "style"},
    "figcaption": {"class", "style"},
}


def sanitize_post_content(content: str) -> str:
    if not content:
        return ""

    return nh3.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        url_schemes={"http", "https"},
        filter_style_properties={"background-color", "color", "text-align"},
    )
