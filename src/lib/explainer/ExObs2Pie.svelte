<script lang="ts">
  import { fade } from 'svelte/transition'
  import Rail from './Rail.svelte'
  import Pie from './Pie.svelte'

  let { active, step }: { active: boolean; step: number } = $props()

  // 2-1: >30% risers are a quarter of the ITEM COUNT; 2-2: but only 12% by WEIGHT
  const fraction = $derived(step >= 1 ? 0.12 : 0.25)
</script>

<div class="obs">
  <Rail current={2} />

  <div class="text">
    <p class="kicker">觀察2</p>
    <h2>物價指數的計算方式<br />讓體感物價漲很兇</h2>

    {#if step === 0}
      <div in:fade={{ duration: 350 }}>
        <p class="body">觀察過去 10 年台灣的物價變化</p>
        <p class="body">
          從上漲的品項數量來看<br />
          <span class="hl">漲幅超過 30% 的品項</span>高達四分之一
        </p>
      </div>
    {:else}
      <div in:fade={{ duration: 350 }}>
        <p class="body">
          但因為每個品項的影響力大小不同<br />
          實際上漲幅超過 30% 的品項權重只佔 12%
        </p>
        <p class="body">
          換句話說，<span class="hl">雖然有 1/4 的品項漲很兇<br />但這些品項佔人們的支出比例並不高</span>
        </p>
      </div>
    {/if}
  </div>

  <div class="visual" class:active>
    <Pie {fraction} size={380} {active} sliceLabel={'漲幅\n>30%'} />
    <p class="caption">
      2013-2023年<br />
      {#if step === 0}
        <b in:fade={{ duration: 300 }}>漲幅超過30%的品項數</b>
      {:else}
        <b in:fade={{ duration: 300 }}>漲幅超過30%的權重數</b>
      {/if}
    </p>
  </div>
</div>

<style>
  .obs {
    position: relative;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: clamp(2rem, 6vw, 8rem);
    padding: 0 clamp(1rem, 8vw, 9rem);
  }

  .text {
    flex: 0 1 470px;
  }

  .kicker {
    color: var(--steady);
    font-weight: 900;
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
  }

  h2 {
    font-size: clamp(1.5rem, 2.6vw, 2.1rem);
    font-weight: 900;
    line-height: 1.5;
    margin-bottom: 1.4rem;
  }

  .body {
    font-size: 0.95rem;
    font-weight: 700;
    line-height: 1.9;
    margin-bottom: 1.2rem;
  }

  .hl {
    color: var(--steady);
  }

  .visual {
    flex: 0 0 auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.2rem;
    opacity: 0;
    transition: opacity 0.6s ease;
  }

  .visual.active {
    opacity: 1;
  }

  .caption {
    text-align: center;
    font-size: 1.05rem;
    font-weight: 700;
    line-height: 1.6;
  }

  .caption b {
    font-weight: 900;
  }

  @media (max-width: 900px) {
    .obs {
      flex-direction: column;
      gap: 1.4rem;
      text-align: center;
    }
    .visual :global(svg) {
      width: min(56vw, 300px);
      height: auto;
    }
  }
</style>
