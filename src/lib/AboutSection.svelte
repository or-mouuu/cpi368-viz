<script lang="ts">
  import type { CpiMeta } from './types'
  import { fullpage } from './fullpage.svelte'
  import { metaYearSpan } from './chartMath'

  let { meta }: { meta: CpiMeta } = $props()
  const years = $derived(metaYearSpan(meta.dataStart, meta.dataEnd))

  let scroller = $state<HTMLElement | null>(null)
  $effect(() => {
    if (fullpage.active === 4) {
      fullpage.scrollerEl = scroller
    }
  })
</script>

<div class="about">
  <div class="inner" bind:this={scroller}>
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
        每個品項以 12 個月移動平均計算趨勢線，將「長線趨勢」與「季節震盪」分開衡量，再依形狀特徵分類：
        {years} 年趨勢漲逾 15% 為「上漲」，其中近三年貢獻過半漲幅、或近期斜率劇烈變陡者為<b>近期急漲</b>；
        曾有階梯式跳漲或早期已漲完，且近一年幾乎不再漲的品項為<b>漲後不跌</b>；
        原始資料逐月波動極大、或趨勢線反覆曲折且從高點回落者為<b>波動上漲</b>；其餘為<b>緩緩上漲</b>。
        {years} 年變動在 −5%～+15% 之間為<b>沒什麼漲</b>，低於 −5% 為<b>越來越俗</b>。
      </p>
      <details class="methodology-details">
        <summary>詳細分類計算方式說明</summary>
        <div class="details-content">
          <p>為了將主觀的「漲相」轉化為量化指標，我們將每個品項的原始價格指數（Series）取 12 個月移動平均以消弭季節性，形成趨勢線（Trend），再以演算法逐一過濾：</p>
          <ul class="methodology-list">
            <li>
              <strong>基礎特徵</strong>：
              <ul class="methodology-sublist">
                <li><strong>總漲幅 (change10y)</strong>：趨勢線終點相對於起點的變化率。</li>
                <li><strong>近期漲幅佔比 (late3)</strong>：近三年漲幅佔總漲幅的比例。</li>
                <li><strong>近期動能 (momentum)</strong>：近一年的趨勢漲幅。</li>
                <li><strong>波段跳躍 (jump)</strong>：12 個月內的最大漲幅，並計算其佔總漲幅的比例。</li>
                <li><strong>波動與折返 (volatility & wiggles)</strong>：原始數值的月變動標準差（波動度），以及趨勢線上大於 1% 的方向折返次數。</li>
              </ul>
            </li>
            <li>
              <strong>判定門檻與順序</strong>：
              <ol class="methodology-sublist">
                <li><strong>越來越俗 / 沒什麼漲</strong>：總漲幅低於 -5% 為「越來越俗」，介於 -5%～15% 為「沒什麼漲」。大於 15% 進入上漲組分類。</li>
                <li><strong>波動上漲 (Wavy)</strong>：原始波動度大於 3.5% 或趨勢折返超過 12 次。若曾大幅上漲但近期顯著回落（retrace > 25%）且未達高原期標準，亦屬此類。</li>
                <li><strong>漲後不跌 (Plateau)</strong>：近期動能極低（momentum &lt; 4.0），且曾出現集中式的波段跳躍（jump 佔比 &gt; 35%），或早期跳漲後近三年幾乎停滯（late3 &le; 0.25）。（此判定會自動剔除超高波動度的例外品項）</li>
                <li><strong>近期急漲 (Surge)</strong>：近三年貢獻了過半漲幅（late3 &ge; 0.52），或近期斜率劇烈變陡（slope2 &gt; 2.7 且 late3 &ge; 0.48）。例外優先權：若近一年動能極端強勢（momentum &ge; 10.0），則無條件觸發此分類。</li>
                <li><strong>緩緩上漲 (Steady)</strong>：漲幅超過 15% 且不符合以上任何極端特徵，呈現線性或階梯式平穩上漲者。</li>
              </ol>
            </li>
          </ul>
        </div>
      </details>
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

  .methodology-details {
    margin-top: 1.5rem;
    background: rgba(0, 0, 0, 0.03);
    border-radius: 8px;
    padding: 0.8rem 1.2rem;
    font-size: 0.85rem;
  }

  .methodology-details summary {
    font-weight: 700;
    cursor: pointer;
    user-select: none;
    outline: none;
  }

  .methodology-details summary:hover {
    color: var(--brand);
  }

  .details-content {
    margin-top: 1rem;
    line-height: 1.7;
  }

  .details-content p {
    margin-bottom: 0.8rem;
  }

  .methodology-list {
    padding-left: 1.2rem;
    margin-bottom: 1rem;
  }

  .methodology-list > li {
    margin-bottom: 0.8rem;
  }

  .methodology-sublist {
    padding-left: 1.2rem;
    margin-top: 0.4rem;
  }

  .methodology-sublist li {
    margin-bottom: 0.3rem;
  }
</style>
