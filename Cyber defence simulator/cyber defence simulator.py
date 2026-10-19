"""Extention+ task"""


THREATS = {
    "botnet": {
        "impact": "Hijacked machines can be used together for crime.",
        "defence": "Use protection software and apply prompt updates."
    },
    "ddos": {
        "impact": "A service is flooded so real users cannot get through.",
        "defence": "Filter suspicious traffic and keep spare capacity."
    },
    "ransomware": {
        "impact": "Data is encrypted and payment is demanded.",
        "defence": "Keep tested backups, patch systems and avoid unsafe downloads."
    },
    "sql injection": {
        "impact": "Database commands are smuggled through input boxes.",
        "defence": "Validate and sanitise input before using it."
    }
}

def show_advice(threat_name, score, label, urgent):
    threat_name = threat_name.strip().lower()
    if threat_name in THREATS:
        print("\n--- SOC ADVICE REPORT ---")
        print("Threat:", threat_name.title())
        print("Score:", score)
        print("Level:", label)
        print("Urgent:", urgent)
        print("Impact:", THREATS[threat_name]["impact"])
        print("Defence:", THREATS[threat_name]["defence"])
    else:
        print("Threat not found. Try botnet, ddos, ransomware or sql injection.")

def calculate_risk(likelihood, impact):
    # likelihood and impact are scored 1 to 5
    score = float(likelihood * impact)
    if score >= 16:
        label = "High"
        urgent = True
    elif score >= 8:
        label = "Medium"
        urgent = False
    else:
        label = "Low"
        urgent = False
    return score, label, urgent


EVENTS = [
    {"source": "web-form", "threat": "sql injection", "impact": 4},
    {"source": "server", "threat": "ddos", "impact": 5},
    {"source": "laptop-12", "threat": "ransomware", "impact": 5},
    {"source": "pc-04", "threat": "botnet", "impact": 3}
]

def analyse_events(events):
    counts = {}
    for event in events:
        threat = event["threat"]
        counts[threat] = counts.get(threat, 0) + 1
    return counts


summary = analyse_events(EVENTS)
for threat, total in summary.items():
    print(f"{threat.title()}: {total} event(s)") 

running = True
while running:
    print("\nCyber Defence Simulator")
    print("Options:", ", ".join(THREATS.keys()))
    choice = input("Enter a threat to investigate or q to quit: ")
    if choice.lower() == "q":
        running = False
    else:
        likelihoodValid = False
        while likelihoodValid == False:
            likelihood = int(input("Enter the likelihood of the threat (1 to 5, decimals accepted): "))
            if likelihood >= 1 and likelihood <= 5:
                likelihoodValid = True
            else:
                print("Invalid input, please enter numbers between 1 and 5, for example 3.5.")
        impactValid = False
        while impactValid == False:
            impact = int(input("Enter the impact of the threat (1 to 5, decimals accepted): "))
            if impact >= 1 and impact <= 5:
                impactValid = True
            else:
                print("Invalid input, please enter numbers between 1 and 5, for example 3.5.")
        score, label, urgent = calculate_risk(likelihood, impact)
        show_advice(choice, score, label, urgent)
