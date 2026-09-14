"""Safe rich-content sanitizer for seller-authored listing descriptions."""
import html
import re
from html.parser import HTMLParser
from urllib.parse import urlparse


ALLOWED_TAGS = {
    "h2", "h3", "h4", "p", "strong", "em", "u", "ul", "ol", "li",
    "blockquote", "a", "span", "div", "br", "hr", "code",
}
VOID_TAGS = {"br", "hr"}
ALLOWED_CSS_PROPERTIES = {
    "color", "background-color", "font-size", "font-weight", "font-style",
    "line-height", "text-align", "text-decoration", "letter-spacing",
    "margin", "margin-top", "margin-right", "margin-bottom", "margin-left",
    "padding", "padding-top", "padding-right", "padding-bottom", "padding-left",
    "border", "border-color", "border-width", "border-style", "border-radius",
    "display", "gap", "grid-template-columns", "max-width", "width",
}


def sanitize_css_declarations(css):
    declarations = []
    for declaration in (css or "").split(";"):
        if ":" not in declaration:
            continue
        prop, value = (part.strip() for part in declaration.split(":", 1))
        prop = prop.lower()
        lowered = value.lower()
        if prop not in ALLOWED_CSS_PROPERTIES:
            continue
        if any(token in lowered for token in ("url(", "expression", "javascript:", "@import", "\\")):
            continue
        if any(char in value for char in "{}<>;") or len(value) > 160:
            continue
        declarations.append(f"{prop}:{value}")
    return ";".join(declarations)


class RichHTMLSanitizer(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.output = []
        self.open_tags = []
        self.ignored_depth = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in {"script", "style", "iframe", "object", "svg"}:
            self.ignored_depth += 1
            return
        if self.ignored_depth or tag not in ALLOWED_TAGS:
            return
        safe_attrs = []
        attrs = dict(attrs)
        class_name = attrs.get("class", "")
        if class_name and re.fullmatch(r"[\w\- ]{1,120}", class_name):
            safe_attrs.append(("class", class_name))
        inline_style = sanitize_css_declarations(attrs.get("style", ""))
        if inline_style:
            safe_attrs.append(("style", inline_style))
        if tag == "a":
            href = attrs.get("href", "").strip()
            parsed = urlparse(href)
            if href and parsed.scheme in {"http", "https", "mailto"}:
                safe_attrs.extend((("href", href), ("target", "_blank"), ("rel", "noopener noreferrer nofollow")))
        rendered_attrs = "".join(f' {name}="{html.escape(value, quote=True)}"' for name, value in safe_attrs)
        self.output.append(f"<{tag}{rendered_attrs}>")
        if tag not in VOID_TAGS:
            self.open_tags.append(tag)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in {"script", "style", "iframe", "object", "svg"} and self.ignored_depth:
            self.ignored_depth -= 1
            return
        if self.ignored_depth or tag not in self.open_tags:
            return
        while self.open_tags:
            opened = self.open_tags.pop()
            self.output.append(f"</{opened}>")
            if opened == tag:
                break

    def handle_data(self, data):
        if not self.ignored_depth:
            self.output.append(html.escape(data))

    def result(self):
        while self.open_tags:
            self.output.append(f"</{self.open_tags.pop()}>")
        return "".join(self.output)


def sanitize_html(source):
    parser = RichHTMLSanitizer()
    parser.feed(source or "")
    parser.close()
    return parser.result()


def sanitize_scoped_css(source):
    source = re.sub(r"/\*.*?\*/", "", source or "", flags=re.S)
    rules = []
    for selectors, declarations in re.findall(r"([^{}]+)\{([^{}]*)\}", source):
        safe_declarations = sanitize_css_declarations(declarations)
        if not safe_declarations:
            continue
        safe_selectors = []
        for selector in selectors.split(","):
            selector = selector.strip()
            if not selector or selector.startswith("@") or len(selector) > 120:
                continue
            if re.search(r"(^|[\s>+~])(html|body|:root|\*)([\s>+~.#:\[]|$)", selector, re.I):
                continue
            if not re.fullmatch(r"[\w\s.#>+~:\-\[\]=\"'()]+", selector):
                continue
            safe_selectors.append(f".aboutplatform-user-content {selector}")
        if safe_selectors:
            rules.append(f"{','.join(safe_selectors)}{{{safe_declarations}}}")
    return "".join(rules)


def build_safe_rich_content(html_source, css_source):
    safe_html = sanitize_html(html_source)
    safe_css = sanitize_scoped_css(css_source)
    if not safe_html and not safe_css:
        return None
    style = f"<style>{safe_css}</style>" if safe_css else ""
    return f'<div class="aboutplatform-user-content">{safe_html}</div>{style}'
