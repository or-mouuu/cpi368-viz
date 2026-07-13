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
  const margin = { top: 24, right: 20, bottom: 36, left: 20 }
  const plotX0 = margin.left
  const plotX1 = width - margin.right
  const plotY0 = margin.top
  const plotY1 = height - margin.bottom

  const rebased = $derived(rebase(item.series))

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

  const y = $derived.by(() => {
    const min = Math.min(...rebased, 100)
    const max = Math.max(...rebased, 100)
    const span = max - min || 10
    return scaleLinear()
      .domain([min - span * 0.6, max + span * 0.6])
      .range([plotY1, plotY0])
  })

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

  const guessPath = $derived.by(() => {
    if (points.length < 2) return ''
    return points.map((p, i) => `${i === 0 ? 'M' : 'L'}${p.x},${p.y}`).join(' ')
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
    if (points.length === 0) return null
    let best = points[0]
    for (const p of points) if (p.x > best.x) best = p
    return y.invert(best.y)
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
    <line x1={plotX0} x2={plotX1} y1={y(100)} y2={y(100)} class="gridline baseline" />
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

  .xtick {
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
