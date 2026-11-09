// Kid-friendly English UI copy (1-3 uppercase words per button label) + emoji tokens
// for Derpy Tiger Minecraft Chapter 3D! (Round Face, Round Butt & Voxel Rescue).
// Zero CJK characters anywhere.

export const STRINGS = Object.freeze({
  GAME_TITLE: 'DERPY TIGER MINECRAFT 3D!',
  GAME_SUBTITLE: 'PAT POTS UPRIGHT \u2022 JUMP & THROW \u2022 RESCUE MIKEY!',

  TITLE: Object.freeze({
    kicker: '\uD83D\uDC2F DERPY TIGER & SUSSIE MAGPIE \u2022 MINECRAFT CHAPTER 3D \uD83D\uDC26',
    heading: 'DERPY TIGER MINECRAFT 3D!',
    sub: 'PAT POTS UPRIGHT \u2022 JUMP & THROW \u2022 RESCUE MIKEY!',
    continueBtn: 'CONTINUE!',
    continueAria: 'Continue Saved Minecraft Adventure',
    playBtn: 'PLAY!',
    playAria: 'Play Derpy Tiger Minecraft Chapter 3D',
    voiceBtn: 'VOICE',
    voiceAria: 'Replay Voice Guide',
  }),

  HUD: Object.freeze({
    starsAria: 'Star Gems',
    powerAria: 'Tiger Power Level',
    shieldsAria: 'Honmoon Hearts',
    trophiesAria: 'Minecraft Rescue Trophies',
    spinLabel: 'SPIN',
    spinFree: 'FREE!',
    spinAria: 'Open Diamond Safe Lucky Spin Chest',
    potPlantLabel: 'UPRIGHT',
    potGrowLabel: 'BLOOM',
    potMaxLabel: 'MAX!',
    potAria: 'Pat Porcelain Peony Flowerpot Upright or Bloom It',
    voiceLabel: 'VOICE',
    voiceAria: 'Replay Voice Line',
    menuLabel: 'PAUSE',
    menuAria: 'Open Pause Menu',
    jumpLabel: 'JUMP!',
    jumpAirLabel: 'AIR!',
    jumpAria: 'Jump Up High with Derpy Tiger',
    drumLabel: 'THROW!',
    drumAria: 'Throw Boomerang & Smash Lucky Blocks',
  }),

  ROULETTE: Object.freeze({
    title: 'DIAMOND SAFE SPIN!',
    spinBtn: 'SPIN!',
    spinFreeBtn: 'FREE SPIN!',
    spinningBtn: 'SPINNING...',
    awesomeBtn: 'EQUIPPED!',
    closeBtn: 'PLAY!',
    spinAria: 'Spin Diamond Safe Chest for Minecraft Gear',
    closeAria: 'Close Diamond Safe Chest and Play',
    awesomeAria: 'Keep New Gear and Play',
    hintReady: 'TAP SPIN FOR HONMOON & DIAMOND GEAR!',
    hintFree: 'FREE GOLDEN SPIN READY!',
    hintNeedStars: 'SMASH LUCKY BLOCKS OR PAT POTS FOR STARS!',
    hintSpinning: 'ROUND AND ROUND IT GOES...',
    equippedBadge: 'EQUIPPED!',
  }),

  PAUSE: Object.freeze({
    title: 'GAME PAUSED',
    musicLabel: 'MUSIC',
    soundLabel: 'SOUND',
    voiceLabel: 'VOICE',
    chaosLabel: '2X PARTY',
    stateOn: 'ON',
    stateOff: 'OFF',
    resumeBtn: 'PLAY ON!',
    newIslandBtn: 'NEW MAP!',
    musicAria: 'Toggle K-Pop Chiptune Music',
    soundAria: 'Toggle Sound Effects',
    voiceAria: 'Toggle English Voiceover',
    chaosAria: 'Toggle 2X Honmoon Party Mode',
    resumeAria: 'Resume Playing',
    newIslandAria: 'Generate a New Voxel Map',
  }),

  VICTORY: Object.freeze({
    title: 'COMEBACK CHAMPION!',
    crownBadge: '4 / 4 BOSSES BONKED & MIKEY RESCUED!',
    playMoreBtn: 'KEEP PLAYING!',
    chaosOnBtn: '2X PARTY: ON!',
    chaosOffBtn: '2X PARTY!',
    newIslandBtn: 'NEW MAP!',
    playMoreAria: 'Continue Free Play on Current Map',
    chaosAria: 'Toggle 2X Honmoon Party Mode',
    newIslandAria: 'Start a New Seeded Voxel Map',
  }),

  BOSS: Object.freeze({
    readyTag: 'BONK!',
    needPrefix: 'NEED',
  }),

  COMIC: Object.freeze({
    hitWords: Object.freeze(['PAW!', 'BONK!', 'ROAR!', 'BOOM!', 'SMASH!']),
    boingWord: 'BOING! NEED STARS!',
  }),

  WEAPONS: Object.freeze({
    wooden_kentungan_bat: Object.freeze({
      short: 'GAT HAT',
      title: 'SUSSIE GAT BOOMERANG',
      emoji: '\uD83C\uDFA9',
    }),
    bronze_temple_gong: Object.freeze({
      short: 'HONMOON BLADE',
      title: 'HONMOON LIGHT BLADE',
      emoji: '\uD83D\uDDE1\uFE0F',
    }),
    golden_sahur_mallet: Object.freeze({
      short: 'DRILL PICK',
      title: 'COOKIE DRILL PICKAXE',
      emoji: '\u26CF\uFE0F',
    }),
    neon_thunder_taiko: Object.freeze({
      short: 'PEONY MALLET',
      title: 'PORCELAIN PEONY MALLET',
      emoji: '\uD83C\uDF38',
    }),
    rainbow_mega_hammer: Object.freeze({
      short: 'DIAMOND SWORD',
      title: 'DIAMOND RESCUE SWORD',
      emoji: '\uD83D\uDC8E',
    }),
  }),

  TITANS: Object.freeze({
    tralalero_tralala: Object.freeze({
      short: 'ZOMBIE CAPTAIN',
      badge: 'ROOFTOP',
      icon: '\uD83E\uDDDF',
    }),
    bombardiro_crocodilo: Object.freeze({
      short: 'DRILL GOLEM',
      badge: 'TUNNEL',
      icon: '\u26CF\uFE0F',
    }),
    brr_brr_patapim: Object.freeze({
      short: 'CLOSET PUPPET',
      badge: 'PORTAL',
      icon: '\uD83C\uDF00',
    }),
    golden_sahur_king: Object.freeze({
      short: 'SECURITY BOSS',
      badge: 'VAULT',
      icon: '\uD83D\uDEE1\uFE0F',
    }),
  }),
});

export function formatTierBadge(tier) {
  const safeTier = Math.max(1, Math.min(5, Math.floor(Number(tier) || 1)));
  return `\u2605${safeTier}`;
}

export function formatStarCost(cost) {
  const n = Math.max(0, Math.floor(Number(cost) || 0));
  return n === 0 ? 'FREE!' : `\u2B50${n}`;
}
