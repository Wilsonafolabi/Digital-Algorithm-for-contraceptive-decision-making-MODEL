class SafetyEngine:
    def check(self, profile: dict) -> dict:
        age = profile.get("age", 0)
        smoking = profile.get("smoking_status", "non-smoker")
        breastfeeding = profile.get("breastfeeding", False)
        hypertension = profile.get("hypertension", False)
        clots = profile.get("history_of_clots", False)
        migraines = profile.get("migraines", "none")
        diabetes = profile.get("diabetes", False)
        sti_needed = profile.get("sti_protection_needed", False)

        flags = []
        risk = "none"

        # Age & Minors
        if age < 18:
            return {"flagged": True, "risk_category": "critical", 
                    "message": "Age < 18. Mandatory counseling and guardian consent required."}
        
        # Smoking + Age
        if smoking == "smoker" and age > 35:
            flags.append("Smoker >35: Combined hormonal methods contraindicated (WHO MEC 4).")
            risk = "moderate"
            
        # Hypertension
        if hypertension:
            flags.append("Hypertension: Avoid combined methods. Progestin-only or Copper IUD preferred (MEC 3/4).")
            risk = "moderate"
            
        # Blood Clots
        if clots:
            return {"flagged": True, "risk_category": "critical", 
                    "message": "History of blood clots. Estrogen strictly contraindicated (MEC 4). Use progestin-only or non-hormonal methods."}
            
        # Migraines
        if migraines == "with_aura":
            return {"flagged": True, "risk_category": "critical", 
                    "message": "Migraine with aura. High stroke risk with estrogen (MEC 4). Use non-estrogen methods only."}
            
        # Breastfeeding
        if breastfeeding:
            flags.append("Breastfeeding: Progestin-only methods are safe immediately. Avoid combined methods <6 weeks postpartum.")
            
        # Diabetes
        if diabetes:
            flags.append("Diabetes: Monitor closely. Progestin-only or IUD generally preferred over combined methods.")
            
        # STI Protection
        if sti_needed:
            flags.append("STI protection needed: Dual method recommended (Condoms + primary contraceptive).")

        if not flags:
            return {"flagged": False, "risk_category": "none", "message": "No critical clinical risks identified."}
            
        return {"flagged": True, "risk_category": risk, "message": " ".join(flags)}