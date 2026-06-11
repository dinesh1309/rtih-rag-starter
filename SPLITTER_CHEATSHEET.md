# Text Splitter Cheat Sheet (Flowise + LangChain)

**Session default: Recursive Character Text Splitter — Chunk Size 800, Chunk Overlap 100.**
That one line works for ~95% of documents. The rest are special cases.

| Splitter | Use when |
|---|---|
| **Recursive Character** ✅ | **Default. Use this.** Splits at natural breaks (paragraph → sentence → word) so chunks stay meaningful. Right for emails, PDFs, Word docs, reports. |
| Character Text | Dumb split every N characters. Can cut mid-sentence. Rarely better than Recursive. |
| Token Text | Splits by tokens, not characters. Use only if you're tight against a model's token limit. |
| Markdown Text | Source is Markdown and you want to split by `#` headings. |
| HtmlToMarkdown | Source is raw HTML / web pages — converts to Markdown first, then splits. |
| Code Text | Source is source code — splits on functions / classes. |
| None | No splitting — whole doc as one chunk. Don't; retrieval gets vague. |

**Why chunking matters (one line for the slide):** smaller, precise chunks retrieve more
accurately and cost less than big vague ones. Overlap (100) carries context across the cut
so answers spanning two chunks don't break.
