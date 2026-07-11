<script lang="ts">
  import { fullpage, SECTION_COUNT } from './fullpage.svelte'

  const labels = ['首頁', '關於漲相', '三種方向', '上漲的漲相', '探索全部品項', '方法說明']
</script>

<nav class="dots" aria-label="頁面導航">
  {#each Array(SECTION_COUNT) as _, i (i)}
    <button
      class="dot"
      class:active={fullpage.active === i}
      aria-label={labels[i]}
      title={labels[i]}
      onclick={() => fullpage.moveTo(i)}
    ></button>
  {/each}
</nav>

<style>
  .dots {
    position: fixed;
    right: 14px;
    top: 50%;
    transform: translateY(-50%);
    z-index: 40;
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 8px 6px;
    background: rgba(239, 236, 225, 0.85);
    border-radius: 999px;
  }

  .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    border: none;
    padding: 0;
    background: rgba(23, 20, 15, 0.25);
    transition: transform 0.2s ease, background 0.2s ease;
  }

  .dot.active {
    background: var(--ink);
    transform: scale(1.5);
  }

  @media (max-width: 640px) {
    .dots {
      right: 8px;
    }
  }
</style>
