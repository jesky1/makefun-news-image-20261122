[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![Rank](https://make.fun/badge/news-image-20261122-rank.svg)](https://make.fun/bounty/news-image-20261122)
[![Reward](https://make.fun/badge/news-image-20261122-reward.svg)](https://make.fun/bounty/news-image-20261122)

# The World in One Day — Sunday 22 November 2026

Entry for the make.fun competition
[news-image-20261122](https://make.fun/bounty/news-image-20261122):
**"Sum up 22 November's world news in one image."**

The entry is a one-page newspaper front page (1024×1024 PNG) drawn from
scratch with Python + Pillow — no photographs, no external images. The
hero panel is a hand-drawn night scene over the Gulf: missile and
interceptor trails above a silhouetted air base with Patriot radar dishes.

## The stories

- **Lead — Gulf crisis:** Iran launched a combined missile-and-drone
  attack on U.S. Patriot radars at two bases in Bahrain (al-Riffa and
  Awali) on Saturday night, claiming two radars destroyed, in retaliation
  for U.S. drone flights over Iranian airspace and a strike on a radar
  site on Hengam Island. Bahrain said the attack hit a civilian
  industrial facility, causing a fire with no injuries; at least three
  oil tankers were attacked in or near the Strait of Hormuz.
- **Ukraine:** Russian missiles hit Lviv — at least 2 killed, 10 wounded;
  a drone hit a Russian cargo ship in the Baltic; Finland tightened
  security.
- **Trade:** The EU and Indonesia signed a landmark trade deal after ten
  years of talks, removing tariffs on about 98.5% of goods.
- **Climate:** COP31 in Antalya ran over schedule, deadlocked over fossil
  fuels.
- **Earthquake:** A magnitude 6.9 quake struck the Andes in Peru (plus a
  6.7 near Carhuamayo); a magnitude 4.1 quake was reported in Myanmar.
- **Also today:** a top Mexican cartel boss on the FBI's 10 most-wanted
  list was captured after a shootout; the FBI is investigating a suspected
  hack of its criminal database; Trump seeks a permanent nuclear deal with
  Iran and met Xi in Shenzhen; Hong Kong's Election Committee voting
  began; Estonia will close its border with Russia; former Brazilian
  president Jair Bolsonaro is in intensive care with an acute bowel
  obstruction.

## How to run it

Render the image (deterministic — every run writes identical bytes):

```sh
python3 compose.py
```

Run the entry program (Node 22; writes `entry.png` to `/output`, or to
`$MAKEFUN_OUTPUT_DIR` when set):

```sh
node main.ts
```

## Files

- `compose.py` — renders `entry.png` deterministically from scratch.
- `entry.png` — the rendered 1024×1024 front page (≤ 1 MiB).
- `main.ts` — entry program: validates the PNG and copies it to the
  output directory.
- `LICENSE` — MIT.
- `.makefun/owner.json` — payout wallet.
