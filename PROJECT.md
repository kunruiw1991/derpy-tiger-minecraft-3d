# Project: Derpy Tiger Minecraft Chapter 3D (`derpy-tiger-minecraft-3d`, Game #63)

## Architecture
- **Engine & Runtime**: Standalone, zero-build, zero-CDN ES-module Three.js r170 WebGL2 3D game (`vendor/three.module.min.js`) targeting 5-year-old players (`[Child]`).
- **Performance & Visual Guardrails**:
  - Software GPU detection (`HeadlessChrome` or `/SwiftShader|llvmpipe|Software/i` via `WEBGL_debug_renderer_info`), adding `.software-gpu` to `document.documentElement`, setting `dpr = isSoftwareGpu ? 0.42 : Math.min(window.devicePixelRatio || 1, 2)`, and disabling shadow maps on software GPU.
  - Material & Sprite guardrail (`enforceMaterialGuardrails(scene)`): all mesh materials clamped to `metalness <= 0.20` (`<= 0.22` audit threshold); all `THREE.Sprite` materials set `toneMapped = false` and `fog = false`.
  - Camera guardrail: `camera.rotation.order = 'YXZ'` and `camera.rotation.z = 0` every frame (`abs(cameraRoll) < 0.001`).
  - Draw call budget: `1 <= renderer.info.render.calls <= 65` using `THREE.InstancedMesh` for voxel terrain, trees, ores, and fences.
  - Play transition latency: clicking `#btn-title-play` transitions from `#title-screen` to `#hud` visible in `<= 80 ms` (with shader pre-compilation at boot).
- **Module Boundaries**:
  - **Game Core & Content (`M1`)**: `index.html`, `styles/main.css`, `vendor/three.module.min.js`, `src/core/`, `src/chars/`, `src/world/`, `src/ui/`, `src/fx/`, `src/data/`, `tools/gen_voice.py`, `assets/voice/`.
  - **E2E Test Suite (`E2E`)**: `tests/cdp.py`, `tests/qa_helpers.py`, `tests/l10n_audit.py`, `tests/layout_audit.py`, `tests/sim_gates.py`, `tests/run_e2e.py`, `tests/run_all_tiers.py`, `TEST_INFRA.md`, `TEST_READY.md`.
  - **E2E Integration & Hardening (`M2`)**: Runs Tiers 1–4 E2E suite against `M1`, fixes any issues, and performs Tier 5 white-box adversarial test coverage hardening.
  - **Deployment & Catalog Index (`M3`)**: `screenshot.jpg`, `README.md`, `.gitignore`, `.nojekyll`, GitHub Pages deployment (`kunruiw1991/derpy-tiger-minecraft-3d`), and `#63` catalog updates in `kunruiw1991/kunruiw1991` and `kunruiw1991/kunruiw1991.github.io`.

## Feature Inventory
Every feature from the Survey phase appears below with its assigned milestone. No feature is left unassigned.

| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| F1 | Derpy Tiger Round Face 3D Mesh | Chubby Korean Minhwa blue tiger head (`SphereGeometry(0.48, ...)` with `x *= 1.18` lower-cheek bulge and flattened front `z` plane, wide cream `muzzleMask` scaled `(1.25, 0.78, 0.58)`, round ears with inner tufts, huge golden saucer eyes `#ffd026` with cross-eyed pupils, flat pink nose, wide goofy grin with 12 white `ConeGeometry` fangs + curled pink tongue, forehead `'王'` mark + 8 cheek stripes) preserving `demon_hunter_repair_game` proportions | M1 | survey_1, survey_2, R1 |
| F2 | Derpy Tiger Round Butt & Pear Torso 3D Mesh | Pear-shaped `bodyLoft` torso (`makeLatheLoft` widening to `r = 0.45` at `y = -0.18`, `scale(1.06, 1.0, 0.92)`), cream belly, pelvis `{ y: -0.44, z: 0.04, rx: 0.38, ry: 0.22, rz: 0.36 }`, explicit sculpted twin round butt cheeks (`buttL`, `buttR`, `SphereGeometry(0.225, ...)` at `(±0.175, -0.24, -0.22)` scaled `(1.08, 0.98, 1.16)` with curved black stripes and waddle/jump bounce), stocky cobalt haunches, 4 paws with pink toe beans, and 9-ringed curling tail | M1 | survey_1, survey_2, R1 |
| F3 | Sussie Six-Eyed Magpie & Hero Squad Companions | Sussie the Six-Eyed Magpie in a miniature black Korean Gat hat perched on/orbiting Derpy Tiger's round head, paired with Rumi (purple dragon braid `leftBraid`/`rightBraid`) and Minecraft Voxel Mikey/JJ companion in the hero trio rig (`group`, `jjGroup`, `mikeyGroup`, `sahurGroup`) | M1 | survey_1, survey_2, R1 |
| F4 | New 5-Zone 72x72 Minecraft Chapter 3D Map (`EgruEB4oZ2E` + `WjAyI6kwylA`) | Blocky voxel Minecraft world (`72x72` grid) contrasting crisp `BoxGeometry` voxel blocks with smooth round Derpy Tiger across 5 zones: (1) Central Hub: Moonlit Rooftop Portal Terrace & White Iron Security House with Glowing Cyan Honmoon Floor Portal, Diamond Safe Lucky Chest, and 4 Tipped-to-Upright Blue-and-White Peony Flowerpots; (2) Q1 (NW): Village Rooftops, Chimney Drop & Buried Cookie Garden; (3) Q2 (NE): Underground Drill Tunnel, Village Well & Torch Carrot Farm; (4) Q3 (SW): Red Laser Security House, CCTV Towers & Rumi's Bedroom Closet/Wastebasket Portal Loft; (5) Q4 (SE): Lava Parkour Stepping Stones, Passcode `1-2-3-4` Keypad, Mikey Cage Rescue, Jinu's Dark Stone Stairs (`"SAVE THE DATE"` card) & Pink `HUNTR/X COMEBACK` Billboard Finale | M1 | survey_1, survey_2, R1, R2 |
| F5 | Mario-Style 3D Jump & Air-Throw Combo (`#btn-hud-jump` / `Space`) | `#btn-hud-jump` button and `Space`/`KeyJ`/`KeyZ` keys trigger `triggerJump()` (`vy = 11.5`, asymmetric gravity `28.0` up / `38.0` down, overhead breakable block head-bonk `'HEAD BONK!'`, body squash-and-stretch + `buttL`/`buttR` landing bounce, dynamic ground shadow scaling, and pressing Jump while airborne triggers mid-air Cappy projectile throw) | M1 | survey_2, survey_3, R2 |
| F6 | Super Mario Odyssey Cappy-Style Returning Projectile Throw (`#btn-hud-drum`) | `#btn-hud-drum` button and `KeyK`/`KeyE`/`KeyF`/`KeyX`/`Enter` launch `throwStick()` using detached `hero.thrownStickGroup` (spinning weapon/Gat-Honmoon disc + golden/cyan `spinRingMesh` aura) across 3 phases (`outbound` 0.32s -> `hover` 0.16s -> `returning` 0.34s over `range = 6.2` units) with swept collisions that break blocks, bonk geared bosses (or harmlessly bounce back `'BOING! NEED STARS!'` if under-geared), pat friendly critters, and vacuum pickups | M1 | survey_2, survey_3, R2 |
| F7 | 4 Tipped Blue-and-White Peony Flowerpots (`#btn-hud-pot` / `#btn-hud-totem`) | Hub station mechanic inspired by `EgruEB4oZ2E` Scene 1 where Derpy Tiger pats tipped flowerpots upright and upgrades them across 3 tiers (15 -> 35 -> 60 gems), showering gems and granting permanent Star Power, Shield Hearts, Move Speed, and Magnet Radius; includes DOM ID aliasing `btn-hud-pot <-> btn-hud-totem` | M1 | survey_1, survey_2, R1, R2 |
| F8 | Diamond Safe Lucky Chest Roulette & 5 Upgradable 3D Weapons (`#btn-hud-spin`) | 8-segment gear roulette modal (`#roulette-modal`, 25 gems per spin, pity rule guarantees non-duplicate upgrade every 2nd spin, never downgrades power) unlocking 5 3D Minecraft/Honmoon weapons and armor/helm/boots gear | M1 | survey_2, R2 |
| F9 | 4 Quadrant Minecraft Boss Encounters & Zero-Frustration Cloud Boing | 4 triggerable quadrant bosses (`q1` Bouncy Zombie Captain, `q2` Drill Golem Mole, `q3` Closet Prankster Puppet, `q4` Giant Long-Arm Security Boss) with telegraphed attacks, dizzy stun windows, 3-bonk defeat for 4 Trophies (`#victory-modal`), and harmless Cloud Boing bounce (`+3` stars, `0` heart loss) when under-geared | M1 | survey_2, R2 |
| F10 | 68 Pre-Recorded Neural English `edge-tts` MP3 Voiceovers & BGM Ducking | `tools/gen_voice.py` (`PYTHONPATH=/tmp/tts_pkgs python3 -P tools/gen_voice.py --force`) generating 68 neural English MP3 voice clips (`assets/voice/<id>.mp3`), `assets/voice/manifest.json`, and `src/data/voice_manifest.js` (`44.1 kHz` mono `64 kbps`), decoded via WebAudio with `-6 dB` BGM ducking, `#btn-hud-voice` replay, focusable `<div id="voice-subtitle">`, zero `speechSynthesis`, zero CJK characters, and zero 404s | M1 | survey_2, survey_3, R2 |
| F11 | Multi-Modal Kid Controls, Responsive 5-Viewport HUD & Automation Seam | Keyboard (`WASD`/Arrows/`Space`/`Enter`), tap-to-walk/act raycasting, drag-move virtual joystick, responsive layout across 5 viewports (`1280x800`, `1024x768`, `768x1024`, `844x390`, `390x844`) with `<= 6` visible HUD buttons and `>= 68px`/`72px` touch targets, and frozen automation seam `window.__DERPY_TIGER__ = window.__JJ_MIKEY_BURGER__ = window.__SAHUR_ISLAND__ = window.__LUCKY_TITAN__` | M1 | survey_2, survey_3, R2 |
| F12 | Opaque-Box E2E Test Suite (Tiers 1–4) & `TEST_READY.md` | Headless Chrome WebGL2 CDP test suite (`tests/cdp.py`, `tests/qa_helpers.py`, `tests/l10n_audit.py`, `tests/layout_audit.py`, `tests/sim_gates.py`, `tests/run_e2e.py`, `tests/run_all_tiers.py`) verifying Tier 1 (`>= 5` tests/feature), Tier 2 (`>= 5` boundary tests/feature), Tier 3 (cross-feature pairwise combinations), and Tier 4 (real-world playthrough & 20-seed bot determinism), documented in `TEST_INFRA.md` and `TEST_READY.md` | E2E, M2 | survey_3, R1, R2 |
| F13 | Tier 5 White-Box Adversarial Coverage Hardening | White-box coverage audit and adversarial stress tests verifying edge cases, rapid multi-input sequences, geometry proportion invariants (Derpy Tiger round face & round butt `buttL`/`buttR`), and zero uncaught console/page/network errors | M2 | survey_3, R1, R2 |
| F14 | Public GitHub Pages Deployment (`kunruiw1991/derpy-tiger-minecraft-3d`) | Public GitHub repository `kunruiw1991/derpy-tiger-minecraft-3d` with token-free `.git/config`, `.gitignore` excluding `.agents/`, `.nojekyll`, `README.md`, `1280x800` `screenshot.jpg`, and live GitHub Pages deployment at `https://kunruiw1991.github.io/derpy-tiger-minecraft-3d/` returning HTTP 200 | M3 | survey_3, R3 |
| F15 | Chronological Game Index `#63` Update in Both Profile & Pages Repos | Appending Game `#63` (`derpy-tiger-minecraft-3d`) to both `README.md` and `index.html` (header counters `#01 -> #63`, `All 63 Games`, HTML `<tr>` row `#63`, and `const GAMES` entry `#63`) in `https://github.com/kunruiw1991/kunruiw1991` and `https://github.com/kunruiw1991/kunruiw1991.github.io` and pushing to `origin/main` | M3 | survey_3, R3 |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Core 3D Game, Derpy Tiger Rig, Voxel Minecraft Map & `edge-tts` Voices | Implement F1–F11 in `index.html`, `styles/`, `vendor/`, `src/`, `tools/gen_voice.py`, and `assets/voice/*.mp3` | none | DONE |
| E2E | Opaque-Box E2E Test Suite (Tiers 1–4) | Implement F12 in `tests/`, `TEST_INFRA.md`, and `TEST_READY.md` covering Tiers 1–4 across F1–F11 | none (parallel with M1 via Interface Contracts) | DONE |
| M2 | Final Milestone: E2E Test Pass (Tiers 1–4) & Adversarial Hardening (Tier 5) | Phase 1: Pass 100% of E2E Tiers 1–4 against M1; Phase 2: Tier 5 white-box adversarial coverage hardening (F12, F13) | M1, E2E | IN_PROGRESS |
| M3 | GitHub Pages Deployment & Chronological Game Index `#63` Update | Capture `screenshot.jpg`, author `README.md`, deploy `kunruiw1991/derpy-tiger-minecraft-3d` to GitHub Pages (HTTP 200), and append `#63` to `kunruiw1991/kunruiw1991` and `kunruiw1991/kunruiw1991.github.io` (F14, F15) | M2 | IN_PROGRESS |

## Interface Contracts

### `M1` (Game Runtime) ↔ `E2E` / `M2` (Automated Verification Suite)
1. **HTTP Entry Point & Query Flags**:
   - Served over HTTP from `/usr/local/google/home/kunruiwang/teamwork_projects/derpy_tiger_minecraft_chapter/index.html` (supports `?seed=<int>` for deterministic RNG and `?reset=1` to clear `localStorage`).
   - Local Three.js r170 bundle at `/vendor/three.module.min.js`.
   - `THREE.WebGLRenderer.prototype.render` hook delegation in `src/core/scene.js` so E2E tests hooking `THREE.WebGLRenderer.prototype.render` capture `(scene, camera, renderer)`.
2. **Derpy Tiger 3D Mesh Contract (`scene` traversal)**:
   - Hero root group in scene contains named parts/groups preserving Derpy Tiger's round face and round butt proportions:
     - `head` (`SphereGeometry(0.48, ...)` with widened lower cheeks `x *= 1.18`, `muzzleMask` scaled `(1.25, 0.78, 0.58)`, `leftEar`, `rightEar`, `eyes`, `derpyGoofyGrin`, `wangForeheadMark`).
     - `torso` (`bodyLoft` lathe geometry widening at hips `r = 0.45`, `creamBelly`).
     - `derpyRoundButt` group containing `buttL` and `buttR` (`SphereGeometry(0.225, ...)` at `(±0.175, -0.24, -0.22)` in `torso` space, scaled `(1.08, 0.98, 1.16)` with curved black tiger stripes) + `tail` + `leftLeg` / `rightLeg` + `leftArm` / `rightArm`.
     - Sussie the Six-Eyed Magpie companion (`sussieMagpie` / Gat hat).
     - All mesh materials in the scene satisfy `material.metalness <= 0.20` (`<= 0.22` max).
3. **DOM & HUD Element IDs**:
   - `#game-canvas`, `#hud`, `#ui-layer`
   - Title screen: `#title-screen`, `#title-banner`, `#btn-title-play`, `#btn-title-continue`, `#btn-title-reset`
   - HUD status: `#hud-status`, `#hud-gems-pill`, `#hud-gems-val`, `#hud-power-pill`, `#hud-weapon-img`, `#hud-power-val`, `#hud-gear-icons`, `#hud-shields-pill`, `#hud-shields-row`, `#hud-trophies-pill`, `#hud-trophy-pips`, `#hud-trophies-val`
   - HUD action buttons (exact 6 buttons visible during active play):
     - `#btn-hud-spin` (`#badge-hud-spin`)
     - `#btn-hud-totem` aliased with `#btn-hud-pot` (`#badge-hud-totem` / `#badge-hud-pot`, `#label-hud-totem` / `#label-hud-pot`)
     - `#btn-hud-voice`
     - `#btn-hud-menu` (`#badge-hud-chaos`)
     - `#btn-hud-jump` (`#badge-hud-jump`, `#label-hud-jump`)
     - `#btn-hud-drum` (`#badge-hud-drum`)
   - Voice subtitle: `<div id="voice-subtitle" class="voice-subtitle" tabindex="0" aria-label="Replay voice" hidden>`
   - Modals: `#roulette-modal` (`#roulette-wheel`, `#roulette-strip`, `#roulette-preview`, `#btn-roulette-spin`, `#btn-roulette-close`), `#titan-intro` (`#titan-intro-portrait`, `#titan-intro-name`, `#titan-intro-title`), `#victory-modal` (`#victory-trophies`, `#btn-victory-continue`, `#btn-victory-replay`), `#pause-modal` (`#btn-pause-resume`, `#btn-pause-voice`, `#btn-pause-chaos`, `#btn-pause-save`, `#btn-pause-reset`).
4. **Global Automation Seam (`window.__DERPY_TIGER__ = window.__JJ_MIKEY_BURGER__ = window.__SAHUR_ISLAND__ = window.__LUCKY_TITAN__`)**:
   - Methods: `startGame()`, `continueGame()`, `tapWorld(x, z)`, `swingDrum()`, `drumSwing()`, `jump()`, `triggerJump()`, `throwStick(opts)`, `triggerStickThrow(opts)`, `breakBlock(blockId)`, `breakDrum(blockId)`, `plantPot(slotIndex)`, `upgradeTotem(slotIndex)`, `spinChest(forcedGearId)`, `spinWheel(forcedGearId)`, `spawnTitan(quadrantId)`, `spawnBoss(quadrantId)`, `bonkTitan(quadrantId)`, `bonkBoss(quadrantId)`, `replayVoice()`, `stepFrames(count, dt)`, `getState()`.
   - `getState()` returns deterministic snapshot including `started`, `paused`, `quadrant`, `gems`, `power`, `shields`, `maxShields`, `equipped`, `inventory`, `totems`, `pots`, `trophies`, `trophyCount`, `player` (`x, y, z, vy, jumping, jumpCount, airTime, grounded, airborne, facing, comboStep, animState`), `stickThrow` (`active, phase, timer, x, y, z, originX, originZ, targetX, targetZ, range, throwCount, hitCount, hits`), `activeTitan`, `activeBlocks`, `pickupsCount`, `critters`, `patCount`, `voice` (`muted, speaking, lastLineId, lastCaption, playCount, loadedCount, totalCount`), `feedback`, `perf` (`frames, fps, drawCalls, triangles, geometries, textures, softwareGpu, cameraRoll`).
5. **Pre-Recorded Voice Assets (`assets/voice/`)**:
   - `assets/voice/manifest.json` and `src/data/voice_manifest.js` listing 68 MP3 clips (`assets/voice/<id>.mp3`, `44100 Hz`, mono, `64 kbps`, `duration > 0.35s`, `bytes > 2000`, total size `<= 4.0 MB`).

## Code Layout
```
/usr/local/google/home/kunruiwang/teamwork_projects/derpy_tiger_minecraft_chapter/
├── PROJECT.md                  # Global project index (Project Orchestrator)
├── TEST_INFRA.md               # E2E test infrastructure doc (E2E Orchestrator)
├── TEST_READY.md               # E2E test suite readiness signal (E2E Orchestrator)
├── README.md                   # Public repository documentation (M3)
├── screenshot.jpg              # 1280x800 live gameplay JPEG screenshot (M3)
├── .gitignore                  # Excludes .agents/, tmp_profiles/, __pycache__/ (M1/M3)
├── .nojekyll                   # GitHub Pages static serving marker (M1/M3)
├── index.html                  # Game HTML entry point (M1)
├── styles/
│   └── main.css                # Kid-friendly responsive HUD & modal styling (M1)
├── vendor/
│   └── three.module.min.js     # Local Three.js r170 ES module build (M1)
├── src/
│   ├── main.js                 # Game loop, Mario jump, Odyssey throw, interactions (M1)
│   ├── core/
│   │   ├── scene.js            # WebGL2 renderer, lighting, material guardrails (M1)
│   │   ├── camera.js           # Follow camera with YXZ order & zero roll (M1)
│   │   ├── input.js            # Keyboard, pointer raycast, drag joystick (M1)
│   │   ├── state.js            # Deterministic PRNG, game state, localStorage (M1)
│   │   └── seam.js             # Global automation seam (__DERPY_TIGER__ / __LUCKY_TITAN__) (M1)
│   ├── chars/
│   │   ├── hero.js             # Derpy Tiger (round face + round butt buttL/buttR) + Sussie + Rumi + Mikey rig (M1)
│   │   ├── critters.js         # Friendly pattable Minecraft/Minhwa critters (M1)
│   │   └── titans.js           # 4 Quadrant Minecraft Bosses (M1)
│   ├── world/
│   │   ├── island.js           # 72x72 5-zone Voxel Minecraft Chapter map (M1)
│   │   ├── blocks.js           # Breakable cookie/diamond/redstone voxel crates (M1)
│   │   ├── totems.js           # 4 Tipped-to-Upright Blue-and-White Peony Flowerpots (M1)
│   │   └── pickups.js          # Gem/cookie/star fountain pickups & magnet vacuum (M1)
│   ├── ui/
│   │   ├── hud.js              # Status pills, 6 HUD buttons, DOM ID aliases (M1)
│   │   └── modals.js           # Title, Roulette, Boss Intro, Pause, Victory modals (M1)
│   ├── fx/
│   │   ├── audio.js            # WebAudio context & -6 dB BGM ducking synth (M1)
│   │   ├── sfx.js              # Procedural jump, throw, bonk, fanfare SFX (M1)
│   │   ├── particles.js        # Ring bursts, confetti, floating text sprites (M1)
│   │   └── voice.js            # Pre-recorded MP3 WebAudio player & subtitle layout (M1)
│   └── data/
│       ├── catalog.js          # Weapons, gear, biomes, bosses, flowerpots config (M1)
│       ├── voice_catalog.js    # 68 Derpy Tiger Minecraft chapter voice specs (M1)
│       └── voice_manifest.js   # Generated MP3 metadata manifest (M1)
├── tools/
│   └── gen_voice.py            # edge-tts MP3 synthesizer & ffprobe validator (M1)
├── assets/
│   └── voice/                  # 68 generated MP3 files + manifest.json (M1)
└── tests/
    ├── cdp.py                  # Zero-dependency Chrome DevTools Protocol WebGL2 harness (E2E)
    ├── qa_helpers.py           # QASession helpers & seam assertions (E2E)
    ├── l10n_audit.py           # Gate F13: 0 CJK & 0 speechSynthesis audit (E2E)
    ├── layout_audit.py         # Gate F11: 5-viewport layout & touch target audit (E2E)
    ├── sim_gates.py            # Gates F1-F12: Mario jump, Odyssey throw, 20-seed bot (E2E)
    ├── run_e2e.py              # E01-E48 + Derpy Tiger round face/butt mesh E2E suite (E2E)
    └── run_all_tiers.py        # Unified runner for Tiers 1-4 (and Tier 5 in M2) (E2E/M2)
```
