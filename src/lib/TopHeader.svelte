<script lang="ts">
  import { fullpage } from './fullpage.svelte'
</script>

{#if fullpage.active > 0}
  <header class="topbar">
    <button class="title" onclick={() => fullpage.moveTo(0)}>368種物價漲相大調查</button>
  </header>
{/if}

<style>
  .topbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 44px;
    z-index: 30;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg);
    border-bottom: 1px solid var(--line-soft);
  }

  .title {
    border: none;
    background: none;
    font-size: 0.82rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    color: var(--ink);
  }
</style>
