// Procedural 16x16 pixel-art CanvasTextures and 8x8 voxel atlas for Derpy Tiger Minecraft Chapter 3D: Sussie, JJ, Mikey & The Underground Portal!
// Theme: Korean Minhwa Courtyard & Minecraft Overworld Security Fortress (EgruEB4oZ2E, WjAyI6kwylA, L0N4m23OSKM).

import * as THREE from '../../vendor/three.module.min.js';
import { createRng } from '../core/rng.js';

const TILE_SIZE = 16;
const ATLAS_COLS = 8;
const ATLAS_ROWS = 8;
const ATLAS_SIZE = TILE_SIZE * ATLAS_COLS; // 128x128

export const TILE_INDEX = Object.freeze({
  grass_top: 0,
  grass_side: 1,
  dirt: 2,
  path_gold: 3,
  hub_plaza: 4,
  lucky_block: 5,
  flower_red_top: 6,
  flower_red_side: 7,
  flower_sun_top: 8,
  flower_sun_side: 9,
  oak_bark: 10,
  oak_top: 11,
  spruce_bark: 12,
  spruce_top: 13,
  leaves_lush: 14,
  leaves_frost: 15,
  hay_side: 16,
  hay_top: 17,
  pumpkin_front: 18,
  pumpkin_side: 19,
  pumpkin_top: 20,
  melon_side: 21,
  melon_top: 22,
  beehive_front: 23,
  beehive_side: 24,
  beehive_top: 25,
  ice_crystal: 26,
  snow_top: 27,
  snow_side: 28,
  castle_brick: 29,
  furnace_front: 30,
  furnace_side: 31,
  amethyst: 32,
  bedrock_gold: 33,
  mega_titan_side: 34,
  mega_titan_top: 35,
  chest_front: 36,
  chest_side: 37,
  chest_top: 38,
  water: 39,
  farm_soil: 40,
  lantern_glow: 41,
  mushroom_red: 42,
  snowman_face: 43,
});

function makeCanvas(w, h) {
  const c = document.createElement('canvas');
  c.width = w;
  c.height = h;
  return c;
}

function finalizePixelTexture(canvas, repeat = false) {
  const tex = new THREE.CanvasTexture(canvas);
  tex.magFilter = THREE.NearestFilter;
  tex.minFilter = THREE.NearestFilter;
  tex.generateMipmaps = false;
  tex.colorSpace = THREE.SRGBColorSpace;
  if (repeat) {
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
  }
  tex.needsUpdate = true;
  return tex;
}

function fillNoise(ctx, rng, palette, x0 = 0, y0 = 0, w = 16, h = 16) {
  for (let y = y0; y < y0 + h; y++) {
    for (let x = x0; x0 + w > x; x++) {
      ctx.fillStyle = rng.pick(palette);
      ctx.fillRect(x, y, 1, 1);
    }
  }
}

function px(ctx, x, y, color, w = 1, h = 1) {
  ctx.fillStyle = color;
  ctx.fillRect(x, y, w, h);
}

function drawBitmap(ctx, rows, colorMap, ox = 0, oy = 0) {
  for (let y = 0; y < rows.length; y++) {
    const row = rows[y];
    for (let x = 0; x < row.length; x++) {
      const ch = row[x];
      if (ch !== '.' && colorMap[ch]) {
        ctx.fillStyle = colorMap[ch];
        ctx.fillRect(ox + x, oy + y, 1, 1);
      }
    }
  }
}

function paintTile(name, ctx, emCtx, rng) {
  switch (name) {
    case 'grass_top': {
      // Minecraft Overworld Emerald Voxel Grass Lawn (#51cf66, #40c057, #37b24d, #69db7c)
      fillNoise(ctx, rng, ['#51cf66', '#40c057', '#37b24d', '#5fd674', '#2f9e44']);
      px(ctx, 2, 3, '#69db7c', 2, 1);
      px(ctx, 10, 5, '#69db7c', 2, 2);
      px(ctx, 5, 11, '#8ce99a', 2, 1);
      px(ctx, 12, 13, '#2b8a3e', 2, 2);
      break;
    }

    case 'grass_side': {
      // Classic Minecraft Grass Block Side (Rich brown voxel dirt with jagged emerald grass overhang)
      fillNoise(ctx, rng, ['#8b5a2b', '#7c4d25', '#6e421f', '#9c6b3b']);
      fillNoise(ctx, rng, ['#51cf66', '#40c057', '#37b24d'], 0, 0, 16, 4);
      // Jagged Minecraft grass blades hanging down onto dirt
      const fringe = [5, 6, 4, 5, 7, 5, 4, 6, 5, 4, 6, 7, 5, 4, 6, 5];
      for (let x = 0; x < 16; x++) {
        px(ctx, x, 3, x % 2 === 0 ? '#40c057' : '#2f9e44', 1, fringe[x] - 3);
      }
      // Small pebble details in dirt
      px(ctx, 3, 10, '#adb5bd', 2, 2);
      px(ctx, 11, 12, '#6c757d', 2, 2);
      break;
    }

    case 'dirt': {
      // Minecraft Coarse Dirt & Cobblestone Foundation Block
      fillNoise(ctx, rng, ['#7c4d25', '#6e421f', '#8b5a2b', '#5c3d24']);
      px(ctx, 2, 2, '#868e96', 3, 2);
      px(ctx, 10, 4, '#adb5bd', 3, 2);
      px(ctx, 5, 9, '#6c757d', 3, 3);
      px(ctx, 11, 12, '#868e96', 3, 2);
      break;
    }

    case 'farm_soil': {
      // Underground Mine Shaft Coarse Dirt, Oak Planks & Iron Minecart Rail Tie (L0N4m23OSKM)
      fillNoise(ctx, rng, ['#5c3d24', '#6e421f', '#4a301c', '#7c4d25']);
      // Horizontal oak wood rail sleepers
      for (let y = 1; y < 16; y += 4) {
        px(ctx, 1, y, '#9c6b3b', 14, 2);
        px(ctx, 1, y, '#b07d48', 14, 1);
      }
      // Twin vertical iron minecart rails
      px(ctx, 3, 0, '#adb5bd', 2, 16);
      px(ctx, 11, 0, '#adb5bd', 2, 16);
      px(ctx, 3, 0, '#dee2e6', 1, 16);
      px(ctx, 11, 0, '#dee2e6', 1, 16);
      break;
    }

    case 'path_gold': {
      // Minecraft Powered Golden Rail & Redstone Lamp Path
      fillNoise(ctx, rng, ['#495057', '#343a40', '#5c646d']);
      // Wooden ties
      for (let y = 1; y < 16; y += 4) {
        px(ctx, 1, y, '#8b5a2b', 14, 2);
      }
      // Golden powered rails on left & right
      px(ctx, 2, 0, '#ffd43b', 2, 16);
      px(ctx, 12, 0, '#ffd43b', 2, 16);
      px(ctx, 2, 0, '#fff3bf', 1, 16);
      px(ctx, 12, 0, '#fff3bf', 1, 16);
      // Glowing redstone circuit core down center
      px(ctx, 7, 0, '#e03131', 2, 16);
      px(ctx, 7, 2, '#ff6b6b', 2, 3);
      px(ctx, 7, 10, '#ff6b6b', 2, 3);
      px(emCtx, 2, 0, '#997a00', 2, 16);
      px(emCtx, 12, 0, '#997a00', 2, 16);
      px(emCtx, 7, 0, '#c92a2a', 2, 16);
      break;
    }

    case 'hub_plaza': {
      // Carved Chiseled Stone Bricks & Korean Minhwa Celadon Jade Courtyard Tiles (#8fd3be, #74c2aa, #adb5bd, #ffd43b)
      fillNoise(ctx, rng, ['#7bc4ae', '#6ab59e', '#8cd1bc']);
      // Outer chiseled granite stone frame
      px(ctx, 0, 0, '#ced4da', 16, 2);
      px(ctx, 0, 14, '#868e96', 16, 2);
      px(ctx, 0, 0, '#ced4da', 2, 16);
      px(ctx, 14, 0, '#868e96', 2, 16);
      // Inner carved celadon border
      px(ctx, 3, 3, '#499982', 10, 10);
      px(ctx, 4, 4, '#96dec8', 8, 8);
      // Golden Minhwa lotus/diamond medallion in tile center
      px(ctx, 7, 5, '#ffd43b', 2, 6);
      px(ctx, 5, 7, '#ffd43b', 6, 2);
      px(ctx, 7, 7, '#fff9db', 2, 2);
      break;
    }

    case 'lucky_block': {
      // Golden Minecraft '?' Lucky Block (#ffd43b, #fcc419, #e67700 gold voxel block with crisp pixel-art '?')
      fillNoise(ctx, rng, ['#fcc419', '#ffd43b', '#fab005', '#f59f00']);
      // Beveled 24K gold block border with corner rivets
      px(ctx, 0, 0, '#fff3bf', 16, 2);
      px(ctx, 0, 14, '#d97706', 16, 2);
      px(ctx, 0, 0, '#fff3bf', 2, 16);
      px(ctx, 14, 0, '#d97706', 2, 16);
      px(ctx, 2, 2, '#b45309', 2, 2);
      px(ctx, 12, 2, '#b45309', 2, 2);
      px(ctx, 2, 12, '#b45309', 2, 2);
      px(ctx, 12, 12, '#b45309', 2, 2);
      const qRows = [
        '..WWWW..',
        '.WWWWWWB',
        '.WW..WWB',
        '....WWWB',
        '...WWWB.',
        '...WWB..',
        '...BBB..',
        '...WW...',
        '...WWB..',
        '....BB..',
      ];
      drawBitmap(ctx, qRows, { W: '#ffffff', B: '#92400e' }, 4, 3);
      drawBitmap(emCtx, qRows, { W: '#ffe066', B: '#78350f' }, 4, 3);
      px(emCtx, 0, 0, '#854d0e', 16, 2);
      px(emCtx, 0, 14, '#854d0e', 16, 2);
      break;
    }

    case 'flower_red_top': {
      // Blue-and-White Minhwa Porcelain Peony Planter Crate Top (EgruEB4oZ2E)
      px(ctx, 0, 0, '#f8fafc', 16, 16);
      // Cobalt blue Joseon porcelain rim
      px(ctx, 0, 0, '#1d4ed8', 16, 2);
      px(ctx, 0, 14, '#1d4ed8', 16, 2);
      px(ctx, 0, 0, '#1d4ed8', 2, 16);
      px(ctx, 14, 0, '#1d4ed8', 2, 16);
      // Rich dark soil + green leaves + blooming Minhwa peony flower
      px(ctx, 3, 3, '#5c3d24', 10, 10);
      px(ctx, 3, 6, '#40c057', 10, 4);
      px(ctx, 6, 3, '#40c057', 4, 10);
      px(ctx, 5, 5, '#ff6b9d', 6, 6);
      px(ctx, 6, 6, '#ffd43b', 4, 4);
      break;
    }

    case 'flower_red_side': {
      // Blue-and-White Minhwa Porcelain Peony Planter Crate Side (EgruEB4oZ2E)
      fillNoise(ctx, rng, ['#f8fafc', '#f1f5f9', '#e2e8f0']);
      // Cobalt blue decorative wave bands top & bottom
      px(ctx, 0, 0, '#1d4ed8', 16, 3);
      px(ctx, 0, 13, '#1d4ed8', 16, 3);
      for (let x = 1; x < 15; x += 4) {
        px(ctx, x, 1, '#93c5fd', 2, 1);
        px(ctx, x, 14, '#93c5fd', 2, 1);
      }
      // Cobalt blue dragon/cloud scroll + blooming peony emblem in center
      px(ctx, 2, 6, '#2563eb', 3, 4);
      px(ctx, 11, 6, '#2563eb', 3, 4);
      px(ctx, 5, 4, '#2f9e44', 6, 8);
      px(ctx, 6, 5, '#ff6b9d', 4, 5);
      px(ctx, 7, 6, '#ffd43b', 2, 3);
      break;
    }

    case 'flower_sun_top': {
      // Minecraft Glowstone & Underground Golden Cookie Jar Top (L0N4m23OSKM)
      fillNoise(ctx, rng, ['#fcc419', '#ffd43b', '#f59f00', '#ffe066']);
      px(ctx, 0, 0, '#b45309', 16, 2);
      px(ctx, 0, 14, '#b45309', 16, 2);
      px(ctx, 0, 0, '#b45309', 2, 16);
      px(ctx, 14, 0, '#b45309', 2, 16);
      // Chocolate-chip cookie pixels + glowstone crystals
      px(ctx, 4, 4, '#78350f', 2, 2);
      px(ctx, 10, 4, '#78350f', 2, 2);
      px(ctx, 4, 10, '#78350f', 2, 2);
      px(ctx, 10, 10, '#78350f', 2, 2);
      px(ctx, 6, 6, '#fff9db', 4, 4);
      px(emCtx, 4, 4, '#d97706', 8, 8);
      break;
    }

    case 'flower_sun_side': {
      // Minecraft Glowstone & Underground Golden Cookie Crate Side (L0N4m23OSKM)
      fillNoise(ctx, rng, ['#92400e', '#78350f', '#b45309']);
      px(ctx, 0, 0, '#ffd43b', 16, 2);
      px(ctx, 0, 14, '#ffd43b', 16, 2);
      // Glowing glass cookie display window
      px(ctx, 2, 3, '#fef08a', 12, 10);
      px(ctx, 4, 4, '#d97706', 8, 8);
      px(ctx, 5, 5, '#78350f', 2, 2);
      px(ctx, 9, 6, '#78350f', 2, 2);
      px(ctx, 6, 9, '#78350f', 2, 2);
      px(emCtx, 3, 4, '#eab308', 10, 8);
      break;
    }

    case 'oak_bark': {
      // Minecraft Oak Log Bark & Minhwa Pavilion Red/Brown Timber Pillar
      for (let x = 0; x < 16; x++) {
        const stripe = x % 4;
        const col = stripe === 0 ? '#54341a' : stripe === 1 ? '#6b4423' : stripe === 2 ? '#7c4d25' : '#5c3d24';
        px(ctx, x, 0, col, 1, 16);
      }
      px(ctx, 2, 4, '#3d2512', 2, 3);
      px(ctx, 9, 10, '#3d2512', 2, 4);
      px(ctx, 13, 3, '#8b5a2b', 1, 5);
      break;
    }

    case 'oak_top': {
      // Minecraft Oak Log Concentric Growth Rings Top
      px(ctx, 0, 0, '#54341a', 16, 16);
      px(ctx, 2, 2, '#d4a359', 12, 12);
      px(ctx, 4, 4, '#b5833d', 8, 8);
      px(ctx, 6, 6, '#d4a359', 4, 4);
      px(ctx, 7, 7, '#8b5a2b', 2, 2);
      break;
    }

    case 'spruce_bark': {
      // Minecraft Chiseled Stone Brick & Mossy Cobblestone Pillar Side
      fillNoise(ctx, rng, ['#868e96', '#adb5bd', '#6c757d']);
      px(ctx, 0, 0, '#495057', 16, 2);
      px(ctx, 0, 14, '#495057', 16, 2);
      px(ctx, 0, 0, '#495057', 2, 16);
      px(ctx, 14, 0, '#495057', 2, 16);
      px(ctx, 3, 3, '#495057', 10, 10);
      px(ctx, 5, 5, '#ced4da', 6, 6);
      // Moss & cyan Honmoon rune center
      px(ctx, 2, 11, '#51cf66', 3, 3);
      px(ctx, 11, 2, '#51cf66', 3, 2);
      px(ctx, 6, 6, '#3bc9db', 4, 4);
      break;
    }

    case 'spruce_top': {
      // Minecraft Chiseled Stone Brick & Mossy Cobblestone Top
      fillNoise(ctx, rng, ['#868e96', '#adb5bd', '#6c757d']);
      px(ctx, 0, 0, '#495057', 16, 2);
      px(ctx, 0, 14, '#495057', 16, 2);
      px(ctx, 0, 0, '#495057', 2, 16);
      px(ctx, 14, 0, '#495057', 2, 16);
      px(ctx, 4, 4, '#495057', 8, 8);
      px(ctx, 6, 6, '#51cf66', 4, 4);
      break;
    }

    case 'leaves_lush': {
      // Minecraft Emerald Pine & Minhwa Bamboo Foliage Block
      fillNoise(ctx, rng, ['#2b8a3e', '#37b24d', '#2f9e44', '#40c057', '#1b5e20']);
      px(ctx, 2, 2, '#69db7c', 2, 2);
      px(ctx, 11, 4, '#69db7c', 2, 2);
      px(ctx, 5, 10, '#8ce99a', 3, 2);
      px(ctx, 12, 12, '#69db7c', 2, 2);
      break;
    }

    case 'leaves_frost': {
      // Korean Minhwa Blue-Glazed Ceramic Giwa Roof Tile (#1864ab, #1c7ed6, #228be6 with #ffd43b golden eaves ridge)
      for (let x = 0; x < 16; x++) {
        const rib = x % 4;
        const col = rib === 0 ? '#103f6e' : rib === 1 ? '#1864ab' : rib === 2 ? '#228be6' : '#1971c2';
        px(ctx, x, 0, col, 1, 16);
      }
      // Horizontal ceramic tile course lines + golden roof trim
      px(ctx, 0, 7, '#0b2e52', 16, 2);
      px(ctx, 0, 14, '#ffd43b', 16, 2);
      px(ctx, 2, 13, '#74c0fc', 2, 1);
      px(ctx, 6, 13, '#74c0fc', 2, 1);
      px(ctx, 10, 13, '#74c0fc', 2, 1);
      px(ctx, 14, 13, '#74c0fc', 2, 1);
      break;
    }

    case 'hay_side': {
      // Classic Minecraft Golden Hay Bale Side (Yellow wheat straw bundled with red binding straps)
      for (let y = 0; y < 16; y++) {
        for (let x = 0; x < 16; x++) {
          const col = (x + y * 3) % 3 === 0 ? '#ca8a04' : (x + y) % 2 === 0 ? '#eab308' : '#facc15';
          px(ctx, x, y, col);
        }
      }
      // Twin red Minecraft hay bale binding bands
      px(ctx, 0, 3, '#dc2626', 16, 2);
      px(ctx, 0, 11, '#dc2626', 16, 2);
      break;
    }

    case 'hay_top': {
      // Classic Minecraft Golden Hay Bale Top
      fillNoise(ctx, rng, ['#eab308', '#ca8a04', '#facc15', '#a16207']);
      px(ctx, 2, 2, '#fef08a', 3, 2);
      px(ctx, 10, 11, '#fef08a', 3, 2);
      break;
    }

    case 'pumpkin_side': {
      // Minecraft Carved Pumpkin Block Side
      for (let x = 0; x < 16; x++) {
        const rib = x % 4 === 0;
        px(ctx, x, 0, rib ? '#c2410c' : '#ea580c', 1, 16);
      }
      px(ctx, 0, 0, '#f97316', 16, 2);
      px(ctx, 0, 14, '#9a3412', 16, 2);
      break;
    }

    case 'pumpkin_front': {
      // Minecraft Glowing Jack-o'-Lantern Block Front
      for (let x = 0; x < 16; x++) {
        const rib = x % 4 === 0;
        px(ctx, x, 0, rib ? '#c2410c' : '#ea580c', 1, 16);
      }
      const jackFace = [
        '..YYY.....YYY..',
        '.YYYYY...YYYYY.',
        '..YYY.....YYY..',
        '......YYY......',
        '...............',
        '.YY.YYY.YYY.YY.',
        '.YYYYYYYYYYYYY.',
        '..YYY.YYY.YYY..',
      ];
      drawBitmap(ctx, jackFace, { Y: '#fef08a' }, 0, 4);
      drawBitmap(emCtx, jackFace, { Y: '#facc15' }, 0, 4);
      break;
    }

    case 'pumpkin_top': {
      // Minecraft Carved Pumpkin Stem Top
      fillNoise(ctx, rng, ['#ea580c', '#c2410c', '#f97316']);
      px(ctx, 6, 6, '#3f6212', 4, 4);
      px(ctx, 7, 7, '#65a30d', 2, 2);
      break;
    }

    case 'melon_side': {
      // Minecraft Redstone TNT & Firework Crate Side (WjAyI6kwylA security trap block — zero text, pixel-art spark icon)
      for (let x = 0; x < 16; x++) {
        const stick = Math.floor(x / 4) % 2 === 0;
        px(ctx, x, 0, stick ? '#e03131' : '#c92a2a', 1, 16);
      }
      // Dark dynamite stick caps top & bottom
      px(ctx, 0, 0, '#212529', 16, 2);
      px(ctx, 0, 14, '#212529', 16, 2);
      // Crisp white center band with pixel-art explosion star icon (NO fillText!)
      px(ctx, 0, 5, '#f8f9fa', 16, 6);
      px(ctx, 7, 5, '#e03131', 2, 6);
      px(ctx, 5, 7, '#e03131', 6, 2);
      px(ctx, 7, 7, '#ffd43b', 2, 2);
      px(emCtx, 5, 6, '#ff6b6b', 6, 4);
      break;
    }

    case 'melon_top': {
      // Minecraft Redstone TNT Crate Top (Bundled dynamite tops with white burning fuses)
      fillNoise(ctx, rng, ['#c92a2a', '#e03131', '#a61e4d']);
      px(ctx, 0, 7, '#212529', 16, 2);
      px(ctx, 7, 0, '#212529', 2, 16);
      px(ctx, 3, 3, '#f8f9fa', 2, 2);
      px(ctx, 11, 3, '#f8f9fa', 2, 2);
      px(ctx, 3, 11, '#f8f9fa', 2, 2);
      px(ctx, 11, 11, '#f8f9fa', 2, 2);
      px(ctx, 7, 7, '#ffd43b', 2, 2);
      break;
    }

    case 'beehive_side': {
      // JJ & Mikey's Chiseled Iron Security Bunker Wall Block Side (WjAyI6kwylA)
      fillNoise(ctx, rng, ['#e9ecef', '#dee2e6', '#f8f9fa', '#ced4da']);
      // Heavy dark iron plate border & corner rivets
      px(ctx, 0, 0, '#495057', 16, 2);
      px(ctx, 0, 14, '#495057', 16, 2);
      px(ctx, 0, 0, '#495057', 2, 16);
      px(ctx, 14, 0, '#495057', 2, 16);
      px(ctx, 3, 3, '#343a40', 2, 2);
      px(ctx, 11, 3, '#343a40', 2, 2);
      px(ctx, 3, 11, '#343a40', 2, 2);
      px(ctx, 11, 11, '#343a40', 2, 2);
      // Horizontal reinforced steel seam
      px(ctx, 2, 7, '#adb5bd', 12, 2);
      break;
    }

    case 'beehive_front': {
      // JJ & Mikey's Security Vault Passcode Keypad & Scanner Block Front (WjAyI6kwylA)
      fillNoise(ctx, rng, ['#dee2e6', '#ced4da', '#e9ecef']);
      px(ctx, 0, 0, '#343a40', 16, 2);
      px(ctx, 0, 14, '#343a40', 16, 2);
      px(ctx, 0, 0, '#343a40', 2, 16);
      px(ctx, 14, 0, '#343a40', 2, 16);
      // Dark steel keypad housing
      px(ctx, 3, 3, '#212529', 10, 10);
      // Cyan scanner screen at top + 4 glowing keypad buttons below
      px(ctx, 4, 4, '#3bc9db', 8, 3);
      px(ctx, 4, 8, '#51cf66', 3, 2);
      px(ctx, 9, 8, '#ffd43b', 3, 2);
      px(ctx, 4, 11, '#4dabf7', 3, 2);
      px(ctx, 9, 11, '#ff4d4f', 3, 2);
      px(emCtx, 4, 4, '#22b8cf', 8, 3);
      px(emCtx, 9, 11, '#e03131', 3, 2);
      break;
    }

    case 'beehive_top': {
      // JJ & Mikey's Chiseled Iron Security Bunker Block Top
      fillNoise(ctx, rng, ['#e9ecef', '#dee2e6', '#ced4da']);
      px(ctx, 0, 0, '#495057', 16, 2);
      px(ctx, 0, 14, '#495057', 16, 2);
      px(ctx, 0, 0, '#495057', 2, 16);
      px(ctx, 14, 0, '#495057', 2, 16);
      px(ctx, 5, 5, '#adb5bd', 6, 6);
      break;
    }

    case 'ice_crystal': {
      // Glowing Cyan Honmoon & Minecraft Diamond Portal Block (EgruEB4oZ2E / L0N4m23OSKM)
      for (let y = 0; y < 16; y++) {
        for (let x = 0; x < 16; x++) {
          const d = Math.hypot(x - 7.5, y - 7.5);
          const col = d < 3 ? '#ffffff' : d < 5.5 ? '#99e9f2' : d < 8 ? '#3bc9db' : '#1098ad';
          px(ctx, x, y, col);
        }
      }
      px(ctx, 0, 0, '#0c8599', 16, 2);
      px(ctx, 0, 14, '#0c8599', 16, 2);
      px(emCtx, 2, 2, '#22b8cf', 12, 12);
      px(emCtx, 5, 5, '#e3fafc', 6, 6);
      break;
    }

    case 'snow_top': {
      // Minecraft Reinforced Deepslate & Iron Security Bunker Floor with Redstone Circuit Lines (WjAyI6kwylA)
      fillNoise(ctx, rng, ['#2b3035', '#343a40', '#212529', '#3d444b']);
      // Chiseled deepslate border with iron corner inlays
      px(ctx, 0, 0, '#495057', 16, 2);
      px(ctx, 0, 14, '#1a1d20', 16, 2);
      px(ctx, 0, 0, '#495057', 2, 16);
      px(ctx, 14, 0, '#1a1d20', 2, 16);
      px(ctx, 2, 2, '#dee2e6', 2, 2);
      px(ctx, 12, 2, '#dee2e6', 2, 2);
      px(ctx, 2, 12, '#dee2e6', 2, 2);
      px(ctx, 12, 12, '#dee2e6', 2, 2);
      // Glowing Redstone security circuit trace in center
      px(ctx, 7, 3, '#e03131', 2, 10);
      px(ctx, 3, 7, '#e03131', 10, 2);
      px(ctx, 7, 7, '#ff6b6b', 2, 2);
      px(emCtx, 7, 7, '#c92a2a', 2, 2);
      break;
    }

    case 'snow_side': {
      // Minecraft Reinforced Deepslate Wall with Yellow/Black Caution & Redstone Laser Trim
      fillNoise(ctx, rng, ['#2b3035', '#343a40', '#212529']);
      for (let x = 0; x < 16; x += 4) {
        px(ctx, x, 0, '#ffd43b', 2, 3);
        px(ctx, x + 2, 0, '#212529', 2, 3);
      }
      px(ctx, 0, 3, '#ff4d4f', 16, 2);
      px(emCtx, 0, 3, '#c92a2a', 16, 2);
      break;
    }

    case 'castle_brick': {
      // Obsidian, Gold Block & Diamond Vault Tiles (#1a1128, #2b1d3d obsidian with #ffd43b gold & #3bc9db diamond)
      fillNoise(ctx, rng, ['#1a1128', '#241838', '#140c20', '#2f1f4a']);
      // Gold & diamond brick mortar lines
      px(ctx, 0, 0, '#ffd43b', 16, 1);
      px(ctx, 0, 7, '#495057', 16, 2);
      px(ctx, 0, 15, '#ffd43b', 16, 1);
      px(ctx, 0, 0, '#ffd43b', 1, 8);
      px(ctx, 7, 8, '#ffd43b', 2, 8);
      // Glowing cyan diamond crystal inlay in center
      px(ctx, 6, 3, '#3bc9db', 4, 3);
      px(ctx, 7, 4, '#e3fafc', 2, 1);
      px(emCtx, 6, 3, '#15aabf', 4, 3);
      break;
    }

    case 'furnace_side': {
      // Minecraft Blast Furnace & Redstone Smelter Block Side
      fillNoise(ctx, rng, ['#495057', '#343a40', '#6c757d']);
      px(ctx, 0, 0, '#212529', 16, 2);
      px(ctx, 0, 7, '#212529', 16, 2);
      px(ctx, 0, 14, '#212529', 16, 2);
      px(ctx, 3, 3, '#adb5bd', 10, 3);
      px(ctx, 3, 10, '#adb5bd', 10, 3);
      break;
    }

    case 'furnace_front': {
      // Minecraft Blast Furnace & Redstone Core Front
      fillNoise(ctx, rng, ['#495057', '#343a40', '#6c757d']);
      px(ctx, 0, 0, '#212529', 16, 2);
      px(ctx, 0, 14, '#212529', 16, 2);
      // Upper iron grill
      px(ctx, 3, 3, '#212529', 10, 4);
      px(ctx, 4, 4, '#ff922b', 2, 2);
      px(ctx, 7, 4, '#ffd43b', 2, 2);
      px(ctx, 10, 4, '#ff922b', 2, 2);
      // Lower glowing smelter firebox
      px(ctx, 3, 8, '#212529', 10, 5);
      px(ctx, 4, 9, '#ff6b6b', 8, 3);
      px(ctx, 5, 10, '#ffd43b', 6, 2);
      px(emCtx, 4, 9, '#f76707', 8, 3);
      break;
    }

    case 'amethyst': {
      // Minecraft Diamond & Emerald Ore Block (Stone matrix embedded with sparkling cyan diamond & green emerald gems)
      fillNoise(ctx, rng, ['#6c757d', '#868e96', '#495057', '#5c646d']);
      // Cyan diamond ore clusters
      px(ctx, 2, 2, '#3bc9db', 3, 3);
      px(ctx, 3, 3, '#e3fafc', 1, 1);
      px(ctx, 10, 4, '#22b8cf', 3, 2);
      px(ctx, 11, 4, '#ffffff', 1, 1);
      px(ctx, 4, 11, '#3bc9db', 3, 3);
      px(ctx, 5, 12, '#e3fafc', 1, 1);
      // Green emerald ore clusters
      px(ctx, 9, 10, '#51cf66', 3, 3);
      px(ctx, 10, 11, '#d3f9d8', 1, 1);
      px(emCtx, 2, 2, '#15aabf', 3, 3);
      px(emCtx, 4, 11, '#15aabf', 3, 3);
      px(emCtx, 9, 10, '#2b8a3e', 3, 3);
      break;
    }

    case 'bedrock_gold': {
      // Minecraft Gilded Blackstone & Chiseled 24K Gold Block
      fillNoise(ctx, rng, ['#212529', '#343a40', '#1a1d20']);
      px(ctx, 0, 0, '#ffd43b', 16, 3);
      px(ctx, 0, 13, '#ffd43b', 16, 3);
      px(ctx, 2, 5, '#fcc419', 5, 5);
      px(ctx, 3, 6, '#fff9db', 3, 3);
      px(ctx, 10, 6, '#3bc9db', 4, 4);
      px(emCtx, 2, 5, '#997a00', 5, 5);
      px(emCtx, 10, 6, '#15aabf', 4, 4);
      break;
    }

    case 'mega_titan_side': {
      // 2x2x2 Giant Minecraft Command Block & Obsidian Boss Spawner Cage
      fillNoise(ctx, rng, ['#1a1128', '#2b1d3d', '#212529']);
      px(ctx, 0, 0, '#ffd43b', 16, 2);
      px(ctx, 0, 14, '#ffd43b', 16, 2);
      px(ctx, 0, 0, '#ffd43b', 2, 16);
      px(ctx, 14, 0, '#ffd43b', 2, 16);
      const emblem = [
        '.C...Y...C.',
        '.CC.YYY.CC.',
        '.YYYYYYYYY.',
        '..CCCCCCC..',
        '....YYY....',
        '....YYY....',
        '....YYY....',
        '...........',
        '....CCC....',
        '....CCC....',
      ];
      drawBitmap(ctx, emblem, { Y: '#ffd43b', C: '#3bc9db' }, 3, 3);
      drawBitmap(emCtx, emblem, { Y: '#fab005', C: '#15aabf' }, 3, 3);
      break;
    }

    case 'mega_titan_top': {
      fillNoise(ctx, rng, ['#1a1128', '#2b1d3d']);
      px(ctx, 0, 0, '#ffd43b', 16, 2);
      px(ctx, 0, 14, '#ffd43b', 16, 2);
      px(ctx, 0, 0, '#ffd43b', 2, 16);
      px(ctx, 14, 0, '#ffd43b', 2, 16);
      px(ctx, 4, 4, '#ffd43b', 8, 8);
      px(ctx, 6, 6, '#3bc9db', 4, 4);
      px(emCtx, 4, 4, '#d97706', 8, 8);
      break;
    }

    case 'chest_front': {
      // Minecraft Diamond & Gold Safe Vault Chest Front (WjAyI6kwylA / L0N4m23OSKM)
      fillNoise(ctx, rng, ['#b45309', '#92400e', '#d97706']);
      // Heavy gold & cyan diamond frame
      px(ctx, 0, 0, '#ffd43b', 16, 2);
      px(ctx, 0, 14, '#ffd43b', 16, 2);
      px(ctx, 0, 0, '#ffd43b', 2, 16);
      px(ctx, 14, 0, '#ffd43b', 2, 16);
      // Chest lid seam + glowing cyan diamond lock latch
      px(ctx, 2, 6, '#212529', 12, 2);
      px(ctx, 6, 4, '#ffd43b', 4, 6);
      px(ctx, 7, 5, '#3bc9db', 2, 4);
      px(emCtx, 6, 4, '#fab005', 4, 6);
      break;
    }

    case 'chest_side': {
      fillNoise(ctx, rng, ['#b45309', '#92400e', '#d97706']);
      px(ctx, 0, 0, '#ffd43b', 16, 2);
      px(ctx, 0, 14, '#ffd43b', 16, 2);
      px(ctx, 0, 0, '#ffd43b', 2, 16);
      px(ctx, 14, 0, '#ffd43b', 2, 16);
      px(ctx, 2, 6, '#212529', 12, 2);
      px(ctx, 5, 9, '#3bc9db', 6, 3);
      break;
    }

    case 'chest_top': {
      fillNoise(ctx, rng, ['#ffd43b', '#f59f00', '#ffe066']);
      px(ctx, 0, 0, '#92400e', 16, 2);
      px(ctx, 0, 14, '#92400e', 16, 2);
      px(ctx, 0, 0, '#92400e', 2, 16);
      px(ctx, 14, 0, '#92400e', 2, 16);
      px(ctx, 5, 5, '#3bc9db', 6, 6);
      px(emCtx, 5, 5, '#15aabf', 6, 6);
      break;
    }

    case 'water': {
      // Minecraft Overworld Azure Water & Minhwa Lotus Pond
      fillNoise(ctx, rng, ['#1864ab', '#1971c2', '#1c7ed6', '#228be6']);
      px(ctx, 2, 3, '#74c0fc', 5, 1);
      px(ctx, 9, 8, '#a5d8ff', 5, 1);
      px(ctx, 4, 13, '#74c0fc', 6, 1);
      break;
    }

    case 'lantern_glow': {
      // Minecraft Glowstone & Sea Lantern Block
      px(ctx, 0, 0, '#b45309', 16, 16);
      px(ctx, 2, 2, '#ffd43b', 12, 12);
      px(ctx, 4, 4, '#fff9db', 8, 8);
      px(emCtx, 1, 1, '#ffd43b', 14, 14);
      px(emCtx, 4, 4, '#ffffff', 8, 8);
      break;
    }

    case 'mushroom_red': {
      // Redstone Laser Emitter & High-Voltage Caution Block (WjAyI6kwylA)
      fillNoise(ctx, rng, ['#212529', '#343a40']);
      for (let x = 0; x < 16; x += 4) {
        px(ctx, x, 0, '#ffd43b', 2, 3);
        px(ctx, x, 13, '#ffd43b', 2, 3);
      }
      // Bright glowing redstone laser beam core
      px(ctx, 0, 5, '#e03131', 16, 6);
      px(ctx, 0, 7, '#ff8787', 16, 2);
      px(emCtx, 0, 5, '#ff4d4f', 16, 6);
      break;
    }

    case 'snowman_face': {
      // Minecraft Iron Bar Security Window & Redstone CCTV Camera Lens Block (WjAyI6kwylA)
      fillNoise(ctx, rng, ['#1a1d20', '#212529']);
      // Heavy iron window frame
      px(ctx, 0, 0, '#dee2e6', 16, 2);
      px(ctx, 0, 14, '#adb5bd', 16, 2);
      px(ctx, 0, 0, '#dee2e6', 2, 16);
      px(ctx, 14, 0, '#adb5bd', 2, 16);
      // Vertical Minecraft iron bars
      px(ctx, 5, 2, '#ced4da', 2, 12);
      px(ctx, 9, 2, '#ced4da', 2, 12);
      px(ctx, 2, 7, '#adb5bd', 12, 2);
      // Glowing red security camera eye in center
      px(ctx, 6, 6, '#ff4d4f', 4, 4);
      px(ctx, 7, 7, '#fff5f5', 2, 2);
      px(emCtx, 6, 6, '#e03131', 4, 4);
      break;
    }

    default: {
      fillNoise(ctx, rng, ['#51cf66', '#ffd43b']);
      break;
    }
  }
}

export function getAtlasUVRect(tileIdx) {
  const col = tileIdx % ATLAS_COLS;
  const row = Math.floor(tileIdx / ATLAS_COLS);
  const pad = 0.12 / ATLAS_SIZE;
  const u0 = (col * TILE_SIZE) / ATLAS_SIZE + pad;
  const u1 = ((col + 1) * TILE_SIZE) / ATLAS_SIZE - pad;
  const v1 = 1 - (row * TILE_SIZE) / ATLAS_SIZE - pad;
  const v0 = 1 - ((row + 1) * TILE_SIZE) / ATLAS_SIZE + pad;
  return { u0, v0, u1, v1 };
}

export function createAtlasBoxGeometry(faceTiles, w = 1, h = 1, d = 1) {
  const geo = new THREE.BoxGeometry(w, h, d);
  const uv = geo.attributes.uv;
  const tiles = [
    faceTiles.px ?? faceTiles.side,
    faceTiles.nx ?? faceTiles.side,
    faceTiles.py ?? faceTiles.top ?? faceTiles.side,
    faceTiles.ny ?? faceTiles.bottom ?? faceTiles.top ?? faceTiles.side,
    faceTiles.pz ?? faceTiles.front ?? faceTiles.side,
    faceTiles.nz ?? faceTiles.back ?? faceTiles.front ?? faceTiles.side,
  ];
  for (let f = 0; f < 6; f++) {
    const { u0, v0, u1, v1 } = getAtlasUVRect(tiles[f]);
    const base = f * 4;
    uv.setXY(base + 0, u0, v1);
    uv.setXY(base + 1, u1, v1);
    uv.setXY(base + 2, u0, v0);
    uv.setXY(base + 3, u1, v0);
  }
  uv.needsUpdate = true;
  return geo;
}

function createRingGlowTexture() {
  const size = 64;
  const canvas = makeCanvas(size, size);
  const ctx = canvas.getContext('2d');
  const cx = size / 2;
  const cy = size / 2;
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const r = Math.hypot(x + 0.5 - cx, y + 0.5 - cy) / (size * 0.5);
      if (r > 1) continue;
      const ringBand = Math.exp(-Math.pow((r - 0.78) / 0.11, 2));
      const innerFill = r < 0.78 ? 0.24 * (1 - r * 0.5) : 0;
      const alpha = Math.min(1, ringBand * 0.92 + innerFill);
      if (alpha > 0.02) {
        ctx.fillStyle = `rgba(255,255,255,${alpha.toFixed(3)})`;
        ctx.fillRect(x, y, 1, 1);
      }
    }
  }
  const tex = new THREE.CanvasTexture(canvas);
  tex.magFilter = THREE.LinearFilter;
  tex.minFilter = THREE.LinearFilter;
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.needsUpdate = true;
  return tex;
}

function createSunTexture() {
  const size = 64;
  const canvas = makeCanvas(size, size);
  const ctx = canvas.getContext('2d');
  const cx = size / 2;
  // Square Minecraft Golden Sun halo + pixelated concentric gold & ivory squares
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const d = Math.max(Math.abs(x + 0.5 - cx), Math.abs(y + 0.5 - cx)) / cx;
      if (d < 1) {
        const glow = Math.pow(Math.max(0, 1 - d), 1.8) * 0.85;
        ctx.fillStyle = `rgba(255,230,110,${glow.toFixed(3)})`;
        ctx.fillRect(x, y, 1, 1);
      }
    }
  }
  px(ctx, 14, 14, '#fab005', 36, 36);
  px(ctx, 18, 18, '#ffd43b', 28, 28);
  px(ctx, 22, 22, '#ffe066', 20, 20);
  px(ctx, 26, 26, '#fff9db', 12, 12);
  const tex = new THREE.CanvasTexture(canvas);
  tex.magFilter = THREE.NearestFilter;
  tex.minFilter = THREE.LinearFilter;
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.needsUpdate = true;
  return tex;
}

function createSparkleTexture() {
  const size = 16;
  const canvas = makeCanvas(size, size);
  const ctx = canvas.getContext('2d');
  px(ctx, 7, 1, 'rgba(255,255,255,0.95)', 2, 14);
  px(ctx, 1, 7, 'rgba(255,255,255,0.95)', 14, 2);
  px(ctx, 5, 5, '#ffffff', 6, 6);
  return finalizePixelTexture(canvas, false);
}

export function createWorldTextures() {
  const rng = createRng(1337);
  const atlasCanvas = makeCanvas(ATLAS_SIZE, ATLAS_SIZE);
  const atlasCtx = atlasCanvas.getContext('2d');
  const emCanvas = makeCanvas(ATLAS_SIZE, ATLAS_SIZE);
  const emCtx = emCanvas.getContext('2d');
  emCtx.fillStyle = '#000000';
  emCtx.fillRect(0, 0, ATLAS_SIZE, ATLAS_SIZE);

  const tiles = {};

  for (const [name, idx] of Object.entries(TILE_INDEX)) {
    const tileCanvas = makeCanvas(TILE_SIZE, TILE_SIZE);
    const tCtx = tileCanvas.getContext('2d');
    const tileEmCanvas = makeCanvas(TILE_SIZE, TILE_SIZE);
    const tEmCtx = tileEmCanvas.getContext('2d');
    tEmCtx.fillStyle = '#000000';
    tEmCtx.fillRect(0, 0, TILE_SIZE, TILE_SIZE);

    paintTile(name, tCtx, tEmCtx, rng);

    const col = idx % ATLAS_COLS;
    const row = Math.floor(idx / ATLAS_COLS);
    atlasCtx.drawImage(tileCanvas, col * TILE_SIZE, row * TILE_SIZE);
    emCtx.drawImage(tileEmCanvas, col * TILE_SIZE, row * TILE_SIZE);

    tiles[name] = finalizePixelTexture(tileCanvas, name === 'water');
  }

  const atlasTexture = finalizePixelTexture(atlasCanvas, false);
  const emissiveAtlasTexture = finalizePixelTexture(emCanvas, false);

  return {
    tiles,
    atlasTexture,
    emissiveAtlasTexture,
    ringGlowTex: createRingGlowTexture(),
    sunTex: createSunTexture(),
    sparkleTex: createSparkleTexture(),
  };
}

export const createProceduralTextures = createWorldTextures;
