<script lang="ts">
  import Sparkline from './Sparkline.svelte'
  import { fullpage } from './fullpage.svelte'
  import { RISING_TYPES, type CpiItem, type CpiMeta } from './types'
  import { metaYearSpan } from './chartMath'

  let { index, items, meta }: { index: number; items: CpiItem[]; meta: CpiMeta } = $props()
  const active = $derived(fullpage.active === index)
  const years = $derived(metaYearSpan(meta.dataStart, meta.dataEnd))

  const risingCount = $derived(items.filter((it) => RISING_TYPES.includes(it.type)).length)
  const flatCount = $derived(items.filter((it) => it.type === 'flat').length)
  const cheaperCount = $derived(items.filter((it) => it.type === 'cheaper').length)

  const groups = $derived([
    {
      key: 'up',
      title: '上漲',
      color: 'var(--steady)',
      desc: `${years}年漲逾15%，共 ${risingCount} 項——但漲法各有面貌，下一頁細看`,
      sample: [10, 10.5, 11, 11.6, 12.1, 12.8, 13.3, 14, 14.6, 15.4, 16, 16.8],
    },
    {
      key: 'flat',
      title: '沒什麼漲',
      color: 'var(--flat)',
      desc: `${years}年變動不到15%，幾乎凍住，共 ${flatCount} 項`,
      sample: [10, 10.1, 9.95, 10.15, 10.05, 10.2, 10.1, 10.05, 10.2, 10.1, 10.25, 10.2],
    },
    {
      key: 'down',
      title: '越來越俗',
      color: 'var(--cheaper)',
      desc: `比${years}年前更便宜，共 ${cheaperCount} 項`,
      sample: [14, 13.6, 13.7, 13.2, 12.8, 12.9, 12.3, 11.9, 11.6, 11.2, 10.8, 10.5],
    },
  ])
</script>

<div class="directions">
  <h2>物價的漲相，先看三種方向</h2>
  <div class="cols">
    {#each groups as g, gi (g.key)}
      <div class="col">
        <h3 style="color:{g.color}">{g.title}</h3>
        <p>{g.desc}</p>
        <div class="chart">
          <span class="axis-label">H</span>
          <Sparkline
            data={g.sample}
            width={220}
            height={110}
            color={g.color}
            strokeWidth={5.25}
            draw={active}
            drawDuration={1400}
            drawDelay={gi * 250}
          />
          <div class="years"><span>'{meta.dataStart.slice(2, 4)}</span><span>'{meta.dataEnd.slice(2, 4)}</span></div>
        </div>
      </div>
    {/each}
  </div>
</div>

<style>
  .directions {
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3.5rem 1.5rem 2rem;
  }

  h2 {
    font-size: clamp(1.4rem, 3vw, 2rem);
    font-weight: 900;
    margin-bottom: 3rem;
    text-align: center;
  }

  .cols {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 3.5rem;
    max-width: 1080px;
    width: 100%;
  }

  @media (max-width: 800px) {
    .cols {
      gap: 1.2rem;
    }
    h2 {
      margin-bottom: 1.5rem;
    }
  }
  @media (max-width: 560px) {
    .cols {
      grid-template-columns: 1fr;
      gap: 0.8rem;
    }
  }

  .col {
    text-align: center;
  }

  h3 {
    font-size: 1.35rem;
    font-weight: 900;
    margin-bottom: 0.5rem;
  }

  .col p {
    font-size: 0.85rem;
    opacity: 0.8;
    min-height: 3em;
    max-width: 260px;
    margin: 0 auto;
  }

  .chart {
    margin-top: 1.5rem;
    display: inline-block;
    position: relative;
    border-top: 1px solid var(--line);
    padding-top: 0.8rem;
    max-width: 100%;
  }

  .chart :global(svg) {
    max-width: 100%;
    height: auto;
  }

  .axis-label {
    position: absolute;
    top: 0.2rem;
    left: -1rem;
    font-size: 0.7rem;
    opacity: 0.5;
  }

  .years {
    display: flex;
    justify-content: space-between;
    border-top: 1px solid var(--ink);
    padding-top: 0.3rem;
    font-size: 0.75rem;
    opacity: 0.6;
  }

  @media (max-width: 560px) {
    .col p {
      min-height: 0;
    }
    .chart :global(svg) {
      height: 60px;
      width: 180px;
    }
  }
</style>
