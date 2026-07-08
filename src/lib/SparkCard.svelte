<script lang="ts">
  import type { CpiItem } from './types'
  import Sparkline from './Sparkline.svelte'
  import { detailState } from './stores.svelte'

  let { item }: { item: CpiItem } = $props()
</script>

<button class="card type-{item.type}" onclick={() => detailState.open(item.id)}>
  <span class="name">{item.name}</span>
  <Sparkline data={item.series} color="var(--type-color)" width={140} height={40} />
</button>

<style>
  .card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 0.5rem;
    padding: 0.85rem 0.9rem;
    background: var(--bg-card);
    border: none;
    border-right: 1px solid var(--line-soft);
    border-bottom: 1px solid var(--line-soft);
    text-align: left;
    min-height: 92px;
    transition: background 0.15s ease;
  }

  .card:hover {
    background: var(--type-soft);
  }

  .name {
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--ink);
    line-height: 1.3;
  }
</style>
