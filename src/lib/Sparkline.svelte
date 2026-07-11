<script lang="ts">
  import { line, curveBasis } from 'd3-shape'
  import { scaleLinear } from 'd3-scale'

  let {
    data,
    width = 140,
    height = 44,
    color = 'currentColor',
    strokeWidth = 2,
    draw = false,
    drawDuration = 1200,
    drawDelay = 0,
  }: {
    data: number[]
    width?: number
    height?: number
    color?: string
    strokeWidth?: number
    /** when flipped to true, the line draws itself from left to right */
    draw?: boolean
    drawDuration?: number
    drawDelay?: number
  } = $props()

  let pathEl = $state<SVGPathElement | null>(null)
  let pathLength = $state(0)

  const path = $derived.by(() => {
    if (data.length < 2) return ''
    const x = scaleLinear().domain([0, data.length - 1]).range([2, width - 2])
    const [min, max] = [Math.min(...data), Math.max(...data)]
    const pad = (max - min) * 0.1 || 1
    const y = scaleLinear().domain([min - pad, max + pad]).range([height - 4, 4])
    const gen = line<number>()
      .x((_, i) => x(i))
      .y((v) => y(v))
      .curve(curveBasis)
    return gen(data) ?? ''
  })

  $effect(() => {
    if (pathEl && path) pathLength = pathEl.getTotalLength()
  })
</script>

<svg viewBox="0 0 {width} {height}" {width} {height} preserveAspectRatio="none" class="spark">
  <path
    bind:this={pathEl}
    d={path}
    fill="none"
    stroke={color}
    stroke-width={strokeWidth}
    stroke-linecap="round"
    stroke-linejoin="round"
    class:drawing={draw && pathLength > 0}
    style={draw && pathLength > 0
      ? `--len:${pathLength}; --dur:${drawDuration}ms; --delay:${drawDelay}ms`
      : ''}
  />
</svg>

<style>
  .spark {
    display: block;
    overflow: visible;
  }

  .drawing {
    stroke-dasharray: var(--len);
    stroke-dashoffset: var(--len);
    animation: draw var(--dur) ease-out var(--delay) forwards;
  }

  @keyframes draw {
    to {
      stroke-dashoffset: 0;
    }
  }
</style>
