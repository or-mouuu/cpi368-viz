<script lang="ts">
  import type { CpiData } from './lib/types'
  import MainPage from './lib/MainPage.svelte'
  import ExplainerPage from './lib/explainer/ExplainerPage.svelte'

  let data = $state<CpiData | null>(null)
  let error = $state<string | null>(null)

  // tiny hash router: '' -> 大調查, '#/explainer' -> explainer
  let route = $state(location.hash)

  $effect(() => {
    const onHash = () => {
      route = location.hash
    }
    window.addEventListener('hashchange', onHash)
    return () => window.removeEventListener('hashchange', onHash)
  })

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

{#if error}
  <p class="status error">資料載入失敗：{error}</p>
{:else if !data}
  <p class="status">載入中…</p>
{:else if route.startsWith('#/explainer')}
  <ExplainerPage />
{:else}
  <MainPage {data} />
{/if}

<style>
  .status {
    padding: 4rem 1rem;
    text-align: center;
    font-size: 1rem;
  }
  .status.error {
    color: var(--steady);
  }
</style>
