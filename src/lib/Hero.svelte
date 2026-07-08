<script lang="ts">
  import type { CpiMeta } from './types'
  let { meta }: { meta: CpiMeta } = $props()

  const icons = [
    { emoji: '🍞', top: '8%', left: '6%', delay: '0s', size: '2.4rem' },
    { emoji: '🎮', top: '4%', left: '22%', delay: '0.6s', size: '2rem' },
    { emoji: '🖥️', top: '10%', left: '86%', delay: '0.3s', size: '2.6rem' },
    { emoji: '🏠', top: '18%', left: '92%', delay: '1s', size: '2.2rem' },
    { emoji: '🧻', top: '46%', left: '4%', delay: '0.9s', size: '2.3rem' },
    { emoji: '🚗', top: '58%', left: '88%', delay: '0.4s', size: '2.4rem' },
    { emoji: '🪴', top: '30%', left: '14%', delay: '1.3s', size: '2rem' },
    { emoji: '👕', top: '66%', left: '10%', delay: '0.2s', size: '2.1rem' },
    { emoji: '🍎', top: '78%', left: '18%', delay: '0.7s', size: '2.2rem' },
    { emoji: '🥤', top: '76%', left: '82%', delay: '1.1s', size: '2.2rem' },
    { emoji: '🧴', top: '86%', left: '90%', delay: '0.5s', size: '2rem' },
    { emoji: '🌳', top: '90%', left: '70%', delay: '0.8s', size: '2.2rem' },
  ]
</script>

<section class="hero">
  <div class="icons" aria-hidden="true">
    {#each icons as icon, i (i)}
      <span
        class="icon"
        style="top:{icon.top}; left:{icon.left}; animation-delay:{icon.delay}; font-size:{icon.size}"
      >
        {icon.emoji}
      </span>
    {/each}
  </div>

  <div class="content">
    <h1><span class="accent">368</span>種物價<br />漲相大調查</h1>
    <p>
      368 種物價指數是由<br />
      臺灣一般家庭購買消費性商品及服務之<br />
      生活中食、衣、住、行、育、樂、醫<br />
      價格水準變動情形的構成<br />
      往下繼續看看這些項目的漲相吧！
    </p>
    {#if meta}
      <p class="meta">資料範圍：{meta.dataStart} ~ {meta.dataEnd}（{meta.basePeriod}）</p>
    {/if}
    <div class="arrow">↓</div>
  </div>
</section>

<style>
  .hero {
    position: relative;
    min-height: 92vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    text-align: center;
  }

  .icons {
    position: absolute;
    inset: 0;
  }

  .icon {
    position: absolute;
    display: inline-block;
    filter: grayscale(1) contrast(1.1);
    opacity: 0.75;
    animation: float 5s ease-in-out infinite;
  }

  @keyframes float {
    0%,
    100% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(-14px);
    }
  }

  .content {
    position: relative;
    z-index: 1;
    max-width: 640px;
    padding: 0 1.25rem;
  }

  h1 {
    font-size: clamp(2.4rem, 7vw, 4.2rem);
    font-weight: 900;
    line-height: 1.15;
    letter-spacing: 0.02em;
  }

  .accent {
    color: var(--hot);
  }

  .content p {
    margin-top: 1.5rem;
    font-size: 0.95rem;
    line-height: 1.8;
    color: var(--ink);
  }

  .meta {
    margin-top: 1rem;
    font-size: 0.78rem;
    opacity: 0.6;
  }

  .arrow {
    margin-top: 2rem;
    font-size: 1.4rem;
    animation: bob 1.6s ease-in-out infinite;
  }

  @keyframes bob {
    0%,
    100% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(6px);
    }
  }
</style>
