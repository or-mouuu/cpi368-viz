<script lang="ts">
  import type { CpiItem } from './types'
  import { TYPE_LABEL, shortName } from './types'
  import { detailState, filterState, matchesFilter } from './stores.svelte'
  import { fullpage } from './fullpage.svelte'
  import { yearSpan } from './chartMath'
  import DetailChart from './DetailChart.svelte'
  import Sparkline from './Sparkline.svelte'

  let { items }: { items: CpiItem[] } = $props()

  const byId = $derived(new Map(items.map((it) => [it.id, it])))

  const filtered = $derived(items.filter((it) => matchesFilter(it, filterState.type, filterState.categories)))
  const activeItem = $derived(items.find((it) => it.id === detailState.activeId) ?? null)
  const activeIndex = $derived(filtered.findIndex((it) => it.id === detailState.activeId))

  const prevItem = $derived(
    filtered.length ? filtered[(activeIndex - 1 + filtered.length) % filtered.length] : null,
  )
  const nextItem = $derived(filtered.length ? filtered[(activeIndex + 1) % filtered.length] : null)

  const similarItems = $derived(
    (activeItem?.similar ?? [])
      .map((s) => ({ item: byId.get(s.id), score: s.score }))
      .filter((s): s is { item: CpiItem; score: number } => !!s.item),
  )

  $effect(() => {
    // while the overlay is open, arrow keys/wheel navigate items, not sections
    fullpage.navLocked = activeItem !== null
  })

  function step(delta: number) {
    if (filtered.length === 0) return
    const base = activeIndex === -1 ? 0 : activeIndex
    const next = (base + delta + filtered.length) % filtered.length
    detailState.open(filtered[next].id)
  }

  function onKeydown(e: KeyboardEvent) {
    if (e.key === 'Escape') detailState.close()
    if (e.key === 'ArrowLeft') step(-1)
    if (e.key === 'ArrowRight') step(1)
  }
</script>

<svelte:window onkeydown={activeItem ? onKeydown : undefined} />

{#if activeItem}
  <div class="overlay type-{activeItem.type}" role="dialog" aria-modal="true">
    <header>
      <div>
        <p class="category">{activeItem.category}</p>
        <h2>{activeItem.name}</h2>
        <p class="type-label">
          {TYPE_LABEL[activeItem.type]} · {yearSpan(activeItem.periods)}年變動 {activeItem.change10y > 0 ? '+' : ''}{activeItem.change10y}%
          {#if activeItem.event}　⚡曾有大行情後回落{/if}
          {#if activeItem.volatile}　〰️價格劇烈波動{/if}
        </p>
      </div>
      <button class="close" aria-label="關閉" onclick={() => detailState.close()}>✕</button>
    </header>

    <div class="chart-wrap">
      <button class="nav prev" aria-label="上一個" onclick={() => step(-1)}>
        <span class="chev">‹</span>
        {#if prevItem}<span class="nav-name">{shortName(prevItem.name)}</span>{/if}
      </button>

      <div class="chart-area">
        <DetailChart item={activeItem} />
      </div>

      <button class="nav next" aria-label="下一個" onclick={() => step(1)}>
        <span class="chev">›</span>
        {#if nextItem}<span class="nav-name">{shortName(nextItem.name)}</span>{/if}
      </button>
    </div>

    {#if similarItems.length}
      <div class="similar">
        <p class="similar-title">走勢最像的品項</p>
        <div class="similar-row">
          {#each similarItems as { item, score } (item.id)}
            <button class="similar-card type-{item.type}" onclick={() => detailState.open(item.id)}>
              <Sparkline data={item.series} color="var(--type-color)" width={110} height={32} strokeWidth={2.5} />
              <span class="similar-name">{shortName(item.name)}</span>
              <span class="similar-meta">
                相似度 {Math.round(score * 100)}%
                {#if item.category !== activeItem?.category}
                  <span class="similar-cross">・{item.category}</span>
                {/if}
              </span>
            </button>
          {/each}
        </div>
      </div>
    {/if}
  </div>
{/if}

<style>
  .overlay {
    position: fixed;
    inset: 0;
    z-index: 50;
    background: var(--bg);
    display: flex;
    flex-direction: column;
    padding: 1.5rem clamp(1rem, 4vw, 3rem) 1rem;
  }

  header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
    flex: 0 0 auto;
  }

  .category {
    font-size: 0.85rem;
    color: var(--line);
    margin-bottom: 0.2rem;
  }

  h2 {
    font-size: clamp(1.6rem, 4vw, 2.4rem);
    font-weight: 800;
  }

  .type-label {
    margin-top: 0.4rem;
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--type-color);
  }

  .close {
    background: none;
    border: none;
    font-size: 1.6rem;
    line-height: 1;
    padding: 0.25rem 0.5rem;
    color: var(--ink);
  }

  .chart-wrap {
    flex: 1 1 auto;
    display: flex;
    align-items: center;
    gap: clamp(0.5rem, 2vw, 2rem);
    min-height: 0;
    padding: 1rem 0;
  }

  .chart-area {
    flex: 1 1 auto;
    height: 100%;
    min-width: 0;
  }

  .nav {
    flex: 0 0 auto;
    max-width: 140px;
    border: none;
    background: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.3rem;
    color: var(--ink);
    padding: 0.5rem;
  }

  .chev {
    font-size: 2rem;
    line-height: 1;
  }

  .nav-name {
    font-size: 0.78rem;
    font-weight: 700;
    text-align: center;
    line-height: 1.3;
  }

  .nav:hover .nav-name {
    text-decoration: underline;
  }

  @media (max-width: 700px) {
    .nav {
      max-width: 64px;
    }
    .nav-name {
      display: none;
    }
  }

  .similar {
    flex: 0 0 auto;
    margin-top: 0.5rem;
  }

  .similar-title {
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--line);
    margin-bottom: 0.8rem;
  }

  .similar-row {
    display: flex;
    gap: 1rem;
    overflow-x: auto;
    padding-bottom: 0.5rem;
  }

  .similar-card {
    flex: 0 0 130px;
    background: var(--surface);
    border: 1px solid var(--surface);
    border-radius: 8px;
    padding: 0.8rem;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.4rem;
    text-align: left;
    transition: transform 0.1s;
  }

  .similar-card:hover {
    transform: translateY(-2px);
    border-color: var(--type-color);
  }

  .similar-name {
    font-size: 0.9rem;
    font-weight: 700;
    line-height: 1.2;
    color: var(--ink);
    margin-top: 0.2rem;
  }

  .similar-meta {
    font-size: 0.75rem;
    color: var(--line);
    display: flex;
    flex-wrap: wrap;
    gap: 0.2rem;
  }

  .similar-cross {
    color: var(--type-color);
  }
</style>
