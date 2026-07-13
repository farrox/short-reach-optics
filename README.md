# Ed (Ehsan) Shah Hosseini

Résumé and technical writing on short-reach optical interconnects for AI compute.

## Résumé

```bash
./compile.sh
```

Output: `main.pdf` (XeLaTeX).

## Book

**[Short-Reach Optics for AI Compute](books/short-reach-optics/)** — IM/DD fundamentals, lasers, WDM, validation, reliability, and AI datacenter networking (137 pages).

```bash
cd books/short-reach-optics && ./compile.sh
```

Source figures regenerate with:

```bash
cd books/short-reach-optics
MPLCONFIGDIR=.mplcache XDG_CACHE_HOME=.cache ./.venv/bin/python sims/make_figures.py
```

Optional local citation PDFs go in `books/short-reach-optics/docs/` (gitignored). See `docs/README.md`.

## Links

- [LinkedIn](https://www.linkedin.com/in/ehsansh/)
- [Google Scholar](https://scholar.google.com/citations?user=i6EaMioAAAAJ&hl=en)
