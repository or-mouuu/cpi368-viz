<script lang="ts">
  import { fullpage } from './fullpage.svelte'
  import type { CpiMeta } from './types'

  let { meta }: { meta: CpiMeta } = $props()
</script>

<div class="intro">
  <p class="statement">
    自{meta.baseYear}年以來，多數東西都變貴了。<br />
    但比「漲多少」更值得看的，是「怎麼漲」——<br />
    有的<span class="t-surge">近期急漲</span>、有的<span class="t-steady">緩緩上漲</span>、<br
    />有的<span class="t-plateau">漲後不跌</span>、有的<span class="t-wavy">波動上漲</span>，<br />
    也有東西<span class="t-flat">沒什麼漲</span>，甚至<span class="t-cheaper">越來越俗</span>。
  </p>

  <button class="explore" onclick={() => fullpage.next()}>
    <span>繼續看</span>
    <span class="chev">⌄</span>
  </button>
</div>

<style>
  .intro {
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 1.5rem;
    position: relative;
  }

  .statement {
    max-width: 880px;
    font-size: clamp(1.3rem, 3.2vw, 2.2rem);
    font-weight: 800;
    line-height: 1.75;
    text-align: left;
  }


  .t-steady {
    color: var(--steady);
  }
  .t-plateau {
    color: var(--plateau);
  }
  .t-surge {
    color: var(--surge);
  }
  .t-wavy {
    color: var(--wavy);
  }
  .t-flat {
    color: var(--flat);
  }
  .t-cheaper {
    color: var(--cheaper);
  }

  .explore {
    position: absolute;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%);
    border: none;
    background: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0;
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--ink);
  }

  .chev {
    font-size: 1.5rem;
    line-height: 0.8;
    animation: bob 1.6s ease-in-out infinite;
  }

  @keyframes bob {
    0%,
    100% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(5px);
    }
  }
</style>
