# Test Infrastructure (`TEST_INFRA.md`) — Derpy Tiger Minecraft Chapter 3D (`derpy-tiger-minecraft-3d`)

## 1. Test Architecture Overview

The E2E Test Suite for **Derpy Tiger Minecraft Chapter 3D** (`derpy-tiger-minecraft-3d`, Game #63) is an opaque-box, zero-dependency Python 3 + Chrome DevTools Protocol (CDP) WebGL2 verification framework located under `/usr/local/google/home/kunruiwang/teamwork_projects/derpy_tiger_minecraft_chapter/tests/`.

It exercises the live browser bundle served via `http.server` in headless Google Chrome (`/usr/bin/google-chrome`) with SwiftShader WebGL2 (`--use-gl=angle --use-angle=swiftshader`), validating:
- **3D Scene Graph & Procedural Geometry**: Inspects `window.__QA_LAST_SCENE__` / `window.__E2E_LAST_SCENE__` (Three.js r169 `Scene`) to verify the KPop Demon Hunters **Derpy Tiger** hero hierarchy (`HeroRoot` -> `DerpyTigerHero`), including its **chubby round face** (`head`, `muzzleMask`, `eyes`, `derpyGoofyGrin`, `wangForeheadMark`), **expressive round butt** (`derpyRoundButt` containing left & right spherical cheeks `buttL` and `buttR` with counter-phase walk bounce), **long striped tail** (`tail`), and **three-eyed Sussie magpie companion** (`sussieMagpie`), as well as the 5-zone Minecraft-inspired world (`hub`, `q1`, `q2`, `q3`, `q4`) and 4 quirky Minecraft-inspired bosses.
- **Deterministic Simulation Seam**: Drives `window.__DERPY_TIGER__` (and aliases `window.__JJ_MIKEY_BURGER__`, `window.__SAHUR_ISLAND__`, `window.__LUCKY_TITAN__`) through `stepFrames(n, dt)` at fixed `1/60s` timesteps (`seed=2026`).
- **DOM / HUD / Responsive Layout**: Audits 5 viewports (`1920x1080`, `1366x768`, `1024x768`, `768x1024`, `844x390`) for zero bounding-box overlaps, zero offscreen clipping, and `>= 88x88px` touch targets on `#btn-hud-jump` (`JUMP! 🦘`) and `#btn-hud-drum` (`BOOM! 🪃`).
- **English-Only Localization & Voiceover Integrity**: Audits all source files for zero CJK characters and zero `window.speechSynthesis` calls, and verifies all 68 edge-tts MP3 voice clips in `assets/voice/manifest.json` return HTTP 200.

## 2. Test Suite Files

| File Path | Role & Coverage |
|---|---|
| `tests/cdp.py` | Pure-Python raw socket WebSocket + HTTP JSON Chrome DevTools Protocol client (`CDPClient`, `launch_chrome_with_cdp`, `open_ StaticServer`). Uses `/tmp/derpy_tiger_minecraft_chapter/tmp_profiles` for isolated temporary Chrome profiles and screenshots. |
| `tests/qa_helpers.py` | JavaScript injection helpers (`PREBOOT_SCRIPT` WebGL2 shader compile/link validator, Three.js scene capture, console/pageerror collectors, `SCENE_AUDIT_JS`, `HUD_LAYOUT_AUDIT_JS`, `CANVAS_SAMPLE_JS`). |
| `tests/l10n_audit.py` | Static + runtime English-only localization audit (`L01`–`L08`). Scans `index.html`, `src/`, `styles/`, and `assets/voice/manifest.json` while skipping `('.git', '.agents', '__pycache__', 'node_modules', 'tmp_profiles', 'tests')`. |
| `tests/layout_audit.py` | Multi-viewport responsive HUD/DOM bounding-box overlap & touch-target audit across 5 viewports (`1920x1080`, `1366x768`, `1024x768`, `768x1024`, `844x390`). |
| `tests/sim_gates.py` | Deterministic simulation gate runner (`F1`–`F12`), 20-seed child-bot full playthrough (`seeds 1001..1020`, 100% completion), and `seed=2026` SHA-256 state hash determinism check. |
| `tests/run_e2e.py` | Comprehensive 50-assertion opaque-box E2E test suite (`E01`–`E50`), including `E47` (Mario 3D Jump), `E48` (Odyssey Returning Projectile Throw), `E49` (Derpy Tiger Round Face & Round Butt `buttL`/`buttR` Geometry), and `E50` (Minecraft Chapter 5-Zone World & 68 Voiceovers). |
| `tests/run_all_tiers.py` | Unified 4-Tier test runner (`Tier 1`: 55 feature checks across `F1`–`F11`; `Tier 2`: 55 boundary checks across `F1`–`F11`; `Tier 3`: 16 cross-feature pairwise checks; `Tier 4`: 7 full E2E scenarios; 133 total checks). |

## 3. Execution Commands

Run from `/usr/local/google/home/kunruiwang/teamwork_projects/derpy_tiger_minecraft_chapter`:

```bash
# Run all 4 Tiers (133 total checks across F1-F11 + E01-E50 + Sim Gates + L10N + Layout)
python3 -P tests/run_all_tiers.py --all

# Run individual Tiers
python3 -P tests/run_all_tiers.py --tier 1
python3 -P tests/run_all_tiers.py --tier 2
python3 -P tests/run_all_tiers.py --tier 3
python3 -P tests/run_all_tiers.py --tier 4

# Run individual audit modules directly
python3 -P tests/l10n_audit.py
python3 -P tests/layout_audit.py
python3 -P tests/sim_gates.py
python3 -P tests/run_e2e.py
```
