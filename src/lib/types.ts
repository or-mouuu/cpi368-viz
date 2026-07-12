export type PriceType = 'surge' | 'steady' | 'plateau' | 'wavy' | 'flat' | 'cheaper'

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
  similar?: { id: number; score: number }[]
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

// 宏觀三分：上漲（四種漲相，依「漲勢的時間分布」排序）→ 持平 → 下跌
export const TYPE_ORDER: PriceType[] = ['surge', 'steady', 'plateau', 'wavy', 'flat', 'cheaper']

export const RISING_TYPES: PriceType[] = ['surge', 'steady', 'plateau', 'wavy']

export const TYPE_LABEL: Record<PriceType, string> = {
  surge: '近期急漲',
  steady: '緩緩上漲',
  plateau: '漲後不跌',
  wavy: '波動上漲',
  flat: '沒什麼漲',
  cheaper: '越來越俗',
}

// takes the number of years the data spans (varies by item; see chartMath.yearSpan)
export const TYPE_DESC: Record<PriceType, (years: number) => string> = {
  surge: () => '漲幅大半集中在最近三年',
  steady: (y) => `${y}年來以穩定的速度慢慢變貴`,
  plateau: () => '前段漲完後停在高原，價格再也沒下來',
  wavy: () => '劇烈波動中越墊越高',
  flat: (y) => `${y}年來變動不到10%，幾乎凍住`,
  cheaper: (y) => `比${y}年前更便宜`,
}

/** List-view display name: "其他XXX(YYY等)" items get truncated to "其他XXX"
 * so the card grid isn't cluttered with the parenthetical examples - the
 * full name still shows once you open the detail view. Only applies to
 * names starting with "其他"; a name like "麥片(粉)" keeps its parenthesis. */
export function shortName(name: string): string {
  if (!name.startsWith('其他')) return name
  const i = name.indexOf('(')
  return i === -1 ? name : name.slice(0, i)
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
