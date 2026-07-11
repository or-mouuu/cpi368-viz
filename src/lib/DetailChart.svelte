<script lang="ts">
  import { line, curveMonotoneX } from 'd3-shape'
  import { scaleLinear, scalePoint, scaleBand } from 'd3-scale'
  import type { CpiItem } from './types'
  import { rebase, monthlyAverages, startYearLabel } from './chartMath'

  let { item }: { item: CpiItem } = $props()

  let tab = $state<'line' | 'month'>('line')
  let hoverIndex = $state<number | null>(null)
  let svgEl = $state<SVGSVGElement | null>(null)

  const width = 1200
  const height = 520
  const margin = { top: 24, right: 32, bottom: 40, left: 56 }

  const rebased = $derived(rebase(item.series))
  const startYear = $derived(startYearLabel(item.periods))

  // reset hover / tab quirks when switching item
  $effect(() => {
    item.id
    hoverIndex = null
  })

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

  const x = $derived(
    scalePoint()
      .domain(item.periods)
      .range([margin.left, width - margin.right]),
  )

  const y = $derived.by(() => {
    const min = Math.min(...rebased, 100)
    const max = Math.max(...rebased, 100)
    const pad = (max - min) * 0.1 || 5
    return scaleLinear()
      .domain([min - pad, max + pad])
      .range([height - margin.bottom, margin.top])
  })

  const yTicks = $derived.by(() => {
    const [d0, d1] = y.domain()
    const step = (d1 - d0) / 4
    return Array.from({ length: 5 }, (_, i) => Math.round(d0 + step * i))
  })

  const path = $derived.by(() => {
    const gen = line<number>()
      .x((_, i) => x(item.periods[i]) ?? 0)
      .y((v) => y(v))
      .curve(curveMonotoneX)
    return gen(rebased) ?? ''
  })

  const months = $derived(monthlyAverages(item))

  const xMonth = $derived(
    scaleBand<number>()
      .domain(months.map((m) => m.month))
      .range([margin.left, width - margin.right])
      .padding(0.28),
  )

  const yMonth = $derived.by(() => {
    // bars grow from the 100 baseline; anchor the floor at exactly 100 when
    // nothing dips below it, so bars sit flush on the axis instead of
    // floating above a padded-down floor like 97/98
    const vals = months.map((m) => m.avg)
    const dataMin = Math.min(...vals)
    const dataMax = Math.max(...vals, 100)
    const span = Math.max(dataMax - Math.min(dataMin, 100), 1)
    const topPad = span * 0.15
    const domainMax = dataMax + topPad
    const domainMin = dataMin >= 100 ? 100 : dataMin - span * 0.08
    return scaleLinear()
      .domain([domainMin, domainMax])
      .range([height - margin.bottom, margin.top])
  })

  const monthHasDip = $derived(Math.min(...months.map((m) => m.avg)) < 99.9)

  const yMonthTicks = $derived.by(() => {
    const [d0, d1] = yMonth.domain()
    const step = (d1 - d0) / 4
    return Array.from({ length: 5 }, (_, i) => Math.round(d0 + step * i))
  })

  function onPointerMove(e: PointerEvent) {
    if (!svgEl) return
    const rect = svgEl.getBoundingClientRect()
    const px = ((e.clientX - rect.left) / rect.width) * width
    const positions = item.periods.map((p) => x(p) ?? 0)
    let nearest = 0
    let best = Infinity
    positions.forEach((px2, i) => {
      const d = Math.abs(px2 - px)
      if (d < best) {
        best = d
        nearest = i
      }
    })
    hoverIndex = nearest
  }

  function onPointerLeave() {
    hoverIndex = null
  }

  const hoverInfo = $derived.by(() => {
    if (hoverIndex === null) return null
    const period = item.periods[hoverIndex]
    const value = rebased[hoverIndex]
    const change = value - 100
    return { period, value, change, px: x(period) ?? 0, py: y(value) }
  })
</script>

<div class="chart-shell">
  <div class="tabs">
    <button class="tab-btn" class:active={tab === 'line'} onclick={() => (tab = 'line')}>
      {startYear}–{item.periods[item.periods.length - 1].split('-')[0]} 折線圖
    </button>
    <button class="tab-btn" class:active={tab === 'month'} onclick={() => (tab = 'month')}>
      1月–12月 月均直條圖
    </button>
  </div>

  {#if tab === 'line'}
    <svg
      bind:this={svgEl}
      viewBox="0 0 {width} {height}"
      class="chart"
      preserveAspectRatio="xMidYMid meet"
      onpointermove={onPointerMove}
      onpointerleave={onPointerLeave}
      role="img"
    >
      {#each yTicks as t (t)}
        <line x1={margin.left} x2={width - margin.right} y1={y(t)} y2={y(t)} class="gridline" />
        <text x={margin.left - 12} y={y(t)} class="ytick" text-anchor="end" dominant-baseline="middle">{t}</text>
      {/each}

      <line x1={margin.left} x2={width - margin.right} y1={y(100)} y2={y(100)} class="gridline baseline" />
      <text x={width - margin.right + 8} y={y(100)} class="ytick baseline-label" dominant-baseline="middle">100</text>

      <line x1={margin.left} x2={width - margin.right} y1={height - margin.bottom} y2={height - margin.bottom} class="axis" />

      {#each yearTicks as t (t.index)}
        <text x={x(item.periods[t.index])} y={height - margin.bottom + 24} class="xtick" text-anchor="middle">
          {t.label}
        </text>
      {/each}

      <path d={path} fill="none" class="line" stroke="var(--type-color)" stroke-width="3.75" />

      {#if hoverInfo}
        <line x1={hoverInfo.px} x2={hoverInfo.px} y1={margin.top} y2={height - margin.bottom} class="crosshair" />
        <circle cx={hoverInfo.px} cy={hoverInfo.py} r="5.5" class="hover-dot" fill="var(--type-color)" />
      {/if}
    </svg>

    {#if hoverInfo}
      <div
        class="tooltip"
        style="left:{(hoverInfo.px / width) * 100}%; top:{(hoverInfo.py / height) * 100}%"
      >
        <div class="tt-period">{hoverInfo.period}</div>
        <div class="tt-value">指數 {hoverInfo.value.toFixed(1)}</div>
        <div class="tt-change" class:pos={hoverInfo.change >= 0} class:neg={hoverInfo.change < 0}>
          較{startYear}年　{hoverInfo.change >= 0 ? '+' : ''}{hoverInfo.change.toFixed(1)}%
        </div>
      </div>
    {/if}

    <p class="note">以起始年（{startYear}）平均 = 100 重新計算，方便跨品項比較；滑過折線可看該月較起始年的變動</p>
  {:else}
    <svg viewBox="0 0 {width} {height}" class="chart" preserveAspectRatio="xMidYMid meet" role="img">
      {#each yMonthTicks as t (t)}
        <line x1={margin.left} x2={width - margin.right} y1={yMonth(t)} y2={yMonth(t)} class="gridline" />
        <text x={margin.left - 12} y={yMonth(t)} class="ytick" text-anchor="end" dominant-baseline="middle">{t}</text>
      {/each}

      {#if monthHasDip}
        <line x1={margin.left} x2={width - margin.right} y1={yMonth(100)} y2={yMonth(100)} class="gridline baseline" />
        <text x={width - margin.right + 8} y={yMonth(100)} class="ytick baseline-label" dominant-baseline="middle">100</text>
      {/if}

      <line x1={margin.left} x2={width - margin.right} y1={height - margin.bottom} y2={height - margin.bottom} class="axis" />

      {#each months as m (m.month)}
        {@const bx = xMonth(m.month) ?? 0}
        {@const bw = xMonth.bandwidth()}
        {@const by = yMonth(m.avg)}
        <rect
          x={bx}
          y={Math.min(by, yMonth(100))}
          width={bw}
          height={Math.abs(yMonth(100) - by)}
          class="bar"
          class:max={m.isMax}
          class:min={m.isMin}
          fill="var(--type-color)"
        />
        <text x={bx + bw / 2} y={height - margin.bottom + 24} class="xtick" text-anchor="middle">{m.month}月</text>
        {#if m.isMax || m.isMin}
          <text x={bx + bw / 2} y={by + (m.avg >= 100 ? -8 : 16)} class="bar-label" text-anchor="middle">
            {m.isMax ? '最高' : '最低'}
          </text>
        {/if}
      {/each}
    </svg>
    <p class="note">以起始年（{startYear}）平均 = 100 重新計算後，各月在十年間的平均水準——看得出哪幾個月通常比較貴</p>
  {/if}
</div>

<style>
  .chart-shell {
    display: flex;
    flex-direction: column;
    height: 100%;
    position: relative;
  }

  .tabs {
    flex: 0 0 auto;
    display: flex;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }

  .tab-btn {
    border: 1px solid var(--line);
    background: var(--bg);
    padding: 0.4rem 0.9rem;
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--ink);
    border-radius: 999px;
  }

  .tab-btn.active {
    background: var(--ink);
    color: var(--bg);
    border-color: var(--ink);
  }

  .chart {
    width: 100%;
    flex: 1 1 auto;
    min-height: 0;
    display: block;
  }

  .gridline {
    stroke: var(--line-soft);
    stroke-width: 1;
  }
  .gridline.baseline {
    stroke: var(--ink);
    stroke-width: 1.25;
    stroke-dasharray: 4 3;
  }
  .baseline-label {
    font-weight: 700;
  }
  .axis {
    stroke: var(--ink);
    stroke-width: 1;
  }
  .ytick,
  .xtick {
    font-size: 15px;
    fill: var(--ink);
    font-family: var(--font-numeric);
  }
  .line {
    stroke-linecap: round;
    stroke-linejoin: round;
  }

  .crosshair {
    stroke: var(--ink);
    stroke-width: 1;
    stroke-dasharray: 3 3;
    opacity: 0.5;
    pointer-events: none;
  }
  .hover-dot {
    stroke: var(--bg);
    stroke-width: 2;
    pointer-events: none;
  }

  .tooltip {
    position: absolute;
    transform: translate(-50%, -115%);
    background: var(--ink);
    color: var(--bg);
    padding: 0.5rem 0.7rem;
    border-radius: 4px;
    font-size: 0.78rem;
    pointer-events: none;
    white-space: nowrap;
    font-family: var(--font-numeric);
  }
  .tt-period {
    opacity: 0.7;
    margin-bottom: 0.1rem;
  }
  .tt-change.pos {
    color: #ff9d70;
  }
  .tt-change.neg {
    color: #8fc2d6;
  }

  .bar {
    opacity: 0.72;
  }
  .bar.max,
  .bar.min {
    opacity: 1;
  }
  .bar-label {
    font-size: 13px;
    font-weight: 700;
    fill: var(--ink);
    font-family: var(--font-body);
  }

  .note {
    flex: 0 0 auto;
    margin-top: 0.4rem;
    font-size: 0.75rem;
    color: var(--line);
  }
</style>
