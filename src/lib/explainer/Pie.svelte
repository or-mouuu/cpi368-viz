<script lang="ts">
  import { tweened } from 'svelte/motion'
  import { cubicOut } from 'svelte/easing'

  let {
    fraction,
    size = 300,
    active = true,
    muted = false,
    sliceLabel = '',
  }: {
    /** 0..1 share of the orange slice, drawn counterclockwise from 12 o'clock */
    fraction: number
    size?: number
    /** when false the pie holds at 0 so it can sweep in on activation */
    active?: boolean
    /** desaturated palette for de-emphasized pies */
    muted?: boolean
    sliceLabel?: string
  } = $props()

  const frac = tweened(0, { duration: 900, easing: cubicOut })

  $effect(() => {
    frac.set(active ? fraction : 0)
  })

  const r = 100
  const c = 105 // small padding inside viewBox

  const slicePath = $derived.by(() => {
    const f = Math.min(0.9999, Math.max(0.0001, $frac))
    const theta = f * Math.PI * 2
    const ex = c - r * Math.sin(theta)
    const ey = c - r * Math.cos(theta)
    const laf = theta > Math.PI ? 1 : 0
    return `M ${c} ${c} L ${c} ${c - r} A ${r} ${r} 0 ${laf} 0 ${ex} ${ey} Z`
  })

  // label sits along the slice's bisector; when the slice is too thin to
  // hold it, it moves just outside the rim and takes the accent color
  const labelOutside = $derived($frac < 0.16)
  const labelPos = $derived.by(() => {
    const theta = ($frac * Math.PI * 2) / 2
    const lr = labelOutside ? r * 1.28 : r * 0.58
    return { x: c - lr * Math.sin(theta), y: c - lr * Math.cos(theta) }
  })
</script>

<svg viewBox="-30 -30 270 270" width={size} height={size} class="pie" class:muted>
  <circle cx={c} cy={c} r={r} class="base" />
  <path d={slicePath} class="slice" />
  {#if sliceLabel}
    <text
      x={labelPos.x}
      y={labelPos.y}
      class="slice-label"
      class:outside={labelOutside}
      text-anchor="middle"
      dominant-baseline="middle"
    >
      {#each sliceLabel.split('\n') as ln, i (i)}
        <tspan x={labelPos.x} dy={i === 0 ? '-0.2em' : '1.15em'}>{ln}</tspan>
      {/each}
    </text>
  {/if}
</svg>

<style>
  .pie {
    display: block;
    max-width: 100%;
    height: auto;
  }

  .base {
    fill: var(--ink);
    transition: fill 0.5s ease;
  }

  .slice {
    fill: var(--steady);
    transition: fill 0.5s ease;
  }

  .pie.muted .base {
    fill: #c9c3b2;
  }

  .pie.muted .slice {
    fill: #f2cdb8;
  }

  .slice-label {
    font-family: var(--font-body);
    font-size: 17px;
    font-weight: 900;
    fill: #fff;
    transition: fill 0.4s ease;
  }

  .slice-label.outside {
    fill: var(--steady);
  }

  .pie.muted .slice-label {
    fill: rgba(23, 20, 15, 0.35);
  }
</style>
