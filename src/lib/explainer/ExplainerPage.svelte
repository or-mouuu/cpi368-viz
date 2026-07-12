<script lang="ts">
  import { expage, EX_SECTION_COUNT } from './expage.svelte'
  import ExHero from './ExHero.svelte'
  import ExObs1Circle from './ExObs1Circle.svelte'
  import ExObs1Weights from './ExObs1Weights.svelte'
  import ExInterlude from './ExInterlude.svelte'
  import ExObs2Pie from './ExObs2Pie.svelte'
  import ExObs3Groups from './ExObs3Groups.svelte'
  import ExObs3Pies from './ExObs3Pies.svelte'

  const labels = ['開頭', '觀察1', '權重範例', '過場', '觀察2', '觀察3', '頻率比較']

  $effect(() => {
    const onWheel = (e: WheelEvent) => expage.handleWheel(e)
    const onTouchStart = (e: TouchEvent) => expage.handleTouchStart(e)
    const onTouchEnd = (e: TouchEvent) => expage.handleTouchEnd(e)
    window.addEventListener('wheel', onWheel, { passive: false })
    window.addEventListener('touchstart', onTouchStart, { passive: true })
    window.addEventListener('touchend', onTouchEnd, { passive: true })
    return () => {
      window.removeEventListener('wheel', onWheel)
      window.removeEventListener('touchstart', onTouchStart)
      window.removeEventListener('touchend', onTouchEnd)
    }
  })
</script>

<svelte:window onkeydown={(e) => expage.handleKey(e)} />

{#if expage.active > 0}
  <header class="topbar">
    <a class="title" href="#/">消費者物價指數的真實漲相</a>
  </header>
{/if}

<nav class="dots" aria-label="頁面導航">
  {#each Array(EX_SECTION_COUNT) as _, i (i)}
    <button
      class="dot"
      class:active={expage.active === i}
      aria-label={labels[i]}
      title={labels[i]}
      onclick={() => expage.moveTo(i)}
    ></button>
  {/each}
</nav>

<div class="viewport">
  <div class="track" style="transform: translateY(-{expage.active * 100}%)">
    <section class="screen"><ExHero /></section>
    <section class="screen"><ExObs1Circle active={expage.active === 1} /></section>
    <section class="screen"><ExObs1Weights active={expage.active === 2} step={expage.active === 2 ? expage.step : 0} /></section>
    <section class="screen"><ExInterlude active={expage.active === 3} /></section>
    <section class="screen"><ExObs2Pie active={expage.active === 4} step={expage.active === 4 ? expage.step : 0} /></section>
    <section class="screen"><ExObs3Groups active={expage.active === 5} /></section>
    <section class="screen"><ExObs3Pies active={expage.active === 6} step={expage.active === 6 ? expage.step : 0} /></section>
  </div>
</div>

<style>
  .viewport {
    height: 100svh;
    overflow: hidden;
  }

  .track {
    height: 100%;
    transition: transform 600ms cubic-bezier(0.6, 0.04, 0.3, 1);
    will-change: transform;
  }

  .screen {
    height: 100%;
    overflow: hidden;
  }

  .topbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 44px;
    z-index: 30;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg);
    border-bottom: 1px solid var(--line-soft);
  }

  .title {
    text-decoration: none;
    font-size: 0.82rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    color: var(--ink);
  }

  .dots {
    position: fixed;
    right: 14px;
    top: 50%;
    transform: translateY(-50%);
    z-index: 40;
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 8px 6px;
    background: rgba(239, 236, 225, 0.85);
    border-radius: 999px;
  }

  .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    border: none;
    padding: 0;
    background: rgba(23, 20, 15, 0.25);
    transition: transform 0.2s ease, background 0.2s ease;
  }

  .dot.active {
    background: var(--ink);
    transform: scale(1.5);
  }

  @media (max-width: 640px) {
    .dots {
      right: 8px;
    }
  }
</style>
