<script lang="ts">
  import { scaleLinear, scalePoint } from 'd3-scale'
  import { line, curveMonotoneX } from 'd3-shape'
  import type { CpiItem } from '../types'
  import { rebase } from '../chartMath'
  import { fullpage } from '../fullpage.svelte'

  let {
    item,
    revealed,
    onDrawn,
  }: { item: CpiItem; revealed: boolean; onDrawn: () => void } = $props()

  const width = 900
  const height = 420
  const margin = { top: 24, right: 20, bottom: 36, left: 52 }
  const plotX0 = margin.left
  const plotX1 = width - margin.right
  const plotY0 = margin.top
  const plotY1 = height - margin.bottom

  const rebased = $derived(rebase(item.series))

  // Fixed y-axis: −50% (=50) at the bottom, +100% (=200) at the top, with the
  // 0% baseline (=100) always at the same place regardless of the item — so no
  // item's chart hints at its answer by where the flat line sits.
  const yTicks = [
    { v: 200, label: '+100%' },
    { v: 150, label: '+50%' },
    { v: 100, label: '0' },
    { v: 50, label: '−50%' },
  ]

  const yearTicks = $derived.by(() => {
    const seen = new Set<string>()
    const ticks: { index: number; label: string }[] = []
    item.periods.forEach((p, i) => {
      const year = p.split('-')[0]
      if (!seen.has(year)) {
        seen.add(year)
        ticks.push({ index: i, label: year })
      }
    })
    return ticks
  })

  const x = $derived(scalePoint().domain(item.periods).range([plotX0, plotX1]))

  // Domain is padded a little beyond the labelled −50%…+100% ticks so real
  // lines that dip below −50% (e.g. 行動電話 ≈ −59%) aren't clipped; the pad is
  // fixed for every item, so 0% (=100) stays at the same pixel across items.
  const y = scaleLinear().domain([35, 210]).range([plotY1, plotY0])

  const realPath = $derived.by(() => {
    const gen = line<number>()
      .x((_, i) => x(item.periods[i]) ?? 0)
      .y((v) => y(v))
      .curve(curveMonotoneX)
    return gen(rebased) ?? ''
  })

  // --- hand-drawn guess capture ---
  let svgEl = $state<SVGSVGElement | null>(null)
  let points = $state<{ x: number; y: number }[]>([])
  let drawing = $state(false)
  let announcedDrawn = false

  function toPlot(e: PointerEvent): { x: number; y: number } {
    const rect = svgEl!.getBoundingClientRect()
    const rawX = ((e.clientX - rect.left) / rect.width) * width
    const rawY = ((e.clientY - rect.top) / rect.height) * height
    return {
      x: Math.min(plotX1, Math.max(plotX0, rawX)),
      y: Math.min(plotY1, Math.max(plotY0, rawY)),
    }
  }

  function onPointerDown(e: PointerEvent) {
    if (revealed) return
    drawing = true
    points = [toPlot(e)]
    fullpage.navLocked = true
    ;(e.currentTarget as Element).setPointerCapture(e.pointerId)
  }

  function onPointerMove(e: PointerEvent) {
    if (!drawing || revealed) return
    points.push(toPlot(e))
  }

  function endDraw() {
    drawing = false
    fullpage.navLocked = false
  }

  // The user draws freehand, but the committed guess is resampled to one point
  // per year (plus the final month) — the line the user sees is these anchors
  // joined, so it stays clean and doesn't wobble with hand jitter.
  const sampleIndices = $derived.by(() => {
    const idx = yearTicks.map((t) => t.index)
    const last = item.periods.length - 1
    if (!idx.includes(last)) idx.push(last)
    return idx
  })

  const sampledGuess = $derived.by(() => {
    if (points.length < 2) return [] as { x: number; y: number }[]
    const maxX = Math.max(...points.map((p) => p.x))
    const out: { x: number; y: number }[] = []
    for (const i of sampleIndices) {
      const xp = x(item.periods[i]) ?? 0
      if (xp > maxX + 2) continue // year not drawn yet
      let best = points[0]
      let bestD = Infinity
      for (const p of points) {
        const d = Math.abs(p.x - xp)
        if (d < bestD) {
          bestD = d
          best = p
        }
      }
      out.push({ x: xp, y: best.y })
    }
    return out
  })

  const guessPath = $derived.by(() => {
    if (sampledGuess.length < 2) return ''
    const gen = line<{ x: number; y: number }>()
      .x((p) => p.x)
      .y((p) => p.y)
      .curve(curveMonotoneX)
    return gen(sampledGuess) ?? ''
  })

  const coverage = $derived.by(() => {
    if (points.length === 0) return 0
    let minX = Infinity
    let maxX = -Infinity
    for (const p of points) {
      if (p.x < minX) minX = p.x
      if (p.x > maxX) maxX = p.x
    }
    return (maxX - minX) / (plotX1 - plotX0)
  })

  const enoughCoverage = $derived(coverage >= 0.9)

  $effect(() => {
    if (enoughCoverage && !announcedDrawn) {
      announcedDrawn = true
      onDrawn()
    }
  })

  const guessedEndValue = $derived.by(() => {
    if (sampledGuess.length === 0) return null
    return y.invert(sampledGuess[sampledGuess.length - 1].y)
  })

  const guessedEndPct = $derived(guessedEndValue === null ? null : guessedEndValue - 100)

  function surpriseText(): string {
    if (guessedEndPct === null) return ''
    const diff = Math.abs(guessedEndPct - item.change10y)
    if (diff < 5) return '你猜得很準！'
    if (guessedEndPct > item.change10y) return `其實沒你想的誇張，實際只漲了 ${item.change10y}%`
    return `比你想的還兇，實際漲了 ${item.change10y}%`
  }

  // --- draw-on animation for the real line once revealed ---
  let realPathEl = $state<SVGPathElement | null>(null)
  let realPathLength = $state(0)

  $effect(() => {
    if (revealed && realPathEl) {
      realPathLength = realPathEl.getTotalLength()
    }
  })
</script>

<div class="drawable-chart">
  <svg
    bind:this={svgEl}
    viewBox="0 0 {width} {height}"
    class="chart"
    preserveAspectRatio="xMidYMid meet"
    role="img"
  >
    {#each yTicks as t (t.v)}
      <line x1={plotX0} x2={plotX1} y1={y(t.v)} y2={y(t.v)} class="gridline" class:baseline={t.v === 100} />
      <text x={plotX0 - 8} y={y(t.v)} class="ytick" text-anchor="end" dominant-baseline="middle">{t.label}</text>
    {/each}
    <line x1={plotX0} x2={plotX1} y1={plotY1} y2={plotY1} class="axis" />

    {#each yearTicks as t (t.index)}
      <text x={x(item.periods[t.index])} y={plotY1 + 22} class="xtick" text-anchor="middle">
        {t.label}
      </text>
    {/each}

    {#if guessPath}
      <path d={guessPath} fill="none" class="guess-line" />
    {/if}

    {#if revealed}
      <path
        bind:this={realPathEl}
        d={realPath}
        fill="none"
        class="real-line"
        class:drawing={realPathLength > 0}
        style={realPathLength > 0 ? `--len:${realPathLength}; --dur:1400ms;` : ''}
      />
    {/if}

    {#if !revealed}
      <rect
        x={plotX0}
        y={plotY0}
        width={plotX1 - plotX0}
        height={plotY1 - plotY0}
        class="capture"
        role="slider"
        aria-label="手繪你猜測的走勢"
        aria-valuenow={guessedEndPct ?? 0}
        tabindex="0"
        onpointerdown={onPointerDown}
        onpointermove={onPointerMove}
        onpointerup={endDraw}
        onpointercancel={endDraw}
      />
    {/if}
  </svg>

  {#if revealed}
    <p class="surprise">{surpriseText()}</p>
  {:else}
    <p class="hint">用手指或滑鼠，從左到右畫出你猜的走勢</p>
  {/if}
</div>

<style>
  .drawable-chart {
    width: 100%;
  }

  .chart {
    width: 100%;
    height: auto;
    display: block;
  }

  .gridline {
    stroke: var(--line);
    stroke-width: 1;
    opacity: 0.35;
  }

  .gridline.baseline {
    stroke: var(--ink);
    stroke-width: 1.25;
    stroke-dasharray: 4 3;
    opacity: 0.5;
  }

  .axis {
    stroke: var(--ink);
    stroke-width: 1;
    opacity: 0.6;
  }

  .xtick,
  .ytick {
    font-size: 15px;
    fill: var(--ink);
    font-family: var(--font-numeric);
    opacity: 0.6;
  }

  .guess-line {
    stroke: var(--ink);
    stroke-width: 3;
    stroke-linecap: round;
    stroke-linejoin: round;
    stroke-dasharray: 6 6;
    opacity: 0.75;
  }

  .real-line {
    stroke: var(--steady);
    stroke-width: 4.5;
    stroke-linecap: round;
    stroke-linejoin: round;
  }

  .real-line.drawing {
    stroke-dasharray: var(--len);
    stroke-dashoffset: var(--len);
    animation: draw-on var(--dur) ease-out forwards;
  }

  @keyframes draw-on {
    to {
      stroke-dashoffset: 0;
    }
  }

  .capture {
    fill: transparent;
    cursor: crosshair;
    touch-action: none;
  }

  .hint,
  .surprise {
    margin-top: 0.8rem;
    text-align: center;
    font-size: 0.85rem;
  }

  .hint {
    opacity: 0.6;
  }

  .surprise {
    font-weight: 800;
    color: var(--steady);
    font-size: 1rem;
  }
</style>
