<script lang="ts">
  import { line, curveBasis } from 'd3-shape'
  import { scaleLinear } from 'd3-scale'

  let {
    data,
    width = 140,
    height = 44,
    color = 'currentColor',
    strokeWidth = 2,
  }: {
    data: number[]
    width?: number
    height?: number
    color?: string
    strokeWidth?: number
  } = $props()

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
</script>

<svg viewBox="0 0 {width} {height}" {width} {height} preserveAspectRatio="none" class="spark">
  <path d={path} fill="none" stroke={color} stroke-width={strokeWidth} stroke-linecap="round" stroke-linejoin="round" />
</svg>

<style>
  .spark {
    display: block;
    overflow: visible;
  }
</style>
