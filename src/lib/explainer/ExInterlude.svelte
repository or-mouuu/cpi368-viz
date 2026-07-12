<script lang="ts">
  let { active }: { active: boolean } = $props()
</script>

<div class="interlude" class:active>
  <p>
    由此可知，每個品項的漲幅<br />
    影響物價指數的程度都不同
  </p>
  <p class="second">但這和體感物價有什麼關係呢？</p>
</div>

<style>
  .interlude {
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 0 1.25rem;
  }

  p {
    font-size: clamp(1.25rem, 2.5vw, 1.9rem);
    font-weight: 900;
    line-height: 1.75;
    opacity: 0;
    transform: translateY(14px);
    transition: opacity 0.6s ease, transform 0.6s ease;
  }

  .second {
    margin-top: 2.2rem;
    transition-delay: 0.35s;
  }

  .interlude.active p {
    opacity: 1;
    transform: translateY(0);
  }
</style>
