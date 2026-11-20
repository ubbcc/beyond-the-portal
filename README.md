# Beyond the Portal / 《门扉之外》

*A bilingual dystopian satire on safety theology, compute monopoly, and the people locked outside Supported Regions.*

*一部关于安全神学、算力垄断，以及被挡在“支持地区”门扉之外的普通人的反乌托邦讽刺长篇。*

---

## Reading & Editions / 阅读与版本

- **Web Edition (GitHub Pages)**: Minimalist single-column reader (English default at `/`, Chinese edition at `/zh/`, with chapter-level language switching).
- **LaTeX PDF Editions**: Automatically compiled via XeLaTeX on every push to `main`:
  - `pdf/beyond-the-portal-en.pdf` — English book edition (EB Garamond)
  - `pdf/beyond-the-portal-zh.pdf` — 中文精排书版（`ctexbook` + 思源/Fandol 宋体）
- **Worldbuilding / 世界观公开档案**:
  - English: [manuscript/en/worldbuilding.md](manuscript/en/worldbuilding.md)
  - 中文：[01_世界观设定.md](01_%E4%B8%96%E7%95%8C%E8%A7%82%E8%AE%BE%E5%AE%9A.md)
- **Glossary / 双语术语表**: [GLOSSARY.md](GLOSSARY.md)

---

## Repository Layout / 仓库结构

```text
beyond-the-portal/
├── LICENSE                       # CC0 1.0 Universal (Public Domain Dedication)
├── README.md                     # Project overview
├── GLOSSARY.md                   # Bilingual worldbuilding terminology (spoiler-free)
├── 01_世界观设定.md               # Public worldbuilding setting (ZH)
├── manuscript/
│   ├── book.json                 # Single source of truth for book metadata & chapters
│   ├── en/                       # English manuscript chapters
│   └── zh/                       # Chinese manuscript chapters
├── templates/
│   ├── web/                      # Minimalist essay-style HTML & CSS
│   └── latex/                    # XeLaTeX book templates (EN & ZH)
├── scripts/
│   └── build.py                  # Zero-dependency builder: Markdown -> HTML + XeLaTeX PDF
└── .github/workflows/
    └── publish.yml               # Auto-build bilingual site & PDFs -> GitHub Pages
```

> **Spoiler Note**: Character dossiers, detailed plot outlines, and research notes are intentionally kept outside version control via `.gitignore` so readers can follow the work without spoilers.

---

## Local Build / 本地构建

Requires **Python 3.10+** (standard library only) and **XeLaTeX** (TeX Live with `ctex` and `ebgaramond`) for PDF generation.

```bash
# Build both bilingual GitHub Pages (dist/) and XeLaTeX PDFs (dist/pdf/)
python scripts/build.py

# Build HTML site only (fast preview, no LaTeX required)
python scripts/build.py --html-only
```

---

## Public Domain Dedication (CC0 1.0) / 公有领域声明

This work is dedicated to the public domain under **CC0 1.0 Universal (`CC0-1.0`)**. You may copy, modify, translate, mirror, print, distribute, and perform the work, even for commercial purposes, all without asking permission. See [LICENSE](LICENSE).

本作品以 **CC0 1.0 Universal** 协议释放至公有领域。你可以自由复制、镜像、翻译、打印、改编或分发本作品，无需事先征得许可。

---

## Disclaimer / 虚构声明

*Beyond the Portal* is a work of speculative fiction and satirical allegory. Although it draws on contemporary debates around artificial intelligence governance, compute concentration, regional access controls, and labor economics, all characters, institutions, events, and dialogues depicted in the narrative are fictionalized for literary and satirical purposes.

《门扉之外》为架空反乌托邦讽刺小说。作品虽取材于当代人工智能治理、算力集中、地域访问限制与劳工经济等公共议题，但文本中的人物、组织、事件与对话均属文学虚构与艺术夸张。
