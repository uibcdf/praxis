"""Offline Markdown and HTML rendering; content is escaped before HTML publication."""

import html


def _markdown_cell(value):
    return html.escape(value, quote=False).replace("|", "\\|").replace("\n", "<br>")


def render(document, format="markdown"):
    if format == "markdown":
        lines = ["# " + _markdown_cell(document.title), "", "Generated: " + document.generated, ""]
        for paragraph in document.paragraphs:
            lines.extend([_markdown_cell(paragraph), ""])
        if document.columns:
            lines.append("| " + " | ".join(map(_markdown_cell, document.columns)) + " |")
            lines.append("| " + " | ".join("---" for _ in document.columns) + " |")
            lines.extend(
                "| " + " | ".join(map(_markdown_cell, row)) + " |" for row in document.rows
            )
        return "\n".join(lines) + "\n"
    if format == "html":
        title = html.escape(document.title)
        paragraphs = "".join("<p>" + html.escape(item) + "</p>" for item in document.paragraphs)
        table = ""
        if document.columns:
            header = "".join("<th>" + html.escape(item) + "</th>" for item in document.columns)
            rows = "".join(
                "<tr>" + "".join("<td>" + html.escape(item) + "</td>" for item in row) + "</tr>"
                for row in document.rows
            )
            table = (
                "<table><thead><tr>" + header + "</tr></thead><tbody>" + rows + "</tbody></table>"
            )
        return (
            '<!doctype html><html lang="en"><meta charset="utf-8"><title>'
            + title
            + "</title><body><h1>"
            + title
            + "</h1><p>Generated: "
            + html.escape(document.generated)
            + "</p>"
            + paragraphs
            + table
            + "</body></html>"
        )
    raise ValueError("Supported report formats are markdown and html")
