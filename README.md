# 流光 · Fleeting Light

A playable chaotic reconstructive spectrometer, in one HTML file.

> 流光容易把人抛。
>
> *Fleeting light casts us aside so easily.* — Jiang Jie, 13th c.

In Chinese, 流光 fuses light and time into a single word. That is not a
metaphor here: what this game asks you to shape is literally the distribution
of light over time.

**Play it: [www.changyanzhu.com](https://www.changyanzhu.com)** — or clone this
repository and open `index.html`. No build step, no dependencies, no server.

---

## What it is

You place circular scatterers inside a leaky rectangular cavity. A handful of
photons are launched from the left wall; the detector is the entire right wall.
Your goal is not to get *more* light out — it is to make the light arrive
**spread out in time**.

That is the whole physics of a reconstructive spectrometer, compressed into a
game rule.

## The mapping to the physics

A reconstructive spectrometer does not disperse light with a prism or a
grating. It throws light into a messy cavity, lets each wavelength come out
with its own interference pattern, and inverts that back into a spectrum.

Two neighbouring wavelengths are distinguishable only because they accumulate
different phase along the same geometric path:

    Δφ = 2πL·Δλ/λ²

The longer the path `L`, the larger the phase difference a given `Δλ` is
amplified into. **Resolution comes from path length, not from intensity.**

A single path is worthless — it contributes one phase and carries no wavelength
information at all. What matters is many paths of many different lengths,
superposed. Their lengths (equivalently, how long a photon lingers in the
cavity) form a distribution `p(t)`: the **dwell-time statistics**. The spectral
correlation is exactly its Fourier transform:

    C(Δν) = |FT{p(t)}|²

The wider `p(t)` spreads, the narrower `C` becomes, and the smaller the
resolvable `δλ`. Designing a spectrometer *is* designing the shape of `p(t)`.

So the game says:

| In the game | In the physics |
|---|---|
| one photon | one sample of `p(t)` |
| a level's N photons | you may describe the whole distribution with N samples |
| the detector's N layers | the ideal distribution cut into N equal-probability blocks |
| a layer's time window | that block's span on the time axis — narrow and crowded early, progressively wider later, because a leaky cavity's ideal `p(t)` decays exponentially |
| stripping a layer | a photon arriving inside that window |
| a window closing empty | your empirical distribution has a hole there → the run fails on the spot |
| all layers stripped | the N samples genuinely covered the target distribution → you win |
| the `δλ` on the victory screen | **inferred** from your own N arrival times: feed their path lengths into `C(Δν)` and take the half-width |

Nothing above is a difficulty knob. The layer count is `N`, the window edges
are quantiles of the exponential, and the resolution is measured from what you
actually built. Rearrange the scatterers and every number moves with you.

## The thing worth finding out for yourself

Press **Regular array**. It looks professional — symmetric, evenly spaced,
meticulous. It almost always loses to a handful of circles dropped by hand.

Symmetry collapses many optical paths onto the same length. `p(t)` falls into a
few spikes, the spread is gone, and most detector channels receive nothing at
all. Chaos is not a side effect of this scheme; **it is the working principle.**

## What this game does *not* do

It is worth being precise about the boundary, because it is easy to overclaim.

The only theory in here is the spectral correlation `C(Δν) = |FT{p(t)}|²`. What
the game demonstrates is one thing: **how inverse design reshapes the
distribution of optical path lengths.** That is a real and central mechanism,
but it is not the whole story, and the game is not a design tool.

The paper below, which inspired the game, treats the fuller problem: the
reconstruction error is governed by the Fisher information, and its bound
`Tr[G⁺]` decomposes into a spectral correlation length and a mean
transmittance — two quantities that trade off against each other, and that
together decide when super-resolution below the correlation-length limit is
achievable. None of that machinery is implemented here.

So: **for how a reconstructive spectrometer should actually be optimally
designed, the paper is the authority. This game is one intuitive facet it
inspired.**

## Repository layout

```
index.html                    the whole game — open it in a browser
LICENSE                       terms, in plain words
LICENSE.cc-by-nc-nd-4.0.txt   verbatim CC BY-NC-ND 4.0 legal code
CITATION.cff                  machine-readable citation (GitHub & Zenodo read this)
.zenodo.json                  Zenodo deposition metadata
tools/validate.py             structural self-check for the single-file page
```

There is no build system on purpose: everything ships as source, so anyone who
opens the page can read exactly how each rule is computed. `tools/validate.py`
is the safety net that replaces a compiler — it checks bracket balance, id
uniqueness, undefined `getElementById` references, i18n key alignment between
the English and Chinese dictionaries, and tag closure.

```sh
python3 tools/validate.py index.html
```

## Citation

If you use or refer to this game, please cite the software itself. The paper
that inspired it — and which remains the reference for the underlying theory —
is:

> C. Zhu, H. Lo, J. Yu, Q. J. Wang, and Y. D. Chong,
> *Resolution and Robustness Bounds for Reconstructive Spectrometers*,
> **Phys. Rev. Lett. 137, 123802 (2026)**.
> [doi:10.1103/yffp-wgsh](https://doi.org/10.1103/yffp-wgsh) ·
> [arXiv:2512.20415](https://arxiv.org/abs/2512.20415)

## Licence

Copyright © 2026 Changyan Zhu. Released under
[CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) —
share it with attribution; no commercial use and no derivative works without
written permission. See [`LICENSE`](LICENSE) for the details and for what the
licence deliberately does *not* cover.

Commercial licensing, classroom packages and bespoke versions:
**changyan.zhu@ntu.edu.sg**

---

## 中文简介

一台可以玩的混沌重建式光谱仪，全部装在一个 HTML 文件里。

名字取自「流光容易把人抛」。中文把光和时间揉进了同一个词里，而这个游戏要你
亲手塑造的，恰好就是光在时间上的分布 —— 这一次不是比喻。

你在一个会漏光的矩形腔里摆放圆形散射体，让光子从左壁射入、整面右壁作为探测器。
目标不是让更多的光出来，而是让光**在时间上尽量散开** —— 这就是重建式光谱仪的
全部物理，被压成了一条游戏规则。

对应关系是严格的，不是装饰：一个光子就是对 dwell time 分布 `p(t)` 的一次抽样；
探测器的 N 层就是把理想分布切成 N 个等概率区块，每层守一个时间窗；剥掉一层就是
有光子落进那个窗；某个窗关闭时还空着，说明你的经验分布在那一段是空的，任务当场
失败；通关画面上那个 `δλ`，是拿你自己这 N 个光子的实际光程代进
`C(Δν) = |FT{p(t)}|²` 取半宽算出来的，不是预设的难度指标。

值得自己去撞一次的地方：点「整齐阵列」。它看起来专业、对称、一丝不苟，却几乎
总是输给随手摆的一堆乱圆 —— 对称让大量光路退化成相同的长度，`p(t)` 塌成几根
尖峰。混沌不是这个方案的副作用，它就是工作原理本身。

边界也要说清楚：这里用到的理论只有谱关联函数 `C(Δν) = |FT{p(t)}|²`，演示的是
逆向设计如何改变**光程差的分布**，并没有实现论文真正的机制 —— 重建误差由 Fisher
信息支配，其下界 `Tr[G⁺]` 可以分解成谱关联长度与平均透过率两部分，二者之间存在
取舍。**重建式光谱仪究竟该如何最优地设计，以论文为准；这个游戏只是它启发出来的
一个直观侧面。**

版权归 Changyan Zhu 所有，以 CC BY-NC-ND 4.0 授权：可以署名转载，禁止商用和
改编。商业授权、课堂使用、定制版本请来信 **changyan.zhu@ntu.edu.sg**。
