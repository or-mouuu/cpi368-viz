export interface ItemNote {
  /** One-line takeaway, always shown. */
  summary: string
  /** Possible contributing factors, revealed on expand. */
  factors: string[]
}

/** Hand-written editorial notes keyed by CpiItem.id (the stable CPI code).
 * Kept separate from public/data/items.json, which the pipeline regenerates
 * every month. These are "possible reasons", deliberately hedged — prices move
 * on many factors at once, so nothing here is the single or definitive cause. */
export const itemNotes: Record<number, ItemNote> = {
  11: {
    summary: '十年來明顯上漲，可能與飼養成本與供給波動有關。',
    factors: [
      '飼料（進口玉米、黃豆）成本隨國際行情與匯率上升',
      '非洲豬瘟防疫下的供給與進口管制調整',
      '人力、運輸等產業鏈成本墊高',
    ],
  },
  20: {
    summary: '長期緩漲，但漲幅其實集中在幾次「蛋荒」——尤其 2023 年前後。',
    factors: [
      '2023 年前後禽流感與氣候使產量驟減、出現缺蛋與快速跳漲',
      '飼料成本受國際行情與匯率牽動',
      '颱風、寒流等短期衝擊與產銷調節',
    ],
  },
  30: {
    summary: '以進口為主，價格主要受國際養殖與物流成本牽動。',
    factors: [
      '幾乎全數仰賴進口（智利、挪威等），受國際鮭魚產量與價格影響',
      '空運、冷鏈與國際運費波動',
      '匯率變化影響進口成本',
    ],
  },
  244: {
    summary: '均價一路走低，可能不是手機變便宜，而是市場結構改變。',
    factors: [
      '中低價位機種（含中國品牌）市占提高，拉低平均成交價',
      '統計以「代表性機種」計價，主流機種下移即帶動均價下降',
      '品質校正下，同價位規格提升會被視為「變便宜」',
    ],
  },
  289: {
    summary: '十年幾乎沒漲，屬於競爭激烈、技術成熟的品項。',
    factors: [
      '品牌與通路競爭激烈、日拋等產品大量供應壓低單價',
      '製程成熟、規模化生產使成本相對穩定',
      '促銷與量販常態化',
    ],
  },
  345: {
    summary: '溫和上漲，主要與原物料（紙漿）成本與一次性搶購事件有關。',
    factors: [
      '國際紙漿、能源與運費波動傳導到售價',
      '2018 年「衛生紙之亂」等搶購造成短期跳漲',
      '匯率影響進口紙漿成本',
    ],
  },
}

/** Shown once at the bottom of every note's expanded section. */
export const NOTE_DISCLAIMER = '物價成因複雜，以上為可能因素、非唯一或確定的解釋。'
