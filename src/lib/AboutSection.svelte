<script lang="ts">
  import type { CpiMeta } from './types'
  import { fullpage } from './fullpage.svelte'
  import { metaYearSpan } from './chartMath'

  let { meta }: { meta: CpiMeta } = $props()
  const years = $derived(metaYearSpan(meta.dataStart, meta.dataEnd))
</script>

<div class="about">
  <div class="inner">
    <div class="main">
      <h2>方法說明</h2>
      <p>
        本站資料來自行政院主計總處「消費者物價基本分類暨項目群指數」（經
        <a href="https://data.gov.tw/dataset/9158" target="_blank" rel="noreferrer">政府資料開放平臺</a>
        發布），涵蓋 CPI 架構下 368 個項目群的月指數，基期為民國110年（2021）＝100，資料回溯至 {meta.baseYear}
        年（資料源最早可查年份）。每月 10 日自動抓取最新資料。目前呈現 {meta.itemCount} 項：少數品項因
        {meta.baseYear} 年後才納入查價、或歷史資料過於稀疏而未分類。
      </p>
      <p>
        每個品項以 12 個月移動平均計算趨勢線，將「趨勢怎麼走」與「圍繞趨勢的季節震盪」分開衡量，再依規則分類：
        {years} 年趨勢漲逾 10% 為「上漲」，其中波動度大於 15% 者為<b>波動上漲</b>；漲幅過半集中在近三年者為<b>近期急漲</b>；
        漲幅早已完成、近一年幾乎不再漲者為<b>漲後不跌</b>；其餘為<b>持續上漲</b>。{years} 年變動在 −5%～+10% 之間為<b>價格持平</b>，低於
        −5% 為<b>越來越俗</b>。
      </p>
      <p>
        曾漲逾兩成後又吐回四成以上漲幅的 6 個品項（雞蛋、蒜頭、西瓜、馬鈴薯、綠花椰菜、火龍果）另以 ⚡
        標記；趨勢持平或下跌但劇烈震盪者以 〰️ 標記。
      </p>
      <p class="caveat">
        注意：指數反映「價格變動」而非「價格水準」，品項之間只能比誰漲得多、不能比誰比較貴；門檻為觀察分布後的人工選點，分類應理解為性格光譜上的分段。
      </p>
    </div>

    <aside class="side">
      <h3>資料</h3>
      <p>
        <a href="https://data.gov.tw/dataset/9158" target="_blank" rel="noreferrer">消費者物價基本分類暨項目群指數</a
        ><br />行政院主計總處
      </p>
      <p class="range">資料期間：{meta.dataStart} ~ {meta.dataEnd}</p>
      <h3>原始碼</h3>
      <p>
        <a href="https://github.com/or-mouuu/cpi368-viz" target="_blank" rel="noreferrer">GitHub</a>
      </p>
    </aside>
  </div>

  <button class="back-top" onclick={() => fullpage.moveTo(0)}>
    <span class="chev">⌃</span>
    <span>回到頂端</span>
  </button>
</div>

<style>
  .about {
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 1.5rem 2rem;
    position: relative;
  }

  .inner {
    display: grid;
    grid-template-columns: minmax(0, 2fr) minmax(180px, 1fr);
    gap: 3rem;
    max-width: 880px;
    overflow-y: auto;
  }

  @media (max-width: 700px) {
    .inner {
      grid-template-columns: 1fr;
      gap: 1.5rem;
    }
  }

  h2 {
    font-size: 1.3rem;
    font-weight: 900;
    margin-bottom: 1rem;
  }

  .main p {
    font-size: 0.88rem;
    line-height: 1.85;
    margin-bottom: 1rem;
  }

  .caveat {
    font-size: 0.78rem !important;
    opacity: 0.65;
  }

  .side h3 {
    font-size: 0.95rem;
    font-weight: 900;
    margin-bottom: 0.4rem;
  }

  .side p {
    font-size: 0.85rem;
    line-height: 1.7;
    margin-bottom: 1.2rem;
  }

  .range {
    font-size: 0.75rem !important;
    opacity: 0.6;
  }

  a {
    color: var(--ink);
    text-underline-offset: 3px;
  }

  .back-top {
    position: absolute;
    bottom: 1.6rem;
    left: 50%;
    transform: translateX(-50%);
    border: none;
    background: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--ink);
  }

  .chev {
    font-size: 1.4rem;
    line-height: 0.7;
  }
</style>
