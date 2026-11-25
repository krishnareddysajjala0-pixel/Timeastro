# Ravan Astro - Release Notes (v1.6.7)
**Version Code:** 14  
**Version Name:** 1.6.7  
**Release Date:** November 25, 2026  

---

### Google Play Console / Store Listing Release Notes

#### Telugu (తెలుగు) - Play Console:
```
• నక్షత్ర పాద కుండలి మెరుగుదలలు: పేజీలో పునరావృతమైన (డూప్లికేట్) బటన్లు తొలగించబడి సులభమైన నావిగేషన్ అందించబడింది.
• ఖచ్చితమైన సింగిల్-పేజ్ PDF ప్రింట్: వెబ్ యాప్ (ravanastro.vercel.app) మాదిరిగానే ఆండ్రాయిడ్ యాప్‌లో కూడా నక్షత్ర కుండలి ఖచ్చితంగా 1 పేజీ A4 పరిమాణంలో, స్పష్టమైన అక్షరాలు (16px) మరియు బోర్డర్లతో ప్రింట్/సేవ్ అవుతుంది.
• పేజీ లేఅవుట్ & మార్జిన్లు: ప్రింట్ సమయంలో అనవసరమైన ఖాళీ స్థలాలు లేకుండా పూర్తి పేజీకి సరిపోయేలా ఆప్టిమైజ్ చేయబడింది.
• వేగవంతమైన పనితీరు మరియు స్థిరత్వ మెరుగుదలలు.
```

#### English - Play Console:
```
• Nakshatra Chart Navigation: Removed duplicate navigation and print buttons for a cleaner, unified interface.
• Identical 1-Page PDF Print: Android app PDF generation now matches the web app (ravanastro.vercel.app) exactly—strict 1-page A4 fit, equal 16px typography, and precise box dimensions.
• Optimized Print Layout: Eliminated excess header margins during print, ensuring no page splits or clipped content.
• General performance optimizations and stability improvements.
```

---

### Technical Change Log:
1. **Nakshatra Pada Kundali UI Cleanup**:
   - Removed redundant Home (`top-btn-home`), Normal Kundali (`top-btn-back`), and Print (`top-btn-print`) buttons from `.top-control-bar`.
   - Preserved Aspects (`#chupuluBtn`) and Language switcher in the top bar.
   - Unified all primary navigation in the bottom floating action bar (`#action-bar`: Home, Kundali, Dasacharamu, Grahalu, Print).
2. **Android PDF Generation Alignment (Web Parity)**:
   - Scoped Android compact screen font rules (`html.is-android-app`) strictly to `@media screen` so they do not leak into the print renderer.
   - Added `html.is-android-app` to `@media print` 16px typography selectors (`.center-box`, `.nak-name-text`, `.pada-row`, `.pada-num`, `.occupant-pill`, `.planet-deg-suffix`).
   - Standardized `body.mobile-pdf-rendering` top margin (`0.8em auto 0.3em auto`), matching `@media print` and preventing page 2 overflow.
   - Applied full 1024px print viewport and `zoom: 0.90` inside `body.mobile-pdf-rendering .container` for exact 1-page A4 output.
3. **Build & Release**:
   - `versionCode`: 13 -> 14
   - `versionName`: 1.6.6 -> 1.6.7
