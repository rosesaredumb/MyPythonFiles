# Define organ systems with receptors and their actions for stimulation and inhibition
organ_systems = {
    "cardiovascular": {
        "a1": {
            "stimulate": ["Vasoconstriction", "Increased blood pressure"],
            "inhibit": ["Vasodilation", "Decreased blood pressure"]
        },
        "a2": {
            "stimulate": ["Decreased sympathetic outflow"],
            "inhibit": ["Increased sympathetic outflow"]
        },
        "b1": {
            "stimulate": ["Increased heart rate", "Increased contractility"],
            "inhibit": ["Decreased heart rate", "Decreased contractility"]
        },
        "m2": {
            "stimulate": ["Decreased heart rate"],
            "inhibit": ["Increased heart rate"]
        }
    },
    "respiratory": {
        "b2": {
            "stimulate": ["Bronchodilation", "Relaxation of airway smooth muscles"],
            "inhibit": ["Bronchoconstriction"]
        },
        "m3": {
            "stimulate": ["Bronchoconstriction"],
            "inhibit": ["Bronchodilation"]
        }
    },
    "muscular": {
        "n1": {
            "stimulate": ["Skeletal muscle contracts"],
            "inhibit": ["Skeletal muscle relaxation"]
        },
        "b2": {
            "stimulate": ["Increased muscle blood flow", "Enhanced glycogenolysis"],
            "inhibit": ["Decreased muscle blood flow", "Reduced energy availability"]
        }
    },
    "ocular": {
        "a1": {
            "stimulate": ["Mydriasis", "Increased outflow of aqueous humor"],
            "inhibit": ["Miosis (pupil constriction)"]
        },
        "a2": {
            "stimulate": ["Decreased aqueous humor production", "Increased uveoscleral outflow"],
            "inhibit": ["Increased aqueous humor production"]
        },
        "m3": {
            "stimulate": ["sphincter pupillae contracts", 
                          "ciliary muscle contracts", 
                          "suspensory ligaments relax and shorten", 
                          "anterior curvature of lens increases", 
                          "vision fixed for near distance", 
                          "vasoconstriction of vessels within ciliary body", 
                          "decreased production of aqueous humour", 
                          "Decreased uveoscleral outflow"],
            "inhibit": ["sphincter pupillae dilates", "Increased uveoscleral outflow"]
        }
    }
}

# Define drugs with their target receptors, organ systems, and whether they stimulate or inhibit
drug_targets = {
    "adrenaline": {
        "cardiovascular": {"a1": "stimulate", "a2": "stimulate", "b1": "stimulate"},
        "respiratory": {"b2": "stimulate"},
        "muscular": {"b2": "stimulate"},
        "ocular": {"a1": "stimulate"}
    },
    "brimonidine": {
        "ocular": {"a2": "stimulate"}
    },
    "atropine": {
        "cardiovascular": {"m2": "inhibit"},
        "respiratory": {"m3": "inhibit"}
    },
    "nicotine": {
        "muscular": {"n1": "stimulate"}
    }
}

# Function to get drug actions grouped by organ system
def get_drug_actions(drug_name):
    if drug_name in drug_targets:
        actions = {}
        for system, receptors in drug_targets[drug_name].items():
            for receptor, action_type in receptors.items():
                effects = organ_systems.get(system, {}).get(receptor, {}).get(action_type, [])
                if effects:
                    if system not in actions:
                        actions[system] = []
                    for effect in effects:
                        actions[system].append(f"{receptor} ({action_type}): {effect}")
        return actions
    else:
        return None

# Input from user
drug_name = input("Enter the drug name: ").strip().lower()

# Get and display actions
actions = get_drug_actions(drug_name)
if actions:
    print(f"Actions caused by {drug_name.capitalize()}:")
    for system, receptor_actions in actions.items():
        print(f"\nOrgan System: {system.capitalize()}")
        for action in receptor_actions:
            print(f"- {action}")
else:
    print("Drug not found.")
