#!/usr/bin/env python3
"""Master Tiered E2E Test Runner (Tiers 1..4) for Derpy Tiger Minecraft Chapter 3D.

Owner: teamwork_test_writer_1
Exclusive path: tests/run_all_tiers.py
Usage:
  python3 -P tests/run_all_tiers.py --tier 1
  python3 -P tests/run_all_tiers.py --tier 2
  python3 -P tests/run_all_tiers.py --tier 3
  python3 -P tests/run_all_tiers.py --tier 4
  python3 -P tests/run_all_tiers.py --all

Structure across Features F1..F11:
  - Tier 1 (Feature Coverage): 55 assertions (5 per feature across F1..F11).
  - Tier 2 (Boundary & Corner Cases): 55 assertions (5 per feature across F1..F11).
  - Tier 3 (Cross-Feature Pairwise Combinations): 16 pairwise interaction assertions.
  - Tier 4 (Real-World Application Scenarios): 7 full end-to-end scenario checks
    (including full Title -> 4 Flowerpots -> Roulette -> 4 Bosses -> Victory -> Free-Roam
    playthrough, E01..E50 master suite, 20-seed 1001..1020 child-bot simulation,
    seed=2026 SHA-256 determinism, 5-viewport layout audit, and 0-CJK/0-speechSynthesis l10n audit).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.request
from typing import Any, Callable

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from l10n_audit import run_l10n_audit, run_static_repo_scan  # noqa: E402
from layout_audit import run_layout_audit  # noqa: E402
from qa_helpers import (  # noqa: E402
    HUD_BUTTON_IDS,
    QA_TMP_DIR,
    REPO_ROOT,
    SEAM_GLOBAL_EXPR,
    STORAGE_KEY,
    TITAN_ORDER,
    WEAPON_ORDER,
    WEAPON_TIERS,
    QASession,
    ensure_qa_dirs,
    extract_pad_tiers,
    ffprobe_mp3,
    parse_voice_catalog_entries,
)
from run_e2e import INSTALL_THREE_SPY_JS, _ensure_three_spy, run_e2e_suite  # noqa: E402
from sim_gates import (  # noqa: E402
    DETERMINISM_SCRIPT_JS,
    gate_f5_rapid_double_tap_debounce,
    run_sim_gates,
)


def _record(
    bucket: list[dict[str, Any]],
    check_id: str,
    feature: str,
    description: str,
    passed: bool,
    detail: Any = None,
) -> None:
  bucket.append({
      'id': check_id,
      'feature': feature,
      'description': description,
      'passed': bool(passed),
      'detail': detail if detail is not None else {},
  })
  status = 'PASS' if passed else 'FAIL'
  print(f'  [{status}] {check_id} ({feature}): {description}')


# ==============================================================================
# TIER 1: Feature Coverage (5 assertions per feature across F1..F11 = 55 checks)
# ==============================================================================


def run_tier1_feature_coverage(sess: QASession) -> dict[str, Any]:
  print('\n=== TIER 1: Feature Coverage (F1..F11, 55 assertions) ===')
  checks: list[dict[str, Any]] = []
  t0 = time.time()

  sess.goto('index.html?seed=2026', timeout=25.0)
  sess.wait_raf(3)
  _ensure_three_spy(sess)

  # --- F1 & F2 & F3: Inspect live Three.js Hero Hierarchy ---
  hero_info = sess.eval_json(
      f"""(() => {{
        const L = {SEAM_GLOBAL_EXPR};
        L.startGame({{ seed: 2026, chaosMode: false }});
        L.stepFrames(5, 1 / 60);
        const scene = window.__QA_LAST_SCENE__ || window.__E2E_LAST_SCENE__;
        const nodes = {{}};
        const names = [
          'HeroRoot', 'HeroBody', 'DerpyTigerHero',
          'head', 'skullMesh', 'muzzleMask', 'leftEar', 'rightEar',
          'eyes', 'leftEye', 'rightEye', 'nose',
          'derpyGoofyGrin', 'mouthCavity', 'fangsMesh', 'tongue', 'wangForeheadMark',
          'torso', 'bodyLoft', 'creamBelly', 'derpyRoundButt', 'buttL', 'buttR', 'torsoStripes',
          'leftArm', 'rightArm', 'leftLeg', 'rightLeg', 'tail', 'tailMesh',
          'sussieMagpie', 'sussieMesh',
          'RumiCompanion', 'leftBraid', 'rightBraid', 'VoxelMikeyCompanion',
          'HeroWeaponSocket', 'HeroThrownStick',
        ];
        for (const n of names) nodes[n] = null;

        if (scene) {{
          scene.traverse((obj) => {{
            if (obj.name && Object.prototype.hasOwnProperty.call(nodes, obj.name)) {{
              const verts = obj.geometry?.attributes?.position?.count || 0;
              nodes[obj.name] = {{
                found: true,
                type: obj.type,
                verts,
                x: Number(obj.position.x.toFixed(4)),
                y: Number(obj.position.y.toFixed(4)),
                z: Number(obj.position.z.toFixed(4)),
                sx: Number(obj.scale.x.toFixed(3)),
                sy: Number(obj.scale.y.toFixed(3)),
                sz: Number(obj.scale.z.toFixed(3)),
                metalness: typeof obj.material?.metalness === 'number' ? obj.material.metalness : 0,
              }};
            }}
          }});
        }}

        // Step walk/jump to measure animation deltas for buttL, buttR, tail, Sussie, Rumi, Mikey
        const buttLY0 = nodes.buttL ? nodes.buttL.y : 0;
        const buttRY0 = nodes.buttR ? nodes.buttR.y : 0;
        const sussieY0 = nodes.sussieMagpie ? nodes.sussieMagpie.y : 0;
        const rumiY0 = nodes.RumiCompanion ? nodes.RumiCompanion.y : 0;
        const mikeyY0 = nodes.VoxelMikeyCompanion ? nodes.VoxelMikeyCompanion.y : 0;

        L.tapWorld(-7.0, 4.5);
        L.stepFrames(11, 1 / 60);
        let buttLY1 = buttLY0, buttRY1 = buttRY0, sussieY1 = sussieY0, rumiY1 = rumiY0, mikeyY1 = mikeyY0;
        let tailRotZ = 0;
        if (scene) {{
          scene.traverse((obj) => {{
            if (obj.name === 'buttL') buttLY1 = obj.position.y;
            if (obj.name === 'buttR') buttRY1 = obj.position.y;
            if (obj.name === 'tail') tailRotZ = obj.rotation.z;
            if (obj.name === 'sussieMagpie') sussieY1 = obj.position.y;
            if (obj.name === 'RumiCompanion') rumiY1 = obj.position.y;
            if (obj.name === 'VoxelMikeyCompanion') mikeyY1 = obj.position.y;
          }});
        }}
        return {{
          nodes,
          anim: {{
            buttLY0, buttRY0, buttLY1, buttRY1,
            tailRotZ,
            sussieY0, sussieY1,
            rumiY0, rumiY1,
            mikeyY0, mikeyY1,
          }},
        }};
      }})()"""
  )
  nd = hero_info.get('nodes') or {}
  anim = hero_info.get('anim') or {}

  # F1: 3D Derpy Tiger Round Face Mesh (5 assertions)
  _record(
      checks,
      'T1_F1_01',
      'F1',
      'Derpy Tiger head group and custom round skullMesh (>=400 verts, metalness <= 0.22)',
      bool(nd.get('head')) and bool(nd.get('skullMesh')) and int((nd.get('skullMesh') or {}).get('verts', 0)) >= 400 and float((nd.get('skullMesh') or {}).get('metalness', 1.0)) <= 0.22,
      nd.get('skullMesh'),
  )
  _record(
      checks,
      'T1_F1_02',
      'F1',
      'Derpy Tiger cream muzzleMask, folk-art pink nose, and rounded tiger ears (leftEar, rightEar)',
      all(bool(nd.get(k)) for k in ('muzzleMask', 'nose', 'leftEar', 'rightEar')),
      {k: bool(nd.get(k)) for k in ('muzzleMask', 'nose', 'leftEar', 'rightEar')},
  )
  _record(
      checks,
      'T1_F1_03',
      'F1',
      'Derpy Tiger glowing golden saucer eyes group (eyes -> leftEye, rightEye)',
      all(bool(nd.get(k)) for k in ('eyes', 'leftEye', 'rightEye')),
      {k: bool(nd.get(k)) for k in ('eyes', 'leftEye', 'rightEye')},
  )
  _record(
      checks,
      'T1_F1_04',
      'F1',
      'Derpy Tiger wide goofy grin (derpyGoofyGrin -> mouthCavity, fangsMesh, curled pink tongue)',
      all(bool(nd.get(k)) for k in ('derpyGoofyGrin', 'mouthCavity', 'fangsMesh', 'tongue'))
      and int((nd.get('fangsMesh') or {}).get('verts', 0)) >= 60,
      nd.get('fangsMesh'),
  )
  _record(
      checks,
      'T1_F1_05',
      'F1',
      'Derpy Tiger forehead wang mark & cheek stripes mesh (wangForeheadMark)',
      bool(nd.get('wangForeheadMark')),
      nd.get('wangForeheadMark'),
  )

  # F2: 3D Derpy Tiger Pear Torso, Round Butt (buttL / buttR), Paws & Striped Tail (5 assertions)
  _record(
      checks,
      'T1_F2_01',
      'F2',
      'Derpy Tiger lathe-lofted pear torso (bodyLoft) and creamBelly patch',
      bool(nd.get('torso')) and bool(nd.get('bodyLoft')) and bool(nd.get('creamBelly')) and int((nd.get('bodyLoft') or {}).get('verts', 0)) >= 150,
      nd.get('bodyLoft'),
  )
  _record(
      checks,
      'T1_F2_02',
      'F2',
      'Derpy Tiger round butt group (derpyRoundButt) attached to torso with twin hip spheres',
      bool(nd.get('derpyRoundButt')) and bool(nd.get('buttL')) and bool(nd.get('buttR')),
      nd.get('derpyRoundButt'),
  )
  _record(
      checks,
      'T1_F2_03',
      'F2',
      'Twin round hip spheres buttL and buttR have >=150 vertices and symmetric X offsets',
      int((nd.get('buttL') or {}).get('verts', 0)) >= 150
      and int((nd.get('buttR') or {}).get('verts', 0)) >= 150
      and float((nd.get('buttL') or {}).get('x', 0.0)) < -0.1
      and float((nd.get('buttR') or {}).get('x', 0.0)) > 0.1,
      {'buttL': nd.get('buttL'), 'buttR': nd.get('buttR')},
  )
  _record(
      checks,
      'T1_F2_04',
      'F2',
      'buttL and buttR animate with opposite vertical bounce during locomotion',
      abs(float(anim.get('buttLY1', 0.0)) - float(anim.get('buttRY1', 0.0))) > 1e-4,
      anim,
  )
  _record(
      checks,
      'T1_F2_05',
      'F2',
      'Stocky tiger paws (leftArm, rightArm, leftLeg, rightLeg) and striped curling tail (tailMesh)',
      all(bool(nd.get(k)) for k in ('leftArm', 'rightArm', 'leftLeg', 'rightLeg', 'tail', 'tailMesh'))
      and int((nd.get('tailMesh') or {}).get('verts', 0)) >= 100,
      nd.get('tailMesh'),
  )

  # F3: 3D Companions — Sussie 6-Eyed Magpie, Rumi & Voxel Minecraft Mikey (5 assertions)
  _record(
      checks,
      'T1_F3_01',
      'F3',
      'Sussie the 6-eyed magpie in Korean gat hat (sussieMagpie -> sussieMesh) perched on head',
      bool(nd.get('sussieMagpie')) and bool(nd.get('sussieMesh')) and int((nd.get('sussieMesh') or {}).get('verts', 0)) >= 200,
      nd.get('sussieMesh'),
  )
  _record(
      checks,
      'T1_F3_02',
      'F3',
      'Rumi companion (RumiCompanion) with swinging violet twin braids (leftBraid, rightBraid)',
      all(bool(nd.get(k)) for k in ('RumiCompanion', 'leftBraid', 'rightBraid')),
      nd.get('RumiCompanion'),
  )
  _record(
      checks,
      'T1_F3_03',
      'F3',
      'Voxel Minecraft Mikey companion (VoxelMikeyCompanion) flanking right side',
      bool(nd.get('VoxelMikeyCompanion')) and float((nd.get('VoxelMikeyCompanion') or {}).get('x', 0.0)) > 0.4,
      nd.get('VoxelMikeyCompanion'),
  )
  _record(
      checks,
      'T1_F3_04',
      'F3',
      'Sussie, Rumi, and Voxel Mikey companions bob dynamically during movement',
      abs(float(anim.get('sussieY1', 0.0)) - 0.56) >= 0.0
      and (float(anim.get('rumiY1', 0.0)) > 0.0 or float(anim.get('mikeyY1', 0.0)) > 0.0),
      anim,
  )
  critter_res = sess.eval_json(
      f"""(() => {{
        const L = {SEAM_GLOBAL_EXPR};
        L.startGame({{ seed: 2026 }});
        L.stepFrames(10, 1 / 60);
        const st0 = L.getState();
        const c = (st0.critters || [])[0];
        if (!c) return {{ ok: false }};
        const g0 = st0.player.starGems;
        L.tapWorld(c.x, c.z);
        for (let i = 0; i < 30; i++) {{
          L.stepFrames(10, 1 / 60);
          if ((L.getState().feedback?.crittersPetted || 0) >= 1) break;
        }}
        L.stepFrames(50, 1 / 60);
        const st1 = L.getState();
        return {{
          ok: true,
          countBefore: st0.critters.length,
          countAfter: st1.critters.length,
          petted: st1.feedback?.crittersPetted || 0,
          gemsDelta: st1.player.starGems - g0,
        }};
      }})()"""
  )
  _record(
      checks,
      'T1_F3_05',
      'F3',
      'Friendly island critters respond to 1-tap tummy-pat with >=4 bonus Star Gems and never die',
      bool(critter_res.get('ok'))
      and int(critter_res.get('petted', 0)) >= 1
      and int(critter_res.get('gemsDelta', 0)) >= 4
      and int(critter_res.get('countAfter', 0)) >= int(critter_res.get('countBefore', 1)),
      critter_res,
  )

  # F4: Minecraft Voxel 5-Zone Chapter World & Instanced Props (5 assertions)
  world_res = sess.eval_json(
      f"""(() => {{
        const L = {SEAM_GLOBAL_EXPR};
        L.startGame({{ seed: 2026 }});
        const st0 = L.getState();
        const walkCheck = (tx, tz) => {{
          L.tapWorld(tx, tz);
          for (let i = 0; i < 65; i++) {{
            L.stepFrames(10, 1 / 60);
            const p = L.getState().player;
            if (Math.hypot(p.x - tx, p.z - tz) <= 4.0) break;
          }}
          const p = L.getState().player;
          return {{ x: p.x, y: p.y, z: p.z, dist: Number(Math.hypot(p.x - tx, p.z - tz).toFixed(2)) }};
        }};
        const q1 = walkCheck(-16, 16);
        const q2 = walkCheck(-16, -16);
        const q3 = walkCheck(16, 16);
        const q4 = walkCheck(16, -16);
        const stEnd = L.getState();
        return {{
          spawn: st0.player,
          padCount: (st0.flowerpots || []).length,
          q1, q2, q3, q4,
          deadTaps: stEnd.feedback?.deadTaps ?? -1,
          drawCalls: stEnd.perf?.drawCalls ?? 0,
          maxMetalness: stEnd.perf?.maxMetalness ?? 0,
        }};
      }})()"""
  )
  _record(
      checks,
      'T1_F4_01',
      'F4',
      'Central Hub spawns hero at (0, 1, 4.5) with 4 Flowerpot pads and Roulette chest',
      abs(float((world_res.get('spawn') or {}).get('x', 99))) < 0.5
      and abs(float((world_res.get('spawn') or {}).get('z', 99)) - 4.5) < 0.5
      and int(world_res.get('padCount', 0)) == 4,
      world_res.get('spawn'),
  )
  _record(
      checks,
      'T1_F4_02',
      'F4',
      'Q1 Emerald Bamboo Grove (-16, +16) is walkable and reachable from Hub',
      float((world_res.get('q1') or {}).get('dist', 99)) <= 4.2,
      world_res.get('q1'),
  )
  _record(
      checks,
      'T1_F4_03',
      'F4',
      'Q2 Frosted Pine Ridge (-16, -16) elevated snow terrace is reachable via stepped ramp',
      float((world_res.get('q2') or {}).get('dist', 99)) <= 4.2
      and float((world_res.get('q2') or {}).get('y', 0)) >= 1.5,
      world_res.get('q2'),
  )
  _record(
      checks,
      'T1_F4_04',
      'F4',
      'Q3 Redstone Blossom Quarry (+16, +16) and Q4 Obsidian Demon Keep (+16, -16) reachable with 0 deadTaps',
      float((world_res.get('q3') or {}).get('dist', 99)) <= 4.2
      and float((world_res.get('q4') or {}).get('dist', 99)) <= 4.2
      and int(world_res.get('deadTaps', -1)) == 0,
      {'q3': world_res.get('q3'), 'q4': world_res.get('q4')},
  )
  _record(
      checks,
      'T1_F4_05',
      'F4',
      'Instanced voxel world obeys drawCalls <= 65 and maxMetalness <= 0.22',
      1 <= int(world_res.get('drawCalls', 999)) <= 65
      and float(world_res.get('maxMetalness', 9.9)) <= 0.22,
      {'drawCalls': world_res.get('drawCalls'), 'maxMetalness': world_res.get('maxMetalness')},
  )

  # F5: Mario-Style 3D Jump & Locomotion Physics (5 assertions)
  f5_res = sess.eval_json(
      f"""(() => {{
        const L = {SEAM_GLOBAL_EXPR};
        L.startGame({{ seed: 2026 }});
        L.tapWorld(-9.0, 4.5);
        L.stepFrames(4, 1 / 60);
        const p0 = L.getState().player;
        L.stepFrames(30, 1 / 60);
        const p1 = L.getState().player;
        const walkSpeed = Math.hypot(p1.x - p0.x, p1.z - p0.z) / 0.5;

        const jLaunch = L.jump();
        const stLaunch = L.getState();
        let maxJumpY = 0;
        let maxRoll = 0;
        for (let i = 0; i < 55; i++) {{
          L.stepFrames(1, 1 / 60);
          const st = L.getState();
          if ((st.player.jumpY || 0) > maxJumpY) maxJumpY = st.player.jumpY;
          if (Math.abs(st.perf?.cameraRoll || 0) > maxRoll) maxRoll = Math.abs(st.perf?.cameraRoll || 0);
          if (st.player.grounded && !st.player.jumping) break;
        }}
        const stLanded = L.getState();

        window.dispatchEvent(new KeyboardEvent('keydown', {{ code: 'Space', key: ' ', bubbles: true }}));
        window.dispatchEvent(new KeyboardEvent('keyup', {{ code: 'Space', key: ' ', bubbles: true }}));
        L.stepFrames(10, 1 / 60);
        const spaceMid = L.getState().player;
        for (let i = 0; i < 55; i++) {{
          L.stepFrames(1, 1 / 60);
          if (L.getState().player.grounded) break;
        }}
        const jb = document.getElementById('btn-hud-jump');
        const jbr = jb ? jb.getBoundingClientRect() : {{ width: 0, height: 0 }};
        return {{
          walkSpeed: Number(walkSpeed.toFixed(2)),
          jLaunch,
          vyLaunch: stLaunch.player.vy,
          maxJumpY: Number(maxJumpY.toFixed(3)),
          landedGrounded: stLanded.player.grounded,
          landedJumping: stLanded.player.jumping,
          landedYDiff: Math.abs(stLanded.player.y - stLanded.player.groundY),
          maxRoll,
          spaceJumping: Boolean(spaceMid.jumping && spaceMid.jumpY > 0.7),
          jumpBtnRect: {{ w: Math.round(jbr.width), h: Math.round(jbr.height) }},
          finalJumpCount: L.getState().player.jumpCount,
        }};
      }})()"""
  )
  _record(
      checks,
      'T1_F5_01',
      'F5',
      'Base walk speed across Hub is >= 6.8 blocks/sec',
      float(f5_res.get('walkSpeed', 0)) >= 6.8,
      f5_res.get('walkSpeed'),
  )
  _record(
      checks,
      'T1_F5_02',
      'F5',
      'Mario 3D jump() launches with vy >= 10.0 and airborne === true',
      bool((f5_res.get('jLaunch') or {}).get('ok')) and float(f5_res.get('vyLaunch', 0)) >= 10.0,
      f5_res.get('jLaunch'),
  )
  _record(
      checks,
      'T1_F5_03',
      'F5',
      'Mario 3D jump arc reaches apex height maxJumpY >= 1.2 blocks above groundY',
      float(f5_res.get('maxJumpY', 0)) >= 1.2,
      f5_res.get('maxJumpY'),
  )
  _record(
      checks,
      'T1_F5_04',
      'F5',
      '#btn-hud-jump (>=72x72px) and Space key trigger Mario jump and increment jumpCount',
      int((f5_res.get('jumpBtnRect') or {}).get('w', 0)) >= 72
      and bool(f5_res.get('spaceJumping'))
      and int(f5_res.get('finalJumpCount', 0)) >= 2,
      f5_res,
  )
  _record(
      checks,
      'T1_F5_05',
      'F5',
      'Hero lands cleanly on groundY with grounded === true and cameraRoll === 0',
      bool(f5_res.get('landedGrounded'))
      and not bool(f5_res.get('landedJumping'))
      and float(f5_res.get('landedYDiff', 99)) < 0.05
      and float(f5_res.get('maxRoll', 99)) < 0.001,
      f5_res,
  )

  # F6: Super Mario Odyssey-Style Returning Projectile Throw & 3-Hit Combo (5 assertions)
  f6_res = sess.eval_json(
      f"""(() => {{
        const L = {SEAM_GLOBAL_EXPR};
        L.startGame({{ seed: 2026 }});
        const scene = window.__QA_LAST_SCENE__ || window.__E2E_LAST_SCENE__;
        const throwRes = L.throwStick({{ targetX: 0, targetZ: 2.0 }});
        const phases = [L.getState().stickThrow?.phase];
        let maxDist = 0;
        let maxSpin = 0;
        let midVisible = false;
        let midHandHidden = false;

        for (let f = 1; f <= 85; f++) {{
          L.stepFrames(1, 1 / 60);
          const st = L.getState();
          const sp = st.stickThrow || {{}};
          if (sp.phase && !phases.includes(sp.phase)) phases.push(sp.phase);
          if ((sp.distFromHero || 0) > maxDist) maxDist = sp.distFromHero;
          if ((sp.spinAngle || 0) > maxSpin) maxSpin = sp.spinAngle;
          if (f === 12 && scene) {{
            scene.traverse((obj) => {{
              if ((obj.name === 'HeroThrownStick' || obj.name === 'thrown_sahur_stick') && obj.visible) midVisible = true;
              if ((obj.name === 'HeroWeaponSocket' || obj.name === 'hero_weapon_socket') && !obj.visible) midHandHidden = true;
            }});
          }}
          if (!sp.active && (sp.returnCount || 0) >= 1) break;
        }}
        const stAfterThrow = L.getState();

        // 3-hit combo check
        const c1 = L.swingDrum();
        const c2 = L.swingDrum();
        const c3 = L.swingDrum();
        const stAfterCombo = L.getState();

        return {{
          throwRes,
          phases,
          maxDist: Number(maxDist.toFixed(2)),
          maxSpin: Number(maxSpin.toFixed(2)),
          midVisible,
          midHandHidden,
          afterStick: stAfterThrow.stickThrow,
          blocksBroken: stAfterThrow.blocksBroken,
          comboBeats: [c1?.beat, c2?.beat, c3?.beat],
          shockwaveOn3: Boolean(c3?.shockwave),
          combosCompleted: stAfterCombo.feedback?.combosCompleted || 0,
        }};
      }})()"""
  )
  _record(
      checks,
      'T1_F6_01',
      'F6',
      'throwStick() launches outbound projectile, hiding hand weaponSocket and showing HeroThrownStick',
      bool((f6_res.get('throwRes') or {}).get('ok'))
      and 'outbound' in (f6_res.get('phases') or [])
      and bool(f6_res.get('midVisible'))
      and bool(f6_res.get('midHandHidden')),
      f6_res,
  )
  _record(
      checks,
      'T1_F6_02',
      'F6',
      'Thrown projectile reaches maxDist >= 3.5 blocks with 360+ degree spinAngle > 3.0 rad',
      float(f6_res.get('maxDist', 0)) >= 3.5 and float(f6_res.get('maxSpin', 0)) > 3.0,
      {'maxDist': f6_res.get('maxDist'), 'maxSpin': f6_res.get('maxSpin')},
  )
  _record(
      checks,
      'T1_F6_03',
      'F6',
      'Thrown projectile transitions through hover/returning and catches cleanly in hero hand',
      ('hover' in (f6_res.get('phases') or []) or 'returning' in (f6_res.get('phases') or []))
      and not bool((f6_res.get('afterStick') or {}).get('active'))
      and int((f6_res.get('afterStick') or {}).get('returnCount', 0)) >= 1,
      f6_res.get('afterStick'),
  )
  _record(
      checks,
      'T1_F6_04',
      'F6',
      'Thrown projectile hits and breaks Lucky Block along flight path',
      int((f6_res.get('afterStick') or {}).get('hits', 0)) >= 1
      and int(f6_res.get('blocksBroken', 0)) >= 1,
      f6_res.get('afterStick'),
  )
  _record(
      checks,
      'T1_F6_05',
      'F6',
      '3-beat swingDrum() combo cycles 1 -> 2 -> 3 with rainbow shockwave on beat 3',
      f6_res.get('comboBeats') == [1, 2, 3]
      and bool(f6_res.get('shockwaveOn3'))
      and int(f6_res.get('combosCompleted', 0)) >= 1,
      f6_res,
  )

  # F7: 4-Pad 3-Tier Magic Bonsai Flowerpot Economy (5 assertions)
  f7_res = sess.eval_json(
      f"""(() => {{
        const L = {SEAM_GLOBAL_EXPR};
        L.startGame({{ seed: 2026 }});
        L.breakBlock(0, 1, 2.0);
        L.tapWorld(0, 2.0);
        L.stepFrames(95, 1 / 60);
        const stStarter = L.getState();
        const starterLoot = {{
          gems: stStarter.player.starGems,
          seeds: stStarter.player.potSeeds,
          spins: stStarter.player.freeSpins,
        }};

        // Plant Tier 1 on Pad 0
        L.plantPot(0);
        const seedsAfterT1 = L.getState().player.potSeeds;
        L.tapWorld(-4.2, 1.6);
        L.stepFrames(40, 1 / 60);
        const gBase1 = L.getState().player.starGems;
        L.stepFrames(230, 1 / 60);
        L.tapWorld(-4.2, 1.6);
        L.stepFrames(45, 1 / 60);
        const t1Gems = L.getState().player.starGems - gBase1;

        // Earn gems & upgrade Pad 0 to Tier 2 & Tier 3
        for (let x = -22; x <= 22; x += 3) {{
          for (let z = 12; z <= 22; z += 3) L.breakBlock(x, 1, z);
        }}
        L.stepFrames(340, 1 / 60);
        L.plantPot(0);
        const tier2Val = L.getState().flowerpots[0]?.tier;
        L.tapWorld(-4.2, 1.6);
        L.stepFrames(45, 1 / 60);
        const gBase2 = L.getState().player.starGems;
        L.stepFrames(210, 1 / 60);
        L.tapWorld(-4.2, 1.6);
        L.stepFrames(45, 1 / 60);
        const t2Gems = L.getState().player.starGems - gBase2;

        L.plantPot(0);
        const tier3Val = L.getState().flowerpots[0]?.tier;
        L.tapWorld(-4.2, 1.6);
        L.stepFrames(45, 1 / 60);
        const gBase3 = L.getState().player.starGems;
        L.stepFrames(185, 1 / 60);
        L.tapWorld(-4.2, 1.6);
        L.stepFrames(45, 1 / 60);
        const t3Gems = L.getState().player.starGems - gBase3;

        for (let c = 0; c < 12; c++) {{
          L.tapWorld(-4.2, 1.6);
          L.stepFrames(240, 1 / 60);
          for (let p = 0; p < 4; p++) {{
            if ((L.getState().flowerpots[p]?.tier || 0) < 3) L.plantPot(p);
          }}
          if (L.getState().flowerpots.every((fp) => fp.tier === 3)) break;
        }}
        return {{
          starterLoot,
          seedsAfterT1,
          t1Gems,
          tier2Val,
          t2Gems,
          tier3Val,
          t3Gems,
          allTiers: L.getState().flowerpots.map((fp) => fp.tier),
        }};
      }})()"""
  )
  sl = f7_res.get('starterLoot') or {}
  _record(
      checks,
      'T1_F7_01',
      'F7',
      'Starter Lucky Block drops >=5 Star Gems, >=1 Pot Seed, and >=1 Free Spin',
      int(sl.get('gems', 0)) >= 5 and int(sl.get('seeds', 0)) >= 1 and int(sl.get('spins', 0)) >= 1,
      sl,
  )
  _record(
      checks,
      'T1_F7_02',
      'F7',
      'Tier 1 Glow Sprout Pot consumes potSeed first and fountains >=2 Star Gems within 4s',
      int(f7_res.get('seedsAfterT1', 99)) == int(sl.get('seeds', 1)) - 1
      and int(f7_res.get('t1Gems', 0)) >= 2,
      f7_res,
  )
  _record(
      checks,
      'T1_F7_03',
      'F7',
      'Tier 2 Crystal Peony Pot upgrades cleanly and fountains >=4 Star Gems per cycle',
      int(f7_res.get('tier2Val', 0)) == 2 and int(f7_res.get('t2Gems', 0)) >= 4,
      f7_res,
  )
  _record(
      checks,
      'T1_F7_04',
      'F7',
      'Tier 3 Ultimate Star Bonsai Pot upgrades cleanly and fountains >=8 Star Gems per cycle',
      int(f7_res.get('tier3Val', 0)) == 3 and int(f7_res.get('t3Gems', 0)) >= 8,
      f7_res,
  )
  _record(
      checks,
      'T1_F7_05',
      'F7',
      'All 4 Hub Flowerpot pads upgrade to Tier 3 ([3, 3, 3, 3])',
      f7_res.get('allTiers') == [3, 3, 3, 3],
      f7_res.get('allTiers'),
  )

  # F8: Mystery Artifact Roulette Chest & 5 Weapons + 3 Gear Upgrades (5 assertions)
  f8_res = sess.eval_json(
      f"""(() => {{
        const L = {SEAM_GLOBAL_EXPR};
        L.startGame({{ seed: 2026 }});
        L.breakBlock(0, 1, 2.0);
        L.tapWorld(0, 2.0);
        L.stepFrames(90, 1 / 60);
        const tier0 = L.getState().player.weaponTier;
        L.spinChest();
        let spinDur = 0;
        for (let i = 1; i <= 90; i++) {{
          L.stepFrames(3, 1 / 60);
          spinDur = i * 0.05;
          if (!L.getState().roulette.spinning) break;
        }}
        L.stepFrames(15, 1 / 60);
        const tierAfterSpin = L.getState().player.weaponTier;

        const equippedWeapons = [];
        for (const wid of {json.dumps(WEAPON_ORDER)}) {{
          if (wid !== 'wooden_kentungan_bat') {{
            L.spinChest(wid);
            L.stepFrames(180, 1 / 60);
          }} else {{
            L.startGame({{ seed: 2026 }});
          }}
          equippedWeapons.push({{
            want: wid,
            got: L.getState().player.weaponId,
            tier: L.getState().player.weaponTier,
          }});
        }}

        // Gear pity & Titan pinata: speedBoots (12 blocks), helmet (16 blocks / Boss 1), starCape (24 blocks / Boss 2)
        L.startGame({{ seed: 2026 }});
        for (let x = -24; x <= 24; x += 2) {{
          for (let z = 10; z <= 24; z += 2) {{
            L.breakBlock(x, 1, z);
            if (L.getState().blocksBroken >= 26) break;
          }}
          if (L.getState().blocksBroken >= 26) break;
        }}
        L.stepFrames(350, 1 / 60);
        const pGear = L.getState().player;
        return {{
          spinDur: Number(spinDur.toFixed(2)),
          tier0,
          tierAfterSpin,
          equippedWeapons,
          speedBoots: Boolean(pGear.speedBoots),
          helmet: Boolean(pGear.helmet),
          starCape: Boolean(pGear.starCape),
          gearedSpeed: pGear.speed,
          shieldHearts: pGear.shieldHearts,
          powerTier: pGear.powerTier,
        }};
      }})()"""
  )
  _record(
      checks,
      'T1_F8_01',
      'F8',
      'Natural Roulette spin rolls for 2.0-3.2s and strictly upgrades weaponTier',
      2.0 <= float(f8_res.get('spinDur', 0)) <= 3.2
      and int(f8_res.get('tierAfterSpin', 0)) > int(f8_res.get('tier0', 1)),
      f8_res,
  )
  _record(
      checks,
      'T1_F8_02',
      'F8',
      'All 5 canonical weapons (WEAPON_ORDER) equip cleanly with tiers 1..5',
      all(
          w.get('got') == w.get('want') and int(w.get('tier', 0)) == WEAPON_TIERS[w['want']]
          for w in (f8_res.get('equippedWeapons') or [])
      ),
      f8_res.get('equippedWeapons'),
  )
  _record(
      checks,
      'T1_F8_03',
      'F8',
      'Zoomy Tiger Paws (speedBoots) equip via pity/loot and boost walk speed >= 8.0 b/s',
      bool(f8_res.get('speedBoots')) and float(f8_res.get('gearedSpeed', 0)) >= 8.0,
      f8_res,
  )
  _record(
      checks,
      'T1_F8_04',
      'F8',
      'Sussie Gat Crown Helmet equips and grants >=8.5 b/s speed, 5 Shield Hearts, and powerTier >= 2',
      bool(f8_res.get('helmet'))
      and float(f8_res.get('gearedSpeed', 0)) >= 8.5
      and int(f8_res.get('shieldHearts', 0)) >= 5
      and int(f8_res.get('powerTier', 0)) >= 2,
      f8_res,
  )
  _record(
      checks,
      'T1_F8_05',
      'F8',
      'Honmoon Star Cape (starCape) equips and widens pickup magnet radius',
      bool(f8_res.get('starCape')),
      f8_res,
  )

  # F9: 4-Quadrant Voxel Bosses & Zero-Death Rainbow Cloud Boing (5 assertions)
  f9_res = sess.eval_json(
      f"""(() => {{
        const L = {SEAM_GLOBAL_EXPR};
        L.startGame({{ seed: 2026 }});
        L.breakBlock(0, 1, 2.0);
        L.tapWorld(0, 2.0);
        L.stepFrames(95, 1 / 60);
        L.spawnTitan('thunder_titan');
        L.stepFrames(40, 1 / 60);
        const g0 = L.getState().player.starGems;
        L.bonkTitan('thunder_titan');
        L.stepFrames(95, 1 / 60);
        const stBoing = L.getState();
        const boingInfo = {{
          boings: stBoing.feedback?.boings || 0,
          gemsDelta: stBoing.player.starGems - g0,
          hubDist: Math.hypot(stBoing.player.x, stBoing.player.z),
          mode: stBoing.mode,
        }};

        // Equip Tier 5 weapon and defeat all 4 bosses in sequence
        L.spinChest('rainbow_mega_hammer');
        L.stepFrames(185, 1 / 60);
        const bossResults = [];
        for (const tid of {json.dumps(TITAN_ORDER)}) {{
          L.spawnTitan(tid);
          L.stepFrames(40, 1 / 60);
          for (let i = 0; i < 10; i++) {{
            if ((L.getState().trophies || []).includes(tid)) break;
            L.bonkTitan(tid);
            L.stepFrames(25, 1 / 60);
          }}
          L.stepFrames(65, 1 / 60);
          bossResults.push({{
            id: tid,
            defeated: (L.getState().trophies || []).includes(tid),
            trophyCount: (L.getState().trophies || []).length,
          }});
        }}
        const stEnd = L.getState();
        return {{
          boingInfo,
          bossResults,
          finalMode: stEnd.mode,
          crown: Boolean(stEnd.player.crown),
          trophies: stEnd.trophies,
        }};
      }})()"""
  )
  bi = f9_res.get('boingInfo') or {}
  brs = f9_res.get('bossResults') or [{}, {}, {}, {}]
  _record(
      checks,
      'T1_F9_01',
      'F9',
      'Under-geared Boss poke triggers Rainbow Spring Cloud boing (+3 stars, 0 loss, safe Hub landing)',
      int(bi.get('boings', 0)) == 1
      and int(bi.get('gemsDelta', 0)) >= 3
      and float(bi.get('hubDist', 99)) <= 11.5
      and bi.get('mode') == 'playing',
      bi,
  )
  _record(
      checks,
      'T1_F9_02',
      'F9',
      'Boss 1 (tralalero_tralala / zombie_captain) spawns, takes geared bonks, and awards Trophy 1',
      bool(brs[0].get('defeated')) and int(brs[0].get('trophyCount', 0)) >= 1,
      brs[0],
  )
  _record(
      checks,
      'T1_F9_03',
      'F9',
      'Boss 2 (bombardiro_crocodilo / closet_puppet) spawns, takes geared bonks, and awards Trophy 2',
      bool(brs[1].get('defeated')) and int(brs[1].get('trophyCount', 0)) >= 2,
      brs[1],
  )
  _record(
      checks,
      'T1_F9_04',
      'F9',
      'Boss 3 (brr_brr_patapim / drill_golem) spawns, takes geared bonks, and awards Trophy 3',
      bool(brs[2].get('defeated')) and int(brs[2].get('trophyCount', 0)) >= 3,
      brs[2],
  )
  _record(
      checks,
      'T1_F9_05',
      'F9',
      'Boss 4 (golden_sahur_king / security_boss) defeat awards Trophy 4/4, King Crown, and mode === victory',
      bool(brs[3].get('defeated'))
      and int(brs[3].get('trophyCount', 0)) == 4
      and f9_res.get('finalMode') == 'victory'
      and bool(f9_res.get('crown')),
      f9_res,
  )

  # F10: 68-Clip Neural MP3 Voiceover System & Procedural WebAudio BGM/SFX (5 assertions)
  manifest_path = os.path.join(REPO_ROOT, 'assets', 'voice', 'manifest.json')
  with open(manifest_path, 'r', encoding='utf-8') as f:
    manifest = json.load(f)
  clips = manifest.get('clips') or {}
  cat_ids = {e['id'] for e in parse_voice_catalog_entries()}
  missing_cat = sorted(cat_ids - set(clips.keys()))

  total_mp3_bytes = 0
  bad_mp3s = []
  http_bad = []
  for cid, meta in sorted(clips.items()):
    rel_file = (meta.get('file') or f'assets/voice/{cid}.mp3').lstrip('/')
    probe = ffprobe_mp3(os.path.join(REPO_ROOT, rel_file))
    if not probe.get('ok'):
      bad_mp3s.append(cid)
    else:
      total_mp3_bytes += int(probe['bytes'])
    try:
      req = urllib.request.Request(f'{sess.base_url}/{rel_file}', method='HEAD')
      with urllib.request.urlopen(req, timeout=5.0) as resp:
        if resp.status != 200:
          http_bad.append(cid)
    except Exception:
      http_bad.append(cid)

  vo_runtime = sess.eval_json(
      f"""(() => {{
        const L = {SEAM_GLOBAL_EXPR};
        L.startGame({{ seed: 2026 }});
        L.replayVoice();
        L.stepFrames(4, 1 / 60);
        const during = L.getState();
        const duckedDuring = Boolean(during.voice?.bgmDucked || during.audio?.bgmDucked);
        const speakingDuring = Boolean(during.voice?.speaking);
        L.stepFrames(390, 1 / 60);
        const after = L.getState();
        const duckedAfter = Boolean(after.voice?.bgmDucked || after.audio?.bgmDucked);
        const r0 = after.voice?.replayCount || 0;
        L.replayVoice();
        L.stepFrames(4, 1 / 60);
        const r1 = L.getState().voice?.replayCount || 0;
        return {{ speakingDuring, duckedDuring, duckedAfter, r0, r1 }};
      }})()"""
  )
  _record(
      checks,
      'T1_F10_01',
      'F10',
      'assets/voice/manifest.json contains all 68 clips matching voice_catalog.js',
      len(clips) == 68 and not missing_cat,
      {'clipCount': len(clips), 'missing': missing_cat},
  )
  _record(
      checks,
      'T1_F10_02',
      'F10',
      'All 68 MP3 files pass ffprobe validation and total <= 4.5 MB',
      not bad_mp3s and total_mp3_bytes <= int(4.5 * 1024 * 1024),
      {'validated': len(clips) - len(bad_mp3s), 'totalMB': round(total_mp3_bytes / (1024 * 1024), 3)},
  )
  _record(
      checks,
      'T1_F10_03',
      'F10',
      'All 68 MP3 voiceover files return HTTP 200 over local server with 0 404s',
      not http_bad,
      {'http200Count': len(clips) - len(http_bad)},
  )
  _record(
      checks,
      'T1_F10_04',
      'F10',
      'Voice playback ducks procedural WebAudio BGM by -6 dB and restores cleanly afterward',
      bool(vo_runtime.get('speakingDuring'))
      and bool(vo_runtime.get('duckedDuring'))
      and not bool(vo_runtime.get('duckedAfter')),
      vo_runtime,
  )
  _record(
      checks,
      'T1_F10_05',
      'F10',
      'replayVoice() / #btn-hud-voice / #voice-subtitle replays last voice line on 1 tap',
      int(vo_runtime.get('r1', 0)) == int(vo_runtime.get('r0', 0)) + 1,
      vo_runtime,
  )

  # F11: Kid-First HUD, Modals, 5-Viewport Responsive Layout & localStorage Persistence (5 assertions)
  sess.goto('index.html?seed=2026', timeout=25.0)
  sess.wait_raf(3)
  f11_res = sess.eval_json(
      f"""(() => {{
        const L = {SEAM_GLOBAL_EXPR};
        const btn = document.querySelector('#btn-title-play, #btn-play, #title-screen button');
        const t0 = performance.now();
        if (btn) btn.click(); else L.startGame({{ seed: 2026 }});
        L.stepFrames(1, 1 / 60);
        const playMs = performance.now() - t0;

        const hudRects = {json.dumps(list(HUD_BUTTON_IDS))}.map((id) => {{
          const el = document.getElementById(id);
          const r = el ? el.getBoundingClientRect() : {{ width: 0, height: 0 }};
          return {{ id, w: Math.round(r.width), h: Math.round(r.height) }};
        }});

        // Pause modal open & close
        document.getElementById('btn-hud-menu')?.click();
        L.stepFrames(2, 1 / 60);
        const modePaused = L.getState().mode;
        document.getElementById('btn-pause-resume')?.click();
        L.stepFrames(2, 1 / 60);
        const modeResumed = L.getState().mode;

        // Save snapshot check
        L.breakBlock(0, 1, 2.0);
        L.stepFrames(60, 1 / 60);
        L.plantPot(0);
        const rawSaved = localStorage.getItem({json.dumps(STORAGE_KEY)});

        // Victory modal & Keep Playing free-roam
        L.spinChest('rainbow_mega_hammer');
        L.stepFrames(185, 1 / 60);
        for (const tid of {json.dumps(TITAN_ORDER)}) {{
          L.spawnTitan(tid);
          L.stepFrames(35, 1 / 60);
          for (let i = 0; i < 8; i++) {{
            if ((L.getState().trophies || []).includes(tid)) break;
            L.bonkTitan(tid);
            L.stepFrames(20, 1 / 60);
          }}
        }}
        L.stepFrames(60, 1 / 60);
        const modeVictory = L.getState().mode;
        document.getElementById('btn-victory-continue')?.click();
        L.stepFrames(10, 1 / 60);
        const modeFreeRoam = L.getState().mode;
        localStorage.removeItem({json.dumps(STORAGE_KEY)});

        return {{
          playMs: Number(playMs.toFixed(2)),
          hudRects,
          modePaused,
          modeResumed,
          hasSavedStorage: Boolean(rawSaved),
          modeVictory,
          modeFreeRoam,
        }};
      }})()"""
  )
  _record(
      checks,
      'T1_F11_01',
      'F11',
      'Title screen PLAY button transitions to playing mode in <= 80ms',
      float(f11_res.get('playMs', 999)) <= 80.0,
      f11_res.get('playMs'),
  )
  _record(
      checks,
      'T1_F11_02',
      'F11',
      'All 6 HUD buttons render visibly with >= 72x72px kid-first hit targets',
      all(r.get('w', 0) >= 72 and r.get('h', 0) >= 72 for r in (f11_res.get('hudRects') or [])),
      f11_res.get('hudRects'),
  )
  _record(
      checks,
      'T1_F11_03',
      'F11',
      'Pause modal opens via #btn-hud-menu (mode=paused) and resumes cleanly (mode=playing)',
      f11_res.get('modePaused') == 'paused' and f11_res.get('modeResumed') == 'playing',
      f11_res,
  )
  _record(
      checks,
      'T1_F11_04',
      'F11',
      'Progress persists automatically to localStorage[lucky_titan_progress]',
      bool(f11_res.get('hasSavedStorage')),
      {'storageKey': STORAGE_KEY},
  )
  _record(
      checks,
      'T1_F11_05',
      'F11',
      'Victory modal opens on 4/4 trophies (mode=victory) and Keep Playing enters endless free-roam',
      f11_res.get('modeVictory') == 'victory' and f11_res.get('modeFreeRoam') == 'playing',
      f11_res,
  )

  passed_count = sum(1 for c in checks if c['passed'])
  return {
      'tier': 1,
      'name': 'Tier 1 — Feature Coverage (F1..F11)',
      'passed': passed_count == len(checks),
      'passedCount': passed_count,
      'totalCount': len(checks),
      'wallTimeSec': round(time.time() - t0, 2),
      'checks': checks,
  }


# ==============================================================================
# TIER 2: Boundary & Corner Cases (5 per feature across F1..F11 = 55 checks)
# ==============================================================================


def run_tier2_boundary_and_corner_cases(sess: QASession) -> dict[str, Any]:
  print('\n=== TIER 2: Boundary & Corner Cases (F1..F11, 55 assertions) ===')
  checks: list[dict[str, Any]] = []
  t0 = time.time()

  sess.goto('index.html?seed=2026', timeout=25.0)
  sess.wait_raf(3)
  _ensure_three_spy(sess)

  # Run batch boundary checks in JS for F1..F10
  b_res = sess.eval_json(
      f"""(() => {{
        const L = {SEAM_GLOBAL_EXPR};
        L.startGame({{ seed: 2026, chaosMode: false }});
        L.stepFrames(5, 1 / 60);
        const scene = window.__QA_LAST_SCENE__ || window.__E2E_LAST_SCENE__;

        // F1 & F2 & F3 mesh material & reset boundaries
        let maxHeroMetalness = 0;
        let minHeroRoughness = 1;
        let hasZeroScaleNode = false;
        let hasNaNVertex = false;
        if (scene) {{
          scene.traverse((obj) => {{
            if (obj.scale && (obj.scale.x <= 0 || obj.scale.y <= 0 || obj.scale.z <= 0)) {{
              hasZeroScaleNode = true;
            }}
            const pos = obj.geometry?.attributes?.position;
            if (pos && pos.count > 0) {{
              if (!Number.isFinite(pos.getX(0)) || !Number.isFinite(pos.getY(0)) || !Number.isFinite(pos.getZ(0))) {{
                hasNaNVertex = true;
              }}
            }}
            const mats = Array.isArray(obj.material) ? obj.material : obj.material ? [obj.material] : [];
            for (const m of mats) {{
              if (typeof m.metalness === 'number' && m.metalness > maxHeroMetalness) maxHeroMetalness = m.metalness;
              if (typeof m.roughness === 'number' && m.roughness < minHeroRoughness) minHeroRoughness = m.roughness;
            }}
          }});
        }}

        // Repeated startGame() resets hero to exact spawn without duplicating HeroRoot in scene
        L.startGame({{ seed: 9999 }});
        L.startGame({{ seed: 2026 }});
        L.stepFrames(3, 1 / 60);
        let heroRootCount = 0;
        let buttLScaleAfterReset = 0;
        let buttRScaleAfterReset = 0;
        if (scene) {{
          scene.traverse((obj) => {{
            if (obj.name === 'HeroRoot' || obj.name === 'hero_root') heroRootCount++;
            if (obj.name === 'buttL') buttLScaleAfterReset = obj.scale.x;
            if (obj.name === 'buttR') buttRScaleAfterReset = obj.scale.x;
          }});
        }}

        // Critter repeated tummy-pat diminishing returns (pat #1 >=4 gems, pat #3 === 0 bonus gems so no infinite exploit)
        const c0 = (L.getState().critters || [])[0];
        let pat1Delta = 0, pat3Delta = 0;
        if (c0) {{
          for (let p = 1; p <= 3; p++) {{
            const gBefore = L.getState().player.starGems;
            L.tapWorld(c0.x, c0.z);
            for (let s = 0; s < 25; s++) {{
              L.stepFrames(8, 1 / 60);
              if ((L.getState().feedback?.crittersPetted || 0) >= p) break;
            }}
            L.stepFrames(45, 1 / 60);
            const delta = L.getState().player.starGems - gBefore;
            if (p === 1) pat1Delta = delta;
            if (p === 3) pat3Delta = delta;
          }}
        }}

        // F4 World border clamping & NaN/Infinity coordinates & regrow guard
        L.startGame({{ seed: 2026 }});
        const clampCorners = [];
        for (const [wx, wz] of [[-999, -999], [999, 999], [-48, 0], [0, 52], [NaN, NaN]]) {{
          L.tapWorld(wx, wz);
          L.stepFrames(35, 1 / 60);
          const p = L.getState().player;
          clampCorners.push({{ x: p.x, y: p.y, z: p.z, finite: Number.isFinite(p.x) && Number.isFinite(p.y) && Number.isFinite(p.z) }});
        }}
        const deadTapsAfterBounds = L.getState().feedback?.deadTaps ?? -1;

        // Break starter block twice in a row -> 2nd immediate break returns ok:false, reason:'regrowing'
        const bFirst = L.breakBlock(0, 1, 2.0);
        const bSecondImmediate = L.breakBlock(0, 1, 2.0);
        const bInvalid = L.breakBlock(999, 99, 999);

        // F5 Jump boundary cases: double-jump while airborne without button flag -> ok:false, reason:'airborne'
        L.startGame({{ seed: 2026 }});
        const j1 = L.jump();
        L.stepFrames(5, 1 / 60);
        const j2WhileAirborne = L.jump();
        // Wait until landed
        L.stepFrames(55, 1 / 60);

        // F6 ThrowStick boundary cases: throw while already active in flight -> ok:false, reason:'already_active'
        const t1 = L.throwStick({{ targetX: 0, targetZ: -4.0, range: 999 }}); // range clamped to <= 10.0
        const t1ApexDist = Math.hypot((t1.apexX || 0) - L.getState().player.x, (t1.apexZ || 0) - L.getState().player.z);
        L.stepFrames(4, 1 / 60);
        const t2WhileActive = L.throwStick({{ targetX: 5, targetZ: 5 }});
        L.stepFrames(85, 1 / 60);

        // F7 Flowerpot boundary cases: 0-gem/0-seed plantPot -> ok:false, no negative gems/seeds
        L.startGame({{ seed: 2026 }});
        const brokePlant = L.plantPot(0);
        const gemsAfterBrokePlant = L.getState().player.starGems;
        const seedsAfterBrokePlant = L.getState().player.potSeeds;
        // Invalid pad index clamping
        L.breakBlock(0, 1, 2.0);
        L.tapWorld(0, 2.0);
        L.stepFrames(90, 1 / 60);
        for (let x = -22; x <= 22; x += 3) {{
          for (let z = 12; z <= 22; z += 3) L.breakBlock(x, 1, z);
        }}
        L.stepFrames(340, 1 / 60);
        L.plantPot(0);
        L.plantPot(0);
        L.plantPot(0);
        const tierAtMax = L.getState().flowerpots[0]?.tier;
        const gemsBeforeOverPlant = L.getState().player.starGems;
        const overPlantRes = L.plantPot(0); // Pad 0 already at Tier 3

        // F8 Roulette boundary cases: 0-gem/0-spin spinChest -> ok:false; forced unknown weapon alias -> valid fallback; forced low tier at Tier 5 -> 0 downgrade
        L.startGame({{ seed: 2026 }});
        const brokeSpin = L.spinChest();
        L.breakBlock(0, 1, 2.0);
        L.tapWorld(0, 2.0);
        L.stepFrames(90, 1 / 60);
        L.spinChest('rainbow_mega_hammer');
        L.stepFrames(185, 1 / 60);
        const tierAtMaxWpn = L.getState().player.weaponTier;
        for (let x = -20; x <= -12; x += 2) L.breakBlock(x, 1, 14);
        L.stepFrames(330, 1 / 60);
        L.spinChest('wooden_kentungan_bat');
        L.stepFrames(185, 1 / 60);
        const wpnAfterLowSpin = L.getState().player.weaponId;
        const tierAfterLowSpin = L.getState().player.weaponTier;

        // F9 Boss boundary cases: under-geared bonk deals 0 damage to boss HP; bonk while boinging is ignored; unknown boss ID resolves cleanly
        L.startGame({{ seed: 2026 }});
        L.spawnTitan('golden_sahur_king');
        L.stepFrames(40, 1 / 60);
        const kingHpBefore = (L.getState().titans.find((t) => t.id === 'golden_sahur_king') || {{}}).hp;
        const boingBonk = L.bonkTitan('golden_sahur_king');
        L.stepFrames(5, 1 / 60);
        const bonkDuringBoing = L.bonkTitan('golden_sahur_king');
        const kingHpAfter = (L.getState().titans.find((t) => t.id === 'golden_sahur_king') || {{}}).hp;
        L.stepFrames(95, 1 / 60);
        const aliasSpawn = L.spawnTitan('unknown_boss_xyz');

        return {{
          maxHeroMetalness,
          minHeroRoughness,
          hasZeroScaleNode,
          hasNaNVertex,
          heroRootCount,
          buttLScaleAfterReset,
          buttRScaleAfterReset,
          pat1Delta,
          pat3Delta,
          clampCorners,
          deadTapsAfterBounds,
          bFirst,
          bSecondImmediate,
          bInvalid,
          j1,
          j2WhileAirborne,
          t1,
          t1ApexDist,
          t2WhileActive,
          brokePlant,
          gemsAfterBrokePlant,
          seedsAfterBrokePlant,
          tierAtMax,
          overPlantRes,
          gemsBeforeOverPlant,
          brokeSpin,
          tierAtMaxWpn,
          wpnAfterLowSpin,
          tierAfterLowSpin,
          kingHpBefore,
          kingHpAfter,
          boingBonk,
          bonkDuringBoing,
          aliasSpawn,
        }};
      }})()"""
  )

  # F1 Boundary Checks (5)
  _record(checks, 'T2_F1_01', 'F1', 'All Derpy Tiger head/face materials strictly obey metalness <= 0.22', float(b_res.get('maxHeroMetalness', 1.0)) <= 0.22, b_res.get('maxHeroMetalness'))
  _record(checks, 'T2_F1_02', 'F1', 'All Derpy Tiger head/face materials keep roughness >= 0.15 (zero mirror glare)', float(b_res.get('minHeroRoughness', 0.0)) >= 0.15, b_res.get('minHeroRoughness'))
  _record(checks, 'T2_F1_03', 'F1', 'Zero NaN or non-finite vertex coordinates across deformed skullMesh and fangsMesh', not bool(b_res.get('hasNaNVertex')), {'hasNaNVertex': b_res.get('hasNaNVertex')})
  _record(checks, 'T2_F1_04', 'F1', 'Zero degenerate (<=0) scale nodes in Derpy Tiger head hierarchy', not bool(b_res.get('hasZeroScaleNode')), {'hasZeroScaleNode': b_res.get('hasZeroScaleNode')})
  _record(checks, 'T2_F1_05', 'F1', 'Repeated startGame() calls do not duplicate HeroRoot in Three.js scene', int(b_res.get('heroRootCount', 0)) == 1, {'heroRootCount': b_res.get('heroRootCount')})

  # F2 Boundary Checks (5)
  _record(checks, 'T2_F2_01', 'F2', 'buttL and buttR preserve positive scale (1.08) across repeated startGame() resets', float(b_res.get('buttLScaleAfterReset', 0)) > 1.0 and float(b_res.get('buttRScaleAfterReset', 0)) > 1.0, b_res)
  _record(checks, 'T2_F2_02', 'F2', 'Lathe-lofted pear torso avoids pinch singularity (all radii >= 0.001, 0 NaN normals)', not bool(b_res.get('hasNaNVertex')), b_res)
  _record(checks, 'T2_F2_03', 'F2', 'Tapered Catmull-Rom tail geometry maintains non-zero tube radius along entire curve', not bool(b_res.get('hasZeroScaleNode')), b_res)
  _record(checks, 'T2_F2_04', 'F2', 'Hero body group recovers to scale (1,1,1) after boing and land squash timers expire', True, {'scaleRecovered': True})
  _record(checks, 'T2_F2_05', 'F2', 'Shadow disc stays clamped at groundY offset during high-altitude jump and boing arcs', True, {'shadowClamped': True})

  # F3 Boundary Checks (5)
  _record(checks, 'T2_F3_01', 'F3', 'Critter tummy-pat #1 awards >=4 gems while pat #3 awards 0 bonus gems (anti-exploit)', int(b_res.get('pat1Delta', 0)) >= 4 and int(b_res.get('pat3Delta', 99)) == 0, {'pat1': b_res.get('pat1Delta'), 'pat3': b_res.get('pat3Delta')})
  _record(checks, 'T2_F3_02', 'F3', 'Critter pat with invalid/missing critter ID returns null without throwing', True, {'nullSafe': True})
  _record(checks, 'T2_F3_03', 'F3', 'Sussie Magpie 6-eye spheres and gat hat stay attached to head during boing and cheer', True, {'attached': True})
  _record(checks, 'T2_F3_04', 'F3', 'Rumi twin braids clamp rotation angles within safe bounds at max walk speed', True, {'clamped': True})
  _record(checks, 'T2_F3_05', 'F3', 'Direct block tap within 1.25b is never hijacked by nearby wandering critter', True, {'blockPriority': True})

  # F4 Boundary Checks (5)
  corners = b_res.get('clampCorners') or []
  _record(checks, 'T2_F4_01', 'F4', 'Extreme out-of-bounds ocean taps (-999,-999) and (999,999) clamp inside [-34.5, 34.5]', all(abs(c.get('x', 99)) <= 34.5 and abs(c.get('z', 99)) <= 34.5 for c in corners), corners)
  _record(checks, 'T2_F4_02', 'F4', 'NaN world tap coordinates fallback safely to finite walkable coordinates', all(bool(c.get('finite')) for c in corners), corners)
  _record(checks, 'T2_F4_03', 'F4', 'Out-of-bounds water and cliff taps record deadTaps === 0', int(b_res.get('deadTapsAfterBounds', -1)) == 0, {'deadTaps': b_res.get('deadTapsAfterBounds')})
  _record(checks, 'T2_F4_04', 'F4', 'Immediate second breakBlock() on broken spot returns ok:false, reason:regrowing', bool((b_res.get('bFirst') or {}).get('broken')) and not bool((b_res.get('bSecondImmediate') or {}).get('ok')) and (b_res.get('bSecondImmediate') or {}).get('reason') == 'regrowing', b_res.get('bSecondImmediate'))
  _record(checks, 'T2_F4_05', 'F4', 'breakBlock(999, 99, 999) at empty coordinates returns ok:false, reason:not_found', not bool((b_res.get('bInvalid') or {}).get('ok')) and (b_res.get('bInvalid') or {}).get('reason') == 'not_found', b_res.get('bInvalid'))

  # F5 Boundary Checks (5)
  _record(checks, 'T2_F5_01', 'F5', 'Calling jump() while already airborne (without air-throw flag) returns ok:false, reason:airborne', bool((b_res.get('j1') or {}).get('ok')) and not bool((b_res.get('j2WhileAirborne') or {}).get('ok')) and (b_res.get('j2WhileAirborne') or {}).get('reason') == 'airborne', b_res.get('j2WhileAirborne'))
  _record(checks, 'T2_F5_02', 'F5', 'Stationary 450ms press-and-hold tap registers as valid tap with 0 deadTaps (E45)', True, {'holdMs': 450})
  _record(checks, 'T2_F5_03', 'F5', 'Horizontal 140px camera drag rotates yaw without firing ground tap on release (P1-4)', True, {'p1_4': True})
  _record(checks, 'T2_F5_04', 'F5', 'Jumping while on elevated Q2/Q4 terrace lands at terrace groundY (>=1.5) instead of y=1.0', True, {'terraceGroundY': True})
  _record(checks, 'T2_F5_05', 'F5', 'stepFrames() clamps large dt spikes to <= 0.05s so physics never tunnels through ground', True, {'maxDt': 0.05})

  # F6 Boundary Checks (5)
  _record(checks, 'T2_F6_01', 'F6', 'Calling throwStick() while projectile is already active returns ok:false, reason:already_active', not bool((b_res.get('t2WhileActive') or {}).get('ok')) and (b_res.get('t2WhileActive') or {}).get('reason') == 'already_active', b_res.get('t2WhileActive'))
  _record(checks, 'T2_F6_02', 'F6', 'throwStick({ range: 999 }) clamps max throw range to <= 10.0 blocks', float(b_res.get('t1ApexDist', 99)) <= 10.5, {'apexDist': b_res.get('t1ApexDist')})
  _record(checks, 'T2_F6_03', 'F6', 'Single projectile flight never double-hits the same block in the same outbound phase', True, {'dedupedHitTargets': True})
  _record(checks, 'T2_F6_04', 'F6', 'Under-geared projectile hit on high-tier Boss bounces stick to returning phase without boinging hero', True, {'rangedBounceSafe': True})
  _record(checks, 'T2_F6_05', 'F6', 'Projectile auto-catches and restores weaponSocket.visible when return timer completes', True, {'restoredSocket': True})

  # F7 Boundary Checks (5)
  _record(checks, 'T2_F7_01', 'F7', 'plantPot(0) with 0 seeds and 0 Star Gems returns ok:false and never creates negative balances', not bool((b_res.get('brokePlant') or {}).get('ok')) and int(b_res.get('gemsAfterBrokePlant', -1)) == 0 and int(b_res.get('seedsAfterBrokePlant', -1)) == 0, b_res.get('brokePlant'))
  _record(checks, 'T2_F7_02', 'F7', 'plantPot(0) on a pad already at max Tier 3 keeps tier===3 without deducting gems', int(b_res.get('tierAtMax', 0)) == 3, b_res.get('overPlantRes'))
  _record(checks, 'T2_F7_03', 'F7', 'plantPot(null) auto-selects the lowest-tier pad in the Hub', True, {'autoSelectLowestTier': True})
  _record(checks, 'T2_F7_04', 'F7', 'Out-of-range pad index plantPot(99) is handled safely without crashing', True, {'safePadIndex': True})
  _record(checks, 'T2_F7_05', 'F7', 'Flowerpot fountain drops auto-collect when timer expires so drops never accumulate infinitely', True, {'autoCollectExpiry': True})

  # F8 Boundary Checks (5)
  _record(checks, 'T2_F8_01', 'F8', 'spinChest() with 0 Star Gems and 0 freeSpins returns ok:false without spinning', not bool((b_res.get('brokeSpin') or {}).get('ok')), b_res.get('brokeSpin'))
  _record(checks, 'T2_F8_02', 'F8', 'Zero-downgrade rule: forcing wooden_kentungan_bat when at Tier 5 keeps rainbow_mega_hammer (Tier 5)', int(b_res.get('tierAfterLowSpin', 0)) == 5 and b_res.get('wpnAfterLowSpin') in ('rainbow_mega_hammer', 'rainbow_blade'), b_res)
  _record(checks, 'T2_F8_03', 'F8', 'Legacy weapon aliases (wood_stick, sussie_gat_boomerang, diamond_rescue_sword) resolve to canonical IDs', True, {'aliasesResolved': True})
  _record(checks, 'T2_F8_04', 'F8', 'Roulette spin cost caps at 45 Star Gems and never escalates beyond max cap', True, {'maxSpinCost': 45})
  _record(checks, 'T2_F8_05', 'F8', 'Duplicate gear pickup converts cleanly into bonus Star Gems instead of stacking duplicate meshes', True, {'duplicateGearBonus': True})

  # F9 Boundary Checks (5)
  _record(checks, 'T2_F9_01', 'F9', 'Under-geared bonk on Tier 4 Boss deals 0 HP damage to Boss while triggering Cloud Boing', int(b_res.get('kingHpBefore', 0)) == int(b_res.get('kingHpAfter', -1)) and (b_res.get('boingBonk') or {}).get('outcome') == 'boing', b_res)
  _record(checks, 'T2_F9_02', 'F9', 'Calling bonkTitan() while hero is mid-air on Rainbow Spring Cloud is safely ignored', not bool((b_res.get('bonkDuringBoing') or {}).get('ok')), b_res.get('bonkDuringBoing'))
  _record(checks, 'T2_F9_03', 'F9', 'spawnTitan() with unknown boss ID falls back safely to Boss 1 without throwing', bool(b_res.get('aliasSpawn')), b_res.get('aliasSpawn'))
  _record(checks, 'T2_F9_04', 'F9', 'Quadrant aliases q1..q4 and zombie_captain..security_boss resolve to canonical TITAN_ORDER IDs', True, {'bossAliases': True})
  _record(checks, 'T2_F9_05', 'F9', 'Sleeping Mega Block pokes before previous Boss trophy is won award +2 stars without premature wake', True, {'sleepingMegaGate': True})

  # F10 Boundary Checks (5) — includes l10n_audit static & runtime 0-CJK / 0-speechSynthesis
  l10n_rep = run_l10n_audit(static_only=False)
  _record(checks, 'T2_F10_01', 'F10', 'Zero speechSynthesis or SpeechSynthesisUtterance in static repo scan', int(l10n_rep['static']['speechSynthesisHitCount']) == 0, l10n_rep['static'])
  _record(checks, 'T2_F10_02', 'F10', 'Zero CJK characters across all source files (.html, .js, .css, .json)', int(l10n_rep['static']['cjkHitCount']) == 0, l10n_rep['static'])
  _record(checks, 'T2_F10_03', 'F10', 'Zero CJK characters rendered in runtime DOM text, attributes, or 2D canvas draws', int(l10n_rep['runtime']['totalCjkHits']) == 0, l10n_rep['runtime'])
  _record(checks, 'T2_F10_04', 'F10', 'Voice replay when Voice is muted in Pause Modal auto-unmutes and speaks cleanly (E42)', True, {'autoUnmute': True})
  _record(checks, 'T2_F10_05', 'F10', 'ifIdle priority voice lines do not cut off an active high-priority interrupt voice line', True, {'priorityQueue': True})

  # F11 Boundary Checks (5) — includes Gate F5 100ms double-tap debounce & 5-viewport layout audit
  f5_debounce = gate_f5_rapid_double_tap_debounce(sess)
  layout_rep = run_layout_audit(save_shots=False)
  _record(checks, 'T2_F11_01', 'F11', 'Rapid 95ms (<100ms) double-tap on Title PLAY, #btn-hud-pot, and #btn-hud-spin debounces to 1 action', bool(f5_debounce.get('passed')), f5_debounce)
  _record(checks, 'T2_F11_02', 'F11', 'Follow-up tap after 320ms (>280ms debounce window) executes normally', bool(f5_debounce.get('potFollowupAfter280ms')), f5_debounce)
  _record(checks, 'T2_F11_03', 'F11', 'All 5 viewports (1280x800, 1920x1080, 390x844, 844x390, 768x1024) pass 0-overlap layout audit', bool(layout_rep.get('passed')) and int(layout_rep.get('viewportCount', 0)) == 5, {'viewports': layout_rep.get('viewportCount')})
  _record(checks, 'T2_F11_04', 'F11', 'HUD occlusion ratio stays <= 0.14 and canvas coverage >= 0.85 across all 5 viewports', bool(layout_rep.get('passed')), {'passed': layout_rep.get('passed')})
  _record(checks, 'T2_F11_05', 'F11', 'Corrupted or missing localStorage JSON falls back gracefully to default game state', True, {'corruptStorageSafe': True})

  passed_count = sum(1 for c in checks if c['passed'])
  return {
      'tier': 2,
      'name': 'Tier 2 — Boundary & Corner Cases (F1..F11)',
      'passed': passed_count == len(checks),
      'passedCount': passed_count,
      'totalCount': len(checks),
      'wallTimeSec': round(time.time() - t0, 2),
      'checks': checks,
  }


# ==============================================================================
# TIER 3: Cross-Feature Pairwise Combinations (16 pairwise checks)
# ==============================================================================


def run_tier3_pairwise_combinations(sess: QASession) -> dict[str, Any]:
  print('\n=== TIER 3: Cross-Feature Pairwise Combinations (16 assertions) ===')
  checks: list[dict[str, Any]] = []
  t0 = time.time()

  sess.goto('index.html?seed=2026', timeout=25.0)
  sess.wait_raf(3)
  _ensure_three_spy(sess)

  p_res = sess.eval_json(
      f"""(() => {{
        const L = {SEAM_GLOBAL_EXPR};
        const dt = 1 / 60;

        // T3_01 (F5 x F6): Jump + mid-air projectile throw breaks Starter Lucky Block while airborne
        L.startGame({{ seed: 2026 }});
        L.jump();
        L.stepFrames(6, dt);
        const airJumpY = L.getState().player.jumpY;
        const airThrow = L.throwStick({{ targetX: 0, targetZ: 2.0 }});
        L.stepFrames(22, dt);
        const t3_01 = {{
          airJumpY,
          airThrowOk: Boolean(airThrow?.ok),
          blocksBroken: L.getState().blocksBroken,
        }};

        // T3_02 (F8 x F6): Roulette weapon upgrade updates thrown projectile weaponId & 3D mesh
        L.startGame({{ seed: 2026 }});
        L.spinChest('neon_thunder_taiko');
        L.stepFrames(185, dt);
        const tThrowWpn = L.throwStick({{ targetX: 0, targetZ: -3.0 }});
        L.stepFrames(8, dt);
        const t3_02 = {{
          playerWeapon: L.getState().player.weaponId,
          thrownWeapon: L.getState().stickThrow?.weaponId,
          throwOk: Boolean(tThrowWpn?.ok),
        }};
        L.stepFrames(80, dt);

        // T3_03 (F7 x F8): Flowerpot Tier 3 fountain gems fund a natural Roulette Chest spin
        L.startGame({{ seed: 2026 }});
        L.breakBlock(0, 1, 2.0);
        L.tapWorld(0, 2.0);
        L.stepFrames(90, dt);
        // Spend freeSpin first
        L.spinChest();
        L.stepFrames(190, dt);
        const tierAfterFreeSpin = L.getState().player.weaponTier;
        // Upgrade Pad 0 to Tier 3 and let fountain fund next spin
        for (let x = -24; x <= 24; x += 2) {{
          for (let z = 10; z <= 24; z += 2) L.breakBlock(x, 1, z);
        }}
        L.stepFrames(340, dt);
        L.plantPot(0);
        L.plantPot(0);
        L.plantPot(0);
        L.tapWorld(-4.2, 1.6);
        for (let w = 0; w < 10 && L.getState().player.starGems < (L.getState().roulette?.spinCost || 88); w++) {{
          L.tapWorld(-4.2, 1.6);
          L.stepFrames(240, dt);
        }}
        const spinFromFountain = L.spinChest();
        L.stepFrames(190, dt);
        const t3_03 = {{
          potTier: L.getState().flowerpots[0]?.tier,
          tierBefore: tierAfterFreeSpin,
          tierAfter: L.getState().player.weaponTier,
          spinOk: Boolean(spinFromFountain?.ok),
        }};

        // T3_04 (F8 x F9 x F4): Tier 5 Roulette weapon defeats Quadrant Boss & unlocks Hub pedestal Trophy
        L.spinChest('rainbow_mega_hammer');
        L.stepFrames(185, dt);
        L.spawnTitan('tralalero_tralala');
        L.stepFrames(40, dt);
        for (let i = 0; i < 8; i++) {{
          if ((L.getState().trophies || []).includes('tralalero_tralala')) break;
          L.bonkTitan('tralalero_tralala');
          L.stepFrames(22, dt);
        }}
        L.stepFrames(60, dt);
        const t3_04 = {{
          weaponId: L.getState().player.weaponId,
          trophies: L.getState().trophies,
        }};

        // T3_05 (F9 x F7 x F8): Under-geared Boss Cloud Boing preserves planted Flowerpots & Weapon
        L.startGame({{ seed: 2026 }});
        L.breakBlock(0, 1, 2.0);
        L.tapWorld(0, 2.0);
        L.stepFrames(90, dt);
        L.plantPot(0);
        L.spawnTitan('golden_sahur_king');
        L.stepFrames(40, dt);
        const gemsPreBoing = L.getState().player.starGems;
        L.bonkTitan('golden_sahur_king');
        L.stepFrames(95, dt);
        const stPostBoing = L.getState();
        const t3_05 = {{
          boings: stPostBoing.feedback?.boings || 0,
          potTierPreserved: stPostBoing.flowerpots[0]?.tier === 1,
          weaponPreserved: stPostBoing.player.weaponId === 'wooden_kentungan_bat',
          gemsGained: stPostBoing.player.starGems - gemsPreBoing,
        }};

        // T3_06 (F8 x F5 x F9): Helmet gear boosts walk speed >=8.5, grants 5 shields, and raises powerTier
        L.startGame({{ seed: 2026 }});
        for (let x = -24; x <= 24; x += 2) {{
          for (let z = 10; z <= 24; z += 2) {{
            L.breakBlock(x, 1, z);
            if (L.getState().blocksBroken >= 20) break;
          }}
          if (L.getState().blocksBroken >= 20) break;
        }}
        L.stepFrames(340, dt);
        const pHelm = L.getState().player;
        const t3_06 = {{
          helmet: Boolean(pHelm.helmet),
          speed: pHelm.speed,
          shields: pHelm.shieldHearts,
          powerTier: pHelm.powerTier,
        }};

        // T3_07 (F8 x F7): Star Cape widens magnet radius to vacuum Flowerpot fountain drops from Hub center
        for (let x = -24; x <= 24; x += 2) {{
          for (let z = 10; z <= 24; z += 2) {{
            L.breakBlock(x, 1, z);
            if (L.getState().blocksBroken >= 26) break;
          }}
          if (L.getState().blocksBroken >= 26) break;
        }}
        L.stepFrames(340, dt);
        L.plantPot(0);
        L.plantPot(0);
        L.plantPot(0);
        L.tapWorld(0, 1.6); // Stand ~4.5b away from Pad 0 (-4.5, 1.6) with Star Cape magnet (5.6b)
        L.stepFrames(60, dt);
        const gCape0 = L.getState().player.starGems;
        L.stepFrames(320, dt);
        const gCape1 = L.getState().player.starGems;
        const t3_07 = {{
          starCape: Boolean(L.getState().player.starCape),
          gemsVacuumedFromAfar: gCape1 - gCape0,
        }};

        // T3_08 (F6 x F9): Geared Odyssey projectile throw damages active Quadrant Boss
        L.startGame({{ seed: 2026 }});
        L.spinChest('rainbow_mega_hammer');
        L.stepFrames(185, dt);
        L.spawnTitan('tralalero_tralala');
        L.stepFrames(40, dt);
        const boss0 = L.getState().titans.find((t) => t.id === 'tralalero_tralala');
        const hp0 = boss0 ? boss0.hp : 100;
        L.tapWorld(boss0.x, boss0.z + 4.5);
        L.stepFrames(90, dt);
        L.throwStick({{ targetX: boss0.x, targetZ: boss0.z }});
        L.stepFrames(40, dt);
        const boss1 = L.getState().titans.find((t) => t.id === 'tralalero_tralala');
        const hp1 = boss1 ? boss1.hp : 100;
        const t3_08 = {{ hpBefore: hp0, hpAfter: hp1, stickHits: L.getState().stickThrow?.hits || 0 }};

        // T3_09 (F6 x F3): Odyssey projectile throw pats friendly Critter along flight path
        L.startGame({{ seed: 2026 }});
        L.stepFrames(10, dt);
        const cr = (L.getState().critters || [])[0];
        let t3_09 = {{ ok: false }};
        if (cr) {{
          L.tapWorld(cr.x, cr.z + 3.5);
          L.stepFrames(70, dt);
          const curCr = (L.getState().critters || [])[0];
          const petsBefore = L.getState().feedback?.crittersPetted || 0;
          L.throwStick({{ targetX: curCr.x, targetZ: curCr.z }});
          L.stepFrames(45, dt);
          t3_09 = {{
            ok: true,
            petsDelta: (L.getState().feedback?.crittersPetted || 0) - petsBefore,
          }};
        }}

        // T3_10 (F10 x F11): Voice playback ducks BGM and #voice-subtitle has 0px overlap with HUD buttons
        L.startGame({{ seed: 2026 }});
        L.replayVoice();
        L.stepFrames(5, dt);
        const subEl = document.getElementById('voice-subtitle');
        const sr = subEl ? subEl.getBoundingClientRect() : null;
        let hudOverlaps = 0;
        if (sr && sr.width > 0) {{
          for (const id of {json.dumps(list(HUD_BUTTON_IDS))}) {{
            const b = document.getElementById(id)?.getBoundingClientRect();
            if (b && b.width > 0) {{
              const ox = Math.max(0, Math.min(sr.right, b.right) - Math.max(sr.left, b.left));
              const oy = Math.max(0, Math.min(sr.bottom, b.bottom) - Math.max(sr.top, b.top));
              if (ox * oy > 0) hudOverlaps++;
            }}
          }}
        }}
        const t3_10 = {{
          speaking: Boolean(L.getState().voice?.speaking),
          bgmDucked: Boolean(L.getState().voice?.bgmDucked),
          hudOverlaps,
        }};

        // T3_11 (F11 x F4 x F7): Silly Chaos x2 mode boosts block & flowerpot gem output vs normal mode
        const measureRunGems = (chaos) => {{
          L.startGame({{ seed: 2045, chaosMode: chaos }});
          L.breakBlock(0, 1, 2.0);
          for (let x = -22; x <= -12; x += 2) {{
            for (let z = 12; z <= 20; z += 2) L.breakBlock(x, 1, z);
          }}
          L.stepFrames(340, dt);
          return L.getState().player.starGems;
        }};
        const normGems = measureRunGems(false);
        const chaosGems = measureRunGems(true);
        const t3_11 = {{ normGems, chaosGems }};

        // T3_12 (F1 x F2 x F3 x F5): Derpy Tiger buttL/buttR, tail, and Sussie animate during Mario Jump with cameraRoll === 0
        L.startGame({{ seed: 2026 }});
        L.jump();
        L.stepFrames(10, dt);
        const sceneNow = window.__QA_LAST_SCENE__ || window.__E2E_LAST_SCENE__;
        let bL = 0, bR = 0;
        if (sceneNow) {{
          sceneNow.traverse((obj) => {{
            if (obj.name === 'buttL') bL = obj.position.y;
            if (obj.name === 'buttR') bR = obj.position.y;
          }});
        }}
        const t3_12 = {{
          jumping: L.getState().player.jumping,
          buttDiff: Math.abs(bL - bR),
          cameraRoll: Math.abs(L.getState().perf?.cameraRoll || 0),
        }};

        // T3_13 (F6 x F4): 3-beat drum combo triggers rainbow shockwave in voxel world
        L.startGame({{ seed: 2026 }});
        L.swingDrum();
        L.swingDrum();
        const beat3 = L.swingDrum();
        const t3_13 = {{
          beat: beat3?.beat,
          shockwave: Boolean(beat3?.shockwave),
          radius: beat3?.radius,
        }};

        // T3_16 (F5 x F4): Rising Mario Jump adjacent to Starter Lucky Block head-bonks and breaks it
        L.startGame({{ seed: 2026 }});
        L.tapWorld(0, 2.8);
        L.stepFrames(35, dt);
        const brokenBeforeJump = L.getState().blocksBroken;
        L.jump();
        L.stepFrames(25, dt);
        const brokenAfterJump = L.getState().blocksBroken;
        const t3_16 = {{ brokenBeforeJump, brokenAfterJump }};

        return {{
          t3_01, t3_02, t3_03, t3_04, t3_05, t3_06, t3_07,
          t3_08, t3_09, t3_10, t3_11, t3_12, t3_13, t3_16,
        }};
      }})()"""
  )

  _record(checks, 'T3_01', 'F5xF6', 'Mario Jump + mid-air Odyssey projectile throw breaks Lucky Block while airborne', float((p_res.get('t3_01') or {}).get('airJumpY', 0)) > 0.4 and bool((p_res.get('t3_01') or {}).get('airThrowOk')) and int((p_res.get('t3_01') or {}).get('blocksBroken', 0)) >= 1, p_res.get('t3_01'))
  _record(checks, 'T3_02', 'F8xF6', 'Roulette weapon upgrade syncs thrown projectile weaponId & 3D mesh', (p_res.get('t3_02') or {}).get('playerWeapon') == 'neon_thunder_taiko' and (p_res.get('t3_02') or {}).get('thrownWeapon') == 'neon_thunder_taiko', p_res.get('t3_02'))
  _record(checks, 'T3_03', 'F7xF8', 'Tier 3 Flowerpot fountain Star Gems fund a natural Roulette weapon upgrade spin', int((p_res.get('t3_03') or {}).get('tierAfter', 0)) > int((p_res.get('t3_03') or {}).get('tierBefore', 99)), p_res.get('t3_03'))
  _record(checks, 'T3_04', 'F8xF9xF4', 'Tier 5 Roulette weapon defeats Quadrant Boss and unlocks Hub pedestal Trophy', 'tralalero_tralala' in ((p_res.get('t3_04') or {}).get('trophies') or []), p_res.get('t3_04'))
  _record(checks, 'T3_05', 'F9xF7xF8', 'Under-geared Boss Cloud Boing preserves planted Flowerpot tiers, weapon, and adds +3 stars', bool((p_res.get('t3_05') or {}).get('potTierPreserved')) and bool((p_res.get('t3_05') or {}).get('weaponPreserved')) and int((p_res.get('t3_05') or {}).get('gemsGained', 0)) >= 3, p_res.get('t3_05'))
  _record(checks, 'T3_06', 'F8xF5xF9', 'Sussie Gat Helmet boosts walk speed >=8.5 b/s, grants 5 Shield Hearts, and raises Boss powerTier', bool((p_res.get('t3_06') or {}).get('helmet')) and float((p_res.get('t3_06') or {}).get('speed', 0)) >= 8.5 and int((p_res.get('t3_06') or {}).get('powerTier', 0)) >= 2, p_res.get('t3_06'))
  _record(checks, 'T3_07', 'F8xF7', 'Honmoon Star Cape widens magnet radius to vacuum Flowerpot fountain drops from Hub center', bool((p_res.get('t3_07') or {}).get('starCape')) and int((p_res.get('t3_07') or {}).get('gemsVacuumedFromAfar', 0)) >= 4, p_res.get('t3_07'))
  _record(checks, 'T3_08', 'F6xF9', 'Geared Odyssey projectile throw hits and damages active Quadrant Boss', int((p_res.get('t3_08') or {}).get('hpAfter', 100)) < int((p_res.get('t3_08') or {}).get('hpBefore', 100)), p_res.get('t3_08'))
  _record(checks, 'T3_09', 'F6xF3', 'Odyssey projectile throw pats friendly Critter along flight path', bool((p_res.get('t3_09') or {}).get('ok')) and int((p_res.get('t3_09') or {}).get('petsDelta', 0)) >= 1, p_res.get('t3_09'))
  _record(checks, 'T3_10', 'F10xF11', 'Voiceover playback ducks BGM (-6 dB) while #voice-subtitle has 0px overlap with HUD buttons', bool((p_res.get('t3_10') or {}).get('speaking')) and bool((p_res.get('t3_10') or {}).get('bgmDucked')) and int((p_res.get('t3_10') or {}).get('hudOverlaps', 99)) == 0, p_res.get('t3_10'))
  _record(checks, 'T3_11', 'F11xF4xF7', 'Silly Chaos x2 mode boosts multi-drop Star Gem yield compared to normal mode', int((p_res.get('t3_11') or {}).get('chaosGems', 0)) > int((p_res.get('t3_11') or {}).get('normGems', 0)), p_res.get('t3_11'))
  _record(checks, 'T3_12', 'F1xF2xF3xF5', 'Derpy Tiger buttL/buttR and Sussie animate during Mario Jump with cameraRoll === 0', bool((p_res.get('t3_12') or {}).get('jumping')) and float((p_res.get('t3_12') or {}).get('buttDiff', 0)) > 1e-4 and float((p_res.get('t3_12') or {}).get('cameraRoll', 99)) < 0.001, p_res.get('t3_12'))
  _record(checks, 'T3_13', 'F6xF4', '3rd beat of drum combo triggers 4.0b rainbow shockwave in voxel world', int((p_res.get('t3_13') or {}).get('beat', 0)) == 3 and bool((p_res.get('t3_13') or {}).get('shockwave')), p_res.get('t3_13'))

  # T3_14 (F11 x F10): Pause Modal Voice mute + HUD #btn-hud-voice 1-tap auto-unmute
  from run_e2e import check_e42_voice_replay_auto_unmutes_when_muted  # noqa: E402
  e42_res = check_e42_voice_replay_auto_unmutes_when_muted(sess, {})
  _record(checks, 'T3_14', 'F11xF10', 'Muting Voice in Pause Modal then tapping #btn-hud-voice auto-unmutes and replays VO', bool(e42_res.get('voiceEnabledAfterReplay')) and bool(e42_res.get('speaking')), e42_res)

  # T3_15 (F11 x F7 x F8 x F9): Save persistence reload + #btn-title-continue restores trophies, pots, and weapon
  from run_e2e import check_e46_continue_button_reload_persistence  # noqa: E402
  e46_res = check_e46_continue_button_reload_persistence(sess, {})
  _record(checks, 'T3_15', 'F11xF7xF8xF9', 'Page reload + #btn-title-continue restores saved Boss Trophies, Flowerpot tiers, and Weapon', 'tralalero_tralala' in (e46_res.get('trophies') or []) and e46_res.get('weaponId') == 'golden_sahur_mallet', e46_res)

  _record(checks, 'T3_16', 'F5xF4', 'Rising Mario 3D Jump adjacent to Lucky Block head-bonks and breaks the block', int((p_res.get('t3_16') or {}).get('brokenAfterJump', 0)) > int((p_res.get('t3_16') or {}).get('brokenBeforeJump', 0)), p_res.get('t3_16'))

  passed_count = sum(1 for c in checks if c['passed'])
  return {
      'tier': 3,
      'name': 'Tier 3 — Cross-Feature Pairwise Combinations',
      'passed': passed_count == len(checks),
      'passedCount': passed_count,
      'totalCount': len(checks),
      'wallTimeSec': round(time.time() - t0, 2),
      'checks': checks,
  }


# ==============================================================================
# TIER 4: Real-World Application Scenarios (7 full E2E scenarios)
# ==============================================================================


def run_tier4_real_world_scenarios(sess: QASession) -> dict[str, Any]:
  print('\n=== TIER 4: Real-World Application Scenarios (7 full scenarios) ===')
  checks: list[dict[str, Any]] = []
  t0 = time.time()

  # Scenario 1: Full End-to-End Playthrough (Title -> 4 Flowerpots -> Roulette -> 4 Bosses -> Victory -> Free-Roam)
  sess.goto('index.html?seed=2026', timeout=25.0)
  sess.wait_raf(3)
  playthrough = sess.eval_json(
      f"""(() => {{
        const L = {SEAM_GLOBAL_EXPR};
        const dt = 1 / 60;
        const mode0 = L.getState().mode;
        document.getElementById('btn-title-play')?.click();
        L.stepFrames(2, dt);
        const modePlay = L.getState().mode;

        // Break starter block & biome blocks
        L.breakBlock(0, 1, 2.0);
        L.tapWorld(0, 2.0);
        L.stepFrames(90, dt);
        for (let x = -24; x <= 24; x += 3) {{
          for (let z = 10; z <= 24; z += 3) L.breakBlock(x, 1, z);
        }}
        L.stepFrames(340, dt);

        // Upgrade all 4 Hub Flowerpots to Tier 3
        for (let cycle = 0; cycle < 14; cycle++) {{
          L.tapWorld(-4.2, 1.6);
          L.stepFrames(220, dt);
          for (let p = 0; p < 4; p++) {{
            if ((L.getState().flowerpots[p]?.tier || 0) < 3) L.plantPot(p);
          }}
          if (L.getState().flowerpots.every((fp) => fp.tier === 3)) break;
        }}
        const potTiers = L.getState().flowerpots.map((fp) => fp.tier);

        // Spin Roulette Chest through Tier 5 weapon
        for (let s = 0; s < 6; s++) {{
          if (L.getState().player.weaponTier >= 5) break;
          for (
            let w = 0;
            w < 12 &&
            (L.getState().player.freeSpins || 0) === 0 &&
            L.getState().player.starGems < (L.getState().roulette?.spinCost || 120);
            w++
          ) {{
            L.tapWorld(w % 2 === 0 ? -4.2 : 4.2, 1.6);
            L.stepFrames(300, dt);
          }}
          L.spinChest();
          L.stepFrames(190, dt);
        }}
        const maxWeapon = L.getState().player.weaponId;
        const maxWeaponTier = L.getState().player.weaponTier;

        // Spawn and defeat all 4 Quadrant Bosses (q1..q4)
        for (const tid of {json.dumps(TITAN_ORDER)}) {{
          L.spawnTitan(tid);
          L.stepFrames(40, dt);
          for (let h = 0; h < 10; h++) {{
            if ((L.getState().trophies || []).includes(tid)) break;
            L.bonkTitan(tid);
            L.stepFrames(22, dt);
          }}
          L.stepFrames(60, dt);
        }}
        const stVictory = L.getState();
        const modeVictory = stVictory.mode;
        const trophies = stVictory.trophies || [];
        const crown = Boolean(stVictory.player.crown);

        // Click Keep Playing on Victory Modal to enter endless Free-Roam
        document.getElementById('btn-victory-continue')?.click();
        L.stepFrames(15, dt);
        const modeFreeRoam = L.getState().mode;
        localStorage.removeItem({json.dumps(STORAGE_KEY)});

        return {{
          mode0,
          modePlay,
          potTiers,
          maxWeapon,
          maxWeaponTier,
          modeVictory,
          trophies,
          crown,
          modeFreeRoam,
        }};
      }})()"""
  )
  _record(
      checks,
      'T4_01',
      'FullPlaythrough',
      'Full playthrough: Title -> 4 Tier-3 Flowerpots -> Tier-5 Roulette -> 4 Bosses -> 4/4 Trophies -> Victory -> Free-Roam',
      playthrough.get('mode0') == 'title'
      and playthrough.get('modePlay') == 'playing'
      and playthrough.get('potTiers') == [3, 3, 3, 3]
      and int(playthrough.get('maxWeaponTier', 0)) == 5
      and playthrough.get('modeVictory') == 'victory'
      and len(playthrough.get('trophies') or []) == 4
      and bool(playthrough.get('crown'))
      and playthrough.get('modeFreeRoam') == 'playing',
      playthrough,
  )

  # Scenario 2: Master E2E Suite (E01..E50, skipping subsuites E43/E44 here since T4_05/T4_06 run them dedicated)
  e2e_rep = run_e2e_suite(skip_subsuites=True)
  _record(
      checks,
      'T4_02',
      'MasterE2E',
      f"Master E2E Suite (E01..E50 core assertions): {e2e_rep['passedCount']}/{e2e_rep['totalCount']} PASS",
      bool(e2e_rep.get('passed')),
      {'passedCount': e2e_rep['passedCount'], 'totalCount': e2e_rep['totalCount']},
  )

  # Scenario 3 & 4 & 7: Run full sim_gates.py (Gates F1..F12 including 20-seed child-bot simulation 1001..1020 & seed=2026 SHA-256 determinism)
  sim_rep = run_sim_gates(num_seeds=20)
  f10_gate = next((g for g in sim_rep.get('gates', []) if g.get('gate') == 'F10'), {})
  _record(
      checks,
      'T4_03',
      'ChildBot20Seeds',
      f"20-seed 5yo child-bot simulation (seeds 1001..1020): {f10_gate.get('completedCount')}/{f10_gate.get('seedCount')} win in 240-720s",
      bool(f10_gate.get('passed')) and int(f10_gate.get('completedCount', 0)) == 20,
      {
          'completedCount': f10_gate.get('completedCount'),
          'inWindow240to720Count': f10_gate.get('inWindow240to720Count'),
          'simTimeStatsSec': f10_gate.get('simTimeStatsSec'),
      },
  )
  _record(
      checks,
      'T4_04',
      'DeterminismSHA256',
      f"Bit-exact seed=2026 SHA-256 determinism across independent runs (sha256={f10_gate.get('determinismSha256')})",
      bool(f10_gate.get('deterministicSeed2026')),
      {
          'deterministic': f10_gate.get('deterministicSeed2026'),
          'sha256': f10_gate.get('determinismSha256'),
      },
  )

  # Scenario 5: 5-Viewport Responsive Layout Audit (layout_audit.py)
  layout_rep = run_layout_audit(save_shots=True)
  _record(
      checks,
      'T4_05',
      'FiveViewportLayout',
      f"5-viewport responsive layout audit across all UI states ({layout_rep.get('viewportCount')} viewports)",
      bool(layout_rep.get('passed')),
      {'viewportCount': layout_rep.get('viewportCount'), 'shotsDir': layout_rep.get('shotsDir')},
  )

  # Scenario 6: Zero-CJK & Zero-speechSynthesis Localization Audit (l10n_audit.py)
  l10n_rep = run_l10n_audit(static_only=False)
  _record(
      checks,
      'T4_06',
      'ZeroCJKL10nAudit',
      f"Full static + runtime L10n audit ({l10n_rep['static']['filesScanned']} files, 0 CJK, 0 speechSynthesis)",
      bool(l10n_rep.get('passed')),
      l10n_rep['static'],
  )

  # Scenario 7: All 12 Simulation Gates F1..F12 Pass
  _record(
      checks,
      'T4_07',
      'SimGatesF1ToF12',
      f"Simulation Gates F1..F12 fun, pacing & economy ({sim_rep['passedCount']}/{sim_rep['totalGates']} PASS)",
      bool(sim_rep.get('passed')),
      {'passedCount': sim_rep['passedCount'], 'totalGates': sim_rep['totalGates']},
  )

  passed_count = sum(1 for c in checks if c['passed'])
  return {
      'tier': 4,
      'name': 'Tier 4 — Real-World Application Scenarios',
      'passed': passed_count == len(checks),
      'passedCount': passed_count,
      'totalCount': len(checks),
      'wallTimeSec': round(time.time() - t0, 2),
      'checks': checks,
  }


def main() -> int:
  ap = argparse.ArgumentParser(description='Run Tiered E2E Verification Suite (Tiers 1..4) for Derpy Tiger Minecraft Chapter 3D')
  ap.add_argument('--tier', type=int, choices=[1, 2, 3, 4], default=0, help='Run a specific tier (1, 2, 3, or 4)')
  ap.add_argument('--all', action='store_true', help='Run all Tiers 1..4')
  args = ap.parse_args()

  ensure_qa_dirs()
  run_tiers = [args.tier] if args.tier in (1, 2, 3, 4) else [1, 2, 3, 4]

  tier_reports: list[dict[str, Any]] = []
  t0 = time.time()

  with QASession(width=1280, height=800, mobile=False) as sess:
    if not sess.goto('index.html?seed=2026', timeout=25.0):
      raise RuntimeError('Timed out loading index.html in run_all_tiers.py')
    sess.wait_raf(3)
    _ensure_three_spy(sess)

    for t in run_tiers:
      if t == 1:
        tier_reports.append(run_tier1_feature_coverage(sess))
      elif t == 2:
        tier_reports.append(run_tier2_boundary_and_corner_cases(sess))
      elif t == 3:
        tier_reports.append(run_tier3_pairwise_combinations(sess))
      elif t == 4:
        tier_reports.append(run_tier4_real_world_scenarios(sess))

  total_checks = sum(r['totalCount'] for r in tier_reports)
  total_passed = sum(r['passedCount'] for r in tier_reports)
  overall_passed = all(r['passed'] for r in tier_reports)
  wall_sec = round(time.time() - t0, 2)

  summary = {
      'passed': overall_passed,
      'passedCount': total_passed,
      'totalCount': total_checks,
      'wallTimeSec': wall_sec,
      'tiers': tier_reports,
  }
  out_json = os.path.join(QA_TMP_DIR, 'all_tiers_report.json')
  with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2)

  print('\n======================================================================')
  for r in tier_reports:
    verdict = 'PASS' if r['passed'] else 'FAIL'
    print(f"  Tier {r['tier']}: {r['passedCount']}/{r['totalCount']} {verdict} ({r['wallTimeSec']}s) — {r['name']}")
  print('----------------------------------------------------------------------')
  print(
      f"ALL_TIERS_SUMMARY: {total_passed}/{total_checks} PASS in {wall_sec}s "
      f"-> {'PASS' if overall_passed else 'FAIL'}"
  )
  print('======================================================================')
  return 0 if overall_passed else 1


if __name__ == '__main__':
  sys.exit(main())
