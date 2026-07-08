import type { CategoryFilter, CpiItem, PriceType } from './types'

class FilterState {
  type = $state<PriceType | 'all'>('all')
  category = $state<CategoryFilter>('全部')
  categoryOpen = $state(false)

  setType(t: PriceType | 'all') {
    this.type = t
  }

  setCategory(c: CategoryFilter) {
    this.category = c
  }

  toggleCategoryMenu() {
    this.categoryOpen = !this.categoryOpen
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
