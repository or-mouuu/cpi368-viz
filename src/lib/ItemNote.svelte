<script lang="ts">
  import type { ItemNote } from './itemNotes'
  import { NOTE_DISCLAIMER } from './itemNotes'

  let { note }: { note: ItemNote } = $props()
  let expanded = $state(false)
</script>

<div class="item-note">
  <p class="summary">{note.summary}</p>
  {#if note.factors.length}
    <button class="toggle" aria-expanded={expanded} onclick={() => (expanded = !expanded)}>
      可能原因 <span class="chev" class:open={expanded}>▾</span>
    </button>
    {#if expanded}
      <ul class="factors">
        {#each note.factors as f (f)}
          <li>{f}</li>
        {/each}
      </ul>
      <p class="disclaimer">{NOTE_DISCLAIMER}</p>
    {/if}
  {/if}
</div>

<style>
  .item-note {
    max-width: 640px;
    margin: 0.5rem auto 0;
    padding: 0 1rem;
    text-align: center;
  }

  .summary {
    font-size: 0.92rem;
    font-weight: 700;
    line-height: 1.6;
    color: var(--ink);
    opacity: 0.9;
  }

  .toggle {
    margin-top: 0.5rem;
    border: none;
    background: none;
    padding: 0.2rem 0.4rem;
    font-family: inherit;
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--ink);
    opacity: 0.6;
    cursor: pointer;
  }

  .chev {
    display: inline-block;
    transition: transform 0.15s ease;
  }
  .chev.open {
    transform: rotate(180deg);
  }

  .factors {
    margin: 0.4rem auto 0;
    max-width: 520px;
    padding-left: 1.1rem;
    text-align: left;
    list-style: disc;
  }

  .factors li {
    font-size: 0.85rem;
    line-height: 1.7;
    color: var(--ink);
    opacity: 0.8;
  }

  .disclaimer {
    margin-top: 0.6rem;
    font-size: 0.72rem;
    line-height: 1.5;
    color: var(--ink);
    opacity: 0.5;
  }
</style>
