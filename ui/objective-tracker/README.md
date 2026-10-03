# Gothic Objective Tracker UI

Gotik horror atmosferine uygun **Current Objective** HUD konsepti.

## Dosyalar

| Dosya | Açıklama |
| --- | --- |
| `mockup-ingame-final.jpg` | **Final:** yeni HUD, oyun sahnesi üzerinde |
| `mockup-widget-closeup.jpg` | Widget close-up |
| `gothic-objective-tracker-ui.jpg` | Atmosferik konsept |
| `objective-widget-isolated.jpg` | İzole widget referansı (asset üretimi) |
| `reference-ingame-clean.jpg` | Eski UI temizlenmiş sahne |
| `index.html` + `objective-tracker.css` | Galeri + canlı CSS prototip |

Mockup’ı görmek için:

```bash
cd ui/objective-tracker
python3 -m http.server 8765
# http://localhost:8765
```

## Tasarım dili

- **Çerçeve:** işlenmiş demir + bronz filigree, kesik köşeler (düz dikdörtgen yok)
- **Dolgu:** yarı saydam kömür taş / parşömen, hafif doku
- **Sol:** dikey altın progress rail (görev ilerlemesi)
- **Sağ:** karga + eriyen mum (sıcak ışık, soğuk mavi sahneyle kontrast)
- **Tipografi:** Cinzel (başlık/label) + Cormorant Garamond (açıklama)
- **Palet:** ink `#07090d`, gold `#c9a45c`, fog `#a8b0bc`, ember `#ffb35a`

## Unreal Engine (UMG) kurulum özeti

1. **Widget Blueprint** oluştur: `WBP_ObjectiveTracker`
2. **Canvas Panel** → sağ-üst anchor (`1,0` / alignment `1,0`), offset ~`X=-24 Y=36`, size ~`420×110`
3. Katmanlar (alt → üst):
   - `Image_Frame` — demir çerçeve (PNG, 9-slice / retained border)
   - `Image_Fill` — yarı saydam dolgu
   - `ProgressBar_Rail` — dikey, fill color gold/ember
   - `VerticalBox` metin: Label / Title / Description / Count
   - `Overlay_Ornament` — Raven + Candle (ayrı texture veya Niagara soft glow)
4. **Font:** Cinzel / benzeri serif’i `Font Face` olarak import et; label’a letter-spacing ver
5. **Animasyonlar (UMG / Widget Animation):**
   - `Appear`: 0→1 opacity + sağdan 18px slide (~0.7s EaseOut)
   - `CandleFlicker`: flame scale/opacity ping-pong veya materyal `Time` node
   - `Complete`: rail fill → 100%, kısa gold flash, sonra fade-out
6. **Materyal ipuçları:**
   - Frame: soft metallic + slight roughness noise
   - Candle glow: additive sprite / UI material with emissive
   - Fill: desaturated paper noise at low opacity (~0.15)

## Metin bağlama

```
Label:        CURRENT OBJECTIVE
Title:        {ObjectiveTitle}
Description:  {ObjectiveDescription}
Count:        {Current}/{Required}
```

Blueprint’te `SetObjective(FText Title, FText Desc, int32 Current, int32 Required)` ile güncelle.
