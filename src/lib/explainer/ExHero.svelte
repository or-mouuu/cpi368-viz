<script lang="ts">
  import { expage } from './expage.svelte'
</script>

<div class="exhero">
  <h1>
    <span class="line accent">消費者物價指數</span>
    <span class="line">的真實漲相</span>
  </h1>
  <p>
    你是不是也這樣想？「感覺上」物價明明就漲很兇！<br />
    為什麼「體感物價」會和「物價指數」差這麼多？<br />
    到底兩者的差異是什麼？讓我們從三個面向開始了解吧
  </p>
  <button class="arrow" aria-label="往下捲動" onclick={() => expage.next()}>↓</button>
</div>

<style>
  .exhero {
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 0 1.25rem;
  }

  h1 {
    font-family: var(--font-display);
    font-weight: 400;
    line-height: 1.35;
    letter-spacing: 0.06em;
    display: flex;
    flex-direction: column;
  }

  .line {
    font-size: clamp(2rem, 5.4vw, 4rem);
    white-space: nowrap;
  }

  .accent {
    color: var(--steady);
  }

  p {
    margin-top: 1.8rem;
    font-size: 0.95rem;
    line-height: 2;
    font-weight: 700;
    color: var(--ink);
  }

  .arrow {
    margin-top: 3rem;
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
</style>
