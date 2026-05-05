
import sys
import os

def test_advanced_logic():
    # Setup mock data for advanced scenarios
    
    # 1. 7th House Rahu (Single, effect suppressed by 2+ opposing)
    # Opposing for Rahu: Sun, Moon, Mars, Jupiter
    house_num = 7
    occ_planets_1 = [
        {"name": "రాహు", "is_friend": False},
        {"name": "సూర్యుడు", "is_friend": True},
        {"name": "గురు", "is_friend": True}
    ]
    
    special_note = ""
    rk_p = [p for p in occ_planets_1 if any(x in p['name'] for x in ["రాహు", "కేతు"])]
    if rk_p:
        rk_name = "రాహు"
        opposing_count = 0
        for p in occ_planets_1:
            if rk_name == "రాహు" and any(x in p['name'] for x in ["సూర్యుడు", "చంద్రుడు", "కుజుడు", "గురు"]):
                opposing_count += 1
        
        if opposing_count >= 2:
            special_note += f"{rk_p[0]['name']} 7వ స్థానములో ఉన్నప్పటికీ, వ్యతిరేక గ్రహముల ప్రభావమువలన రెండవ వివాహము లేదా అక్రమ సంబంధముల ఆటంకములు తొలగిపోవును. "
        else:
            special_note += f"{rk_p[0]['name']} 7వ స్థానములో ఉన్నందున రెండవ పెళ్ళికి లేదా అక్రమ సంబంధములకు అవకాశమున్నది. "
    
    print(f"Test 1 (7th Rahu suppressed): {special_note}")

    # 2. Lagna Mars + Venus Discord
    house_num = 1
    occ_planets_2 = [
        {"name": "కుజుడు", "is_friend": False},
        {"name": "శుక్రుడు", "is_friend": False}
    ]
    special_note = ""
    has_mars = any("కుజుడు" in p['name'] for p in occ_planets_2)
    has_venus = any("శుక్రుడు" in p['name'] for p in occ_planets_2)
    if has_mars and has_venus:
        special_note += "కుజుడు మరియు శుక్రుడు ఇద్దరూ లగ్నములో కలిసి ఉన్నందున, భార్యాభర్తల మధ్య అన్యోన్యత లోపించి తరచూ పోట్లాటలు జరిగే సూచనలున్నవి. "
    
    print(f"Test 2 (Lagna Discord): {special_note}")

    # 3. 5th House Moon Intelligence
    house_num = 5
    occ_planets_3 = [{"name": "చంద్రుడు", "is_friend": True}]
    special_note = ""
    if house_num == 5:
        moon_p = [p for p in occ_planets_3 if "చంద్రుడు" in p['name']]
        if moon_p:
            special_note += "చంద్రుడు 5వ స్థానములో ఉన్నందున మీరు గొప్ప మేధాశక్తి మరియు మంచి బుద్ధి గలవారై ఉంటారు. "
    
    print(f"Test 3 (5th Moon Intelligence): {special_note}")

if __name__ == "__main__":
    test_advanced_logic()
