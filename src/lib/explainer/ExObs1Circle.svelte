<script lang="ts">
  import Rail from './Rail.svelte'
  import imgController from '../../assets/explainer/e49.svg?url'
  import imgPaper from '../../assets/explainer/e50.svg?url'
  import imgCar from '../../assets/explainer/e51.svg?url'
  import imgHouse from '../../assets/explainer/e52.svg?url'
  import imgShirt from '../../assets/explainer/e53.svg?url'
  import imgApple from '../../assets/explainer/e54.svg?url'

  let { active }: { active: boolean } = $props()

  // arranged around the orange 368 circle per the mockup
  const icons = [
    { src: imgShirt, top: '8%', left: '-8%', w: 118, delay: 0 },
    { src: imgHouse, top: '-12%', left: '32%', w: 130, delay: 0.5 },
    { src: imgController, top: '8%', left: '74%', w: 124, delay: 1.0 },
    { src: imgApple, top: '58%', left: '-10%', w: 116, delay: 0.7 },
    { src: imgPaper, top: '76%', left: '32%', w: 118, delay: 0.2 },
    { src: imgCar, top: '58%', left: '76%', w: 128, delay: 1.3 },
  ]
</script>

<div class="obs">
  <Rail current={1} />

  <div class="text">
    <p class="kicker">觀察1</p>
    <h2>物價指數<br />是怎麼計算出來的？</h2>
    <p class="body">
      消費者物價指數（以下簡稱物價指數）<br />
      是由食衣住行育樂醫共 368 個品項所構成
    </p>
    <p class="body">
      但物價指數的計算<br />
      並不是單純平均 368 個品項的漲幅
    </p>
  </div>

  <div class="visual" class:active>
    <div class="ball">
      <span class="num">368</span>
    </div>
    {#each icons as ic, i (i)}
      <img src={ic.src} alt="" class="icon" style="top:{ic.top}; left:{ic.left}; width:{ic.w}px; animation-delay:{ic.delay}s" />
    {/each}
  </div>
</div>

<style>
  .obs {
    position: relative;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: clamp(2rem, 7vw, 8rem);
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
    position: relative;
    flex: 0 0 auto;
    width: clamp(260px, 30vw, 400px);
    aspect-ratio: 1;
  }

  .ball {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    background: var(--steady);
    display: flex;
    align-items: center;
    justify-content: center;
    transform: scale(0.4);
    opacity: 0;
    transition: transform 0.7s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.5s ease;
  }

  .visual.active .ball {
    transform: scale(1);
    opacity: 1;
  }

  .num {
    font-family: var(--font-display);
    font-size: clamp(3.6rem, 7vw, 6rem);
    color: var(--ink);
  }

  .icon {
    position: absolute;
    opacity: 0;
    transform: translateY(16px);
    transition: opacity 0.5s ease, transform 0.5s ease;
  }

  .visual.active .icon {
    opacity: 1;
    transform: translateY(0);
    animation: float 5s ease-in-out infinite;
  }

  @keyframes float {
    0%,
    100% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(-10px);
    }
  }

  @media (max-width: 900px) {
    .obs {
      flex-direction: column;
      justify-content: center;
      gap: 2rem;
      text-align: center;
    }
    .text {
      flex: 0 0 auto;
    }
    .visual {
      width: min(58vw, 300px);
    }
    .icon {
      width: 24% !important;
    }
  }
</style>
