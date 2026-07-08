<script lang="ts">
  import { TYPE_ORDER, TYPE_LABEL, TYPE_DESC, type PriceType } from './types'
  import Sparkline from './Sparkline.svelte'

  const SAMPLE: Record<PriceType, number[]> = {
    hot: [10, 11, 10.5, 12, 13, 12.5, 14, 15, 16, 18, 21, 26],
    normal: [10, 10.2, 10.1, 10.5, 10.6, 10.4, 10.8, 11, 11.2, 11.1, 11.4, 11.5],
    falling: [14, 13.6, 13.7, 13.2, 12.8, 12.9, 12.3, 11.9, 11.6, 11.2, 10.8, 10.5],
    seasonal: [8, 3, 6, 2, 7, 3, 8, 2.5, 6.5, 3, 7.5, 2],
  }

  const YEAR_LABEL: Record<PriceType, [string, string]> = {
    hot: ['2016', '2026'],
    normal: ['2016', '2026'],
    falling: ['2016', '2026'],
    seasonal: ['JAN', 'DEC'],
  }
</script>

<section class="explainer">
  <h2>物價的漲相<br />大致可以分為四種類型</h2>

  <div class="cols">
    {#each TYPE_ORDER as t (t)}
      <div class="col type-{t}">
        <h3>{TYPE_LABEL[t]}</h3>
        <p>{TYPE_DESC[t]}</p>
        <div class="chart-block">
          <span class="yr start">{YEAR_LABEL[t][0]}</span>
          <Sparkline data={SAMPLE[t]} width={160} height={70} color="var(--type-color)" strokeWidth={3} />
          <span class="yr end">{YEAR_LABEL[t][1]}</span>
        </div>
      </div>
    {/each}
  </div>
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
    margin-bottom: 2rem;
  }

  .cols {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0;
    border-top: 1px solid var(--line);
  }

  @media (max-width: 900px) {
    .cols {
      grid-template-columns: repeat(2, 1fr);
    }
  }
  @media (max-width: 520px) {
    .cols {
      grid-template-columns: 1fr;
    }
  }

  .col {
    padding: 1.25rem 1.5rem 1.5rem 0;
    border-left: 1px solid var(--line);
    padding-left: 1.5rem;
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
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 0.5rem;
  }

  .yr {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--line);
  }
</style>
