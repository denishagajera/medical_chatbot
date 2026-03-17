"""
Medical Knowledge Base
Static knowledge used to ground the AI's responses.
"""

# ── General medical knowledge ──────────────────────────────────────────────────
MEDICAL_KNOWLEDGE = {
    "hypertension": "High blood pressure (>130/80 mmHg). Often called the 'silent killer'. Risk factors: obesity, stress, salt intake, family history. Managed with lifestyle changes and medication.",
    "diabetes_type2": "Chronic condition affecting insulin use. Symptoms: increased thirst, frequent urination, fatigue, blurred vision. Managed with diet, exercise, and medication.",
    "diabetes_type1": "Autoimmune condition destroying insulin-producing cells. Requires daily insulin. Common in younger people.",
    "asthma": "Chronic airway inflammation causing wheezing, shortness of breath, chest tightness. Triggers: allergens, exercise, cold air. Treated with inhalers.",
    "cardiovascular_disease": "Includes coronary artery disease, heart failure, arrhythmias. Main risk factors: hypertension, high cholesterol, smoking, obesity, diabetes.",
    "pneumonia": "Lung infection (bacterial, viral, or fungal). Symptoms: cough, fever, chills, difficulty breathing. Treatment depends on cause.",
    "anemia": "Low red blood cell count or hemoglobin. Causes: iron deficiency, B12 deficiency, chronic disease. Symptoms: fatigue, pale skin, shortness of breath.",
    "hypothyroidism": "Underactive thyroid gland. Symptoms: fatigue, weight gain, cold sensitivity, constipation, depression. Treated with levothyroxine.",
    "hyperthyroidism": "Overactive thyroid. Symptoms: weight loss, rapid heartbeat, anxiety, sweating. Treated with medication, radioiodine, or surgery.",
    "migraine": "Intense recurring headaches often with nausea, vomiting, light/sound sensitivity. Triggers: stress, hormones, certain foods, sleep changes.",
    "gerd": "Gastroesophageal reflux disease — chronic acid reflux. Symptoms: heartburn, regurgitation, chest pain. Managed with diet, lifestyle, PPIs.",
    "arthritis": "Joint inflammation. Osteoarthritis (wear-and-tear) and rheumatoid arthritis (autoimmune). Symptoms: pain, stiffness, swelling.",
    "depression": "Mood disorder with persistent sadness, loss of interest, fatigue, sleep/appetite changes. Treated with therapy, medication, lifestyle changes.",
    "anxiety": "Excessive worry, fear, or nervousness. Types: GAD, panic disorder, social anxiety. Treated with CBT, medication, mindfulness.",
    "urinary_tract_infection": "Bacterial infection of urinary system. Symptoms: burning urination, frequent urge, cloudy urine, pelvic pain. Treated with antibiotics.",
    "common_cold": "Viral upper respiratory infection. Symptoms: runny nose, sore throat, cough, congestion, mild fever. Self-limiting, 7–10 days.",
    "influenza": "Flu — more severe than cold. Sudden fever, body aches, headache, fatigue, cough. Prevented with annual vaccine.",
    "covid19": "Respiratory illness caused by SARS-CoV-2. Symptoms range from mild (cough, fever, fatigue) to severe (pneumonia, breathing difficulty). Prevention: vaccination, masks.",
    "obesity": "BMI ≥ 30. Risk factor for diabetes, heart disease, joint problems, sleep apnea. Managed with diet, exercise, behavioral therapy, sometimes medication/surgery.",
    "osteoporosis": "Low bone density, increased fracture risk. Common in postmenopausal women. Prevention: calcium, vitamin D, weight-bearing exercise.",
    "cholesterol": "High LDL ('bad') cholesterol increases heart disease risk. Managed with diet, exercise, statins. HDL ('good') cholesterol is protective.",
    "kidney_disease": "Chronic kidney disease: gradual loss of kidney function. Symptoms often absent early. Risk factors: diabetes, hypertension. Monitored via GFR, creatinine.",
    "liver_disease": "Includes fatty liver, hepatitis, cirrhosis. Symptoms: jaundice, fatigue, abdominal pain. Alcohol, obesity, viral hepatitis are common causes.",
    "allergies": "Immune response to harmless substances. Types: food, environmental, drug. Symptoms: sneezing, itching, rash, anaphylaxis in severe cases.",
    "sleep_apnea": "Breathing repeatedly stops during sleep. Symptoms: loud snoring, daytime sleepiness, morning headaches. Treatment: CPAP, lifestyle changes.",
}

# ── Symptom checker by body system ────────────────────────────────────────────
SYMPTOM_CHECKER = {
    "Cardiovascular (Heart)": [
        "Chest pain or pressure",
        "Shortness of breath",
        "Palpitations (irregular heartbeat)",
        "Swollen ankles/feet",
        "Fatigue with exertion",
        "Dizziness or fainting",
    ],
    "Respiratory (Lungs)": [
        "Persistent cough",
        "Shortness of breath",
        "Wheezing",
        "Coughing up blood",
        "Chest tightness",
        "Night sweats with cough",
    ],
    "Neurological (Brain/Nerves)": [
        "Severe headache",
        "Dizziness or vertigo",
        "Numbness or tingling",
        "Memory problems",
        "Seizures",
        "Difficulty speaking or understanding",
    ],
    "Gastrointestinal (Digestive)": [
        "Abdominal pain",
        "Nausea or vomiting",
        "Diarrhea or constipation",
        "Blood in stool",
        "Heartburn/acid reflux",
        "Bloating or gas",
    ],
    "Musculoskeletal (Joints/Muscles)": [
        "Joint pain or swelling",
        "Muscle weakness",
        "Back pain",
        "Limited range of motion",
        "Morning stiffness",
        "Muscle cramps",
    ],
    "Endocrine (Hormones)": [
        "Excessive thirst or urination",
        "Unexplained weight changes",
        "Fatigue",
        "Temperature sensitivity",
        "Hair loss",
        "Mood changes",
    ],
    "Skin & Dermatology": [
        "Rash or hives",
        "Unusual moles or lesions",
        "Jaundice (yellow skin/eyes)",
        "Excessive bruising",
        "Persistent itching",
        "Skin color changes",
    ],
    "Mental Health": [
        "Persistent sadness or low mood",
        "Excessive anxiety or worry",
        "Sleep disturbances",
        "Loss of interest in activities",
        "Mood swings",
        "Difficulty concentrating",
    ],
    "Urinary & Reproductive": [
        "Painful urination",
        "Frequent urination",
        "Blood in urine",
        "Pelvic pain",
        "Unusual discharge",
        "Changes in menstrual cycle",
    ],
    "Eyes & Vision": [
        "Blurred vision",
        "Eye pain or redness",
        "Sudden vision loss",
        "Seeing floaters or flashes",
        "Double vision",
        "Light sensitivity",
    ],
}

# ── Emergency keywords that should trigger immediate alert ─────────────────────
EMERGENCY_KEYWORDS = [
    # Cardiac emergencies
    "heart attack", "cardiac arrest", "chest pain", "crushing chest",
    "left arm pain", "jaw pain spreading",
    
    # Stroke
    "stroke", "face drooping", "arm weakness", "sudden numbness",
    "sudden confusion", "sudden severe headache", "can't speak", "slurred speech",
    "facial drooping",
    
    # Breathing
    "can't breathe", "cannot breathe", "not breathing", "stopped breathing",
    "choking", "airway blocked", "severe asthma attack", "anaphylaxis",
    "allergic reaction severe",
    
    # Bleeding / trauma
    "severe bleeding", "uncontrolled bleeding", "heavy bleeding",
    "deep wound", "cut artery", "blood loss",
    
    # Consciousness
    "unconscious", "unresponsive", "passed out", "fainted", "collapsed",
    "seizure", "convulsion", "not waking up",
    
    # Mental health crisis
    "suicidal", "want to die", "kill myself", "overdose", "took too many pills",
    "self harm", "harming myself",
    
    # Other critical
    "poisoning", "swallowed poison", "high fever seizure", "meningitis",
    "diabetic coma", "severe allergic", "throat closing",
    "emergency", "dying", "someone is dying",
]

# ── Common medications reference ───────────────────────────────────────────────
COMMON_MEDICATIONS = {
    "paracetamol": "Pain reliever and fever reducer. Also known as acetaminophen. Max adult dose: 4g/day. Avoid with liver conditions.",
    "ibuprofen": "NSAID for pain, fever, inflammation. Take with food. Avoid with kidney disease, stomach ulcers, or if pregnant.",
    "aspirin": "NSAID also used as blood thinner. Not for children under 16. Used in low doses to prevent heart attacks.",
    "metformin": "First-line diabetes medication. Reduces glucose production in liver. Take with meals to reduce GI side effects.",
    "lisinopril": "ACE inhibitor for blood pressure and heart failure. Common side effect: dry cough.",
    "atorvastatin": "Statin for high cholesterol. Take at night. Monitor liver enzymes. Avoid grapefruit juice.",
    "omeprazole": "Proton pump inhibitor (PPI) for acid reflux, GERD, ulcers. Reduces stomach acid production.",
    "sertraline": "SSRI antidepressant for depression and anxiety. Takes 4-6 weeks for full effect.",
    "salbutamol": "Bronchodilator inhaler for asthma. Relieves acute wheezing. Also called albuterol.",
    "levothyroxine": "Thyroid hormone replacement for hypothyroidism. Take on empty stomach, 30 min before breakfast.",
}

# ── Healthy ranges reference ───────────────────────────────────────────────────
NORMAL_RANGES = {
    "blood_pressure": "Normal: <120/80 mmHg | Elevated: 120-129/<80 | High: ≥130/80 mmHg",
    "heart_rate": "Normal adult: 60-100 bpm | Athletes may have 40-60 bpm",
    "blood_glucose_fasting": "Normal: 70-99 mg/dL | Prediabetes: 100-125 mg/dL | Diabetes: ≥126 mg/dL",
    "bmi": "Underweight: <18.5 | Normal: 18.5-24.9 | Overweight: 25-29.9 | Obese: ≥30",
    "temperature": "Normal: 36.1-37.2°C (97-99°F) | Low-grade fever: 37.3-38°C | Fever: >38°C (100.4°F)",
    "oxygen_saturation": "Normal: 95-100% SpO2 | Concerning: <92% — seek medical attention",
    "cholesterol_total": "Desirable: <200 mg/dL | Borderline: 200-239 mg/dL | High: ≥240 mg/dL",
    "hemoglobin": "Men: 13.5-17.5 g/dL | Women: 12-15.5 g/dL | Low = anemia",
}
