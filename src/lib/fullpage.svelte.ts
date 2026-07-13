// fullPage-style section snap controller: one wheel gesture / key press / swipe
// moves exactly one section, with an eased transform transition. A section can
// opt into internal free scrolling (the explorer grid); section changes then
// only happen when its inner scroller hits an edge.

export const SECTION_COUNT = 5
export const EXPLORER_INDEX = 3 // the free-scrolling grid section

const TRANSITION_MS = 600
const WHEEL_THRESHOLD = 60 // accumulated deltaY before a move triggers

class FullPageState {
  active = $state(0)
  animating = $state(false)
  // set by DetailOverlay so arrow keys navigate items instead of sections
  navLocked = $state(false)

  #cooldownUntil = 0
  #wheelAccum = 0
  #touchStartY = 0

  scrollerEl: HTMLElement | null = null // explorer's inner scroller

  moveTo(index: number) {
    const clamped = Math.max(0, Math.min(SECTION_COUNT - 1, index))
    if (clamped === this.active || this.animating) return
    this.active = clamped
    this.animating = true
    this.#cooldownUntil = performance.now() + TRANSITION_MS + 100
    setTimeout(() => {
      this.animating = false
    }, TRANSITION_MS)
  }

  next() {
    this.moveTo(this.active + 1)
  }
  prev() {
    this.moveTo(this.active - 1)
  }

  #scrollerAtTop(): boolean {
    return !this.scrollerEl || this.scrollerEl.scrollTop <= 1
  }
  #scrollerAtBottom(): boolean {
    if (!this.scrollerEl) return true
    const { scrollTop, scrollHeight, clientHeight } = this.scrollerEl
    return scrollTop + clientHeight >= scrollHeight - 1
  }

  handleWheel(e: WheelEvent) {
    if (this.navLocked) return
    const hasScroller = this.active === EXPLORER_INDEX || this.active === SECTION_COUNT - 1
    if (hasScroller) {
      // let the inner scroller consume the event unless it's at an edge
      if (e.deltaY > 0 && !this.#scrollerAtBottom()) return
      if (e.deltaY < 0 && !this.#scrollerAtTop()) return
    }
    e.preventDefault()
    if (performance.now() < this.#cooldownUntil) return
    this.#wheelAccum += e.deltaY
    if (this.#wheelAccum > WHEEL_THRESHOLD) {
      this.#wheelAccum = 0
      this.next()
    } else if (this.#wheelAccum < -WHEEL_THRESHOLD) {
      this.#wheelAccum = 0
      this.prev()
    }
  }

  handleKey(e: KeyboardEvent) {
    if (this.navLocked) return
    const hasScroller = this.active === EXPLORER_INDEX || this.active === SECTION_COUNT - 1
    if (e.key === 'ArrowDown' || e.key === 'PageDown') {
      if (hasScroller && !this.#scrollerAtBottom()) return
      e.preventDefault()
      this.next()
    } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
      if (hasScroller && !this.#scrollerAtTop()) return
      e.preventDefault()
      this.prev()
    }
  }

  handleTouchStart(e: TouchEvent) {
    this.#touchStartY = e.touches[0].clientY
  }

  handleTouchEnd(e: TouchEvent) {
    if (this.navLocked) return
    const dy = this.#touchStartY - e.changedTouches[0].clientY
    if (Math.abs(dy) < 100) return
    const hasScroller = this.active === EXPLORER_INDEX || this.active === SECTION_COUNT - 1
    if (hasScroller) {
      if (dy > 0 && !this.#scrollerAtBottom()) return
      if (dy < 0 && !this.#scrollerAtTop()) return
    }
    if (dy > 0) this.next()
    else this.prev()
  }
}

export const fullpage = new FullPageState()
