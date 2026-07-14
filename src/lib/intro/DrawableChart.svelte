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

  // Fixed y-axis: the 0% baseline (=100) is always at the same pixel across
  // items so no chart hints at its answer by where the flat line sits. Ticks
  // span −100%…+150%; the domain is padded beyond them so lines never clip.
  const yTicks = [
    { v: 250, label: '+150%' },
    { v: 200, label: '+100%' },
    { v: 150, label: '+50%' },
    { v: 100, label: '0' },
    { v: 50, label: '−50%' },
    { v: 0, label: '−100%' },
  ]

  const y = scaleLinear().domain([-12, 262]).range([plotY1, plotY0])

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

  // --- anchor: the real line is shown for 2013 up to the draw-from point
  // (first month of 2014); the user extends the rest, You-Draw-It style. ---
  const drawFromIndex = $derived.by(() => {
    const i = item.periods.findIndex((p) => p.split('-')[0] === '2014')
    return i >= 0 ? i : Math.min(12, item.periods.length - 1)
  })
  const drawFromX = $derived(x(item.periods[drawFromIndex]) ?? plotX0)
  const drawFromY = $derived(y(rebased[drawFromIndex]))

  const lineGen = (data: number[]) =>
    line<number>()
      .x((_, i) => x(item.periods[i]) ?? 0)
      .y((v) => y(v))
      .curve(curveMonotoneX)(data) ?? ''

  const anchorPath = $derived(lineGen(rebased.slice(0, drawFromIndex + 1)))
  const realPath = $derived(lineGen(rebased))

  // one guess vertex per quarter (months 1/4/7/10) across the draw region,
  // plus the final month — the drawn line is these anchors joined, so it stays
  // clean instead of wobbling with hand jitter.
  const quarterIndices = $derived.by(() => {
    const out: number[] = []
    for (let i = drawFromIndex; i < item.periods.length; i++) {
      const m = Number(item.periods[i].split('-')[1])
      if (m === 1 || m === 4 || m === 7 || m === 10) out.push(i)
    }
    const last = item.periods.length - 1
    if (out.length === 0 || out[out.length - 1] !== last) out.push(last)
    if (out[0] !== drawFromIndex) out.unshift(drawFromIndex)
    return out
  })

  // --- sweep capture ---
  let svgEl = $state<SVGSVGElement | null>(null)
  let guessY = $state<(number | null)[]>([])
  let sweptX = $state(0)
  let drawing = $state(false)
  let cursor = $state<{ x: number; y: number } | null>(null)
  let announcedDrawn = false

  // reset whenever the item (hence the quarter layout / anchor) changes
  $effect(() => {
    item.id
    const init: (number | null)[] = Array(quarterIndices.length).fill(null)
    if (init.length) init[0] = drawFromY
    guessY = init
    sweptX = drawFromX
    cursor = null
    announcedDrawn = false
  })

  function toPlot(e: PointerEvent): { x: number; y: number } {
    const rect = svgEl!.getBoundingClientRect()
    const rawX = ((e.clientX - rect.left) / rect.width) * width
    const rawY = ((e.clientY - rect.top) / rect.height) * height
    return {
      x: Math.min(plotX1, Math.max(plotX0, rawX)),
      y: Math.min(plotY1, Math.max(plotY0, rawY)),
    }
  }

  // half the spacing between quarter vertices — the cursor "captures" the
  // nearest column within this tolerance, so a sweep that gets close to the
  // final vertex (which sits on the right edge) still fills it.
  const quarterTol = $derived((plotX1 - plotX0) / Math.max(1, quarterIndices.length - 1) / 2)

  // forward-fill: every quarter the cursor sweeps past (rightward only) takes
  // the cursor's height; moving back left never overwrites — "no backtracking".
  function applySweep(p: { x: number; y: number }) {
    cursor = p
    let changed = false
    const next = guessY.slice()
    // once the cursor is within ~one quarter of the right edge, treat it as
    // reaching the end and fill any remaining trailing quarters — so finishing
    // never requires hitting the last pixel exactly.
    const nearEnd = p.x >= plotX1 - 2 * quarterTol
    quarterIndices.forEach((qi, k) => {
      if (k === 0 || next[k] != null) return // k=0 locked to the anchor end
      const qx = x(item.periods[qi]) ?? 0
      if (qx > sweptX && (nearEnd || qx <= p.x + quarterTol)) {
        next[k] = p.y
        changed = true
      }
    })
    if (p.x > sweptX) sweptX = p.x
    if (changed) guessY = next
  }

  function onPointerDown(e: PointerEvent) {
    if (revealed) return
    drawing = true
    fullpage.navLocked = true
    ;(e.currentTarget as Element).setPointerCapture(e.pointerId)
    applySweep(toPlot(e))
  }
  function onPointerMove(e: PointerEvent) {
    if (!drawing || revealed) return
    applySweep(toPlot(e))
  }
  function endDraw() {
    drawing = false
    fullpage.navLocked = false
  }

  const guessPoints = $derived.by(() => {
    const pts: { x: number; y: number }[] = []
    quarterIndices.forEach((qi, k) => {
      const gy = guessY[k]
      if (gy != null) pts.push({ x: x(item.periods[qi]) ?? 0, y: gy })
    })
    return pts
  })

  const guessPath = $derived.by(() => {
    if (guessPoints.length < 2) return ''
    return (
      line<{ x: number; y: number }>()
        .x((p) => p.x)
        .y((p) => p.y)
        .curve(curveMonotoneX)(guessPoints) ?? ''
    )
  })

  const leadDot = $derived.by(() => {
    if (drawing && cursor) return { x: Math.min(cursor.x, plotX1), y: cursor.y }
    return guessPoints[guessPoints.length - 1] ?? { x: drawFromX, y: drawFromY }
  })

  const reachedEnd = $derived(guessY.length > 0 && guessY.every((v) => v != null))

  $effect(() => {
    if (reachedEnd && !announcedDrawn) {
      announcedDrawn = true
      onDrawn()
    }
  })

  const guessedEndValue = $derived.by(() => {
    const last = guessPoints[guessPoints.length - 1]
    return last ? y.invert(last.y) : null
  })
  const guessedEndPct = $derived(guessedEndValue === null ? null : guessedEndValue - 100)

  // Cognition gap = mean absolute distance between the drawn line and the real
  // line, measured at every drawn quarter (in index points ≈ percentage
  // points), à la Flourish's "off by X, on average".
  const meanAbsError = $derived.by(() => {
    let sum = 0
    let n = 0
    quarterIndices.forEach((qi, k) => {
      if (k === 0) return // anchor is real, not a guess
      const gy = guessY[k]
      if (gy == null) return
      sum += Math.abs(y.invert(gy) - rebased[qi])
      n++
    })
    return n ? sum / n : null
  })

  function surpriseText(): string {
    if (meanAbsError === null) return ''
    const e = meanAbsError
    const n = e.toFixed(1)
    if (e < 5) return `神準！平均只差 ${n} 個百分點`
    if (e < 12) return `👍 很不錯！平均差了 ${n} 個百分點`
    if (e < 25) return `還行，平均差了 ${n} 個百分點`
    return `落差不小，平均差了 ${n} 個百分點`
  }

  // --- draw-on animation for the real line once revealed ---
  let realPathEl = $state<SVGPathElement | null>(null)
  let realPathLength = $state(0)
  $effect(() => {
    if (revealed && realPathEl) realPathLength = realPathEl.getTotalLength()
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

    <!-- real anchor line (2013 → draw-from) -->
    <path d={anchorPath} fill="none" class="anchor-line" />
    <circle cx={drawFromX} cy={drawFromY} r="5" class="origin-dot" />

    {#if guessPath}
      <path d={guessPath} fill="none" class="guess-line" />
    {/if}

    {#if !revealed && guessPoints.length}
      <circle cx={leadDot.x} cy={leadDot.y} r="5" class="lead-dot" />
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
        aria-label="從 2014 往右畫出你猜的走勢"
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
    <p class="hint">從 2014 往右畫出你猜的走勢</p>
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

  .anchor-line {
    stroke: var(--steady);
    stroke-width: 4.5;
    stroke-linecap: round;
    stroke-linejoin: round;
  }

  .origin-dot {
    fill: var(--steady);
  }

  .guess-line {
    stroke: var(--ink);
    stroke-width: 3;
    stroke-linecap: round;
    stroke-linejoin: round;
    stroke-dasharray: 6 6;
    opacity: 0.75;
  }

  .lead-dot {
    fill: var(--ink);
    opacity: 0.85;
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
