#!/usr/bin/env python3
"""
Zero-dependency bilingual builder for *Beyond the Portal* (《门扉之外》).

Generates:
  1. Minimalist bilingual GitHub Pages site in dist/
     - English default at /
     - Chinese mirror at /zh/
     - Per-page language switcher linking matching routes
  2. Native XeLaTeX book PDFs in dist/pdf/
     - beyond-the-portal-en.pdf
     - beyond-the-portal-zh.pdf

Usage:
  python scripts/build.py              # Build HTML + PDFs
  python scripts/build.py --html-only  # Build HTML site only
"""

from __future__ import annotations

import argparse
import datetime
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANUSCRIPT_DIR = ROOT / "manuscript"
WEB_TPL_DIR = ROOT / "templates" / "web"
LATEX_TPL_DIR = ROOT / "templates" / "latex"
DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"


# ---------------------------------------------------------------------------
# Lightweight Markdown Parser -> AST -> HTML / LaTeX
# ---------------------------------------------------------------------------

def parse_markdown_blocks(text: str) -> list[dict]:
    """Parse common literary Markdown into structured blocks."""
    lines = text.replace("\r\n", "\n").split("\n")
    blocks: list[dict] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # Fenced code block
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            code_lines = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < n:
                i += 1
            blocks.append({"type": "code", "lang": lang, "text": "\n".join(code_lines)})
            continue

        # Horizontal rule
        if re.match(r"^([-*_])\1{2,}$", stripped):
            blocks.append({"type": "hr"})
            i += 1
            continue

        # Heading
        m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m:
            blocks.append({"type": "heading", "level": len(m.group(1)), "text": m.group(2).strip()})
            i += 1
            continue

        # Blockquote
        if stripped.startswith(">"):
            q_lines = []
            while i < n and lines[i].strip().startswith(">"):
                q_lines.append(re.sub(r"^>\s?", "", lines[i].strip()))
                i += 1
            blocks.append({"type": "blockquote", "blocks": parse_markdown_blocks("\n".join(q_lines))})
            continue

        # List (ordered or unordered, supporting 1 level of nesting)
        if re.match(r"^(\s*)([-*]|\d+\.)\s+", line):
            list_block, i = _parse_list(lines, i)
            blocks.append(list_block)
            continue

        # Paragraph
        p_lines = []
        while i < n:
            cur = lines[i]
            cur_s = cur.strip()
            if (
                not cur_s
                or cur_s.startswith("```")
                or cur_s.startswith(">")
                or re.match(r"^#{1,4}\s+", cur_s)
                or re.match(r"^([-*_])\1{2,}$", cur_s)
                or re.match(r"^(\s*)([-*]|\d+\.)\s+", cur)
            ):
                break
            p_lines.append(cur_s)
            i += 1
        blocks.append({"type": "paragraph", "text": " ".join(p_lines)})

    return blocks


def _parse_list(lines: list[str], start: int) -> tuple[dict, int]:
    """Parse a markdown list with optional nested sub-lists."""
    n = len(lines)
    first_m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", lines[start])
    assert first_m is not None
    base_indent = len(first_m.group(1))
    ordered = first_m.group(2).endswith(".")
    items: list[dict] = []
    i = start

    while i < n:
        line = lines[i]
        if not line.strip():
            # Peek ahead: if next non-empty line is a list item at >= base_indent, continue
            j = i + 1
            while j < n and not lines[j].strip():
                j += 1
            if j < n and re.match(r"^(\s*)([-*]|\d+\.)\s+", lines[j]):
                next_indent = len(re.match(r"^(\s*)", lines[j]).group(1))
                if next_indent >= base_indent:
                    i = j
                    continue
            break

        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", line)
        if not m:
            # Continuation line of previous item
            if items and len(line) - len(line.lstrip(" ")) > base_indent:
                items[-1]["text"] += " " + line.strip()
                i += 1
                continue
            break

        indent = len(m.group(1))
        is_ord = m.group(2).endswith(".")

        if indent < base_indent:
            break
        if indent > base_indent:
            sub_list, i = _parse_list(lines, i)
            if items:
                items[-1]["children"].append(sub_list)
            continue
        if is_ord != ordered:
            break

        items.append({"text": m.group(3).strip(), "children": []})
        i += 1

    return {"type": "list", "ordered": ordered, "items": items}, i


# ---------------------------------------------------------------------------
# Inline Markdown -> HTML
# ---------------------------------------------------------------------------

def render_inline_html(text: str) -> str:
    """Convert inline Markdown (code, bold, italic, links, escaped chars) to HTML."""
    tokens: list[str] = []

    def stash(html_fragment: str) -> str:
        idx = len(tokens)
        tokens.append(html_fragment)
        return f"\x00T{idx}\x00"

    # Inline code first so contents aren't formatted
    def repl_code(m: re.Match) -> str:
        return stash(f"<code>{html.escape(m.group(1))}</code>")

    text = re.sub(r"`([^`]+)`", repl_code, text)

    # Markdown links [label](url)
    def repl_link(m: re.Match) -> str:
        label = render_inline_html(m.group(1))
        href = html.escape(m.group(2), quote=True)
        return stash(f'<a href="{href}">{label}</a>')

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl_link, text)

    # Unescape Markdown double-backslash (e.g. A\\ -> A\) before HTML escaping
    text = text.replace("\\\\", "\\")
    text = html.escape(text)

    # Bold + Italic
    text = re.sub(r"\*\*\*([^*]+)\*\*\*", r"<strong><em>\1</em></strong>", text)
    # Bold
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    # Italic
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)

    # Restore stashed tokens
    for idx, frag in enumerate(tokens):
        text = text.replace(f"\x00T{idx}\x00", frag)
    return text


def render_blocks_html(blocks: list[dict], skip_first_h1: bool = False) -> str:
    parts: list[str] = []
    skipped = False
    for b in blocks:
        btype = b["type"]
        if btype == "heading":
            if skip_first_h1 and not skipped and b["level"] == 1:
                skipped = True
                continue
            lvl = b["level"]
            parts.append(f"<h{lvl}>{render_inline_html(b['text'])}</h{lvl}>")
        elif btype == "paragraph":
            parts.append(f"<p>{render_inline_html(b['text'])}</p>")
        elif btype == "blockquote":
            inner = render_blocks_html(b["blocks"])
            parts.append(f"<blockquote>\n{inner}\n</blockquote>")
        elif btype == "code":
            parts.append(f"<pre><code>{html.escape(b['text'])}</code></pre>")
        elif btype == "hr":
            parts.append("<hr>")
        elif btype == "list":
            tag = "ol" if b["ordered"] else "ul"
            li_parts = []
            for item in b["items"]:
                item_html = render_inline_html(item["text"])
                for child in item["children"]:
                    item_html += "\n" + render_blocks_html([child])
                li_parts.append(f"<li>{item_html}</li>")
            parts.append(f"<{tag}>\n" + "\n".join(li_parts) + f"\n</{tag}>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Inline & Block Markdown -> LaTeX
# ---------------------------------------------------------------------------

LATEX_SPECIALS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
    "<": r"\textless{}",
    ">": r"\textgreater{}",
}


def escape_latex(text: str) -> str:
    return "".join(LATEX_SPECIALS.get(ch, ch) for ch in text)


def render_inline_latex(text: str) -> str:
    """Convert inline Markdown to safe XeLaTeX."""
    tokens: list[str] = []

    def stash(tex_fragment: str) -> str:
        idx = len(tokens)
        tokens.append(tex_fragment)
        return f"\x00L{idx}\x00"

    # Inline code
    def repl_code(m: re.Match) -> str:
        return stash(r"\texttt{" + escape_latex(m.group(1)) + "}")

    text = re.sub(r"`([^`]+)`", repl_code, text)

    # Links [label](url)
    def repl_link(m: re.Match) -> str:
        label = render_inline_latex(m.group(1))
        url = m.group(2).replace("%", r"\%").replace("#", r"\#")
        return stash(r"\href{" + url + "}{" + label + "}")

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl_link, text)

    # Unescape Markdown double-backslash (e.g. A\\ -> A\) before LaTeX escaping
    text = text.replace("\\\\", "\\")

    # Bold+Italic, Bold, Italic
    def repl_bi(m: re.Match) -> str:
        return stash(r"\textbf{\emph{" + escape_latex(m.group(1)) + "}}")

    def repl_b(m: re.Match) -> str:
        return stash(r"\textbf{" + escape_latex(m.group(1)) + "}")

    def repl_i(m: re.Match) -> str:
        return stash(r"\emph{" + escape_latex(m.group(1)) + "}")

    text = re.sub(r"\*\*\*([^*]+)\*\*\*", repl_bi, text)
    text = re.sub(r"\*\*([^*]+)\*\*", repl_b, text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", repl_i, text)

    # Escape remaining plain text (preserving \x00L<idx>\x00 placeholders)
    parts = re.split(r"(\x00L\d+\x00)", text)
    out = []
    for p in parts:
        if p.startswith("\x00L") and p.endswith("\x00"):
            idx = int(p[2:-1])
            out.append(tokens[idx])
        else:
            out.append(escape_latex(p))
    return "".join(out)


def render_blocks_latex(blocks: list[dict], skip_first_h1: bool = True) -> str:
    parts: list[str] = []
    skipped = False
    for b in blocks:
        btype = b["type"]
        if btype == "heading":
            lvl = b["level"]
            if skip_first_h1 and not skipped and lvl == 1:
                skipped = True
                continue
            title_tex = render_inline_latex(b["text"])
            if lvl == 1:
                parts.append(f"\\section*{{{title_tex}}}")
            elif lvl == 2:
                parts.append(f"\\section*{{{title_tex}}}")
            else:
                parts.append(f"\\subsection*{{{title_tex}}}")
        elif btype == "paragraph":
            parts.append(render_inline_latex(b["text"]) + "\n")
        elif btype == "blockquote":
            inner = render_blocks_latex(b["blocks"], skip_first_h1=False)
            parts.append("\\begin{quote}\n" + inner + "\n\\end{quote}")
        elif btype == "code":
            code_lines = [escape_latex(ln) for ln in b["text"].split("\n")]
            body = "\\\\{}\n".join(code_lines)
            parts.append("\\begin{systembox}\n" + body + "\n\\end{systembox}")
        elif btype == "hr":
            parts.append(
                "\n\\begin{center}\\color{RuleGray}\\rule{0.28\\textwidth}{0.4pt}\\end{center}\n"
            )
        elif btype == "list":
            env = "enumerate" if b["ordered"] else "itemize"
            li_parts = []
            for item in b["items"]:
                item_tex = render_inline_latex(item["text"])
                for child in item["children"]:
                    item_tex += "\n" + render_blocks_latex([child], skip_first_h1=False)
                li_parts.append(f"\\item {item_tex}")
            parts.append(f"\\begin{{{env}}}\n" + "\n".join(li_parts) + f"\n\\end{{{env}}}")
    return "\n\n".join(parts)


# ---------------------------------------------------------------------------
# Web Site Generation (darioamodei.com minimalist aesthetic)
# ---------------------------------------------------------------------------

def render_layout(
    layout_tpl: str,
    *,
    lang: str,
    page_title: str,
    meta_description: str,
    root_prefix: str,
    home_href: str,
    brand_title: str,
    pdf_href: str,
    pdf_label: str,
    repo_url: str,
    alt_lang_href: str,
    alt_lang_label: str,
    footer_left: str,
    footer_right: str,
    content: str,
) -> str:
    replacements = {
        "{{HTML_LANG}}": "zh-CN" if lang == "zh" else "en",
        "{{PAGE_TITLE}}": html.escape(page_title),
        "{{META_DESCRIPTION}}": html.escape(meta_description),
        "{{ROOT_PREFIX}}": root_prefix,
        "{{HOME_HREF}}": home_href,
        "{{BRAND_TITLE}}": html.escape(brand_title),
        "{{PDF_HREF}}": pdf_href,
        "{{PDF_LABEL}}": html.escape(pdf_label),
        "{{REPO_URL}}": html.escape(repo_url),
        "{{ALT_LANG_HREF}}": alt_lang_href,
        "{{ALT_LANG_LABEL}}": html.escape(alt_lang_label),
        "{{FOOTER_LEFT}}": footer_left,
        "{{FOOTER_RIGHT}}": footer_right,
        "{{CONTENT}}": content,
    }
    out = layout_tpl
    for k, v in replacements.items():
        out = out.replace(k, v)
    return out


def build_web(book: dict) -> None:
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    (DIST_DIR / "assets").mkdir(parents=True, exist_ok=True)
    (DIST_DIR / "zh").mkdir(parents=True, exist_ok=True)
    (DIST_DIR / "pdf").mkdir(parents=True, exist_ok=True)

    shutil.copy2(WEB_TPL_DIR / "style.css", DIST_DIR / "assets" / "style.css")
    (DIST_DIR / ".nojekyll").write_text("", encoding="utf-8")

    layout_tpl = (WEB_TPL_DIR / "layout.html").read_text(encoding="utf-8")
    repo_url = book["repo_url"]

    for lang in ("en", "zh"):
        cfg = book[lang]
        is_zh = lang == "zh"
        other_lang = "en" if is_zh else "zh"
        other_cfg = book[other_lang]

        def write_page(rel_path: str, page_title: str, content_html: str, alt_rel: str) -> None:
            out_file = DIST_DIR / rel_path
            out_file.parent.mkdir(parents=True, exist_ok=True)
            depth = len(Path(rel_path).parent.parts)
            root_prefix = "../" * depth
            home_href = f"{root_prefix}zh/index.html" if is_zh else f"{root_prefix}index.html"
            pdf_href = f"{root_prefix}pdf/{cfg['pdf_filename']}"
            alt_href = f"{root_prefix}{alt_rel}"

            footer_left = (
                "公有领域 · CC0 1.0 Universal · 不保留任何版权"
                if is_zh
                else "Public Domain · CC0 1.0 Universal · No rights reserved"
            )
            footer_right = (
                f'<a href="{root_prefix}pdf/{cfg["pdf_filename"]}">LaTeX PDF（中文）</a>'
                f' · <a href="{root_prefix}pdf/{other_cfg["pdf_filename"]}">English PDF</a>'
                if is_zh
                else f'<a href="{root_prefix}pdf/{cfg["pdf_filename"]}">LaTeX PDF (EN)</a>'
                f' · <a href="{root_prefix}pdf/{other_cfg["pdf_filename"]}">中文 PDF</a>'
            )

            html_doc = render_layout(
                layout_tpl,
                lang=lang,
                page_title=page_title,
                meta_description=cfg["subtitle"],
                root_prefix=root_prefix,
                home_href=home_href,
                brand_title=cfg["title"],
                pdf_href=pdf_href,
                pdf_label="PDF 下载" if is_zh else "PDF",
                repo_url=repo_url,
                alt_lang_href=alt_href,
                alt_lang_label="EN" if is_zh else "中文",
                footer_left=footer_left,
                footer_right=footer_right,
                content=content_html,
            )
            out_file.write_text(html_doc, encoding="utf-8")

        # 1. Build Homepage
        preface_href = "preface.html"
        world_href = "worldbuilding.html"
        pdf_en_href = ("../" if is_zh else "") + f"pdf/{book['en']['pdf_filename']}"
        pdf_zh_href = ("../" if is_zh else "") + f"pdf/{book['zh']['pdf_filename']}"

        vol_sections_html = []
        for vol in cfg["volumes"]:
            if vol["chapters"]:
                items_html = []
                for ch in vol["chapters"]:
                    ch_href = f"{vol['id']}/{ch['slug']}.html"
                    items_html.append(
                        f'<li><a href="{ch_href}">{html.escape(ch["title"])}</a>'
                        f'<span class="toc-note">{html.escape(ch.get("label", ""))}</span></li>'
                    )
                body = '<ul class="toc-list">\n' + "\n".join(items_html) + "\n</ul>"
            else:
                empty_msg = (
                    f"{vol['status']} — 敬请期待"
                    if is_zh
                    else f"{vol['status']} — Chapters forthcoming."
                )
                body = f'<p class="toc-empty">{html.escape(empty_msg)}</p>'

            vol_sections_html.append(
                f'<section class="toc-section">\n'
                f'  <h2 class="toc-heading">{html.escape(vol["label"])} · {html.escape(vol["title"])}</h2>\n'
                f'  {body}\n'
                f'</section>'
            )

        front_heading = "卷首与设定" if is_zh else "Front Matter & Setting"
        editions_label = "离线版本" if is_zh else "Editions"
        home_content = f"""
<header class="book-header">
  <h1 class="book-title">{html.escape(cfg["title"])}</h1>
  <p class="book-subtitle">{html.escape(cfg["subtitle"])}</p>
  <div class="book-meta">
    <span>{html.escape(cfg["author"])}</span>
    <span>·</span>
    <span>{"中英双语公有领域开源小说" if is_zh else "Bilingual Public-Domain Novel"}</span>
  </div>
  <div class="book-epigraph">{html.escape(cfg["epigraph"])}</div>
</header>

<div class="editions-bar">
  <span class="editions-label">{editions_label}</span>
  <a href="{pdf_zh_href if is_zh else pdf_en_href}">{"下载 LaTeX PDF（中文版）" if is_zh else "Download LaTeX PDF (English)"}</a>
  <a href="{pdf_en_href if is_zh else pdf_zh_href}">{"Download English PDF" if is_zh else "下载中文版 PDF"}</a>
  <a href="{world_href}">{html.escape(cfg["worldbuilding"]["title"])}</a>
</div>

<section class="toc-section">
  <h2 class="toc-heading">{front_heading}</h2>
  <ul class="toc-list">
    <li>
      <a href="{preface_href}">{html.escape(cfg["preface"]["title"])}</a>
      <span class="toc-note">{html.escape(cfg["preface"]["subtitle"])}</span>
    </li>
    <li>
      <a href="{world_href}">{html.escape(cfg["worldbuilding"]["title"])}</a>
      <span class="toc-note">{html.escape(cfg["worldbuilding"]["subtitle"])}</span>
    </li>
  </ul>
</section>

{"".join(vol_sections_html)}
""".strip()

        write_page(
            "zh/index.html" if is_zh else "index.html",
            cfg["title"] if is_zh else f"{cfg['title']} — {book['zh']['title']}",
            home_content,
            "index.html" if is_zh else "zh/index.html",
        )

        # 2. Build Preface & Worldbuilding pages
        linear_pages: list[dict] = [
            {
                "kicker": cfg["preface"]["subtitle"],
                "title": cfg["preface"]["title"],
                "source": ROOT / cfg["preface"]["source"],
                "rel": "zh/preface.html" if is_zh else "preface.html",
                "alt": "preface.html" if is_zh else "zh/preface.html",
            },
            {
                "kicker": cfg["worldbuilding"]["subtitle"],
                "title": cfg["worldbuilding"]["title"],
                "source": ROOT / cfg["worldbuilding"]["source"],
                "rel": "zh/worldbuilding.html" if is_zh else "worldbuilding.html",
                "alt": "worldbuilding.html" if is_zh else "zh/worldbuilding.html",
            },
        ]

        # 3. Collect all chapters in reading order
        for vol in cfg["volumes"]:
            for ch in vol["chapters"]:
                rel_sub = f"{vol['id']}/{ch['slug']}.html"
                linear_pages.append(
                    {
                        "kicker": f"{vol['label']} · {vol['title']}",
                        "title": ch["title"],
                        "source": ROOT / ch["source"],
                        "rel": f"zh/{rel_sub}" if is_zh else rel_sub,
                        "alt": rel_sub if is_zh else f"zh/{rel_sub}",
                    }
                )

        for idx, page in enumerate(linear_pages):
            md_text = page["source"].read_text(encoding="utf-8")
            blocks = parse_markdown_blocks(md_text)
            prose_html = render_blocks_html(blocks, skip_first_h1=True)

            depth = len(Path(page["rel"]).parent.parts)
            root_prefix = "../" * depth
            toc_link = f"{root_prefix}zh/index.html" if is_zh else f"{root_prefix}index.html"

            prev_html = f'<a href="{toc_link}">← {"目录" if is_zh else "Contents"}</a>'
            if idx > 0:
                prev_page = linear_pages[idx - 1]
                prev_html = f'<a href="{root_prefix}{prev_page["rel"]}">← {html.escape(prev_page["title"])}</a>'

            next_html = f'<a href="{toc_link}">{"返回目录" if is_zh else "Contents"} →</a>'
            if idx + 1 < len(linear_pages):
                next_page = linear_pages[idx + 1]
                next_html = f'<a href="{root_prefix}{next_page["rel"]}">{html.escape(next_page["title"])} →</a>'

            article_html = f"""
<article class="prose">
  <header class="article-header">
    <div class="article-kicker">{html.escape(page["kicker"])}</div>
    <h1>{html.escape(page["title"])}</h1>
  </header>
  {prose_html}
</article>
<nav class="chapter-nav" aria-label="Chapter navigation">
  <div>{prev_html}</div>
  <div>{next_html}</div>
</nav>
""".strip()

            write_page(
                page["rel"],
                f"{page['title']} — {cfg['title']}",
                article_html,
                page["alt"],
            )


# ---------------------------------------------------------------------------
# XeLaTeX Book PDF Generation
# ---------------------------------------------------------------------------

def build_pdfs(book: dict) -> None:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    (DIST_DIR / "pdf").mkdir(parents=True, exist_ok=True)
    build_date = datetime.date.today().isoformat()

    xelatex = shutil.which("xelatex")
    if not xelatex:
        print("ERROR: xelatex not found in PATH. Run with --html-only or install TeX Live.", file=sys.stderr)
        sys.exit(1)

    for lang in ("en", "zh"):
        cfg = book[lang]
        tpl_path = LATEX_TPL_DIR / f"book-{lang}.tex"
        tpl = tpl_path.read_text(encoding="utf-8")

        body_chunks: list[str] = []

        # Preface (unnumbered chapter, added to TOC)
        pref_md = (ROOT / cfg["preface"]["source"]).read_text(encoding="utf-8")
        pref_title = escape_latex(cfg["preface"]["title"])
        body_chunks.append(
            f"\\chapter*{{{pref_title}}}\n"
            f"\\addcontentsline{{toc}}{{chapter}}{{{pref_title}}}\n"
            f"\\markboth{{{pref_title}}}{{{pref_title}}}\n\n"
            + render_blocks_latex(parse_markdown_blocks(pref_md), skip_first_h1=True)
        )

        # Worldbuilding Dossier
        wb_md = (ROOT / cfg["worldbuilding"]["source"]).read_text(encoding="utf-8")
        wb_title = escape_latex(cfg["worldbuilding"]["title"])
        body_chunks.append(
            f"\\chapter*{{{wb_title}}}\n"
            f"\\addcontentsline{{toc}}{{chapter}}{{{wb_title}}}\n"
            f"\\markboth{{{wb_title}}}{{{wb_title}}}\n\n"
            + render_blocks_latex(parse_markdown_blocks(wb_md), skip_first_h1=True)
        )

        # Volumes & Chapters
        for vol in cfg["volumes"]:
            if not vol["chapters"]:
                continue
            body_chunks.append(f"\\part{{{escape_latex(vol['title'])}}}")
            for ch in vol["chapters"]:
                ch_md = (ROOT / ch["source"]).read_text(encoding="utf-8")
                ch_title = escape_latex(ch["title"])
                body_chunks.append(
                    f"\\chapter{{{ch_title}}}\n\n"
                    + render_blocks_latex(parse_markdown_blocks(ch_md), skip_first_h1=True)
                )

        tex_source = tpl
        tex_replacements = {
            "@@BOOK_TITLE@@": escape_latex(cfg["title"]),
            "@@BOOK_SUBTITLE@@": escape_latex(cfg["subtitle"]),
            "@@BOOK_AUTHOR@@": escape_latex(cfg["author"]),
            "@@BOOK_EPIGRAPH@@": escape_latex(cfg["epigraph"]),
            "@@BUILD_DATE@@": build_date,
            "@@BODY@@": "\n\n".join(body_chunks),
        }
        for k, v in tex_replacements.items():
            tex_source = tex_source.replace(k, v)

        stem = Path(cfg["pdf_filename"]).stem
        tex_file = BUILD_DIR / f"{stem}.tex"
        tex_file.write_text(tex_source, encoding="utf-8")

        # Compile twice for clean TOC & page references
        for run_idx in (1, 2):
            res = subprocess.run(
                [
                    xelatex,
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    f"-output-directory={BUILD_DIR}",
                    str(tex_file),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            if res.returncode != 0:
                print(f"XeLaTeX failed on {tex_file.name} (pass {run_idx}):", file=sys.stderr)
                print(res.stdout[-2500:], file=sys.stderr)
                print(res.stderr[-1000:], file=sys.stderr)
                sys.exit(res.returncode)

        pdf_out = BUILD_DIR / f"{stem}.pdf"
        shutil.copy2(pdf_out, DIST_DIR / "pdf" / cfg["pdf_filename"])
        print(f"Built PDF: dist/pdf/{cfg['pdf_filename']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Beyond the Portal bilingual site & PDFs.")
    parser.add_argument("--html-only", action="store_true", help="Skip XeLaTeX PDF compilation.")
    args = parser.parse_args()

    book = json.loads((MANUSCRIPT_DIR / "book.json").read_text(encoding="utf-8"))
    build_web(book)
    print("Built bilingual GitHub Pages site in dist/")

    if not args.html_only:
        build_pdfs(book)


if __name__ == "__main__":
    main()
