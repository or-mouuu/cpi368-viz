<script lang="ts">
  import type { CpiMeta } from './types'
  import { fullpage } from './fullpage.svelte'

  let { meta }: { meta: CpiMeta } = $props()

  const icons = import.meta.glob('../assets/hero/*.svg', { eager: true, query: '?url', import: 'default' })
  const urls = Object.keys(icons)
    .sort()
    .map((k) => icons[k] as string)

  // scattered around the edges like the design mockup, floating slowly
  const layout = [
    { top: '6%', left: '4%', size: 92, delay: 0 },
    { top: '4%', left: '17%', size: 76, delay: 0.7 },
    { top: '30%', left: '9%', size: 84, delay: 1.4 },
    { top: '55%', left: '4%', size: 96, delay: 0.3 },
    { top: '76%', left: '12%', size: 88, delay: 1.1 },
    { top: '90%', left: '28%', size: 72, delay: 0.5 },
    { top: '6%', left: '84%', size: 90, delay: 0.9 },
    { top: '24%', left: '92%', size: 78, delay: 0.2 },
    { top: '46%', left: '88%', size: 92, delay: 1.6 },
    { top: '68%', left: '93%', size: 74, delay: 0.6 },
    { top: '84%', left: '84%', size: 88, delay: 1.2 },
    { top: '92%', left: '64%', size: 70, delay: 0.4 },
    { top: '88%', left: '46%', size: 78, delay: 1.5 },
    { top: '2%', left: '64%', size: 72, delay: 0.8 },
  ]
</script>

<div class="hero">
  <div class="icons" aria-hidden="true">
    {#each urls as url, i (url)}
      {#if layout[i]}
        <img
          src={url}
          alt=""
          class="icon"
          style="top:{layout[i].top}; left:{layout[i].left}; width:{layout[i].size}px; animation-delay:{layout[i].delay}s"
        />
      {/if}
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
    <button class="arrow" aria-label="往下捲動" onclick={() => fullpage.next()}>↓</button>
  </div>
</div>

<style>
  .hero {
    position: relative;
    height: 100%;
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
    animation: float 5.5s ease-in-out infinite;
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
    color: var(--steady);
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
    border: none;
    background: none;
    font-size: 1.4rem;
    color: var(--ink);
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
