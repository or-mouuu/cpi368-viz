<script lang="ts">
  import type { CpiData } from './types'
  import { fullpage } from './fullpage.svelte'
  import GuessTotalSection from './intro/GuessTotalSection.svelte'
  import GuessItemSection from './intro/GuessItemSection.svelte'
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
    <section class="screen"><GuessTotalSection meta={data.meta} /></section>
    <section class="screen">
      <GuessItemSection items={data.items} trioNames={['豬肉', '雞蛋', '鮭魚']} quizIndex={1} isLast={false} />
    </section>
    <section class="screen">
      <GuessItemSection
        items={data.items}
        trioNames={['行動電話', '隱形眼鏡', '衛生紙、面紙及紙巾']}
        quizIndex={2}
        isLast={true}
      />
    </section>
    <section class="screen"><ExplorerSection items={data.items} index={3} /></section>
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
