<script lang="ts">
  import { line, curveMonotoneX } from 'd3-shape'
  import { scaleLinear, scalePoint } from 'd3-scale'
  import type { CpiItem } from './types'

  let { item }: { item: CpiItem } = $props()

  const width = 820
  const height = 360
  const margin = { top: 16, right: 24, bottom: 28, left: 44 }

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
    const min = Math.min(...item.series)
    const max = Math.max(...item.series)
    const pad = (max - min) * 0.08 || 1
    return scaleLinear()
      .domain([min - pad, max + pad])
      .range([height - margin.bottom, margin.top])
  })

  const yTicks = $derived.by(() => {
    const [d0, d1] = y.domain()
    const step = (d1 - d0) / 4
    return Array.from({ length: 5 }, (_, i) => Math.round((d0 + step * i) * 10) / 10)
  })

  const path = $derived.by(() => {
    const gen = line<number>()
      .x((_, i) => x(item.periods[i]) ?? 0)
      .y((v) => y(v))
      .curve(curveMonotoneX)
    return gen(item.series) ?? ''
  })
</script>

<svg viewBox="0 0 {width} {height}" class="chart" preserveAspectRatio="xMidYMid meet">
  {#each yTicks as t (t)}
    <line x1={margin.left} x2={width - margin.right} y1={y(t)} y2={y(t)} class="gridline" />
    <text x={margin.left - 10} y={y(t)} class="ytick" text-anchor="end" dominant-baseline="middle">{t}</text>
  {/each}

  <line
    x1={margin.left}
    x2={width - margin.right}
    y1={height - margin.bottom}
    y2={height - margin.bottom}
    class="axis"
  />

  {#each yearTicks as t (t.index)}
    <text x={x(item.periods[t.index])} y={height - margin.bottom + 18} class="xtick" text-anchor="middle">
      {t.label}
    </text>
  {/each}

  <path d={path} fill="none" class="line type-{item.type}" stroke="var(--type-color)" stroke-width="2.5" />
</svg>

<style>
  .chart {
    width: 100%;
    height: auto;
    display: block;
  }
  .gridline {
    stroke: var(--line-soft);
    stroke-width: 1;
  }
  .axis {
    stroke: var(--ink);
    stroke-width: 1;
  }
  .ytick,
  .xtick {
    font-size: 12px;
    fill: var(--ink);
    font-family: var(--font-body);
  }
  .line {
    stroke-linecap: round;
    stroke-linejoin: round;
  }
</style>
