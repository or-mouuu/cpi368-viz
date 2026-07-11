export type PriceType = 'steady' | 'plateau' | 'surge' | 'wavy' | 'flat' | 'cheaper'

export interface CpiItem {
  id: number
  name: string
  category: string
  type: PriceType
  change10y: number
  volatility: number
  volatile: boolean
  event: boolean
  series: number[]
  periods: string[]
}

export interface CpiMeta {
  itemCount: number
  dataStart: string
  dataEnd: string
  baseYear: number
  basePeriod: string
  source: string
}

export interface CpiData {
  meta: CpiMeta
  items: CpiItem[]
}

// 宏觀三分：上漲（四種漲相）→ 持平 → 下跌
export const TYPE_ORDER: PriceType[] = ['steady', 'plateau', 'surge', 'wavy', 'flat', 'cheaper']

export const RISING_TYPES: PriceType[] = ['steady', 'plateau', 'surge', 'wavy']

export const TYPE_LABEL: Record<PriceType, string> = {
  steady: '持續上漲',
  plateau: '漲後不跌',
  surge: '近期急漲',
  wavy: '波動上漲',
  flat: '價格持平',
  cheaper: '越來越俗',
}

// takes the number of years the data spans (varies by item; see chartMath.yearSpan)
export const TYPE_DESC: Record<PriceType, (years: number) => string> = {
  steady: (y) => `${y}年來全程持續變貴，不知不覺回不去`,
  plateau: () => '前段漲完後停在高原，價格再也沒下來',
  surge: () => '漲幅大半集中在最近三年',
  wavy: () => '劇烈波動中越墊越高',
  flat: (y) => `${y}年來變動不到10%，幾乎凍住`,
  cheaper: (y) => `比${y}年前更便宜`,
}

export const CATEGORY_ORDER = [
  '全部',
  '食物類',
  '衣著類',
  '居住類',
  '交通及通訊類',
  '醫藥保健類',
  '教養娛樂類',
  '雜項類',
] as const

export type CategoryFilter = (typeof CATEGORY_ORDER)[number]
