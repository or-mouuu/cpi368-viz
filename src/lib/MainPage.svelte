<script lang="ts">
  import type { CpiData } from './types'
  import { fullpage } from './fullpage.svelte'
  import HeroSection from './HeroSection.svelte'
  import IntroSection from './IntroSection.svelte'
  import DirectionsSection from './DirectionsSection.svelte'
  import ShapesSection from './ShapesSection.svelte'
  import ExplorerSection from './ExplorerSection.svelte'
  import AboutSection from './AboutSection.svelte'
  import NavDots from './NavDots.svelte'
  import TopHeader from './TopHeader.svelte'
  import DetailOverlay from './DetailOverlay.svelte'

  let { data }: { data: CpiData } = $props()

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
</script>

<svelte:window onkeydown={(e) => fullpage.handleKey(e)} />

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
</style>
