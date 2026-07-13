<script lang="ts">
  import type { CpiItem } from '../types'
  import { shortName } from '../types'
  import { fullpage } from '../fullpage.svelte'
  import DrawableChart from './DrawableChart.svelte'

  let {
    items,
    trioNames,
    quizIndex,
    isLast,
  }: { items: CpiItem[]; trioNames: string[]; quizIndex: 1 | 2; isLast: boolean } = $props()

  const trio = $derived(
    trioNames.map((n) => items.find((it) => it.name === n)).filter((it): it is CpiItem => !!it),
  )

  let phase = $state<'pick' | 'draw' | 'reveal'>('pick')
  let selected = $state<CpiItem | null>(null)
  let drawnEnough = $state(false)

  function pick(item: CpiItem) {
    selected = item
    drawnEnough = false
    phase = 'draw'
  }

  function backToPick() {
    selected = null
    phase = 'pick'
    drawnEnough = false
  }

  function confirmDraw() {
    if (!drawnEnough) return
    phase = 'reveal'
  }
</script>

<div class="guess-item">
  <p class="kicker">第 {quizIndex} 題 / 共 2 題</p>

  {#if phase === 'pick'}
    <h2 class="prompt">你猜猜看，這個品項這幾年怎麼漲？</h2>
    <div class="cards">
      {#each trio as item (item.id)}
        <button class="pick-card" onclick={() => pick(item)}>
          <span class="pick-name">{shortName(item.name)}</span>
          <span class="pick-cta">畫畫看 →</span>
        </button>
      {/each}
    </div>
  {:else if selected}
    <h2 class="prompt">{shortName(selected.name)}</h2>
    <div class="chart-wrap">
      <DrawableChart
        item={selected}
        revealed={phase === 'reveal'}
        onDrawn={() => (drawnEnough = true)}
      />
    </div>

    <div class="actions">
      {#if phase === 'draw'}
        <button class="confirm" disabled={!drawnEnough} onclick={confirmDraw}>確認</button>
      {:else}
        <button class="secondary" onclick={backToPick}>換一個</button>
        {#if isLast}
          <button class="primary" onclick={() => fullpage.next()}>進入完整調查 →</button>
        {:else}
          <button class="primary" onclick={() => fullpage.next()}>下一題 →</button>
        {/if}
      {/if}
    </div>
  {/if}
</div>

<style>
  .guess-item {
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2.5rem 1.5rem;
    text-align: center;
  }

  .kicker {
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    opacity: 0.55;
  }

  .prompt {
    margin-top: 0.6rem;
    font-size: clamp(1.2rem, 3vw, 1.7rem);
    font-weight: 900;
  }

  .cards {
    margin-top: 2.2rem;
    display: grid;
    grid-template-columns: repeat(3, minmax(140px, 1fr));
    gap: 1rem;
    width: 100%;
    max-width: 720px;
  }

  .pick-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.8rem;
    border: 1px solid var(--line);
    background: var(--bg-card);
    border-radius: var(--radius-card, 2px);
    padding: 1.8rem 1rem;
    font-weight: 800;
    transition: background 0.15s ease, color 0.15s ease, transform 0.15s ease;
  }

  .pick-card:hover {
    background: var(--ink);
    color: var(--bg);
    transform: translateY(-3px);
  }

  .pick-name {
    font-size: 1.05rem;
  }

  .pick-cta {
    font-size: 0.78rem;
    opacity: 0.65;
  }

  .chart-wrap {
    margin-top: 1.8rem;
    width: 100%;
    max-width: 640px;
  }

  .actions {
    margin-top: 1.6rem;
    display: flex;
    gap: 0.8rem;
  }

  .confirm,
  .primary {
    border: none;
    background: var(--ink);
    color: var(--bg);
    padding: 0.65rem 1.8rem;
    font-size: 0.9rem;
    font-weight: 800;
    border-radius: 999px;
  }

  .confirm:disabled {
    opacity: 0.35;
    cursor: not-allowed;
  }

  .secondary {
    border: 1px solid var(--line);
    background: none;
    color: var(--ink);
    padding: 0.65rem 1.5rem;
    font-size: 0.9rem;
    font-weight: 800;
    border-radius: 999px;
  }

  @media (max-width: 640px) {
    .cards {
      grid-template-columns: 1fr;
      max-width: 280px;
    }
  }
</style>
