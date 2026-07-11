<script lang="ts">
  import type { CpiItem } from './types'
  import Sparkline from './Sparkline.svelte'
  import { detailState } from './stores.svelte'

  let { item, flyStyle = '' }: { item: CpiItem; flyStyle?: string } = $props()
</script>

<button class="card type-{item.type}" class:fly={flyStyle !== ''} style={flyStyle} onclick={() => detailState.open(item.id)}>
  <span class="head">
    <span class="name">{item.name}</span>
    <span class="badges">
      {#if item.event}<span class="badge" title="曾有一波大行情後回落">⚡</span>{/if}
      {#if item.volatile}<span class="badge" title="價格劇烈波動">〰️</span>{/if}
    </span>
  </span>
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

  .card.fly {
    opacity: 0;
    animation: fly-in 0.65s cubic-bezier(0.22, 1, 0.36, 1) var(--fly-delay, 0ms) forwards;
  }

  @keyframes fly-in {
    from {
      opacity: 0;
      transform: translate(var(--fly-x, 0px), var(--fly-y, 60px)) rotate(var(--fly-r, 0deg));
    }
    to {
      opacity: 1;
      transform: translate(0, 0) rotate(0deg);
    }
  }

  .card:hover {
    background: var(--type-soft);
  }

  .head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 0.25rem;
  }

  .name {
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--ink);
    line-height: 1.3;
  }

  .badges {
    flex: 0 0 auto;
    font-size: 0.7rem;
    line-height: 1;
  }
</style>
