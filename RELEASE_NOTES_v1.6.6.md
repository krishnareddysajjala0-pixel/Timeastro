# Ravan Astro - Release Notes (v1.6.6)
**Version Code:** 13  
**Version Name:** 1.6.6  
**Release Date:** November 25, 2026  

---

### Google Play Console / Store Listing Release Notes

#### Telugu (తెలుగు) - Play Console:
```
• ఖచ్చితమైన గోచార కుండలి: గోచార కుండలి మధ్య భాగంలో తేదీ, సమయం మరియు లాహిరి అయనాంశ ఆధారిత ఖచ్చితమైన గ్రహ స్థితి వివరాలు.
• నక్షత్ర పాద కుండలి: గ్రహాల పేర్లు మరియు డిగ్రీల అక్షర పరిమాణం మరింత స్పష్టంగా, ఆకర్షణీయంగా మెరుగుపరచబడ్డాయి.
• బ్యాక్ బటన్ & స్థిరత్వం: బ్యాక్ బటన్ నావిగేషన్ మరియు యాప్ నిశ్చలంగా ఉన్నా స్క్రీన్ ఆగిపోకుండా ఆటోమేటిక్ రీకనెక్షన్ సదుపాయం.
• వేగవంతమైన లోడింగ్ మరియు స్థిరత్వ మెరుగుదలలు.
```

#### English - Play Console:
```
• Accurate Transit Chart: Transit (Gochara) kundali center box now features precise date, time, and Lahiri ayanamsa calculations.
• Nakshatra Pada Kundali: Enhanced planet names and degree sizing for optimal clarity and readability.
• Seamless Back Navigation: Upgraded Android back button handling and instant auto-recovery after idle background periods.
• General performance optimizations and stability fixes.
```

---

### Technical Change Log:
1. **Astronomy & Transit Calculations**:
   - Explicitly locked Lahiri Ayanamsa (`swe.set_sid_mode(swe.SIDM_LAHIRI)`) across all transit endpoints.
   - Transit kundali center box now displays formatted real-time date and time.
2. **Nakshatra Pada Kundali UI**:
   - Increased planet name pills and degree suffix to 12px for desktop/web browser viewing.
   - Retained responsive compact mobile view for Android devices.
3. **Android App Resilience**:
   - Added `OnBackPressedCallback` for Android 13+ / 14 gesture navigation.
   - Added automatic health-check ping and background server reconnection when resuming after idle time.
   - Added safety timeout guards to dismiss loading overlays on back/forward cache and visibility change.
4. **Build & Release**:
   - `versionCode`: 12 -> 13
   - `versionName`: 1.6.5 -> 1.6.6
