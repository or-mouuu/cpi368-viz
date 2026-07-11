import type { CategoryFilter, CpiItem, PriceType } from './types'

export type SortMode = 'default' | 'change_desc' | 'change_asc'

class FilterState {
  type = $state<PriceType | 'all'>('all')
  category = $state<CategoryFilter>('全部')
  categoryOpen = $state(false)
  search = $state('')
  sort = $state<SortMode>('default')

  setType(t: PriceType | 'all') {
    this.type = t
  }

  setCategory(c: CategoryFilter) {
    this.category = c
  }

  toggleCategoryMenu() {
    this.categoryOpen = !this.categoryOpen
  }

  setSearch(q: string) {
    this.search = q
  }

  setSort(s: SortMode) {
    this.sort = s
  }
}

export const filterState = new FilterState()

class DetailState {
  activeId = $state<number | null>(null)

  open(id: number) {
    this.activeId = id
  }

  close() {
    this.activeId = null
  }
}

export const detailState = new DetailState()

export function matchesFilter(item: CpiItem, type: PriceType | 'all', category: CategoryFilter): boolean {
  if (type !== 'all' && item.type !== type) return false
  if (category !== '全部' && item.category !== category) return false
  return true
}

export function matchesSearch(item: CpiItem, query: string): boolean {
  if (!query.trim()) return true
  return item.name.toLowerCase().includes(query.trim().toLowerCase())
}

export function sortItems(items: CpiItem[], sort: SortMode): CpiItem[] {
  if (sort === 'default') return items
  const sorted = [...items]
  sorted.sort((a, b) => (sort === 'change_desc' ? b.change10y - a.change10y : a.change10y - b.change10y))
  return sorted
}
