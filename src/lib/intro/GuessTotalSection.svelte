<script lang="ts">
  import { tweened } from 'svelte/motion'
  import { cubicOut } from 'svelte/easing'
  import type { CpiMeta } from '../types'
  import { fullpage } from '../fullpage.svelte'

  let { meta }: { meta: CpiMeta } = $props()

  const MAX = 60

  let phase = $state<'guess' | 'reveal'>('guess')
  let guess = $state(20)
  let showNext = $state(false)

  const real = tweened(0, { duration: 1400, easing: cubicOut })

  const guessPct = $derived(Math.min(100, (guess / MAX) * 100))
  const realPct = $derived(Math.min(100, ($real / MAX) * 100))

  function confirm() {
    phase = 'reveal'
    showNext = false
    real.set(meta.totalChange).then(() => {
      showNext = true
    })
  }

  function diffText(): string {
    const diff = guess - meta.totalChange
    if (Math.abs(diff) < 3) return '你很準！'
    if (diff > 0) return `其實沒你想的多，你多估了 ${diff.toFixed(1)} 個百分點`
    return `你少估了 ${Math.abs(diff).toFixed(1)} 個百分點`
  }
</script>

<div class="guess-total">
  <h1 class="headline">漲得跟你想得一樣嗎？</h1>
  <p class="sub">你覺得從 {meta.baseYear} 年到現在，整體物價漲了幾 %？</p>

  {#if phase === 'guess'}
    <div class="guess-area">
      <div class="big-number">{guess}<span class="pct-sign">%</span></div>
      <div class="bar-track">
        <div class="bar-fill" style="width:{guessPct}%"></div>
      </div>
      <input
        type="range"
        min="0"
        max={MAX}
        step="1"
        bind:value={guess}
        class="slider"
        aria-label="你的猜測百分比"
      />
      <button class="confirm" onclick={confirm}>確認</button>
    </div>
  {:else}
    <div class="reveal-area">
      <div class="compare-row">
        <div class="compare-col">
          <p class="compare-label">你的猜測</p>
          <div class="bar-track">
            <div class="bar-fill guess-fill" style="width:{guessPct}%"></div>
          </div>
          <p class="compare-value">{guess}%</p>
        </div>
        <div class="compare-col">
          <p class="compare-label">真實值</p>
          <div class="bar-track">
            <div class="bar-fill real-fill" style="width:{realPct}%"></div>
          </div>
          <p class="compare-value">{$real.toFixed(2)}%</p>
        </div>
      </div>
      <p class="diff-text">{diffText()}</p>
      <p class="bridge">
        官方說整體只漲了 {meta.totalChange}%，但等等你會看到很多東西漲得比這兇得多
      </p>
      {#if showNext}
        <button class="next" onclick={() => fullpage.next()}>下一個 ↓</button>
      {/if}
    </div>
  {/if}
</div>

<style>
  .guess-total {
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2.5rem 1.5rem;
    text-align: center;
  }

  .headline {
    font-family: var(--font-body);
    font-weight: 900;
    font-size: clamp(1.6rem, 4vw, 2.6rem);
    line-height: 1.3;
  }

  .sub {
    margin-top: 0.9rem;
    font-size: clamp(0.95rem, 1.8vw, 1.15rem);
    font-weight: 700;
    opacity: 0.85;
  }

  .guess-area,
  .reveal-area {
    margin-top: 2.4rem;
    width: 100%;
    max-width: 460px;
  }

  .big-number {
    font-family: var(--font-numeric);
    font-size: clamp(3.2rem, 10vw, 5.5rem);
    font-weight: 700;
    line-height: 1;
    color: var(--steady);
  }

  .pct-sign {
    font-size: 0.5em;
    margin-left: 0.15em;
  }

  .bar-track {
    margin-top: 1rem;
    height: 22px;
    border: 1px solid var(--line);
    border-radius: 999px;
    overflow: hidden;
    background: var(--bg-card);
  }

  .bar-fill {
    height: 100%;
    background: var(--steady);
    transition: width 60ms linear;
  }

  .slider {
    margin-top: 1.6rem;
    width: 100%;
    accent-color: var(--steady);
  }

  .confirm,
  .next {
    margin-top: 1.8rem;
    border: none;
    background: var(--ink);
    color: var(--bg);
    padding: 0.7rem 2rem;
    font-size: 0.95rem;
    font-weight: 800;
    border-radius: 999px;
  }

  .compare-row {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
  }

  .compare-col {
    text-align: left;
  }

  .compare-label {
    font-size: 0.8rem;
    font-weight: 700;
    opacity: 0.65;
    margin-bottom: 0.35rem;
  }

  .guess-fill {
    background: var(--line);
    opacity: 0.55;
  }

  .real-fill {
    background: var(--steady);
  }

  .compare-value {
    margin-top: 0.35rem;
    font-family: var(--font-numeric);
    font-weight: 700;
    font-size: 1.1rem;
  }

  .diff-text {
    margin-top: 1.5rem;
    font-size: 1.05rem;
    font-weight: 800;
    color: var(--steady);
  }

  .bridge {
    margin-top: 1.1rem;
    font-size: 0.85rem;
    opacity: 0.75;
    line-height: 1.6;
  }

  @media (max-width: 560px) {
    .guess-area,
    .reveal-area {
      max-width: 320px;
    }
  }
</style>
