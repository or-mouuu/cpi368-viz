<script lang="ts">
  import type { CpiItem } from './types'
  import SparkCard from './SparkCard.svelte'
  import { filterState, matchesFilter, matchesSearch, sortItems } from './stores.svelte'

  let { items, flyIn = false }: { items: CpiItem[]; flyIn?: boolean } = $props()

  const filtered = $derived(
    sortItems(
      items.filter(
        (it) => matchesFilter(it, filterState.type, filterState.categories) && matchesSearch(it, filterState.search),
      ),
      filterState.sort,
    ),
  )

  const FLY_COUNT = 64 // only the first screenful assembles with the fly-in

  // pseudo-random but deterministic scatter per card index
  function flyStyle(i: number): string {
    if (!flyIn || i >= FLY_COUNT) return ''
    const angle = ((i * 137.5) % 360) * (Math.PI / 180) // golden-angle spread
    const dist = 320 + ((i * 97) % 260)
    const x = Math.round(Math.cos(angle) * dist)
    const y = Math.round(Math.sin(angle) * dist)
    const r = ((i * 53) % 21) - 10
    const delay = i * 14
    return `--fly-x:${x}px; --fly-y:${y}px; --fly-r:${r}deg; --fly-delay:${delay}ms`
  }
</script>

<div class="grid">
  {#each filtered as item, i (item.id)}
    <SparkCard {item} flyStyle={flyStyle(i)} showChange={filterState.sort !== 'default'} />
  {:else}
    <p class="empty">找不到符合的品項</p>
  {/each}
</div>

<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    border-top: 1px solid var(--line-soft);
    border-left: 1px solid var(--line-soft);
  }

  @media (max-width: 1400px) {
    .grid {
      grid-template-columns: repeat(6, 1fr);
    }
  }
  @media (max-width: 1000px) {
    .grid {
      grid-template-columns: repeat(4, 1fr);
    }
  }
  @media (max-width: 640px) {
    .grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  .empty {
    grid-column: 1 / -1;
    padding: 3rem 1rem;
    text-align: center;
    color: var(--line);
  }
</style>
