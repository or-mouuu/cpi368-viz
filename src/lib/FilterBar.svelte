<script lang="ts">
  import { CATEGORY_ORDER, TYPE_LABEL, TYPE_ORDER, type CategoryFilter, type PriceType } from './types'
  import { filterState } from './stores.svelte'

  const CATEGORY_SHORT: Record<CategoryFilter, string> = {
    全部: '全部',
    食物類: '食物類',
    衣著類: '衣著類',
    居住類: '居住類',
    交通及通訊類: '交通及通訊類',
    醫藥保健類: '醫藥保健類',
    教養娛樂類: '教養娛樂類',
    雜項類: '雜項類',
  }
</script>

<div class="filterbar">
  <div class="row">
    <button
      class="hamburger"
      aria-label="展開類別篩選"
      aria-expanded={filterState.categoryOpen}
      onclick={() => filterState.toggleCategoryMenu()}
    >
      <span></span><span></span><span></span>
    </button>

    <button class="tab all" class:active={filterState.type === 'all'} onclick={() => filterState.setType('all')}>
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

  {#if filterState.categoryOpen}
    <div class="categories">
      {#each CATEGORY_ORDER as c (c)}
        <button
          class="cat-chip"
          class:active={filterState.category === c}
          onclick={() => filterState.setCategory(c)}
        >
          {CATEGORY_SHORT[c]}
        </button>
      {/each}
    </div>
  {/if}
</div>

<style>
  .filterbar {
    position: sticky;
    top: 0;
    z-index: 20;
    background: var(--bg);
    border-bottom: 1px solid var(--line);
  }

  .row {
    display: flex;
    align-items: stretch;
    overflow-x: auto;
    scrollbar-width: none;
  }
  .row::-webkit-scrollbar {
    display: none;
  }

  .hamburger {
    flex: 0 0 auto;
    width: 48px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
    background: var(--ink);
    border: none;
  }
  .hamburger span {
    display: block;
    width: 20px;
    height: 2px;
    background: var(--bg);
  }

  .tab {
    flex: 0 0 auto;
    padding: 0.85rem 1.1rem;
    background: var(--bg);
    border: none;
    border-left: 1px solid var(--line-soft);
    font-weight: 700;
    font-size: 0.9rem;
    color: var(--ink);
    white-space: nowrap;
  }

  .tab.active {
    background: var(--ink);
    color: var(--bg);
  }

  .tab.type-hot.active {
    background: var(--hot);
    color: #fff;
  }
  .tab.type-normal.active {
    background: var(--normal);
    color: #fff;
  }
  .tab.type-falling.active {
    background: var(--falling);
    color: var(--ink);
  }
  .tab.type-seasonal.active {
    background: var(--seasonal);
    color: #fff;
  }

  .categories {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    padding: 0.7rem 0.9rem;
    border-top: 1px solid var(--line-soft);
  }

  .cat-chip {
    padding: 0.4rem 0.8rem;
    border: 1px solid var(--line);
    border-radius: 999px;
    background: var(--bg);
    font-size: 0.8rem;
    font-weight: 600;
  }

  .cat-chip.active {
    background: var(--ink);
    color: var(--bg);
  }
</style>
