import type { CpiItem } from './types'

/** Rebase a series to "first-year average = 100" so every item's line starts
 * from the same visual baseline and is directly comparable across items.
 * Using the first 12 months' average (not a single month) avoids one cheap
 * or expensive month distorting the whole line for volatile items. */
export function rebase(series: number[]): number[] {
  const base = series.slice(0, 12).reduce((a, b) => a + b, 0) / Math.min(12, series.length)
  if (!base) return series.map(() => 100)
  return series.map((v) => (v / base) * 100)
}

export function changeVsStart(rebased: number[]): number {
  const last = rebased[rebased.length - 1]
  return last - 100
}

export interface MonthStat {
  month: number // 1-12
  avg: number
  isMax: boolean
  isMin: boolean
}

/** Average rebased index per calendar month across the full window - answers
 * "which months does this item tend to be expensive/cheap in". */
export function monthlyAverages(item: CpiItem): MonthStat[] {
  const rebased = rebase(item.series)
  const sums = Array(12).fill(0)
  const counts = Array(12).fill(0)
  item.periods.forEach((p, i) => {
    const month = Number(p.split('-')[1]) - 1
    sums[month] += rebased[i]
    counts[month]++
  })
  const avgs = sums.map((s, i) => (counts[i] ? s / counts[i] : 0))
  const max = Math.max(...avgs)
  const min = Math.min(...avgs)
  return avgs.map((avg, i) => ({
    month: i + 1,
    avg,
    isMax: avg === max,
    isMin: avg === min,
  }))
}

export function startYearLabel(periods: string[]): string {
  return periods[0]?.split('-')[0] ?? ''
}
