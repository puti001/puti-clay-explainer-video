        // ============================================================
        //  67 秒版：固定攝影機 + 螢幕座標走位 + 七通道情緒
        //  角色一律用「螢幕像素」定位：mark(px, py, hpx)
        // ============================================================
        const CAM_POS = [0.0, 3.15, 12.0];
        const CAM_LOOK = [0.0, 1.05, 0.0];

        camera.fov = 27;
        camera.position.set(CAM_POS[0], CAM_POS[1], CAM_POS[2]);
        camera.lookAt(CAM_LOOK[0], CAM_LOOK[1], CAM_LOOK[2]);
        camera.updateProjectionMatrix();
        camera.updateMatrixWorld(true);

        const v3 = (x, y, z) => new THREE.Vector3(x, y, z);
        const gPlane = new THREE.Plane(v3(0, 1, 0), 0);
        const gRay = new THREE.Raycaster();
        const gNdc = new THREE.Vector2();
        const gHit = new THREE.Vector3();

        // 螢幕點 → 地面（y = 0）世界座標
        function groundAt(px, py) {
          gNdc.set((px / W) * 2 - 1, -(py / H) * 2 + 1);
          gRay.setFromCamera(gNdc, camera);
          if (!gRay.ray.intersectPlane(gPlane, gHit)) return { x: 0, z: 0 };
          return { x: gHit.x, z: gHit.z };
        }

        // 該位置 1 世界單位 = 幾螢幕像素
        function ppuAt(x, z) {
          const a = v3(x, 0, z).project(camera);
          const b = v3(x, 1, z).project(camera);
          return Math.max(30, Math.abs(b.y - a.y) * H * 0.5);
        }

        function mark(px, py, hpx) {
          const g = groundAt(px, py);
          const ppu = ppuAt(g.x, g.z);
          return { x: g.x, z: g.z, ppu: ppu, k: hpx / ppu };
        }

        // 永遠面向鏡頭（角色正面在 +z）
        function faceCam(x, z) {
          return Math.atan2(CAM_POS[0] - x, CAM_POS[2] - z);
        }

        // ---- 情緒表：[t, joy, wow, ner, ang, sad, cold, wind] ----
        const EMO = [
          [0.00, 0.45, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
          [0.90, 0.62, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
          [1.80, 0.80, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
          [2.55, 0.30, 0.70, 0.15, 0.00, 0.00, 0.00, 0.05],
          [3.20, 0.15, 0.95, 0.20, 0.00, 0.00, 0.00, 0.05],
          [3.95, 0.10, 0.30, 0.85, 0.00, 0.00, 0.00, 0.00],
          [4.70, 0.15, 0.10, 0.95, 0.00, 0.00, 0.05, 0.00],
          [5.35, 0.55, 0.00, 0.30, 0.00, 0.00, 0.00, 0.00],
          [6.10, 0.92, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
          [6.90, 0.85, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
          [7.60, 0.90, 0.00, 0.00, 0.00, 0.00, 0.00, 0.05],
          [9.10, 0.70, 0.00, 0.10, 0.00, 0.00, 0.10, 0.15],
          [10.40, 0.55, 0.25, 0.15, 0.00, 0.00, 0.20, 0.20],
          [11.40, 0.75, 0.00, 0.00, 0.00, 0.00, 0.05, 0.05],
          [12.40, 1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
          [13.20, 0.85, 0.00, 0.00, 0.00, 0.00, 0.05, 0.00],
          [14.90, 0.65, 0.00, 0.00, 0.00, 0.00, 0.10, 0.10],
          [15.80, 0.30, 0.00, 0.10, 0.00, 0.00, 0.70, 0.45],
          [16.80, 0.15, 0.00, 0.15, 0.00, 0.00, 0.90, 0.55],
          [17.80, 0.10, 0.00, 0.20, 0.00, 0.00, 0.95, 0.60],
          [19.10, 0.10, 0.00, 0.25, 0.00, 0.00, 0.70, 0.85],
          [20.10, 0.10, 0.15, 0.30, 0.00, 0.00, 0.60, 0.95],
          [21.40, 0.15, 0.10, 0.30, 0.00, 0.00, 0.55, 0.70],
          [22.90, 0.20, 0.00, 0.20, 0.00, 0.00, 0.55, 0.40],
          [23.80, 0.15, 0.00, 0.10, 0.00, 0.00, 0.80, 0.25],
          [25.30, 0.10, 0.30, 0.10, 0.00, 0.00, 0.65, 0.15],
          [25.95, 0.05, 1.00, 0.05, 0.00, 0.05, 0.35, 0.10],
          [26.80, 0.10, 0.75, 0.10, 0.00, 0.10, 0.40, 0.10],
          [27.90, 0.20, 0.10, 0.15, 0.00, 0.20, 0.45, 0.20],
          [28.90, 0.55, 0.00, 0.00, 0.00, 0.10, 0.20, 0.10],
          [30.20, 0.65, 0.00, 0.00, 0.00, 0.00, 0.10, 0.05],
          [31.90, 0.20, 0.00, 0.05, 0.00, 0.55, 0.25, 0.10],
          [33.00, 0.12, 0.00, 0.00, 0.00, 0.70, 0.15, 0.10],
          [34.20, 0.05, 0.00, 0.00, 0.00, 0.95, 0.10, 0.05],
          [35.40, 0.10, 0.00, 0.00, 0.00, 0.85, 0.05, 0.05],
          [36.60, 0.20, 0.00, 0.00, 0.00, 0.45, 0.00, 0.05],
          [37.60, 0.70, 0.00, 0.00, 0.00, 0.10, 0.00, 0.00],
          [38.60, 0.90, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
          [39.90, 0.30, 0.00, 0.10, 0.00, 0.00, 0.35, 0.65],
          [41.20, 0.15, 0.00, 0.15, 0.15, 0.00, 0.35, 0.85],
          [42.40, 0.05, 0.00, 0.10, 0.65, 0.00, 0.30, 0.60],
          [43.20, 0.05, 0.00, 0.05, 0.90, 0.00, 0.25, 0.45],
          [44.10, 0.10, 0.20, 0.05, 0.75, 0.00, 0.20, 0.40],
          [44.80, 0.20, 0.75, 0.05, 0.25, 0.00, 0.15, 0.45],
          [45.80, 0.35, 0.85, 0.00, 0.05, 0.00, 0.10, 0.40],
          [46.80, 0.55, 0.30, 0.00, 0.00, 0.00, 0.05, 0.30],
          [47.90, 0.75, 0.00, 0.00, 0.00, 0.00, 0.00, 0.10],
          [49.00, 0.85, 0.00, 0.00, 0.00, 0.00, 0.00, 0.05],
          [50.20, 0.95, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
          [51.60, 1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
          [52.80, 0.95, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
          [54.20, 0.50, 0.40, 0.05, 0.00, 0.00, 0.00, 0.00],
          [54.80, 0.35, 0.95, 0.05, 0.00, 0.00, 0.00, 0.00],
          [55.80, 0.45, 0.70, 0.05, 0.00, 0.00, 0.00, 0.00],
          [56.80, 0.30, 0.30, 0.55, 0.00, 0.00, 0.00, 0.00],
          [57.60, 0.25, 0.15, 0.70, 0.00, 0.00, 0.00, 0.00],
          [58.40, 0.40, 0.05, 0.40, 0.00, 0.00, 0.00, 0.00],
          [59.50, 0.85, 0.00, 0.10, 0.00, 0.00, 0.00, 0.00],
          [60.30, 0.95, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
          [61.20, 1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
          [63.40, 0.95, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
          [65.00, 0.90, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
          [67.00, 0.85, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        ];
        const CH = ["joy", "wow", "ner", "ang", "sad", "cold", "wind"];

        function moodAt(t) {
          let i = 0;
          for (let k = 1; k < EMO.length; k++) if (t >= EMO[k][0]) i = k;
          const a = EMO[i];
          const b = EMO[Math.min(i + 1, EMO.length - 1)];
          const u = b[0] > a[0] ? sm(t, a[0], b[0]) : 0;
          const o = {};
          for (let j = 0; j < CH.length; j++) o[CH[j]] = a[j + 1] + (b[j + 1] - a[j + 1]) * u;
          return o;
        }

        // ---- 走位表：螢幕像素（腳底位置）----
        // [時間, 腳底 x, 腳底 y, 螢幕高度 px, 這一段的動作]
        const POS = [
          [0.00, 1580, 606, 190, "slide"],
          [1.02, 224, 636, 186, "hold"],
          [2.28, 224, 636, 186, "walk"],
          [2.72, 314, 632, 186, "hold"],
          [4.24, 314, 632, 186, "walk"],
          [4.66, 252, 634, 186, "hold"],
          [6.30, 252, 634, 186, "walk"],
          [6.94, 652, 600, 164, "hold"],
          [14.30, 652, 600, 164, "walk"],
          [14.94, 212, 612, 200, "hold"],
          [16.30, 212, 612, 200, "walk"],
          [16.74, 300, 607, 200, "hold"],
          [17.30, 300, 607, 200, "walk"],
          [17.72, 242, 610, 200, "hold"],
          [22.30, 242, 610, 200, "walk"],
          [22.94, 156, 686, 160, "hold"],
          [25.60, 156, 686, 160, "walk"],
          [26.02, 232, 682, 160, "hold"],
          [30.30, 232, 682, 160, "walk"],
          [30.94, 180, 674, 168, "hold"],
          [34.60, 180, 674, 168, "walk"],
          [35.04, 292, 670, 168, "hold"],
          [39.30, 292, 670, 168, "walk"],
          [39.94, 1046, 530, 186, "hold"],
          [42.90, 1046, 530, 186, "walk"],
          [43.34, 1084, 538, 186, "hold"],
          [47.30, 1084, 538, 186, "walk"],
          [47.94, 1082, 620, 178, "hold"],
          [50.90, 1082, 620, 178, "walk"],
          [51.34, 958, 614, 178, "hold"],
          [55.20, 958, 614, 178, "walk"],
          [55.64, 1086, 618, 178, "hold"],
          [58.80, 1086, 618, 178, "walk"],
          [59.44, 1084, 628, 188, "hold"],
          [62.40, 1084, 628, 188, "walk"],
          [62.84, 1134, 626, 186, "hold"],
          [67.00, 1134, 626, 186, "hold"],
        ];

        function segAt(t) {
          let i = 0;
          for (let k = 1; k < POS.length; k++) if (t >= POS[k][0]) i = k;
          const a = POS[i];
          const b = POS[Math.min(i + 1, POS.length - 1)];
          const mode = a[4];
          const u = b[0] > a[0] ? prog(t, a[0], b[0]) : 0;
          let e = u;
          if (mode === "walk") e = eio(u);
          else if (mode === "slide") e = 1 - Math.pow(1 - u, 2.4);
          const px = a[1] + (b[1] - a[1]) * e;
          const py = a[2] + (b[2] - a[2]) * e;
          const hpx = a[3] + (b[3] - a[3]) * e;
          let hop = 0;
          if (mode === "walk") {
            const dist = Math.abs(b[1] - a[1]);
            const n = Math.max(1, Math.round(dist / 95));
            hop = Math.abs(Math.sin(Math.PI * n * u)) * (9 + Math.min(9, dist / 34));
          }
          return { px, py, hpx, hop, mode, u };
        }

        // ---- 加碼跳躍 [起, 高度 px, 長度] / 旋轉 [起, 長度] ----
        const JUMPS = [
          [3.86, 26, 0.34], [5.16, 22, 0.30], [10.42, 28, 0.36], [11.30, 22, 0.30],
          [16.40, 24, 0.32], [19.10, 28, 0.36], [20.55, 22, 0.30],
          [23.60, 14, 0.30], [25.92, 16, 0.34], [26.62, 12, 0.28], [28.85, 14, 0.30],
          [33.40, 14, 0.30], [34.85, 16, 0.32], [37.15, 16, 0.32], [38.25, 14, 0.30],
          [41.25, 12, 0.30], [42.45, 12, 0.30], [44.95, 12, 0.30],
          [49.40, 26, 0.34], [50.60, 26, 0.34], [52.20, 30, 0.38], [53.15, 22, 0.30],
          [54.85, 32, 0.42], [56.85, 24, 0.32], [58.20, 24, 0.32],
          [60.20, 32, 0.40], [61.35, 28, 0.36], [62.95, 24, 0.32],
          [64.30, 28, 0.38], [65.35, 24, 0.32], [66.25, 20, 0.30],
        ];
        const SPINS = [[12.42, 0.78], [62.88, 0.52]];

        // ---- 落地壓縮 ----
        const IMPACT = [[1.04, 1.5]];
        for (let i = 1; i < POS.length; i++) {
          if (POS[i - 1][4] !== "hold") IMPACT.push([POS[i][0], 0.9]);
        }
        JUMPS.forEach((j) => IMPACT.push([j[0] + j[2], 0.35 + j[1] / 70]));

        // ---- 動作 ----
        function motionAt(t, m) {
          const s = segAt(t);
          let rx = 0;
          let ry = 0;
          let rz = 0;
          let jump = s.hop;

          for (const j of JUMPS) {
            if (t > j[0] && t < j[0] + j[2]) {
              jump += Math.sin(Math.PI * prog(t, j[0], j[0] + j[2])) * j[1];
            }
          }
          for (const sp of SPINS) {
            if (t > sp[0] && t < sp[0] + sp[1]) ry += Math.PI * 2 * eio(prog(t, sp[0], sp[0] + sp[1]));
          }

          // 開場急滑 + 後仰
          if (t < 1.14) {
            const u = prog(t, 0, 1.14);
            const k = Math.sin(Math.PI * Math.min(1, u * 1.12));
            rz -= 0.30 * k;
            rx -= 0.10 * k;
          }

          // 冷到發抖
          rz += 0.030 * Math.sin(t * 37.5) * m.cold;
          rx += 0.018 * Math.sin(t * 31.0) * m.cold;
          // 生氣抖 + 脹
          rz += 0.045 * Math.sin(t * 41.0) * m.ang;
          // 風吹：整塊往左倒 + 抖
          rz += 0.20 * m.wind + 0.045 * m.wind * Math.sin(t * 2.7);
          rx += 0.05 * m.wind;

          let sy = 1;
          let sxz = 1;
          sy *= 1 - 0.15 * m.sad;
          sxz *= 1 + 0.06 * m.sad;
          rx += 0.05 * m.sad;
          sy *= 1 - 0.05 * m.cold;
          sxz *= 1 + 0.03 * m.cold;
          sy *= 1 + 0.03 * m.ang + 0.008 * Math.sin(t * 17) * m.ang;
          sy *= 1 + 0.05 * m.wow;
          sxz *= 1 - 0.03 * m.wow;
          sy *= 1 + 0.012 * Math.sin(t * 2.3);
          sxz *= 1 - 0.006 * Math.sin(t * 2.3);

          for (const im of IMPACT) {
            const d = t - im[0];
            if (d > 0 && d < 0.5) {
              const k = Math.exp(-d * 8.5) * Math.sin(d * 24);
              sy += 0.20 * im[1] * k;
              sxz -= 0.14 * im[1] * k;
            }
          }

          return { px: s.px, py: s.py, hpx: s.hpx, jump, rx, ry, rz, sy, sxz };
        }

        // ---- 表情 ----
        const BLINKS = [];
        for (let i = 0; i < 30; i++) BLINKS.push(1.65 + i * 2.31 + (i % 3) * 0.21);

        function faceAt(t, m) {
          let blink = 0;
          for (const b of BLINKS) {
            if (t > b && t < b + 0.15) blink = Math.sin(prog(t, b, b + 0.15) * Math.PI);
          }

          const happy = clamp01(m.joy);
          const narrow = m.ang;
          const soft = m.sad;
          const cold = m.cold;

          const eyeSY =
            (1 + 0.3 * m.wow - 0.45 * narrow - 0.28 * soft - 0.14 * cold - 0.16 * m.wind) *
            (1 - 0.9 * blink);
          const eyeSX = 1 + 0.22 * m.wow - 0.05 * narrow;

          const browTilt = 0.34 * narrow - 0.3 * soft - 0.24 * m.ner - 0.16 * cold;
          const browY = 0.805 + 0.028 * m.wow - 0.02 * narrow - 0.012 * soft + 0.005 * cold;
          const look = m.ner * 0.055 * Math.sin(t * 4.2) + m.wind * 0.03 * Math.sin(t * 1.7);

          return {
            happy: happy,
            narrow: narrow,
            soft: soft,
            eyeSY: eyeSY,
            eyeSX: eyeSX,
            browTilt: browTilt,
            browY: browY,
            browVis: clamp01(narrow + soft + m.ner + m.wow + cold),
            look: look,
            mouth: restMouth({
              smile: clamp01(happy),
              frown: clamp01(soft),
              flat: clamp01(0.75 * m.ner + 0.9 * narrow + 0.6 * cold),
              oh: clamp01(m.wow),
            }),
            cheekOp: 0.5 + 0.28 * narrow - 0.34 * soft,
            cheekColor: new THREE.Color(0xe08a6e)
              .lerp(new THREE.Color(0xd4341c), narrow)
              .lerp(new THREE.Color(0xa9b3c4), Math.max(soft, cold * 0.8)),
            skin: new THREE.Color(S.gold)
              .lerp(new THREE.Color(0xe6c34a), m.wow * 0.55)
              .lerp(new THREE.Color(S.angry), narrow * 0.95)
              .lerp(new THREE.Color(0xb3aea0), soft * 0.45)
              .lerp(new THREE.Color(0xe6ecef), cold * 0.55),
          };
        }

        function restMouth(w) {
          const sum = w.smile + w.frown + w.flat + w.oh;
          w.smile = clamp01(w.smile + 0.56 * clamp01(1 - sum));
          return w;
        }

        function weigh(mesh, w) {
          mesh.visible = w > 0.02;
          mesh.scale.setScalar(Math.max(0.001, w));
        }

        // ---- 主渲染 ----
        const ANG_T0 = 41.35;
        const FLASHES = [42.55, 43.30, 44.05];
        // 這版角色都站在卡片下方，烏雲會整朵躲在卡片後面，
        // 所以傷心戲改用眼淚＋垂垮＋臉色，烏雲與雨暫時關閉（保留程式碼）
        const RAIN_SCENE = false;

        function renderAt(t) {
          const m = moodAt(t);
          const mo = motionAt(t, m);
          const fc = faceAt(t, m);
          const mk = mark(mo.px, mo.py, mo.hpx);

          hero.position.set(mk.x, mo.jump / mk.ppu, mk.z);
          hero.scale.setScalar(mk.k);
          hero.rotation.set(mo.rx, mo.ry + faceCam(mk.x, mk.z), mo.rz);

          body.position.y = 0;
          body.scale.set(mo.sxz, mo.sy, mo.sxz);

          // 臉色
          clayMat.color.copy(fc.skin);
          clayMat.emissive.setRGB(0.34 * m.ang, 0.03 * m.ang, 0.0);
          angerLight.intensity = 2.6 * m.ang;
          angerLight.position.set(mk.x + 0.2, 0.15, mk.z + 1.1);

          // 眼睛
          eyeL.scale.set(fc.eyeSX, fc.eyeSY, 0.6);
          eyeR.scale.set(fc.eyeSX, fc.eyeSY, 0.6);
          eyesGroup.position.x = fc.look;
          weigh(eyeL, 1 - fc.happy);
          weigh(eyeR, 1 - fc.happy);
          weigh(happyL, fc.happy);
          weigh(happyR, fc.happy);

          // 眉毛
          browL.position.y = fc.browY;
          browR.position.y = fc.browY;
          browL.rotation.z = -fc.browTilt;
          browR.rotation.z = fc.browTilt;
          weigh(browL, fc.browVis);
          weigh(browR, fc.browVis);

          // 嘴
          weigh(smile, fc.mouth.smile);
          weigh(frown, fc.mouth.frown);
          weigh(flatMouth, fc.mouth.flat);
          weigh(ohMouth, fc.mouth.oh);

          // 腮紅
          cheekMat.color.copy(fc.cheekColor);
          cheekMat.opacity = Math.max(0, fc.cheekOp);

          // 接觸陰影
          heroShadow.position.set(mk.x, 0.004, mk.z);
          const hgt = mo.jump / mk.ppu;
          const sc = 1 - Math.min(0.55, hgt * 0.55);
          heroShadow.scale.setScalar(mk.k * (0.92 * sc + 0.18));
          heroShadow.material.opacity = 0.72 * (0.35 + 0.65 * sc);

          // 汗滴
          const sw = m.ner;
          sweat.visible = sw > 0.06;
          if (sweat.visible) {
            const u = (t * 0.72) % 1;
            sweat.position.set(0.36, 0.85 - u * 0.26, 0.45);
            sweat.material.opacity = 0.95 * (1 - u * 0.5) * Math.min(1, sw * 1.6);
            sweat.scale.set(1, 1.45, 1);
          }

          // 眼淚
          const tearMix = clamp01((m.sad - 0.45) / 0.22);
          const tcyc = (t * 1.24) % 1;
          [tearL, tearR].forEach((d, i) => {
            const win = i === 0 ? tcyc < 0.5 : tcyc >= 0.5;
            const u = i === 0 ? tcyc * 2 : (tcyc - 0.5) * 2;
            const on = tearMix > 0.02 && win;
            d.visible = on;
            if (!on) return;
            d.position.set(i ? 0.255 : -0.255, 0.58 - u * 0.3, 0.49);
            d.material.opacity = 0.95 * tearMix * (1 - u * 0.45);
            d.scale.set(1, 1.5 + u * 0.4, 1);
          });

          // 冒煙（掛在 hero 底下，跟著角色縮放走位）
          const smokeOn = m.ang > 0.25;
          puffs.forEach((p, i) => {
            const local = t - ANG_T0 - p.delay * 0.55;
            if (!smokeOn || local < 0) {
              p.m.material.opacity = 0;
              p.m.visible = false;
              return;
            }
            const life = local % 1.45;
            const u = life / 1.0;
            p.m.visible = u < 1;
            p.m.material.opacity =
              u < 1
                ? 0.9 * Math.pow(1 - u, 0.55) * Math.min(1, m.ang * 1.6) * Math.min(1, u * 5)
                : 0;
            p.m.position.set(
              p.side + 0.09 * u * (i % 2 ? 1 : -1),
              0.96 + u * 0.55,
              0.1,
            );
            const sc2 = 0.42 + u * 0.72;
            p.m.scale.setScalar(sc2 * (0.85 + 0.15 * Math.sin(i * 2.1)));
          });

          // 閃電（角色左側，避免壓到標題與字幕）
          let flash = 0;
          let flashIdx = 0;
          FLASHES.forEach((ft, i) => {
            const d = t - ft;
            if (d > 0 && d < 0.28) {
              const k = Math.pow(1 - d / 0.28, 0.65) * (0.55 + 0.45 * Math.abs(Math.sin(d * 58)));
              if (k > flash) {
                flash = k;
                flashIdx = i;
              }
            }
          });
          bolts.forEach((b, i) => {
            const on = flash > 0 && i === flashIdx % 2;
            b.visible = on;
            b.material.opacity = on ? Math.min(1, flash * 1.9) : 0;
            b.position.set(i === 0 ? -1.18 : -0.62, 1.18 + (i === 0 ? 0.06 : 0.18), 0.42);
            b.scale.set(i === 0 ? 0.74 : 0.56, 0.62 + 0.14 * flash, 1);
          });

          // 烏雲
          const sad = m.sad;
          const sadFx = RAIN_SCENE && sad > 0.05;
          cloudGroup.visible = sadFx;
          cloudGroup.position.set(Math.sin(t * 0.9) * 0.06, 1.88 - 0.1 * (1 - sad), 0.12);
          cloudGroup.scale.setScalar(0.56 + 0.34 * sad);
          cloudMat.opacity = 1;

          // 雨
          rainMat.opacity = sadFx ? 0.55 * clamp01((sad - 0.35) / 0.4) : 0;
          rainGroup.visible = sadFx && sad > 0.4;
          drops.forEach((d) => {
            const u = ((t * d.speed * 0.55 + d.ph) % 1 + 1) % 1;
            d.m.visible = true;
            d.m.position.set(d.x, 1.62 - u * 0.95, d.z);
            d.m.scale.y = 1 + 0.35 * u;
          });

          renderer.render(scene, camera);
        }

        window.__dbg = (tt) => {
          const q = tt === undefined ? 0 : tt;
          const m = moodAt(q);
          const s = segAt(q);
          const mk = mark(s.px, s.py, s.hpx);
          return {
            t: q,
            px: Math.round(s.px),
            py: Math.round(s.py),
            hpx: Math.round(s.hpx),
            k: +mk.k.toFixed(2),
            x: +mk.x.toFixed(2),
            z: +mk.z.toFixed(2),
            joy: +m.joy.toFixed(2),
            wow: +m.wow.toFixed(2),
            ang: +m.ang.toFixed(2),
            sad: +m.sad.toFixed(2),
            cold: +m.cold.toFixed(2),
            wind: +m.wind.toFixed(2),
          };
        };
