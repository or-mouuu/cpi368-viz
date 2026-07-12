<script lang="ts">
  import type { CpiItem } from './types'
  import { CATEGORY_ORDER, TYPE_LABEL, TYPE_ORDER, type CategoryFilter, type PriceType } from './types'
  import { filterState, type SortMode } from './stores.svelte'
  import { fullpage } from './fullpage.svelte'
  import CardGrid from './CardGrid.svelte'
  import iconAll from '../assets/category/all.svg?url'
  import iconFood from '../assets/category/food.svg?url'
  import iconClothing from '../assets/category/cloth.svg?url'
  import iconHousing from '../assets/category/house.svg?url'
  import iconTransport from '../assets/category/transport.svg?url'
  import iconHealth from '../assets/category/hospt.svg?url'
  import iconEducation from '../assets/category/learn.svg?url'
  import iconMisc from '../assets/category/others.svg?url'

  const SORT_OPTIONS: { key: SortMode; label: string }[] = [
    { key: 'default', label: '預設排序' },
    { key: 'change_desc', label: '漲幅最高' },
    { key: 'change_asc', label: '漲幅最低' },
  ]

  const CATEGORY_ICON: Record<CategoryFilter, string> = {
    全部: iconAll,
    食物類: iconFood,
    衣著類: iconClothing,
    居住類: iconHousing,
    交通及通訊類: iconTransport,
    醫藥保健類: iconHealth,
    教養娛樂類: iconEducation,
    雜項類: iconMisc,
  }

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
    <button
      class="hamburger"
      aria-label="切換類別篩選"
      aria-expanded={catOpen}
      onclick={() => (catOpen = !catOpen)}
    >
      <svg viewBox="0 0 24 24" aria-hidden="true"><line x1="3" y1="7" x2="21" y2="7" /><line x1="3" y1="12" x2="21" y2="12" /><line x1="3" y1="17" x2="21" y2="17" /></svg>
    </button>

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

  {#if catOpen}
    <div class="cat-icons">
      {#each CATEGORY_ORDER as c (c)}
        <button
          class="cat-tile"
          class:selected={filterState.isCategorySelected(c)}
          aria-pressed={filterState.isCategorySelected(c)}
          onclick={() => filterState.toggleCategory(c)}
        >
          <span class="tile-icon">
            <img src={CATEGORY_ICON[c]} alt="" class="tile-svg" />
          </span>
          <span class="tile-label">{c}</span>
        </button>
      {/each}
    </div>
  {/if}

  <div class="toolbar">
    <input
      class="search"
      type="search"
      placeholder="搜尋品項名稱⋯"
      value={filterState.search}
      oninput={(e) => filterState.setSearch(e.currentTarget.value)}
    />
    <div class="sort">
      {#each SORT_OPTIONS as opt (opt.key)}
        <button class="sort-btn" class:active={filterState.sort === opt.key} onclick={() => filterState.setSort(opt.key)}>
          {opt.label}
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

  .hamburger {
    flex: 0 0 auto;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    background: var(--ink);
    border-radius: 4px;
  }

  .hamburger svg {
    width: 20px;
    height: 20px;
  }

  .hamburger line {
    stroke: var(--bg);
    stroke-width: 2;
    stroke-linecap: round;
  }

  .cat-icons {
    flex: 0 0 auto;
    display: flex;
    flex-wrap: wrap;
    gap: 1.1rem;
    padding: 1rem;
    border-bottom: 1px solid var(--line);
    background: var(--bg);
  }

  .cat-tile {
    flex: 0 0 auto;
    width: 96px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.4rem;
    border: none;
    background: none;
  }

  .tile-icon {
    width: 92px;
    height: 92px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: none;
    border-radius: 16px;
    transition: background 0.15s ease;
  }

  .cat-tile.selected .tile-icon {
    background: var(--steady);
  }

  .tile-svg {
    width: 88%;
    height: 88%;
    object-fit: contain;
  }

  .tile-label {
    font-size: 0.78rem;
    font-weight: 800;
    color: var(--ink);
    text-align: center;
  }

  .cat-tile.selected .tile-label {
    color: var(--steady);
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
    padding: 0.5rem 0.8rem;
    font-size: 0.85rem;
    font-weight: 800;
    letter-spacing: 0.03em;
    color: var(--type-color, var(--ink));
    white-space: nowrap;
    border-radius: 999px;
    transition: background 0.15s ease, color 0.15s ease;
  }

  .tab.active {
    background: var(--type-color, var(--ink));
    color: #fff;
  }

  .tab.type-flat.active,
  .tab.type-cheaper.active {
    color: var(--ink);
  }

  .toolbar {
    flex: 0 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    padding: 0.5rem 1rem;
    border-bottom: 1px solid var(--line-soft);
    background: var(--bg);
  }

  .search {
    flex: 0 1 240px;
    min-width: 0;
    padding: 0.4rem 0.7rem;
    font-size: 0.82rem;
    font-family: inherit;
    color: var(--ink);
    background: var(--bg-card);
    border: 1px solid var(--line);
    border-radius: 999px;
  }

  .search::placeholder {
    color: rgba(23, 20, 15, 0.4);
  }

  .sort {
    flex: 0 0 auto;
    display: flex;
    gap: 0.3rem;
  }

  .sort-btn {
    border: 1px solid var(--line);
    background: var(--bg);
    padding: 0.35rem 0.7rem;
    font-size: 0.76rem;
    font-weight: 700;
    color: var(--ink);
    border-radius: 999px;
    white-space: nowrap;
  }

  .sort-btn.active {
    background: var(--ink);
    color: var(--bg);
    border-color: var(--ink);
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
    .tabs {
      justify-content: flex-start;
    }
    .cat-icons {
      gap: 0.7rem;
      padding: 0.8rem;
    }
    .cat-tile {
      width: 74px;
    }
    .tile-icon {
      width: 70px;
      height: 70px;
      border-radius: 12px;
    }
    .tile-label {
      font-size: 0.68rem;
    }
    .toolbar {
      flex-direction: column;
      align-items: stretch;
    }
    .search {
      flex-basis: auto;
    }
    .sort {
      justify-content: flex-start;
      overflow-x: auto;
    }
  }
</style>
