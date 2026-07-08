<script lang="ts">
  import type { CpiData } from './lib/types'
  import Hero from './lib/Hero.svelte'
  import TypeExplainer from './lib/TypeExplainer.svelte'
  import FilterBar from './lib/FilterBar.svelte'
  import CardGrid from './lib/CardGrid.svelte'
  import DetailOverlay from './lib/DetailOverlay.svelte'

  let data = $state<CpiData | null>(null)
  let error = $state<string | null>(null)

  $effect(() => {
    fetch(`${import.meta.env.BASE_URL}data/items.json`)
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`)
        return r.json()
      })
      .then((d: CpiData) => {
        data = d
      })
      .catch((e) => {
        error = String(e)
      })
  })
</script>

<main>
  {#if error}
    <p class="status error">資料載入失敗：{error}</p>
  {:else if !data}
    <p class="status">載入中…</p>
  {:else}
    <Hero meta={data.meta} />
    <TypeExplainer />
    <FilterBar />
    <CardGrid items={data.items} />
    <DetailOverlay items={data.items} />
  {/if}
</main>

<style>
  .status {
    padding: 4rem 1rem;
    text-align: center;
    font-size: 1rem;
  }
  .status.error {
    color: var(--hot);
  }
</style>
