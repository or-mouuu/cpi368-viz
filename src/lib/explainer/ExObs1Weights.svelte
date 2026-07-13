<script lang="ts">
  import { fade } from 'svelte/transition'
  import { tweened } from 'svelte/motion'
  import { cubicOut } from 'svelte/easing'
  import Rail from './Rail.svelte'
  import imgTrio from '../../assets/explainer/e56.svg?url'

  let { active, step }: { active: boolean; step: number } = $props()

  // the 1-2 -> 1-3 example: rent 60->63, apple 2->3, total 100->104
  const house = tweened(60, { duration: 700, easing: cubicOut })
  const apple = tweened(2, { duration: 700, easing: cubicOut })
  const total = tweened(100, { duration: 700, easing: cubicOut })

  $effect(() => {
    const bumped = active && step >= 1
    house.set(bumped ? 63 : 60)
    apple.set(bumped ? 3 : 2)
    total.set(bumped ? 104 : 100)
  })
</script>

<div class="obs">
  <Rail current={1} />

  <div class="text">
    <p class="kicker">觀察1</p>
    <h2>物價指數的計算和<br />人們的花費佔比有關</h2>

    {#if step === 0}
      <div class="step-copy" in:fade={{ duration: 350 }}>
        <p class="body">
          物價指數的計算會依據<br />
          全台家庭消費結構來調整 368 個品項的權重
        </p>
        <p class="body">
          舉例來說每月花費是 100 元，花費較多的房租權重較大，花費較少的蘋果權重較小
        </p>
      </div>
    {:else}
      <div class="step-copy" in:fade={{ duration: 350 }}>
        <p class="body">
          權重大小除了反映人們如何分配花費<br />
          也代表每個品項對物價的影響力大小
        </p>
        <p class="body">
          即使蘋果大漲 50%，也只會讓物價指數漲 1%<br />
          但房租只要漲 5%，就會讓物價指數漲 3%
        </p>
      </div>
    {/if}
  </div>

  <div class="visual" class:active>
    <div class="stage">
      <img src={imgTrio} alt="" class="trio" />

      <span class="price house" class:bump={step >= 1}>${Math.round($house)}</span>
      <span class="price apple" class:bump={step >= 1}>${Math.round($apple)}</span>
      <span class="price shirt">$38</span>

      {#if step >= 1}
        <span class="pct roof" in:fade={{ duration: 300, delay: 150 }}>+5%</span>
        <span class="pct stem" in:fade={{ duration: 300, delay: 300 }}>+50%</span>
      {/if}

      <!-- e56 has both ground rules built in (y=275.6 and y=393); the total
           belongs in the band between them -->
      <div class="total-row">
        <span class="total" class:bump={step >= 1}>${Math.round($total)}</span>
        {#if step >= 1}
          <span class="total-badge" in:fade={{ duration: 300, delay: 400 }}>+4%</span>
        {/if}
      </div>
    </div>
  </div>
</div>

<style>
  .obs {
    position: relative;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: clamp(2rem, 6vw, 7rem);
    padding: 0 clamp(1rem, 8vw, 9rem);
  }

  .text {
    flex: 0 1 460px;
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

  .visual {
    flex: 0 0 auto;
    width: clamp(300px, 36vw, 540px);
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.6s ease, transform 0.6s ease;
  }

  .visual.active {
    opacity: 1;
    transform: translateY(0);
  }

  .stage {
    position: relative;
    width: 100%;
    aspect-ratio: 554.75 / 395.03; /* e56's intrinsic viewBox */
  }

  .trio {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
  }

  .price {
    position: absolute;
    font-family: var(--font-display);
    color: var(--ink);
    transition: color 0.4s ease;
    transform: translate(-50%, -50%);
    white-space: nowrap;
  }

  .price.bump {
    color: var(--steady);
  }

  .price.house {
    left: 24%;
    top: 49%;
    font-size: clamp(1.4rem, 2.6vw, 2.2rem);
  }

  .price.apple {
    left: 53%;
    top: 58%;
    font-size: clamp(0.75rem, 1.3vw, 1.1rem);
  }

  .price.shirt {
    left: 77%;
    top: 45%;
    font-size: clamp(1.05rem, 1.9vw, 1.6rem);
    color: var(--ink);
  }

  .pct {
    position: absolute;
    font-family: var(--font-display);
    color: var(--steady);
    font-size: clamp(0.85rem, 1.5vw, 1.25rem);
    transform: translate(-50%, -50%);
    white-space: nowrap;
  }

  .pct.roof {
    left: 24%;
    top: 3%;
  }

  .pct.stem {
    left: 53%;
    top: 38%;
  }

  .total-row {
    position: absolute;
    left: 0;
    right: 0;
    top: 70%;
    bottom: 1.5%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.9rem;
  }

  .total {
    font-family: var(--font-display);
    font-size: clamp(2rem, 3.6vw, 3.2rem);
    color: var(--ink);
    transition: color 0.4s ease;
  }

  .total.bump {
    color: var(--steady);
  }

  .total-badge {
    width: clamp(48px, 4.5vw, 64px);
    aspect-ratio: 1;
    border-radius: 50%;
    background: var(--steady);
    color: #fff;
    font-family: var(--font-display);
    font-size: clamp(0.85rem, 1.4vw, 1.15rem);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  @media (max-width: 900px) {
    .obs {
      flex-direction: column;
      gap: 1.5rem;
      text-align: center;
    }
    .visual {
      width: min(86vw, 420px);
    }
  }
</style>
