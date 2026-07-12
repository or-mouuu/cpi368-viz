<script lang="ts">
  import { fade } from 'svelte/transition'
  import Rail from './Rail.svelte'
  import Pie from './Pie.svelte'

  let { active, step }: { active: boolean; step: number } = $props()

  // step 0 (3-2): all vivid - mid/high freq have ~half >30% risers, low freq ~8%
  // step 1 (3-3): low-freq pie de-emphasized, story on the vivid high/mid pies
  // step 2 (3-4): flipped - the big low-freq pie is the story, others muted
</script>

<div class="obs">
  <Rail current={3} />

  <div class="text">
    <p class="kicker">觀察3</p>
    <h2>「購買頻率」<br />也容易影響漲相判斷</h2>

    {#if step === 0}
      <div in:fade={{ duration: 350 }}>
        <p class="body">
          中、高購買頻率的品項有將近一半漲幅超過 30%，低購買頻率的品項則相對穩定。
        </p>
        <p class="body">換句話說，人們常買的東西漲得特別兇！</p>
      </div>
    {:else if step === 1}
      <div in:fade={{ duration: 350 }}>
        <p class="body">
          人們常買的東西漲得很兇<br />
          但因為權重較小所以對物價指數影響不大
        </p>
        <p class="body">
          權重較大的耐久性商品雖然沒什麼漲<br />
          但因為人們久久才買一次所以感受不明顯
        </p>
      </div>
    {:else}
      <div in:fade={{ duration: 350 }}>
        <p class="body">
          反之低購買頻率的品項漲得相對溫和，<br />
          加上支出占比高（權重大），<br />
          對物價指數的影響較大。
        </p>
        <p class="body">
          因此，這就是物價指數 10 年來只漲 9.9%<br />
          但可能難以反映你的體感物價的原因之一
        </p>
      </div>
    {/if}

    <div class="legend">
      {#if step < 2}
        <span class="key" in:fade={{ duration: 250 }}><i class="sw ink"></i>漲幅30%以下</span>
        <span class="key" in:fade={{ duration: 250 }}><i class="sw up"></i>漲幅超過30%</span>
      {:else}
        <span class="key" in:fade={{ duration: 250 }}><i class="sw ink"></i>漲幅不到10%</span>
        <span class="key" in:fade={{ duration: 250 }}><i class="sw pale"></i>漲幅10%-30%</span>
        <span class="key" in:fade={{ duration: 250 }}><i class="sw up"></i>漲幅30%以上</span>
      {/if}
    </div>
  </div>

  <div class="visual" class:active>
    <div class="pie low" class:dim={step === 1}>
      <span class="plabel rot-l" class:dimtext={step === 1}>低購買頻率</span>
      <Pie fraction={0.08} size={300} {active} muted={step === 1} />
    </div>
    <div class="pie high" class:dim={step === 2}>
      <span class="plabel rot-r" class:dimtext={step === 2}>高購買頻率</span>
      <Pie fraction={0.45} size={210} {active} muted={step === 2} />
    </div>
    <div class="pie mid" class:dim={step === 2}>
      <span class="plabel rot-r" class:dimtext={step === 2}>中購買頻率</span>
      <Pie fraction={0.42} size={200} {active} muted={step === 2} />
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
    gap: clamp(2rem, 5vw, 6rem);
    padding: 0 clamp(1rem, 7vw, 8rem);
  }

  .text {
    flex: 0 1 470px;
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

  .legend {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-top: 1.6rem;
  }

  .key {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.8rem;
    font-weight: 700;
  }

  .sw {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    display: inline-block;
  }

  .sw.ink {
    background: var(--ink);
  }

  .sw.up {
    background: var(--steady);
  }

  .sw.pale {
    background: #f2cdb8;
  }

  .visual {
    position: relative;
    flex: 0 0 auto;
    width: clamp(330px, 40vw, 580px);
    aspect-ratio: 1.12;
    opacity: 0;
    transition: opacity 0.6s ease;
  }

  .visual.active {
    opacity: 1;
  }

  .pie {
    position: absolute;
    transition: opacity 0.5s ease;
  }

  .pie.low {
    left: 0;
    top: 22%;
  }

  .pie.high {
    right: 4%;
    top: 0;
  }

  .pie.mid {
    right: 7%;
    bottom: 2%;
  }

  .plabel {
    position: absolute;
    font-size: 0.92rem;
    font-weight: 900;
    white-space: nowrap;
    transition: color 0.5s ease;
  }

  .plabel.rot-l {
    left: -6%;
    top: 4%;
    transform: rotate(-32deg);
  }

  .plabel.rot-r {
    right: -4%;
    top: 2%;
    transform: rotate(30deg);
  }

  .plabel.dimtext {
    color: rgba(23, 20, 15, 0.3);
  }

  .pie :global(svg) {
    max-width: none;
  }

  @media (max-width: 1100px) {
    .pie.low :global(svg) {
      width: 240px;
      height: 240px;
    }
    .pie.high :global(svg),
    .pie.mid :global(svg) {
      width: 165px;
      height: 165px;
    }
  }

  @media (max-width: 900px) {
    .obs {
      flex-direction: column;
      gap: 1rem;
      text-align: center;
    }
    .legend {
      justify-content: center;
    }
    .visual {
      width: min(88vw, 400px);
    }
    .pie.low :global(svg) {
      width: 190px;
      height: 190px;
    }
    .pie.high :global(svg),
    .pie.mid :global(svg) {
      width: 130px;
      height: 130px;
    }
  }
</style>
