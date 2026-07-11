<script lang="ts">
  import { shortName, type CpiItem } from './types'
  import Sparkline from './Sparkline.svelte'
  import { detailState } from './stores.svelte'

  let {
    item,
    flyStyle = '',
    showChange = false,
  }: { item: CpiItem; flyStyle?: string; showChange?: boolean } = $props()
</script>

<button class="card type-{item.type}" class:fly={flyStyle !== ''} style={flyStyle} onclick={() => detailState.open(item.id)}>
  <span class="head">
    <span class="name">{shortName(item.name)}</span>
  </span>
  <span class="foot">
    <Sparkline data={item.series} color="var(--type-color)" width={showChange ? 104 : 140} height={40} />
    {#if showChange}
      <span class="change" class:pos={item.change10y >= 0} class:neg={item.change10y < 0}>
        {item.change10y > 0 ? '+' : ''}{item.change10y.toFixed(1)}%
      </span>
    {/if}
  </span>
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
  }

  .name {
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--ink);
    line-height: 1.3;
  }

  .foot {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 0.4rem;
  }

  .change {
    flex: 0 0 auto;
    font-family: var(--font-numeric);
    font-size: 0.8rem;
    font-weight: 700;
  }
  .change.pos {
    color: var(--steady);
  }
  .change.neg {
    color: var(--cheaper);
  }
</style>
