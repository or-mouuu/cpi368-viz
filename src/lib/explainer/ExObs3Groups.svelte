<script lang="ts">
  import Rail from './Rail.svelte'
  import imgBread from '../../assets/hero/item02.svg?url'
  import imgBroccoli from '../../assets/hero/item13.svg?url'
  import imgDrink from '../../assets/hero/item14.svg?url'
  import imgPill from '../../assets/hero/item01.svg?url'
  import imgPlant from '../../assets/hero/item09.svg?url'
  import imgLaptop from '../../assets/hero/item10.svg?url'
  import imgTissue from '../../assets/hero/item12.svg?url'
  import imgSoap from '../../assets/hero/item11.svg?url'

  let { active }: { active: boolean } = $props()

  const groups = [
    {
      key: 'high',
      label: '高購買頻率',
      sub: '每月至少購買1次',
      pos: 'top: 4%; left: 42%;',
      labelSide: 'right',
      icons: [
        { src: imgBread, style: 'top:8%; left:14%; width:52%; transform:rotate(-8deg)' },
        { src: imgBroccoli, style: 'top:46%; left:6%; width:44%' },
        { src: imgDrink, style: 'top:34%; left:52%; width:40%' },
      ],
      delay: 0,
    },
    {
      key: 'low',
      label: '低購買頻率',
      sub: '每季購買不到1次',
      pos: 'top: 26%; left: 2%;',
      labelSide: 'left',
      icons: [
        { src: imgPill, style: 'top:8%; left:16%; width:38%; transform:rotate(-14deg)' },
        { src: imgPlant, style: 'top:12%; left:56%; width:34%' },
        { src: imgLaptop, style: 'top:48%; left:12%; width:66%' },
      ],
      delay: 0.35,
    },
    {
      key: 'mid',
      label: '中購買頻率',
      sub: '每季至少購買1次',
      pos: 'top: 52%; left: 46%;',
      labelSide: 'right',
      icons: [
        { src: imgSoap, style: 'top:14%; left:56%; width:32%' },
        { src: imgTissue, style: 'top:48%; left:14%; width:44%' },
      ],
      delay: 0.7,
    },
  ]
</script>

<div class="obs">
  <Rail current={3} />

  <div class="text">
    <p class="kicker">觀察3</p>
    <h2>「購買頻率」<br />也容易影響漲相判斷</h2>
    <p class="body">
      體感物價漲得特別兇的另一個原因<br />
      和人們「常不常買這個東西」有關
    </p>
    <p class="body">
      我們將 368 個品項分成高、中、低購買頻率<br />
      分別觀察個別的漲幅差異
    </p>
  </div>

  <div class="visual" class:active>
    {#each groups as g (g.key)}
      <div class="bubble-wrap" style={g.pos} style:transition-delay="{g.delay}s">
        <div class="bubble" style:animation-delay="{g.delay}s">
          {#each g.icons as ic, i (i)}
            <img src={ic.src} alt="" class="mini" style={ic.style} />
          {/each}
        </div>
        <div class="glabel" class:left={g.labelSide === 'left'}>
          <b>{g.label}</b>
          <span>{g.sub}</span>
        </div>
      </div>
    {/each}
  </div>
</div>

<style>
  .obs {
    position: relative;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: clamp(2rem, 6vw, 7rem);
    padding: 0 clamp(1rem, 7vw, 8rem);
  }

  .text {
    flex: 0 1 460px;
  }

  .kicker {
    color: var(--steady);
    font-weight: 900;
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
  }

  h2 {
    font-size: clamp(1.5rem, 2.6vw, 2.1rem);
    font-weight: 900;
    line-height: 1.5;
    margin-bottom: 1.4rem;
  }

  .body {
    font-size: 0.95rem;
    font-weight: 700;
    line-height: 1.9;
    margin-bottom: 1.2rem;
  }

  .visual {
    position: relative;
    flex: 0 0 auto;
    width: clamp(320px, 38vw, 560px);
    aspect-ratio: 1.15;
  }

  .bubble-wrap {
    position: absolute;
    display: flex;
    align-items: flex-start;
    gap: 0.7rem;
    opacity: 0;
    transform: translateY(18px);
    transition: opacity 0.55s ease, transform 0.55s ease;
  }

  .visual.active .bubble-wrap {
    opacity: 1;
    transform: translateY(0);
  }

  .bubble {
    position: relative;
    width: clamp(130px, 13vw, 190px);
    aspect-ratio: 1;
    border-radius: 50%;
    background: #fff;
    flex: 0 0 auto;
  }

  .visual.active .bubble {
    animation: float 5.5s ease-in-out infinite;
  }

  @keyframes float {
    0%,
    100% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(-9px);
    }
  }

  .mini {
    position: absolute;
  }

  .glabel {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
    padding-top: 0.9rem;
    white-space: nowrap;
  }

  .glabel.left {
    order: -1;
    text-align: right;
  }

  .glabel b {
    font-size: 1.02rem;
    font-weight: 900;
  }

  .glabel span {
    font-size: 0.78rem;
    font-weight: 700;
    opacity: 0.75;
  }

  @media (max-width: 900px) {
    .obs {
      flex-direction: column;
      gap: 1.2rem;
      text-align: center;
    }
    .visual {
      width: min(88vw, 420px);
    }
  }
</style>
