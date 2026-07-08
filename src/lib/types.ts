export type PriceType = 'hot' | 'normal' | 'falling' | 'seasonal'

export interface CpiItem {
  id: number
  name: string
  category: string
  type: PriceType
  change10y: number
  seasonalVar: number
  series: number[]
  periods: string[]
}

export interface CpiMeta {
  itemCount: number
  dataStart: string
  dataEnd: string
  basePeriod: string
  source: string
}

export interface CpiData {
  meta: CpiMeta
  items: CpiItem[]
}

export const TYPE_ORDER: PriceType[] = ['hot', 'normal', 'falling', 'seasonal']

export const TYPE_LABEL: Record<PriceType, string> = {
  hot: '漲相很兇',
  normal: '漲相普通',
  falling: '漲相下跌',
  seasonal: '漲相隨季節',
}

export const TYPE_DESC: Record<PriceType, string> = {
  hot: '和10年前相比漲幅超過15%',
  normal: '和10年前相比漲幅介於0–15%',
  falling: '和10年前相比價格下跌',
  seasonal: '價格隨季節劇烈波動（12個月VAR>100）',
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
