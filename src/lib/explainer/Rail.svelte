<script lang="ts">
  // left-side progress rail: three slots for the three observations, the
  // active one shown as a numbered orange circle, the rest as small dots
  let { current }: { current: 1 | 2 | 3 } = $props()
</script>

<div class="rail" aria-hidden="true">
  {#each [1, 2, 3] as n (n)}
    {#if n === current}
      <span class="num">{n}</span>
    {:else}
      <span class="dot"></span>
    {/if}
  {/each}
</div>

<style>
  .rail {
    position: absolute;
    left: clamp(1rem, 5vw, 6.5rem);
    top: 50%;
    transform: translateY(-50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.4rem;
    z-index: 2;
  }

  .num {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: var(--steady);
    color: #fff;
    font-family: var(--font-body);
    font-weight: 900;
    font-size: 1.05rem;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: var(--ink);
  }

  @media (max-width: 900px) {
    .rail {
      display: none;
    }
  }
</style>
