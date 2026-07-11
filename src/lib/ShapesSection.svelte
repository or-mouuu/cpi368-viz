<script lang="ts">
  import Sparkline from './Sparkline.svelte'
  import { fullpage } from './fullpage.svelte'
  import { RISING_TYPES, TYPE_LABEL, TYPE_DESC, type CpiItem, type CpiMeta } from './types'
  import { metaYearSpan } from './chartMath'

  let { index, items, meta }: { index: number; items: CpiItem[]; meta: CpiMeta } = $props()
  const active = $derived(fullpage.active === index)

  const years = $derived(metaYearSpan(meta.dataStart, meta.dataEnd))
  const risingCount = $derived(items.filter((it) => RISING_TYPES.includes(it.type)).length)

  const SAMPLE: Record<string, number[]> = {
    surge: [10, 10.1, 10.2, 10.2, 10.3, 10.4, 10.6, 11, 12, 13.4, 15, 16.8],
    accel: [10, 10.3, 10.5, 10.8, 11, 11.3, 11.7, 12.2, 12.9, 13.7, 14.7, 15.9],
    steady: [10, 10.4, 10.9, 11.2, 11.8, 12.1, 12.6, 13.2, 13.6, 14.1, 14.7, 15.2],
    plateau: [10, 10.6, 11.8, 13.2, 14.1, 14.4, 14.5, 14.4, 14.5, 14.4, 14.5, 14.4],
    wavy: [10, 13, 9.5, 12.5, 10.5, 14, 11, 15, 12, 16, 13, 17],
  }

  const EXAMPLES: Record<string, string> = {
    surge: '例：金飾、診所掛號費',
    accel: '例：豬肉、雞蛋、中式早點',
    steady: '例：麵包、牛肉、住宅租金',
    plateau: '例：鮭魚、鮮奶、汽油、香菸',
    wavy: '例：蔥、芹菜、萵苣',
  }

  const CN_NUM = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九']
  const shapeCount = CN_NUM[RISING_TYPES.length] ?? String(RISING_TYPES.length)
</script>

<div class="shapes">
  <h2>「上漲」的{shapeCount}種漲相</h2>
  <p class="lede">{risingCount} 個上漲的品項，依「怎麼漲」分成{shapeCount}種性格</p>
  <div class="cols">
    {#each RISING_TYPES as t, ti (t)}
      <div class="col type-{t}">
        <h3>{TYPE_LABEL[t]}</h3>
        <p>{TYPE_DESC[t](years)}</p>
        <div class="chart">
          <Sparkline
            data={SAMPLE[t]}
            width={190}
            height={95}
            color="var(--type-color)"
            strokeWidth={5.25}
            draw={active}
            drawDuration={1300}
            drawDelay={ti * 220}
          />
          <div class="years"><span>'{meta.dataStart.slice(2, 4)}</span><span>'{meta.dataEnd.slice(2, 4)}</span></div>
        </div>
        <p class="examples">{EXAMPLES[t]}</p>
      </div>
    {/each}
  </div>
</div>

<style>
  .shapes {
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
    text-align: center;
  }

  .lede {
    margin-top: 0.5rem;
    font-size: 0.9rem;
    opacity: 0.7;
    margin-bottom: 2.5rem;
  }

  .cols {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1.6rem;
    max-width: 1240px;
    width: 100%;
  }

  @media (max-width: 1000px) {
    .cols {
      grid-template-columns: repeat(3, 1fr);
      gap: 1rem;
    }
    .lede {
      margin-bottom: 1.2rem;
    }
  }
  @media (max-width: 640px) {
    .cols {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  .col {
    text-align: center;
  }

  h3 {
    font-size: 1.15rem;
    font-weight: 900;
    color: var(--type-color);
    margin-bottom: 0.4rem;
  }

  .col p {
    font-size: 0.8rem;
    opacity: 0.8;
    min-height: 3em;
    max-width: 230px;
    margin: 0 auto;
  }

  .chart {
    margin-top: 1rem;
    display: inline-block;
    border-top: 1px solid var(--line);
    padding-top: 0.7rem;
    max-width: 100%;
  }

  .chart :global(svg) {
    max-width: 100%;
    height: auto;
  }

  .years {
    display: flex;
    justify-content: space-between;
    border-top: 1px solid var(--ink);
    padding-top: 0.3rem;
    font-size: 0.72rem;
    opacity: 0.6;
  }

  .examples {
    margin-top: 0.6rem;
    font-size: 0.75rem !important;
    opacity: 0.6 !important;
    min-height: 0 !important;
  }

  @media (max-width: 560px) {
    .col p {
      min-height: 0;
    }
    .chart :global(svg) {
      height: 56px;
      width: 150px;
    }
  }
</style>
