// Shared reactive "is this a mobile-width viewport" flag (matchMedia-backed).
const mq = typeof window !== 'undefined' ? window.matchMedia('(max-width: 700px)') : null

class Viewport {
  mobile = $state(mq ? mq.matches : false)
  constructor() {
    mq?.addEventListener('change', (e) => (this.mobile = e.matches))
  }
}

export const viewport = new Viewport()
