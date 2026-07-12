<script lang="ts">
  import type { CpiMeta } from './types'
  import { fullpage } from './fullpage.svelte'

  let { meta }: { meta: CpiMeta } = $props()

  const icons = import.meta.glob('../assets/hero/*.svg', { eager: true, query: '?url', import: 'default' })
  const url = (n: number) => icons[`../assets/hero/item${String(n).padStart(2, '0')}.svg`] as string

  // two side clusters per the design mockup (positions in % of the hero,
  // sizes in px at 1440w - scaled down proportionally on narrower screens)
  // 01藥丸 02麵包 03手把 04電視框 05車 06房 07衣 08蘋果 09盆栽 10筆電 11沐浴乳 12衛生紙 13花椰菜 14飲料杯
  const layout = [
    // left cluster
    { n: 4, top: '10%', left: '1.5%', mTop: '35%', mLeft: '60%', size: 140, rot: -12, delay: 0.2 },
    { n: 3, top: '11%', left: '13%', mTop: '25%', mLeft: '-15%', size: 150, rot: 4, delay: 0.9 },
    { n: 9, top: '33%', left: '22%', mTop: '85%', mLeft: '5%', size: 105, rot: 0, delay: 1.4 },
    { n: 12, top: '37%', left: '8%', mTop: '40%', mLeft: '20%', size: 165, rot: 0, delay: 0.5 },
    { n: 2, top: '42%', left: '-3%', mTop: '15%', mLeft: '65%', size: 140, rot: -8, delay: 1.1 },
    { n: 8, top: '60%', left: '2.5%', mTop: '75%', mLeft: '50%', size: 160, rot: 0, delay: 0.3 },
    { n: 14, top: '62%', left: '17%', mTop: '80%', mLeft: '75%', size: 150, rot: 3, delay: 0.8 },
    // right cluster
    { n: 10, top: '9%', left: '87%', mTop: '5%', mLeft: '45%', size: 185, rot: 5, delay: 0.6 },
    { n: 6, top: '23%', left: '72%', mTop: '55%', mLeft: '60%', size: 150, rot: 0, delay: 1.2 },
    { n: 5, top: '33%', left: '84%', mTop: '45%', mLeft: '-10%', size: 180, rot: 8, delay: 0.4 },
    { n: 1, top: '46%', left: '96.5%', mTop: '8%', mLeft: '5%', size: 120, rot: -10, delay: 1.0 },
    { n: 7, top: '52%', left: '72.5%', mTop: '65%', mLeft: '-10%', size: 160, rot: -5, delay: 0.7 },
    { n: 11, top: '58%', left: '90.5%', mTop: '25%', mLeft: '45%', size: 110, rot: 0, delay: 1.5 },
    { n: 13, top: '70%', left: '83%', mTop: '60%', mLeft: '25%', size: 130, rot: 0, delay: 0.1 },
  ]
</script>

<div class="hero">
  <div class="icons" aria-hidden="true">
    {#each layout as it (it.n)}
      <img
        src={url(it.n)}
        alt=""
        class="icon"
        style="--top:{it.top}; --left:{it.left}; --m-top:{it.mTop}; --m-left:{it.mLeft}; width:clamp({it.size * 0.65}px, {(it.size / 14.4).toFixed(1)}vw, {it.size}px); --rot:{it.rot}deg; animation-delay:{it.delay}s"
      />
    {/each}
  </div>

  <div class="content">
    <h1>
      <span class="line accent">{meta.itemCount}種物價</span>
      <!-- 査＝Dela Gothic One 的日文字形；此字型無台灣慣用的「查」，僅視覺標題使用 -->
      <span class="line">漲相大調査</span>
    </h1>
    <p>
      {meta.itemCount} 種物價指數是由<br />
      臺灣一般家庭購買消費性商品及服務之<br />
      生活中食、衣、住、行、育、樂、醫<br />
      價格水準變動情形的構成<br />
      往下繼續看看這些項目的漲相吧！
    </p>
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
    top: var(--top);
    left: var(--left);
    transform: rotate(var(--rot, 0deg));
    animation: float 5.5s ease-in-out infinite;
  }

  @keyframes float {
    0%,
    100% {
      transform: translateY(0) rotate(var(--rot, 0deg));
    }
    50% {
      transform: translateY(-12px) rotate(var(--rot, 0deg));
    }
  }

  .content {
    position: relative;
    z-index: 1;
    max-width: 680px;
    padding: 0 1.25rem;
  }

  h1 {
    font-family: var(--font-display);
    font-weight: 400; /* Dela Gothic One only ships regular - it is already extra bold */
    line-height: 1.28;
    letter-spacing: 0.04em;
    display: flex;
    flex-direction: column;
  }

  .line {
    font-size: clamp(2.5rem, 6.5vw, 5.2rem);
    white-space: nowrap;
  }

  .accent {
    color: #ff4a00;
  }

  .content p {
    margin-top: 1.6rem;
    font-size: 0.95rem;
    line-height: 1.9;
    font-weight: 700;
    color: var(--ink);
  }

  .meta {
    margin-top: 1rem;
    font-size: 0.78rem !important;
    font-weight: 400 !important;
    opacity: 0.6;
  }

  .arrow {
    margin-top: 2.2rem;
    border: none;
    background: none;
    font-size: 1.5rem;
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

  @media (max-width: 640px) {
    .icon {
      top: var(--m-top);
      left: var(--m-left);
      opacity: 0.45;
    }
  }
</style>
