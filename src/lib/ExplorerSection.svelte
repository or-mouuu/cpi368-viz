<script lang="ts">
  import type { CpiItem } from './types'
  import { CATEGORY_ORDER, TYPE_LABEL, TYPE_ORDER, type PriceType } from './types'
  import { filterState } from './stores.svelte'
  import { fullpage } from './fullpage.svelte'
  import CardGrid from './CardGrid.svelte'

  let { items, index }: { items: CpiItem[]; index: number } = $props()

  let scroller = $state<HTMLElement | null>(null)
  let catOpen = $state(false)
  let hasActivated = $state(false)

  $effect(() => {
    fullpage.scrollerEl = scroller
  })

  $effect(() => {
    if (fullpage.active === index && !hasActivated) hasActivated = true
  })
</script>

<div class="explorer">
  <div class="topbar">
    <div class="cat-wrap">
      <button class="cat-toggle" aria-expanded={catOpen} onclick={() => (catOpen = !catOpen)}>
        {filterState.category === '全部' ? '全部類別' : filterState.category}
        <span class="caret">⌄</span>
      </button>
      {#if catOpen}
        <div class="cat-menu">
          {#each CATEGORY_ORDER as c (c)}
            <button
              class="cat-item"
              class:selected={filterState.category === c}
              onclick={() => {
                filterState.setCategory(c)
                catOpen = false
              }}
            >
              {c === '全部' ? '全部類別' : c}
            </button>
          {/each}
        </div>
      {/if}
    </div>

    <div class="tabs">
      <button class="tab" class:active={filterState.type === 'all'} onclick={() => filterState.setType('all')}>
        全部
      </button>
      {#each TYPE_ORDER as t (t)}
        <button
          class="tab type-{t}"
          class:active={filterState.type === t}
          onclick={() => filterState.setType(t as PriceType)}
        >
          {TYPE_LABEL[t]}
        </button>
      {/each}
    </div>
  </div>

  <div class="scroller" bind:this={scroller}>
    <CardGrid {items} flyIn={hasActivated} />
    <p class="grid-foot">點任一品項看完整走勢．資料：行政院主計總處，每月自動更新</p>
  </div>
</div>

<style>
  .explorer {
    height: 100%;
    display: flex;
    flex-direction: column;
    padding-top: 44px; /* room for the fixed TopHeader */
  }

  .topbar {
    flex: 0 0 auto;
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.4rem 1rem;
    border-bottom: 1px solid var(--line);
    background: var(--bg);
    position: relative;
    z-index: 5;
  }

  .cat-wrap {
    position: relative;
    flex: 0 0 auto;
  }

  .cat-toggle {
    border: none;
    background: none;
    font-size: 0.85rem;
    font-weight: 800;
    color: var(--ink);
    display: flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.5rem 0;
  }

  .caret {
    font-size: 1rem;
    line-height: 0.6;
  }

  .cat-menu {
    position: absolute;
    top: 100%;
    left: 0;
    background: var(--bg);
    border: 1px solid var(--line);
    min-width: 180px;
    z-index: 10;
    display: flex;
    flex-direction: column;
  }

  .cat-item {
    border: none;
    background: none;
    text-align: left;
    padding: 0.55rem 0.9rem;
    font-size: 0.82rem;
    color: var(--ink);
  }

  .cat-item:hover {
    background: var(--line-soft);
  }

  .cat-item.selected {
    font-weight: 800;
  }

  .tabs {
    flex: 1 1 auto;
    display: flex;
    justify-content: center;
    gap: 0.4rem;
    overflow-x: auto;
    scrollbar-width: none;
  }
  .tabs::-webkit-scrollbar {
    display: none;
  }

  .tab {
    border: none;
    background: none;
    padding: 0.5rem 0.65rem;
    font-size: 0.85rem;
    font-weight: 800;
    letter-spacing: 0.03em;
    color: rgba(23, 20, 15, 0.45);
    white-space: nowrap;
  }

  .tab.active {
    color: var(--type-color, var(--ink));
    border-bottom: 2px solid var(--type-color, var(--ink));
  }

  .scroller {
    flex: 1 1 auto;
    overflow-y: auto;
    overscroll-behavior: contain;
  }

  .grid-foot {
    padding: 1.2rem 1rem 2rem;
    text-align: center;
    font-size: 0.75rem;
    opacity: 0.55;
  }

  @media (max-width: 700px) {
    .topbar {
      flex-direction: column;
      gap: 0.2rem;
      align-items: stretch;
    }
    .tabs {
      justify-content: flex-start;
    }
  }
</style>
