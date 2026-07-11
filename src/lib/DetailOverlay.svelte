<script lang="ts">
  import type { CpiItem } from './types'
  import { TYPE_LABEL } from './types'
  import { detailState, filterState, matchesFilter } from './stores.svelte'
  import DetailChart from './DetailChart.svelte'

  let { items }: { items: CpiItem[] } = $props()

  const filtered = $derived(items.filter((it) => matchesFilter(it, filterState.type, filterState.category)))
  const activeItem = $derived(items.find((it) => it.id === detailState.activeId) ?? null)
  const activeIndex = $derived(filtered.findIndex((it) => it.id === detailState.activeId))

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
  <div class="overlay" role="dialog" aria-modal="true">
    <div class="panel type-{activeItem.type}">
      <header>
        <div>
          <p class="category">{activeItem.category}</p>
          <h2>{activeItem.name}</h2>
          <p class="type-label">
            {TYPE_LABEL[activeItem.type]} · 10年變動 {activeItem.change10y > 0 ? '+' : ''}{activeItem.change10y}%
            {#if activeItem.event}　⚡曾有大行情後回落{/if}
            {#if activeItem.volatile}　〰️價格劇烈波動{/if}
          </p>
        </div>
        <button class="close" aria-label="關閉" onclick={() => detailState.close()}>✕</button>
      </header>

      <div class="chart-wrap">
        <button class="nav prev" aria-label="上一個" onclick={() => step(-1)}>‹</button>
        <DetailChart item={activeItem} />
        <button class="nav next" aria-label="下一個" onclick={() => step(1)}>›</button>
      </div>

      <p class="note">指數基期：民國110年=100（2021=100）</p>
    </div>
  </div>
{/if}

<style>
  .overlay {
    position: fixed;
    inset: 0;
    z-index: 50;
    background: rgba(23, 20, 15, 0.55);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1.5rem;
  }

  .panel {
    background: var(--bg);
    width: min(920px, 100%);
    max-height: 90vh;
    overflow-y: auto;
    border: 2px solid var(--ink);
    padding: 1.5rem 1.5rem 1.25rem;
  }

  header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 0.75rem;
  }

  .category {
    font-size: 0.8rem;
    color: var(--line);
    margin-bottom: 0.15rem;
  }

  h2 {
    font-size: 1.6rem;
    font-weight: 800;
  }

  .type-label {
    margin-top: 0.35rem;
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--type-color);
  }

  .close {
    background: none;
    border: none;
    font-size: 1.3rem;
    line-height: 1;
    padding: 0.25rem 0.5rem;
    color: var(--ink);
  }

  .chart-wrap {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .nav {
    flex: 0 0 auto;
    width: 36px;
    height: 36px;
    border: 1px solid var(--line);
    background: var(--bg);
    border-radius: 50%;
    font-size: 1.2rem;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .nav:hover {
    background: var(--ink);
    color: var(--bg);
  }

  .note {
    margin-top: 0.5rem;
    font-size: 0.72rem;
    color: var(--line);
    text-align: right;
  }
</style>
