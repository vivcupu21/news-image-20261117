# news-image-20261117 — The World in One Day

[![make.fun](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/vivcupu21/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/vivcupu21/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117)

A newspaper front page that sums up **Tuesday, 17 November 2026** in one
image: Ukraine strikes the Kerch Bridge to Crimea again, Iran fires drones
at a US radar base in Bahrain, Japan scrambles jets after Russian planes
enter its airspace, a settler kills a 72-year-old woman in Jericho as the
UK sanctions settlement builders, the UN counts 1,600+ drone deaths in
Sudan this year, and Mongolia's president says he will resign — plus a
ticker of the day's other stories.

## How it works

`main.py` (Python 3.13, standard library only) copies the image stored in
this repository (`entry.png`, drawn by `draw.py` with Pillow from the
day's reported news) to `/output/entry.png`. It needs no network and
writes identical bytes on every run.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## The image

- Format: PNG, 1024 × 1024 px, 113,583 bytes (gate: at most 1 MiB and
  1024 × 1024 px)
- Sources for the stories: Reuters, BBC, AP and CNN reporting of
  17 November 2026, as collected in Just Security's Early Edition of
  17 November 2026 and same-day news round-ups.

## License

MIT — see [LICENSE](LICENSE).
