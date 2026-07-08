<script lang="ts">
  import type { CpiItem } from './types'
  import SparkCard from './SparkCard.svelte'
  import { filterState, matchesFilter } from './stores.svelte'

  let { items }: { items: CpiItem[] } = $props()

  const filtered = $derived(items.filter((it) => matchesFilter(it, filterState.type, filterState.category)))
</script>

<div class="grid">
  {#each filtered as item (item.id)}
    <SparkCard {item} />
  {:else}
    <p class="empty">這個篩選條件下沒有項目</p>
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
