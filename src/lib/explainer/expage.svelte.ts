// Snap-scroll controller for the explainer page. Same one-gesture-one-move
// feel as the main page's fullpage controller, plus per-section "steps":
// a section can declare N internal steps (e.g. the weights example that
// mutates $60 -> $63 in place); scrolling advances the step first and only
// moves to the next section once the steps are exhausted.

export const EX_STEPS = [1, 1, 2, 1, 2, 1, 3] as const
export const EX_SECTION_COUNT = EX_STEPS.length

const TRANSITION_MS = 600
const WHEEL_THRESHOLD = 60

class ExplainerPageState {
  active = $state(0)
  step = $state(0) // step within the active section

  #cooldownUntil = 0
  #wheelAccum = 0
  #touchStartY = 0

  moveTo(index: number) {
    const clamped = Math.max(0, Math.min(EX_SECTION_COUNT - 1, index))
    if (clamped === this.active) return
    this.active = clamped
    this.step = 0
    this.#cooldownUntil = performance.now() + TRANSITION_MS + 100
  }

  next() {
    if (this.step < EX_STEPS[this.active] - 1) {
      this.step += 1
      this.#cooldownUntil = performance.now() + TRANSITION_MS
      return
    }
    if (this.active < EX_SECTION_COUNT - 1) {
      this.active += 1
      this.step = 0
      this.#cooldownUntil = performance.now() + TRANSITION_MS + 100
    }
  }

  prev() {
    if (this.step > 0) {
      this.step -= 1
      this.#cooldownUntil = performance.now() + TRANSITION_MS
      return
    }
    if (this.active > 0) {
      this.active -= 1
      // land on the last step of the previous section so backing up replays
      // its final state rather than resetting it
      this.step = EX_STEPS[this.active] - 1
      this.#cooldownUntil = performance.now() + TRANSITION_MS + 100
    }
  }

  handleWheel(e: WheelEvent) {
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
    if (e.key === 'ArrowDown' || e.key === 'PageDown') {
      e.preventDefault()
      this.next()
    } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
      e.preventDefault()
      this.prev()
    }
  }

  handleTouchStart(e: TouchEvent) {
    this.#touchStartY = e.touches[0].clientY
  }

  handleTouchEnd(e: TouchEvent) {
    const dy = this.#touchStartY - e.changedTouches[0].clientY
    if (Math.abs(dy) < 100) return
    if (dy > 0) this.next()
    else this.prev()
  }
}

export const expage = new ExplainerPageState()
