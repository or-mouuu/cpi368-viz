<script lang="ts">
  import type { CpiData } from './lib/types'
  import { fullpage, SECTION_COUNT } from './lib/fullpage.svelte'
  import HeroSection from './lib/HeroSection.svelte'
  import IntroSection from './lib/IntroSection.svelte'
  import DirectionsSection from './lib/DirectionsSection.svelte'
  import ShapesSection from './lib/ShapesSection.svelte'
  import ExplorerSection from './lib/ExplorerSection.svelte'
  import AboutSection from './lib/AboutSection.svelte'
  import NavDots from './lib/NavDots.svelte'
  import TopHeader from './lib/TopHeader.svelte'
  import DetailOverlay from './lib/DetailOverlay.svelte'

  let data = $state<CpiData | null>(null)
  let error = $state<string | null>(null)

  $effect(() => {
    // wheel listeners on window are passive by default in Chrome, which would
    // break preventDefault-based section snapping - attach non-passive ourselves
    const onWheel = (e: WheelEvent) => fullpage.handleWheel(e)
    const onTouchStart = (e: TouchEvent) => fullpage.handleTouchStart(e)
    const onTouchEnd = (e: TouchEvent) => fullpage.handleTouchEnd(e)
    window.addEventListener('wheel', onWheel, { passive: false })
    window.addEventListener('touchstart', onTouchStart, { passive: true })
    window.addEventListener('touchend', onTouchEnd, { passive: true })
    return () => {
      window.removeEventListener('wheel', onWheel)
      window.removeEventListener('touchstart', onTouchStart)
      window.removeEventListener('touchend', onTouchEnd)
    }
  })

  $effect(() => {
    fetch(`${import.meta.env.BASE_URL}data/items.json`)
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`)
        return r.json()
      })
      .then((d: CpiData) => {
        data = d
      })
      .catch((e) => {
        error = String(e)
      })
  })
</script>

<svelte:window onkeydown={(e) => fullpage.handleKey(e)} />

{#if error}
  <p class="status error">資料載入失敗：{error}</p>
{:else if !data}
  <p class="status">載入中…</p>
{:else}
  <TopHeader meta={data.meta} />
  <NavDots />

  <div class="viewport">
    <div class="track" style="transform: translateY(-{fullpage.active * 100}%)">
      <section class="screen"><HeroSection meta={data.meta} /></section>
      <section class="screen"><IntroSection meta={data.meta} /></section>
      <section class="screen"><DirectionsSection index={2} items={data.items} meta={data.meta} /></section>
      <section class="screen"><ShapesSection index={3} items={data.items} meta={data.meta} /></section>
      <section class="screen"><ExplorerSection items={data.items} index={4} /></section>
      <section class="screen"><AboutSection meta={data.meta} /></section>
    </div>
  </div>

  <DetailOverlay items={data.items} />
{/if}

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

  .status {
    padding: 4rem 1rem;
    text-align: center;
    font-size: 1rem;
  }
  .status.error {
    color: var(--steady);
  }
</style>
