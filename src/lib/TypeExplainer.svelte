<script lang="ts">
  import { TYPE_LABEL, TYPE_DESC, RISING_TYPES, type PriceType } from './types'
  import Sparkline from './Sparkline.svelte'

  const SAMPLE: Record<PriceType, number[]> = {
    steady: [10, 10.4, 10.9, 11.2, 11.8, 12.1, 12.6, 13.2, 13.6, 14.1, 14.7, 15.2],
    plateau: [10, 10.6, 11.8, 13.2, 14.1, 14.4, 14.5, 14.4, 14.5, 14.4, 14.5, 14.4],
    surge: [10, 10.1, 10.2, 10.2, 10.3, 10.4, 10.6, 11, 12, 13.4, 15, 16.8],
    wavy: [10, 13, 9.5, 12.5, 10.5, 14, 11, 15, 12, 16, 13, 17],
    flat: [10, 10.1, 10, 10.15, 10.05, 10.2, 10.1, 10.2, 10.15, 10.25, 10.2, 10.3],
    cheaper: [14, 13.6, 13.7, 13.2, 12.8, 12.9, 12.3, 11.9, 11.6, 11.2, 10.8, 10.5],
  }

  const OTHER_TYPES: PriceType[] = ['flat', 'cheaper']
</script>

<section class="explainer">
  <h2>物價的漲相<br />先看漲、平、跌三種方向</h2>
  <p class="lede">十年來上漲的品項最多，但「怎麼漲」各有面貌——這正是漲相要看的。</p>

  <h3 class="group-title rising">上漲的四種漲相</h3>
  <div class="cols four">
    {#each RISING_TYPES as t (t)}
      <div class="col type-{t}">
        <h3>{TYPE_LABEL[t]}</h3>
        <p>{TYPE_DESC[t]}</p>
        <div class="chart-block">
          <Sparkline data={SAMPLE[t]} width={160} height={70} color="var(--type-color)" strokeWidth={3} />
        </div>
      </div>
    {/each}
  </div>

  <div class="cols two">
    {#each OTHER_TYPES as t (t)}
      <div class="col type-{t}">
        <h3>{TYPE_LABEL[t]}</h3>
        <p>{TYPE_DESC[t]}</p>
        <div class="chart-block">
          <Sparkline data={SAMPLE[t]} width={160} height={70} color="var(--type-color)" strokeWidth={3} />
        </div>
      </div>
    {/each}
  </div>

  <p class="badge-note">⚡＝曾有一波大行情後回落　〰️＝價格劇烈波動</p>
</section>

<style>
  .explainer {
    padding: 3rem 1.5rem 4rem;
    max-width: 1200px;
    margin: 0 auto;
  }

  h2 {
    font-size: clamp(1.4rem, 3vw, 2.1rem);
    font-weight: 800;
    line-height: 1.35;
    margin-bottom: 0.6rem;
  }

  .lede {
    font-size: 0.9rem;
    opacity: 0.75;
    margin-bottom: 2rem;
  }

  .group-title {
    font-size: 0.95rem;
    font-weight: 800;
    margin-bottom: 0.6rem;
  }
  .group-title.rising {
    color: var(--steady);
  }

  .cols {
    display: grid;
    gap: 0;
    border-top: 1px solid var(--line);
    margin-bottom: 2rem;
  }
  .cols.four {
    grid-template-columns: repeat(4, 1fr);
  }
  .cols.two {
    grid-template-columns: repeat(2, 1fr);
    max-width: 600px;
  }

  @media (max-width: 900px) {
    .cols.four {
      grid-template-columns: repeat(2, 1fr);
    }
  }
  @media (max-width: 520px) {
    .cols.four,
    .cols.two {
      grid-template-columns: 1fr;
    }
  }

  .col {
    padding: 1.25rem 1.5rem 1.5rem 1.5rem;
    border-left: 1px solid var(--line);
  }

  .col h3 {
    font-size: 1.05rem;
    font-weight: 800;
    color: var(--type-color);
    margin-bottom: 0.4rem;
  }

  .col p {
    font-size: 0.8rem;
    color: var(--ink);
    opacity: 0.8;
    min-height: 2.4em;
  }

  .chart-block {
    margin-top: 1.5rem;
  }

  .badge-note {
    font-size: 0.78rem;
    opacity: 0.65;
  }
</style>
