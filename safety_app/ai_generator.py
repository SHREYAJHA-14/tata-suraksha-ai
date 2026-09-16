"""
AI Safety Scenario & Question Generator for Tata Suraksha AI
Supports both Live Google Gemini API and Built-in Offline Tata Steel Knowledge Base
"""

import copy
import json
import random
import requests
from django.conf import settings

OFFLINE_QUESTIONS = [
    # =========================================================================
    # 1. PERSONAL PROTECTIVE EQUIPMENT (PPE - TSS-01)
    # =========================================================================
    {
        "id": "ppe-01",
        "topic_id": "ppe",
        "topic_title": "Personal Protective Equipment (PPE)",
        "difficulty": "beginner",
        "scenario_context": "Blast Furnace Cast House Entry Gate (06:45 AM Handover)",
        "question": "You are about to enter the operational area and notice that your safety helmet has a hairline crack across the crown from a dropped wrench yesterday. What should you do?",
        "options": [
            {"id": "A", "text": "Immediately replace the helmet at the Tool Crib / Safety Store before crossing the gate.", "is_correct": True},
            {"id": "B", "text": "Enter anyway because the shell is mostly intact and will still protect against minor dust.", "is_correct": False},
            {"id": "C", "text": "Enter the floor, complete the handover first, and replace it during your lunch break.", "is_correct": False},
            {"id": "D", "text": "Borrow a cloth cap from a colleague inside the control room until replacement.", "is_correct": False}
        ],
        "explanation": "Any crack, structural deformity, or severe impact nullifies the shock absorption capacity of an industrial hard hat. Compromised PPE must never enter an operational perimeter.",
        "consequence": "A hairline crack drastically lowers load bearing; falling debris as small as a 20mm bolt from an overhead gantry can shatter the helmet and cause fatal cranial trauma.",
        "sop_reference": "Tata Steel Standard TSS-01 §4.3: Damaged PPE Discard Protocol."
    },
    {
        "id": "ppe-02",
        "topic_id": "ppe",
        "topic_title": "Personal Protective Equipment (PPE)",
        "difficulty": "beginner",
        "scenario_context": "Rolling Mill Floor Walkway",
        "question": "Which safety footwear specification is mandatory when walking through Tata Steel production bays and mill operational areas?",
        "options": [
            {"id": "A", "text": "Any leather shoes with rubber soles and closed heels.", "is_correct": False},
            {"id": "B", "text": "Steel-toe or composite safety shoes with puncture-resistant steel midsole complying with IS 15298.", "is_correct": True},
            {"id": "C", "text": "Heavy canvas sports shoes with non-slip tread.", "is_correct": False},
            {"id": "D", "text": "Standard PVC gumboots without protective toe inserts.", "is_correct": False}
        ],
        "explanation": "Only certified safety footwear with 200 Joules steel toe impact resistance and puncture-resistant midsoles are permitted inside Tata Steel operational bays.",
        "consequence": "Unrated shoes fail to protect against falling steel scraps, sharp metal burrs, and heavy rolling equipment pinch points.",
        "sop_reference": "TSS-01 §5.2: Foot Protection Standards."
    },
    {
        "id": "ppe-03",
        "topic_id": "ppe",
        "topic_title": "Personal Protective Equipment (PPE)",
        "difficulty": "beginner",
        "scenario_context": "General Plant Roads & Raw Materials Yard",
        "question": "When is a high-visibility retro-reflective fluorescent vest mandatory to wear inside Tata Steel plant premises?",
        "options": [
            {"id": "A", "text": "Only at night when road streetlights are illuminated.", "is_correct": False},
            {"id": "B", "text": "Mandatory 24/7 at all times when walking outside administrative office buildings.", "is_correct": True},
            {"id": "C", "text": "Only during rain or heavy fog conditions.", "is_correct": False},
            {"id": "D", "text": "Only when working directly alongside locomotive railway tracks.", "is_correct": False}
        ],
        "explanation": "High-visibility clothing is mandatory 24 hours a day across all plant areas to ensure mobile equipment and crane operators have high visual contrast.",
        "consequence": "Heavy trailers and dumpers have severe peripheral blind spots; pedestrians without high-vis vests risk blind spot run-over fatalities.",
        "sop_reference": "TSS-01 §3.4: Mandatory High Visibility Vest Policy."
    },
    {
        "id": "ppe-04",
        "topic_id": "ppe",
        "topic_title": "Personal Protective Equipment (PPE)",
        "difficulty": "intermediate",
        "scenario_context": "Ladle Furnace (LF) Refining Deck during Argon Rinsing",
        "question": "You are monitoring slag sampling near the ladle furnace deck where radiant heat exceeds 600°C. Your aluminized heat-reflective visor has metallic splatter deposits obscuring part of your view. How do you proceed?",
        "options": [
            {"id": "A", "text": "Tilt the visor up slightly to look under it while holding your hand in front of your face.", "is_correct": False},
            {"id": "B", "text": "Step back into the certified heat-shielded control cabin, isolate yourself from thermal line-of-sight, and swap the visor with a clean approved replacement.", "is_correct": True},
            {"id": "C", "text": "Wipe the hot metal splatter off with your heat-resistant glove while remaining on the deck.", "is_correct": False},
            {"id": "D", "text": "Switch to ordinary safety goggles since they are not obstructed.", "is_correct": False}
        ],
        "explanation": "Tilting or removing heat-reflective shields near liquid steel exposes retinal tissues to irreversible thermal radiation and infrared burns, as well as secondary splash hazards.",
        "consequence": "Direct exposure to molten steel infrared radiation causes rapid cornea burning and cataracts; any secondary micro-splash causes instantaneous facial disfigurement.",
        "sop_reference": "TSS-01 §8.1: High Thermal Zone PPE & Face Shield Mandatory Coverage."
    },
    {
        "id": "ppe-05",
        "topic_id": "ppe",
        "topic_title": "Personal Protective Equipment (PPE)",
        "difficulty": "intermediate",
        "scenario_context": "Continuous Pickling Line Acid Storage Bay",
        "question": "Before unbolting an acid metering pump valve where diluted hydrochloric acid (HCl) might drip, what specialized personal protective gear is required?",
        "options": [
            {"id": "A", "text": "Standard cotton boiler suit and cotton work gloves.", "is_correct": False},
            {"id": "B", "text": "Full chemical-resistant PVC/Neoprene suit, chemical goggles, full-face shield, and butyl rubber gauntlet gloves.", "is_correct": True},
            {"id": "C", "text": "Leather apron and welding gloves.", "is_correct": False},
            {"id": "D", "text": "Ordinary rain poncho and latex exam gloves.", "is_correct": False}
        ],
        "explanation": "Chemical transfers require impervious barrier protection (PVC/Neoprene and butyl rubber) to prevent corrosive chemical burns and irreversible ocular damage.",
        "consequence": "Even minor drops of hydrochloric acid splash will burn through cotton clothing within seconds, causing severe chemical skin necrosis.",
        "sop_reference": "TSS-01 §7.2: Chemical Handling Protective Clothing."
    },
    {
        "id": "ppe-06",
        "topic_id": "ppe",
        "topic_title": "Personal Protective Equipment (PPE)",
        "difficulty": "advanced",
        "scenario_context": "Coke Oven Battery Top - Standpipe Cleaning Operation",
        "question": "During standpipe decarb operations at the battery top, an employee complains that their organic vapor half-mask respirator makes breathing difficult in high humidity. They request permission to wear a standard surgical dust mask instead.",
        "options": [
            {"id": "A", "text": "Approve the dust mask temporarily provided they step out every 15 minutes.", "is_correct": False},
            {"id": "B", "text": "Strictly reject the request, halt work, provide a powered air-purifying respirator (PAPR) or rest break in the positive-pressure rest shelter, and maintain zero tolerance for non-rated masks.", "is_correct": True},
            {"id": "C", "text": "Instruct them to double-fold the cloth mask to filter coal tar volatiles.", "is_correct": False},
            {"id": "D", "text": "Allow them to work without a mask if wind is blowing away from the battery.", "is_correct": False}
        ],
        "explanation": "Surgical/dust masks provide zero protection against polycyclic aromatic hydrocarbons (PAHs), benzene, and toxic coke oven emissions. Only certified cartridge respirators or PAPRs are compliant.",
        "consequence": "Acute benzene and coal tar volatile inhalation causes dizziness, respiratory burns, and long-term carcinogenic hematopoietic cell damage.",
        "sop_reference": "Tata Steel Mandatory Life Saving Rule #3: Respiratory Protection in Chemical/Coke Zones & TSS-01 §6.2."
    },
    {
        "id": "ppe-07",
        "topic_id": "ppe",
        "topic_title": "Personal Protective Equipment (PPE)",
        "difficulty": "advanced",
        "scenario_context": "Blast Furnace Stove Burner Pit Area (High CO Hazard Zone)",
        "question": "An emergency repair requires a team of two technicians to enter a classified high-risk zone where Carbon Monoxide (CO) levels fluctuate unpredictably above 100 PPM. What respiratory equipment is mandatory?",
        "options": [
            {"id": "A", "text": "Canister type chemical cartridge mask with particulate pre-filter.", "is_correct": False},
            {"id": "B", "text": "Positive-pressure Self-Contained Breathing Apparatus (SCBA) or airline breathing system with escape cylinder.", "is_correct": True},
            {"id": "C", "text": "Disposable N95 mask with exhalation valve.", "is_correct": False},
            {"id": "D", "text": "Standard half-face dual-filter vapor mask.", "is_correct": False}
        ],
        "explanation": "Cartridge filters CANNOT filter Carbon Monoxide. Atmospheres with CO > 50 PPM or variable concentrations require positive-pressure supplied air (SCBA) to guarantee zero inward leakage.",
        "consequence": "Cartridge masks give a false sense of security; breathing 100+ PPM CO causes unconsciousness within minutes and asphyxiation fatality.",
        "sop_reference": "TSS-01 §6.4 & TSS-02 §4.1: Supplied Air Respiratory Protection in Toxic Atmospheres."
    },

    # =========================================================================
    # 2. FIRE SAFETY & TOXIC GAS (TSS-02)
    # =========================================================================
    {
        "id": "gas-01",
        "topic_id": "fire-gas",
        "topic_title": "Fire Safety & Toxic Gas Hazards",
        "difficulty": "beginner",
        "scenario_context": "Blast Furnace Gas Cleaning Plant (GCP) Pipeline Gallery",
        "question": "While conducting visual inspection near a gas main, your personal multi-gas detector starts beeping with a reading of 35 PPM Carbon Monoxide (CO). What is your immediate action?",
        "options": [
            {"id": "A", "text": "Silence the detector alarm, finish your inspection checklist quickly, and report it later.", "is_correct": False},
            {"id": "B", "text": "Immediately evacuate upwind or perpendicular to the wind direction, warn nearby personnel, and notify Gas Safety Control Room.", "is_correct": True},
            {"id": "C", "text": "Search around the flanges with soap solution to pinpoint the leak yourself.", "is_correct": False},
            {"id": "D", "text": "Wait 5 minutes to see if the reading drops back to zero.", "is_correct": False}
        ],
        "explanation": "Carbon monoxide (CO) is a silent, odorless killer. At 35 PPM (TWA threshold), any escalation can cause unconsciousness within minutes. Immediate upwind evacuation is non-negotiable.",
        "consequence": "CO binds with hemoglobin 200x faster than oxygen, causing rapid confusion, motor collapse, irreversible cerebral hypoxia, and death.",
        "sop_reference": "TSS-02 §3.1: Blast Furnace Gas Safety & Mandatory Evacuation Triggers."
    },
    {
        "id": "gas-02",
        "topic_id": "fire-gas",
        "topic_title": "Fire Safety & Toxic Gas Hazards",
        "difficulty": "beginner",
        "scenario_context": "Hot Strip Mill Finishing Stand Motor Basement",
        "question": "You discover electrical insulation smoking heavily inside an energized 415V control cubicle. What class of fire is this and which extinguisher is appropriate?",
        "options": [
            {"id": "A", "text": "Class A fire; use high-pressure water jet.", "is_correct": False},
            {"id": "B", "text": "Class C/Electrical fire; use Carbon Dioxide (CO2) or Dry Chemical Powder (DCP) extinguisher.", "is_correct": True},
            {"id": "C", "text": "Class B fire; use ordinary foam extinguisher.", "is_correct": False},
            {"id": "D", "text": "Smother it with wet burlap sacks.", "is_correct": False}
        ],
        "explanation": "Water and conductive foam must NEVER be applied to energized electrical gear due to severe electrocution hazard. Non-conductive agents (CO2 or DCP) are mandatory.",
        "consequence": "Spraying water onto energized switchgear conducts lethal current back to the operator through the water stream, causing fatal shock.",
        "sop_reference": "TSS-02 §7.1: Fire Extinguisher Selection Protocol."
    },
    {
        "id": "gas-03",
        "topic_id": "fire-gas",
        "topic_title": "Fire Safety & Toxic Gas Hazards",
        "difficulty": "intermediate",
        "scenario_context": "Continuous Casting Machine (CCM) Hydraulic Power Pack Room",
        "question": "A pressurized hydraulic hose bursts near the ladle turret, spraying atomized oil onto a hot pipe and igniting an intense Class B fire. Which extinguisher must NOT be used here?",
        "options": [
            {"id": "A", "text": "Pressurized Water Extinguisher.", "is_correct": True},
            {"id": "B", "text": "Dry Chemical Powder (DCP) Extinguisher.", "is_correct": False},
            {"id": "C", "text": "CO2 (Carbon Dioxide) Extinguisher.", "is_correct": False},
            {"id": "D", "text": "Aqueous Film-Forming Foam (AFFF) rated for hydrocarbon pools.", "is_correct": False}
        ],
        "explanation": "Water must NEVER be applied to liquid hydrocarbon or pressurized oil fires. Water turns instantaneously to steam, expanding 1700x and spreading the burning oil explosively.",
        "consequence": "Applying water causes a boiling-liquid-expanding steam fireball (slopover) resulting in massive fire engulfment and third-degree burn casualties.",
        "sop_reference": "TSS-02 §7.3: Flammable Liquid Extinguisher Matrix."
    },
    {
        "id": "gas-04",
        "topic_id": "fire-gas",
        "topic_title": "Fire Safety & Toxic Gas Hazards",
        "difficulty": "intermediate",
        "scenario_context": "Blast Furnace Gas Bleeder and Valve Stations",
        "question": "Because Carbon Monoxide (CO) gas is odorless and colorless, which method is the ONLY acceptable way to confirm the atmosphere is safe before entering?",
        "options": [
            {"id": "A", "text": "Sniffing the air for a sulfur or rotten egg smell.", "is_correct": False},
            {"id": "B", "text": "Calibrated multi-gas detector tested and zeroed in fresh air prior to entry.", "is_correct": True},
            {"id": "C", "text": "Observing if birds or insects are flying around the equipment.", "is_correct": False},
            {"id": "D", "text": "Using a cigarette lighter flame to check for burning gas.", "is_correct": False}
        ],
        "explanation": "Pure CO has zero odor, color, or taste. Electronic multi-gas detectors calibrated with certified span gas are the only legal and scientific life-safety detection method.",
        "consequence": "Relying on human senses leads workers into lethal gas pockets where paralysis occurs before any danger is realized.",
        "sop_reference": "TSS-02 §2.4: Properties of Blast Furnace Gas."
    },
    {
        "id": "gas-05",
        "topic_id": "fire-gas",
        "topic_title": "Fire Safety & Toxic Gas Hazards",
        "difficulty": "advanced",
        "scenario_context": "Gas Exhauster House - Confined Pump Room",
        "question": "You see a co-worker lying motionless inside a sub-level valve pit near the Coke Oven Gas booster. The area has no mechanical ventilation. What should be your FIRST action?",
        "options": [
            {"id": "A", "text": "Jump into the pit immediately to drag your colleague out before they stop breathing.", "is_correct": False},
            {"id": "B", "text": "Do not enter. Sound the Emergency Plant Siren, call the Emergency Response Team (ERT) for SCBA rescue, and deploy forced ventilation.", "is_correct": True},
            {"id": "C", "text": "Hold your breath and run down for 30 seconds to lift them up.", "is_correct": False},
            {"id": "D", "text": "Drop a rope down and wait for them to grab it.", "is_correct": False}
        ],
        "explanation": "Over 60% of confined space gas fatalities are would-be rescuers who rush in without breathing apparatus. Entering an unverified lethal atmosphere without SCBA guarantees a second fatality.",
        "consequence": "Entering without an SCBA results in immediate inhalation of lethal CO/H2S concentration, instant loss of consciousness, and double death.",
        "sop_reference": "Tata Steel Life Saving Rule #1: Confined Space Protocol & Emergency Rescue SOP §11."
    },
    {
        "id": "gas-06",
        "topic_id": "fire-gas",
        "topic_title": "Fire Safety & Toxic Gas Hazards",
        "difficulty": "advanced",
        "scenario_context": "Gas Holder Storage Facility (LD Converter Gas)",
        "question": "A flange on a 2000mm gas main develops a high-pressure blowing leak with CO concentration exceeding 1500 PPM. Wind is carrying the plume toward the central plant canteen. As Incident Commander, what is your first escalation?",
        "options": [
            {"id": "A", "text": "Send two technicians with wrenches to tighten the flange bolts under pressure.", "is_correct": False},
            {"id": "B", "text": "Activate Tier 3 Plant Emergency Siren, order immediate cross-wind evacuation of the canteen zone, establish a 300m exclusion perimeter, and isolate the gas main from remote valves.", "is_correct": True},
            {"id": "C", "text": "Wait for the gas pressure to equalize before taking action.", "is_correct": False},
            {"id": "D", "text": "Use canvas tarpaulins to deflect the gas plume upwards.", "is_correct": False}
        ],
        "explanation": "At 1500 PPM CO, a single breath causes collapse. Massive leaks threatening populated areas require immediate disaster protocol execution, sirens, and remote valve shutdown.",
        "consequence": "Tightening bolts under 1500 PPM gas causes sparks and gas explosion; delayed evacuation of the canteen guarantees mass casualties.",
        "sop_reference": "TSS-02 §9.0: On-Site Emergency Disaster Plan & Escalation."
    },

    # =========================================================================
    # 3. ELECTRICAL SAFETY & LOTO (TSS-03)
    # =========================================================================
    {
        "id": "loto-01",
        "topic_id": "loto",
        "topic_title": "Electrical Safety & LOTO (LOTOTO)",
        "difficulty": "beginner",
        "scenario_context": "Bar Mill Runout Table Motor Maintenance",
        "question": "A drive motor needs routine belt realignment. The technician switches off the local electrical push button on the panel and begins removing the guard. Is this work compliant?",
        "options": [
            {"id": "A", "text": "Yes, because the local emergency stop / push button has de-energized the motor.", "is_correct": False},
            {"id": "B", "text": "No. Local push buttons only stop control circuits. Full LOTOTO (Lockout, Tagout, Try-out) at the MCC breaker with personal padlocks and zero-energy test is mandatory.", "is_correct": True},
            {"id": "C", "text": "Yes, provided a red warning tape is tied across the motor.", "is_correct": False},
            {"id": "D", "text": "Yes, if the shift supervisor gives verbal permission.", "is_correct": False}
        ],
        "explanation": "Control circuit stops (push buttons) can fail, short-circuit, or be overridden by PLC automated sequences. Mechanical intervention requires physical breaker padlocking (LOTOTO).",
        "consequence": "An automated PLC reboot or remote start can engage the drive without warning, amputating limbs inside the belt drive.",
        "sop_reference": "Tata Steel Standard TSS-03 (LOTOTO) §2.1: Prohibition of Control Circuit Isolation."
    },
    {
        "id": "loto-02",
        "topic_id": "loto",
        "topic_title": "Electrical Safety & LOTO (LOTOTO)",
        "difficulty": "beginner",
        "scenario_context": "Central Maintenance Shop",
        "question": "Under Tata Steel LOTOTO policy, who is authorized to remove your personal safety padlock from an isolation lockbox?",
        "options": [
            {"id": "A", "text": "Any shift supervisor who needs the machine running urgently.", "is_correct": False},
            {"id": "B", "text": "Strictly YOU (the lock owner) after verifying yourself and your team are clear and work is complete.", "is_correct": True},
            {"id": "C", "text": "Any co-worker who has finished their portion of the shift.", "is_correct": False},
            {"id": "D", "text": "The security guard using a master bolt cutter.", "is_correct": False}
        ],
        "explanation": "One person, one lock, one key. Only the worker who applied the padlock has the legal authority to remove it. Emergency lock removal requires a rigorous multi-tier sign-off protocol.",
        "consequence": "Removing another worker's lock while they are inside machinery causes catastrophic crushing and electrocution fatalities.",
        "sop_reference": "TSS-03 §4.1: Individual Custody of Isolation Padlocks."
    },
    {
        "id": "loto-03",
        "topic_id": "loto",
        "topic_title": "Electrical Safety & LOTO (LOTOTO)",
        "difficulty": "intermediate",
        "scenario_context": "6.6kV Switchgear Substation Feeder Bay",
        "question": "Before issuing a Permit to Work (PTW) for high-voltage breaker maintenance, which sequence must the authorized electrical engineer execute?",
        "options": [
            {"id": "A", "text": "Turn off switch -> Apply tag -> Allow maintenance crew to start.", "is_correct": False},
            {"id": "B", "text": "De-energize -> Rack out breaker -> Lockout/Tagout -> Prove dead with rated HV detector -> Discharge residual capacitive energy -> Apply portable earth grounds.", "is_correct": True},
            {"id": "C", "text": "Turn off switch -> Check voltage with multimeter -> Start work.", "is_correct": False},
            {"id": "D", "text": "Disconnect power cable and leave open in air without earthing.", "is_correct": False}
        ],
        "explanation": "High-voltage systems store dangerous capacitive charges even when isolated. Proving dead with a calibrated HV tester and applying certified grounding leads is legally mandatory.",
        "consequence": "Stored capacitance or accidental back-feed generates an arc flash explosion with plasma temperatures exceeding 19,000°C, causing fatal blast trauma.",
        "sop_reference": "TSS-03 §5.4: High Voltage Isolation and Earth Grounding Protocol."
    },
    {
        "id": "loto-04",
        "topic_id": "loto",
        "topic_title": "Electrical Safety & LOTO (LOTOTO)",
        "difficulty": "intermediate",
        "scenario_context": "Hot Strip Mill Hydraulic Descaler Pump Room",
        "question": "You have isolated the 415V electrical power to a high-pressure water descaling pump and locked the breaker. What OTHER energy source must be verified and isolated under LOTOTO before opening the valve body?",
        "options": [
            {"id": "A", "text": "Stored hydraulic accumulator pressure and high-pressure fluid lines must be bled to zero, locked with mechanical valves, and verified depressurized.", "is_correct": True},
            {"id": "B", "text": "No other energy; electrical isolation is legally sufficient.", "is_correct": False},
            {"id": "C", "text": "Only the computer SCADA terminal needs to be logged out.", "is_correct": False},
            {"id": "D", "text": "Wiping the exterior with cleaning solvent.", "is_correct": False}
        ],
        "explanation": "LOTOTO covers ALL hazardous energy: electrical, hydraulic, pneumatic, gravitational, thermal, and chemical. Trapped hydraulic pressure must be depressurized and mechanically isolated.",
        "consequence": "Trapped fluid at 200 bar can burst through valve bolts during disassembly, causing high-pressure fluid injection injury which destroys muscle tissue and requires amputation.",
        "sop_reference": "TSS-03 §3.2: Multi-Energy Source Isolation (Zero Energy State)."
    },
    {
        "id": "loto-05",
        "topic_id": "loto",
        "topic_title": "Electrical Safety & LOTO (LOTOTO)",
        "difficulty": "advanced",
        "scenario_context": "33kV Main Step-Down Substation Busbar Coupler",
        "question": "During high-voltage switchgear testing, an engineer needs to enter the arc flash boundary. The calculated incident energy is 38 cal/cm². What arc-rated PPE is mandatory?",
        "options": [
            {"id": "A", "text": "Standard cotton overalls and safety goggles.", "is_correct": False},
            {"id": "B", "text": "40 cal/cm² arc flash suit with hood, arc-rated face shield, hearing protection, and voltage-rated insulated gloves with leather protectors.", "is_correct": True},
            {"id": "C", "text": "Welding leather jacket and clear face shield.", "is_correct": False},
            {"id": "D", "text": "Rubber gumboots and insulated screwdriver.", "is_correct": False}
        ],
        "explanation": "Arc flash PPE must have an Arc Thermal Performance Value (ATPV) exceeding the calculated incident energy level (38 cal/cm² requires Category 4 / 40 cal/cm² minimum protection).",
        "consequence": "An arc flash fault vaporizes copper instantaneously, creating pressure shockwaves and 19,000°C plasma that instantly incinerates non-rated clothing into flesh.",
        "sop_reference": "TSS-03 §8.2: Arc Flash Hazard Analysis and PPE Category 4 Compliance."
    },

    # =========================================================================
    # 4. WORKING AT HEIGHTS & CONFINED SPACES (TSS-04)
    # =========================================================================
    {
        "id": "ht-01",
        "topic_id": "heights",
        "topic_title": "Working at Heights & Confined Spaces",
        "difficulty": "beginner",
        "scenario_context": "BF Highline Conveyor Gantry (Elevated Walkway at 18 Meters)",
        "question": "You need to inspect an idler roller along the elevated gantry. The handrail has a removable section that was taken off for crane access. What must you do before approaching the edge?",
        "options": [
            {"id": "A", "text": "Wear a certified full-body harness, anchor to an approved lifeline or 15kN rated overhead anchor point with 100% tie-off, and erect a physical barrier.", "is_correct": True},
            {"id": "B", "text": "Walk carefully, keep your eyes on the edge, and don’t look down.", "is_correct": False},
            {"id": "C", "text": "Hold onto your co-worker’s hand as an anchor point.", "is_correct": False},
            {"id": "D", "text": "Put on a waist belt and clip to the toe-board.", "is_correct": False}
        ],
        "explanation": "Any open edge over 1.8 meters requires mandatory fall protection. Body waist belts are banned in Tata Steel; only double-lanyard full-body harnesses anchored to certified fall arrest points are permitted.",
        "consequence": "A slip without anchored fall arrest results in an 18-meter free fall onto concrete/steel structures, resulting in instantaneous fatality.",
        "sop_reference": "Tata Steel Life Saving Rule #2 & TSS-04 §1.2: Mandatory Fall Arrest Systems at Heights."
    },
    {
        "id": "ht-02",
        "topic_id": "heights",
        "topic_title": "Working at Heights & Confined Spaces",
        "difficulty": "beginner",
        "scenario_context": "Structural Maintenance Work at 6 Meters",
        "question": "Which scaffolding tag status permits workers to climb and work on tubular scaffolding?",
        "options": [
            {"id": "A", "text": "Red Tag (Danger - Scaffold Unsafe / Incomplete).", "is_correct": False},
            {"id": "B", "text": "Green Tag (Inspected and Certified Safe for Use within the last 7 days).", "is_correct": True},
            {"id": "C", "text": "Yellow Tag (Use with Caution without harness).", "is_correct": False},
            {"id": "D", "text": "No tag is needed if the scaffolding looks sturdy.", "is_correct": False}
        ],
        "explanation": "Only scaffolding bearing an active GREEN TAG inspected and signed by a certified scaffolding inspector within 7 days is legally cleared for work.",
        "consequence": "Climbing red-tagged or uninspected scaffolding leads to structural collapse, missing planks, and unarrested fall fatalities.",
        "sop_reference": "TSS-04 §4.1: Scaffolding Inspection and Green Tagging System."
    },
    {
        "id": "ht-03",
        "topic_id": "heights",
        "topic_title": "Working at Heights & Confined Spaces",
        "difficulty": "intermediate",
        "scenario_context": "Scale Pit Basement - Confined Space Entry",
        "question": "A maintenance technician needs to enter a 4-meter deep underground scale pit. The oxygen level reading is 18.2%. The shift supervisor says: 'It is only a 10-minute valve greasing job, go ahead quickly.' What must you do?",
        "options": [
            {"id": "A", "text": "Follow the supervisor’s order and finish in under 5 minutes.", "is_correct": False},
            {"id": "B", "text": "Exercise your STOP WORK AUTHORITY. An oxygen level below 19.5% is an asphyxiation hazard; entry is strictly prohibited until mechanical ventilation restores O2 to 19.5% - 23.5%.", "is_correct": True},
            {"id": "C", "text": "Wear a cloth dust mask and enter.", "is_correct": False},
            {"id": "D", "text": "Take a deep breath and run down to grease the valve.", "is_correct": False}
        ],
        "explanation": "Tata Steel empowers EVERY employee with Stop Work Authority. Safe oxygen concentration is strictly 19.5% to 23.5%. Below 19.5%, oxygen deficiency rapidly impairs judgement and causes brain death.",
        "consequence": "At 18% oxygen, cognitive impairment occurs within 60 seconds. At 14%, rapid unconsciousness and irreversible asphyxiation occur before the worker can climb the ladder.",
        "sop_reference": "TSS-04 §6.4: Confined Space Atmospheric Criteria & Employee Stop Work Authority."
    },
    {
        "id": "ht-04",
        "topic_id": "heights",
        "topic_title": "Working at Heights & Confined Spaces",
        "difficulty": "intermediate",
        "scenario_context": "Overhead Crane Runway Beam at 24 Meters",
        "question": "While transferring from an aerial boom lift basket onto an overhead crane runway beam, how must the technician transition their double-lanyard shock-absorbing harness?",
        "options": [
            {"id": "A", "text": "Maintain 100% tie-off: connect the second hook to the runway certified anchor line BEFORE disconnecting the first hook from the boom lift anchor.", "is_correct": True},
            {"id": "B", "text": "Unclip both hooks together and quickly latch onto the runway static line in one motion.", "is_correct": False},
            {"id": "C", "text": "Hold the handrail firmly while clipping both hooks.", "is_correct": False},
            {"id": "D", "text": "Disconnect harness because boom lift transitions are considered low risk.", "is_correct": False}
        ],
        "explanation": "100% tie-off means that at NO point in time is the worker ever unattached from a certified fall arrest point. One hook must always be anchored before moving the other.",
        "consequence": "A sudden slip or structural gust during a dual-unhook moment leaves zero fall arrest, causing an unarrested fall from 24 meters.",
        "sop_reference": "TSS-04 §3.1: 100% Continuous Fall Arrest Transition Protocol."
    },
    {
        "id": "ht-05",
        "topic_id": "heights",
        "topic_title": "Working at Heights & Confined Spaces",
        "difficulty": "advanced",
        "scenario_context": "Argon Rinsing Tank Vessel Maintenance (Inert Gas Hazard)",
        "question": "A steel degasser vessel has been purged with Argon gas. The oxygen reading inside the top flange is 20.8%, but the vessel is 8 meters deep with no lower openings. What critical confined space test is mandatory?",
        "options": [
            {"id": "A", "text": "No further test needed; 20.8% O2 at the top confirms the entire vessel is safe.", "is_correct": False},
            {"id": "B", "text": "Test atmospheric stratified layers at top, middle, and bottom (Argon is heavier than air and settles at the bottom, creating a lethal zero-oxygen pocket).", "is_correct": True},
            {"id": "C", "text": "Drop a lit match to the bottom to verify oxygen presence.", "is_correct": False},
            {"id": "D", "text": "Enter with a standard rope tied to your waist.", "is_correct": False}
        ],
        "explanation": "Argon (molecular weight 40) is heavier than air (molecular weight 29) and displaces oxygen at the bottom of vessels. Stratified testing at multiple elevations is mandatory under confined space standards.",
        "consequence": "Stepping into an invisible bottom Argon pocket causes instantaneous anoxia, loss of consciousness within 1 breath, and fatal brain damage in under 3 minutes.",
        "sop_reference": "TSS-04 §7.3: Inert Gas Asphyxiation and Stratified Atmospheric Sampling."
    },

    # =========================================================================
    # 5. MOLTEN METAL & CRANE OPERATIONS (TSS-05)
    # =========================================================================
    {
        "id": "mm-01",
        "topic_id": "molten-metal",
        "topic_title": "Molten Metal & Hot Heavy Cranes",
        "difficulty": "beginner",
        "scenario_context": "LD Converter Slag Pit & Transfer Track",
        "question": "You notice pooled rainwater inside a slag dump pit where red-hot slag (1500°C) is scheduled to be tipped in 10 minutes. What action is mandatory?",
        "options": [
            {"id": "A", "text": "Allow the slag pour; the intense heat will boil the water off harmlessly.", "is_correct": False},
            {"id": "B", "text": "Immediately halt slag pouring, clear the area, and pump/dry the pit completely. Hot slag must NEVER contact water or moisture.", "is_correct": True},
            {"id": "C", "text": "Throw sand on top of the water puddle and proceed with tipping.", "is_correct": False},
            {"id": "D", "text": "Stand behind a column and watch the tipping.", "is_correct": False}
        ],
        "explanation": "When molten slag or steel contacts trapped liquid water, water instantaneously flashes to steam with a 1,700:1 volumetric expansion, creating a devastating physical explosion.",
        "consequence": "Water entrapment underneath liquid slag creates a massive explosion that ejects tons of 1500°C molten shrapnel across 100 meters, destroying buildings and killing personnel.",
        "sop_reference": "TSS-05 §4.2: Prevention of Steam Explosions & Slag Pit Moisture Clearance."
    },
    {
        "id": "mm-02",
        "topic_id": "molten-metal",
        "topic_title": "Molten Metal & Hot Heavy Cranes",
        "difficulty": "beginner",
        "scenario_context": "Torpedo Ladle Car Rail Tracks",
        "question": "A 250-tonne torpedo ladle filled with molten iron is being shunted by an industrial locomotive into the desulfurization bay. What is the mandatory clearance rule?",
        "options": [
            {"id": "A", "text": "Pedestrians may walk along the track edge if wearing helmets.", "is_correct": False},
            {"id": "B", "text": "Clear the entire Red Exclusion Zone (minimum 15-meter clearance); no pedestrian or unauthorized vehicle entry during hot metal transit.", "is_correct": True},
            {"id": "C", "text": "Stand beside the ladle track and guide the driver with hand gestures.", "is_correct": False},
            {"id": "D", "text": "Crossing the track in front of the moving torpedo car if moving under 5 km/h.", "is_correct": False}
        ],
        "explanation": "Hot metal transit routes are designated Red Exclusion Zones. Splash, radiant heat, rail derailment, or metal sloshing present extreme catastrophic hazards.",
        "consequence": "Derailment or sudden slosh can cause 250 tonnes of liquid iron (1400°C) to spill over nearby pathways, vaporizing anything within 15 meters.",
        "sop_reference": "TSS-05 §2.3: Torpedo Ladle Transit & Red Zone Barricading."
    },
    {
        "id": "mm-03",
        "topic_id": "molten-metal",
        "topic_title": "Molten Metal & Hot Heavy Cranes",
        "difficulty": "intermediate",
        "scenario_context": "Teeming Crane Bay (300-tonne Ladle Crane)",
        "question": "During daily pre-shift inspection of a 300-tonne molten metal ladle crane, the rigger identifies 4 broken outer wires in one rope lay of the main hoist wire rope. What is the required decision?",
        "options": [
            {"id": "A", "text": "Continue using it for light ladles only and replace it over the weekend.", "is_correct": False},
            {"id": "B", "text": "Immediately ground the crane, apply LOTOTO, and replace the wire rope before any ladle lift.", "is_correct": True},
            {"id": "C", "text": "Lubricate the rope with heavy grease to minimize further strand breakage.", "is_correct": False},
            {"id": "D", "text": "Reduce crane hoisting speed by 50% and operate with caution.", "is_correct": False}
        ],
        "explanation": "For cranes carrying molten metal (hazardous liquid handling), wire rope discard criteria are twice as strict as general cranes. Broken wires in a single strand require immediate grounding.",
        "consequence": "Catastrophic wire rope failure while hoisting a 300-tonne liquid steel ladle results in ladle drop, total furnace floor destruction, and multi-fatality blast.",
        "sop_reference": "TSS-05 §6.1 & IS 3938: Crane Wire Rope Discard Criteria for Molten Metal Handling."
    },
    {
        "id": "mm-04",
        "topic_id": "molten-metal",
        "topic_title": "Molten Metal & Hot Heavy Cranes",
        "difficulty": "advanced",
        "scenario_context": "Continuous Casting Turret & Mold Deck",
        "question": "While teeming molten steel from a 150-tonne ladle into the tundish, the hydraulic slide gate mechanism jams in the 100% open position and cannot be closed from the local control desk. Liquid steel is overflowing the tundish. What is the immediate life-safety action?",
        "options": [
            {"id": "A", "text": "Climb onto the tundish car with a manual sledgehammer to force the slide gate shut.", "is_correct": False},
            {"id": "B", "text": "Sound the Turret Emergency Alarm, immediately evacuate all casting floor personnel from the splash zone, and activate the emergency ladle dump chute / emergency ladle crane hoist from the safety pulpit.", "is_correct": True},
            {"id": "C", "text": "Spray water nozzles directly onto the overflowing steel to solidify it.", "is_correct": False},
            {"id": "D", "text": "Call the mechanical maintenance department and wait on the floor.", "is_correct": False}
        ],
        "explanation": "Uncontrolled molten steel overflow causes immediate tundish breakout and floor destruction. Personnel must evacuate immediately; manual intervention near molten runaway is prohibited.",
        "consequence": "Approaching a runaway liquid steel stream leads to instant engulfment in 1550°C steel and thermal radiation shockwave.",
        "sop_reference": "TSS-05 §7.2: Molten Steel Runaway Emergency Response."
    },

    # =========================================================================
    # 6. EMERGENCY PROTOCOLS & FIRST AID (TSS-06)
    # =========================================================================
    {
        "id": "em-01",
        "topic_id": "emergency",
        "topic_title": "Emergency Response & Golden Hour Protocols",
        "difficulty": "beginner",
        "scenario_context": "Cold Rolling Mill Acid Pickling Line (Hydrochloric Acid)",
        "question": "During maintenance on an acid metering valve, a seal blows and concentrated hydrochloric acid (HCl) splashes across a worker’s face and chest. What is the critical first action within the first 10 seconds?",
        "options": [
            {"id": "A", "text": "Immediately rush to the Emergency Eyewash / Deluge Safety Shower, activate flow, and flush eyes and skin continuously with copious water for at least 15–20 minutes while stripping contaminated clothing.", "is_correct": True},
            {"id": "B", "text": "Find neutralizer powder or baking soda paste and smear it onto the burn.", "is_correct": False},
            {"id": "C", "text": "Wrap the employee in dry blankets and wait for the ambulance.", "is_correct": False},
            {"id": "D", "text": "Apply burn ointment and gently wipe with paper towels.", "is_correct": False}
        ],
        "explanation": "Water flushing in the first 10 seconds dilutes and washes away corrosive acid. Neutralizing chemicals generate exothermic heat, worsening burns. Continuous 15-20 min water flushing saves vision and skin.",
        "consequence": "Acid penetration into cornea and dermis causes permanent blindness and third-degree chemical necrosis within 30 seconds if not flushed with water immediately.",
        "sop_reference": "TSS-06 §5.1: Chemical Acid Burn Response & Emergency Deluge Shower Protocol."
    },
    {
        "id": "em-02",
        "topic_id": "emergency",
        "topic_title": "Emergency Response & Golden Hour Protocols",
        "difficulty": "beginner",
        "scenario_context": "Plant Central Control Room",
        "question": "A Continuous Wailing Siren (Tone 1 - 3 minutes duration) sounds across the Jamshedpur Works. What does this siren code indicate according to Tata Steel Emergency Protocol?",
        "options": [
            {"id": "A", "text": "Shift changeover announcement.", "is_correct": False},
            {"id": "B", "text": "Major Plant Emergency (Toxic Gas Escape / Explosion). All non-essential personnel must immediately check wind socks and evacuate cross-wind to designated Assembly Points.", "is_correct": True},
            {"id": "C", "text": "All Clear signal - Return to normal operations.", "is_correct": False},
            {"id": "D", "text": "Routine fire alarm test in the administrative building.", "is_correct": False}
        ],
        "explanation": "Continuous wailing tone indicates Tier 2/3 Plant Emergency. Immediate evacuation across wind directions to assigned assembly muster stations is mandatory.",
        "consequence": "Ignoring siren codes results in inhalation of advancing toxic gas plumes or being trapped in industrial blast zones.",
        "sop_reference": "TSS-06 §1.4: Plant Emergency Siren Codes & Muster Station Protocols."
    },
    {
        "id": "em-03",
        "topic_id": "emergency",
        "topic_title": "Emergency Response & Golden Hour Protocols",
        "difficulty": "intermediate",
        "scenario_context": "Blast Furnace Cast House Floor (Summer Shift - Ambient Temp 48°C)",
        "question": "A cast house worker collapses near the iron runner, exhibiting hot dry skin, confusion, rapid shallow breathing, and cessation of sweating. What life-threatening condition is this and what is the emergency treatment?",
        "options": [
            {"id": "A", "text": "Heat Exhaustion; give them hot tea and encourage them to keep working.", "is_correct": False},
            {"id": "B", "text": "Heat Stroke (Medical Emergency). Move immediately to air-conditioned medical room, strip outer flame-retardant clothes, apply ice packs to neck/armpits/groin, douse with cool water, and call emergency ambulance immediately.", "is_correct": True},
            {"id": "C", "text": "Epileptic seizure; place a wooden spoon in their mouth.", "is_correct": False},
            {"id": "D", "text": "Minor dizziness; leave them to rest alone on the floor.", "is_correct": False}
        ],
        "explanation": "Heat Stroke occurs when body temperature regulation fails (>40.5°C). The absence of sweat and mental confusion indicates critical organ failure risk requiring aggressive rapid cooling.",
        "consequence": "Delayed cooling during heat stroke leads to rhabdomyolysis, irreversible neurological brain damage, and cardiac arrest.",
        "sop_reference": "TSS-06 §6.2: Heat Stress Management and Heat Stroke Protocol."
    },
    {
        "id": "em-04",
        "topic_id": "emergency",
        "topic_title": "Emergency Response & Golden Hour Protocols",
        "difficulty": "advanced",
        "scenario_context": "Motor Control Center (MCC) Room",
        "question": "An electrical technician touches an exposed live busbar, collapses unconscious, has no pulse and is not breathing. The power has been safely isolated. What is the immediate life-saving protocol?",
        "options": [
            {"id": "A", "text": "Give them water to drink and wait for the company doctor.", "is_correct": False},
            {"id": "B", "text": "Immediately start Cardiopulmonary Resuscitation (CPR) at 30 chest compressions to 2 breaths, shout for an Automated External Defibrillator (AED), and call Plant Emergency Medical Helpline.", "is_correct": True},
            {"id": "C", "text": "Rub the soles of their feet and turn them on their side.", "is_correct": False},
            {"id": "D", "text": "Search their pockets for medical history cards before taking action.", "is_correct": False}
        ],
        "explanation": "In sudden cardiac arrest from electric shock, the Golden Window is under 4 minutes. High-quality chest compressions and early defibrillation double survival chances.",
        "consequence": "Every minute of delay in CPR reduces survival chance by 10%; irreversible brain hypoxia begins within 4 minutes.",
        "sop_reference": "TSS-06 §4.0: Golden Hour Basic Life Support (BLS) Standards."
    }
]


def shuffle_question_options(question):
    """
    Shuffles the options of a question randomly and reassigns IDs ('A', 'B', 'C', 'D').
    Guarantees that the correct answer is randomly distributed across A, B, C, and D.
    """
    q = copy.deepcopy(question)
    options = q.get("options", [])
    if not options:
        return q

    # Randomly shuffle options order
    random.shuffle(options)

    # Re-assign standard option letters A, B, C, D
    labels = ["A", "B", "C", "D"]
    for i, opt in enumerate(options):
        opt["id"] = labels[i] if i < len(labels) else str(i + 1)

    q["options"] = options
    return q


def generate_questions(topic_id="all", department_name="Plant Operations", difficulty="intermediate", count=5, is_remediation=False, weak_topic_ids=None, api_key=None):
    """
    Generates assessment questions.
    Uses Gemini API if an API key is provided; otherwise uses built-in Tata Steel knowledge base.
    Guarantees that:
    1. Exactly `count` questions are returned (e.g. 3, 5, or 10).
    2. Selected difficulty tier is prioritized.
    3. Correct answer is randomized across A, B, C, D.
    """
    if weak_topic_ids is None:
        weak_topic_ids = []

    # Check for live API Key
    key = api_key or getattr(settings, "GEMINI_API_KEY", None)

    questions = None
    if key:
        try:
            questions = call_gemini_api(
                api_key=key,
                topic_id=topic_id,
                department_name=department_name,
                difficulty=difficulty,
                count=count,
                is_remediation=is_remediation,
                weak_topic_ids=weak_topic_ids
            )
        except Exception as e:
            print(f"[Tata Suraksha AI] Gemini API call error: {e}. Falling back to offline knowledge base.")

    # If Gemini returns fewer questions than requested or failed, use offline engine
    if not questions or len(questions) < count:
        questions = get_offline_questions(topic_id=topic_id, difficulty=difficulty, count=count, is_remediation=is_remediation, weak_topic_ids=weak_topic_ids)

    # Randomly distribute the correct answer across A, B, C, D for every single question
    randomized_questions = [shuffle_question_options(q) for q in questions]
    return randomized_questions[:count]


def get_offline_questions(topic_id="all", difficulty="all", count=5, is_remediation=False, weak_topic_ids=None):
    """
    Filters questions respecting both topic and difficulty tier, and guarantees returning EXACTLY `count` questions.
    """
    if weak_topic_ids is None:
        weak_topic_ids = []

    # 1. Base topic pool
    if is_remediation and weak_topic_ids:
        topic_pool = [q for q in OFFLINE_QUESTIONS if q.get("topic_id") in weak_topic_ids]
        if not topic_pool:
            topic_pool = list(OFFLINE_QUESTIONS)
    elif topic_id and topic_id != "all":
        topic_pool = [q for q in OFFLINE_QUESTIONS if q.get("topic_id") == topic_id]
        if not topic_pool:
            topic_pool = list(OFFLINE_QUESTIONS)
    else:
        topic_pool = list(OFFLINE_QUESTIONS)

    # 2. Difficulty prioritization
    if difficulty and difficulty != "all":
        diff_matching = [q for q in topic_pool if q.get("difficulty") == difficulty]
        other_diff = [q for q in topic_pool if q.get("difficulty") != difficulty]
        # Put matching difficulty first
        pool = diff_matching + other_diff
    else:
        pool = list(topic_pool)

    # 3. If pool is smaller than count, backfill from other topics (prioritizing same difficulty)
    if len(pool) < count:
        remaining_needed = count - len(pool)
        extra_questions = [q for q in OFFLINE_QUESTIONS if q not in pool]
        if difficulty and difficulty != "all":
            extra_same_diff = [q for q in extra_questions if q.get("difficulty") == difficulty]
            extra_other_diff = [q for q in extra_questions if q.get("difficulty") != difficulty]
            pool.extend(extra_same_diff)
            pool.extend(extra_other_diff)
        else:
            pool.extend(extra_questions)

    # 4. Select exactly `count` questions
    if len(pool) >= count:
        # If we have matching difficulty, keep them in the selection
        if difficulty and difficulty != "all":
            matching = [q for q in pool if q.get("difficulty") == difficulty]
            non_matching = [q for q in pool if q.get("difficulty") != difficulty]
            if len(matching) >= count:
                selected = random.sample(matching, count)
            else:
                selected = matching + random.sample(non_matching, count - len(matching))
        else:
            selected = random.sample(pool, count)
    else:
        # In the unlikely event pool is smaller, repeat with variation
        selected = [random.choice(pool) for _ in range(count)]

    # Randomize the question display order
    random.shuffle(selected)
    return selected


def call_gemini_api(api_key, topic_id, department_name, difficulty, count, is_remediation, weak_topic_ids):
    """
    Calls Google Gemini REST API using Python requests library.
    """
    system_prompt = (
        "You are Tata Suraksha AI, Senior Industrial Safety Officer at Tata Steel Works. "
        "Generate realistic shop-floor safety assessment questions and dilemmas for plant employees. "
        f"You MUST generate EXACTLY {count} questions at the '{difficulty}' level. "
        "Randomly distribute the correct answer among options A, B, C, and D. Do not put the correct answer on the same option every time. "
        "Output ONLY a raw JSON array matching this exact schema: "
        '[{"id": "q1", "topic_id": "ppe", "topic_title": "...", "difficulty": "' + str(difficulty) + '", '
        '"scenario_context": "Exact plant setting", "question": "Clear dilemma", '
        '"options": [{"id": "A", "text": "...", "is_correct": false}, {"id": "B", "text": "...", "is_correct": true}, {"id": "C", "text": "...", "is_correct": false}, {"id": "D", "text": "...", "is_correct": false}], '
        '"explanation": "Why correct choice is safe", "consequence": "Severe catastrophe of wrong choice", "sop_reference": "TSS-01 §4.2"}]'
    )

    if is_remediation:
        task_prompt = f"Generate EXACTLY {count} {difficulty} level targeted remediation questions for an employee in '{department_name}' who failed past safety questions in topics: {weak_topic_ids}."
    else:
        task_prompt = f"Generate EXACTLY {count} {difficulty} level questions for '{department_name}' department regarding topic '{topic_id}'."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": f"{system_prompt}\n\nTask:\n{task_prompt}"}]}
        ],
        "generationConfig": {
            "temperature": 0.5,
            "responseMimeType": "application/json"
        }
    }

    resp = requests.post(url, json=payload, timeout=12)
    resp.raise_for_status()
    data = resp.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"].strip()

    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]

    parsed = json.loads(text.strip())
    if isinstance(parsed, list) and len(parsed) > 0:
        return parsed

    raise ValueError("Invalid format received from Gemini API")
