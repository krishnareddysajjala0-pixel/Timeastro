
import sys
import os

# Mock session and flask for testing
class MockSession(dict):
    pass

def test_results_logic():
    # Setup mock data similar to what's in app.py
    # This is a simplified version of the logic in app.py
    
    LAGNA_ORDER = ["మేషం", "వృషభం", "మిథునం", "కర్కాటకం", "సింహం", "కన్య", "తులా", "వృశ్చికం", "ధనస్సు", "మకరం", "కుంభం", "మీనం"]
    GURU_PARTY_PLANETS = ["సూర్యుడు", "భూమి", "కుజుడు", "గురు", "కేతు", "చంద్రుడు"]
    
    # Mock planet positions for a test case
    # Let's say Sun is in Leo (Own House, 4th house from Lagna Taurus)
    # Lagna = "వృషభం" (Taurus - Sani Party)
    lagna = "వృషభం"
    native_party = "శని వర్గము"
    
    # Sun in Leo is 4th house from Taurus (Vrishabha -> Mithuna -> Kataka -> Simha)
    # 1: Vrishabha, 2: Mithuna, 3: Kataka, 4: Simha
    
    planet_positions = [
        {"name": "సూర్యుడు", "lagna": "సింహం", "color": "#FFD700"}
    ]
    
    # Simplified results logic execution
    results_data = []
    for p in planet_positions:
        p_name = p['name']
        p_lagna = p['lagna']
        is_green = any(gp in p_name for gp in GURU_PARTY_PLANETS)
        is_friend = (is_green == (native_party == "గురు వర్గము"))
        results_data.append({"name": p_name, "current_lagna": p_lagna, "is_friend": is_friend})

    lagna_idx = LAGNA_ORDER.index(lagna)
    bhava_report = []
    for i in range(12):
        house_num = i + 1
        house_lagna = LAGNA_ORDER[(lagna_idx + i) % 12]
        occ_planets = [p for p in results_data if p['current_lagna'] == house_lagna]
        
        special_note = ""
        if house_num == 4:
            sun_p = [p for p in occ_planets if "సూర్యుడు" in p['name']]
            if sun_p:
                p = sun_p[0]
                if p['is_friend']:
                    special_note += "సూర్యుడు 4వ లగ్నములో ఉండటమువలన మీకు పై అంతస్థు భవనములు కట్టించు ప్రేరణ చేయును. ఒకవేళ పేదవారైనా ఆ ఇంటిలో నివాసము కల్గునట్లు చేయును. "
                else:
                    special_note += "సూర్యుడు శత్రుగ్రహమై 4వ లగ్నములో ఉన్నందున గృహ సుఖములు లోపించును. ఉన్న పెద్ద ఇల్లును కూడా అమ్మి చిన్న ఇల్లును కొందామనుకొనును. "
        
        if occ_planets or special_note:
            print(f"House {house_num} ({house_lagna}): Planets: {[p['name'] for p in occ_planets]}, Note: {special_note}")

if __name__ == "__main__":
    test_results_logic()
