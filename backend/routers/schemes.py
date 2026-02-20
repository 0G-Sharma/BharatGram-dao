from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/ai/schemes", tags=["AI Schemes Assistant"])

# ============================================================
# INDIA GOVERNMENT SCHEMES DATABASE — EXPANDED
# ============================================================
SCHEMES_DB = [
    {
        "name": "PM Kisan Samman Nidhi", "hindi": "प्रधानमंत्री किसान सम्मान निधि",
        "amount": "₹6,000/year (₹2,000 per installment)", "for": "farmers",
        "min_age": 18,
        "description": "Direct income support ₹6,000/year to small & marginal farmers having up to 2 hectares land",
        "how_to_apply": "Visit pmkisan.gov.in or nearest CSC/Kisan Seva Kendra",
        "documents": ["Aadhaar card", "Bank account", "Land records (Khasra/Khatauni)"],
        "keywords": ["kisan", "farmer", "kheti", "agriculture", "krishi", "land"],
        "for_gender": None, "for_occupation": ["farmer"], "max_income": None, "for_caste": None
    },
    {
        "name": "Pradhan Mantri Awas Yojana (Gramin)", "hindi": "प्रधानमंत्री आवास योजना - ग्रामीण",
        "amount": "₹1.20 lakh grant (plain), ₹1.30 lakh (hilly/NE)", "for": "BPL families",
        "description": "Housing grant for rural poor families living in kutcha/damaged houses",
        "how_to_apply": "Apply through Gram Panchayat or pmayg.nic.in",
        "documents": ["Aadhaar", "Bank account", "BPL/SECC list inclusion", "Land proof"],
        "keywords": ["house", "ghar", "awas", "home", "makaan", "gramin", "rural", "kutcha"],
        "for_gender": None, "for_occupation": None, "max_income": 15000, "for_caste": None
    },
    {
        "name": "Ayushman Bharat PM-JAY", "hindi": "आयुष्मान भारत योजना",
        "amount": "₹5 lakh health cover/year (per family)", "for": "Low income families",
        "description": "Free health insurance ₹5 lakh/family/year at 25,000+ empanelled hospitals",
        "how_to_apply": "Check eligibility at pmjay.gov.in | Visit Ayushman Mitra at hospital",
        "documents": ["Aadhaar", "Ration card"],
        "keywords": ["health", "hospital", "treatment", "ilaj", "swasthya", "bimari", "insurance", "dawai"],
        "for_gender": None, "for_occupation": None, "max_income": 20000, "for_caste": None
    },
    {
        "name": "PM Ujjwala Yojana 2.0", "hindi": "प्रधानमंत्री उज्ज्वला योजना",
        "amount": "Free LPG connection + First refill free", "for": "Women from BPL/EWS families",
        "description": "Free LPG cylinder connection to women from economically weaker sections",
        "how_to_apply": "Visit nearest gas agency or pmuy.gov.in",
        "documents": ["Aadhaar", "BPL Ration Card", "Bank account", "Passport photo"],
        "keywords": ["gas", "lpg", "ujjwala", "cylinder", "cooking", "chulha"],
        "for_gender": "female", "for_occupation": None, "max_income": 15000, "for_caste": None
    },
    {
        "name": "PM Jan Dhan Yojana", "hindi": "प्रधानमंत्री जन धन योजना",
        "amount": "Zero balance bank account + ₹10,000 overdraft + ₹2 lakh accident insurance",
        "for": "Unbanked citizens",
        "description": "Zero balance savings account with RuPay debit card and insurance benefits",
        "how_to_apply": "Visit any bank branch with Aadhaar & address proof",
        "documents": ["Aadhaar or any ID proof"],
        "keywords": ["bank", "account", "jandhan", "jan dhan", "money", "paisa", "savings", "khata"],
        "for_gender": None, "for_occupation": None, "max_income": None, "for_caste": None
    },
    {
        "name": "Post-Matric Scholarship (SC/ST/OBC)", "hindi": "अनुसूचित जाति/जनजाति/OBC छात्रवृत्ति",
        "amount": "₹230 to ₹1,200/month + maintenance allowance", "for": "SC/ST/OBC students",
        "description": "Post-matric scholarships for Class 11 to PhD students from SC/ST/OBC communities",
        "how_to_apply": "Apply at scholarships.gov.in or via school/college",
        "documents": ["Caste certificate", "Income certificate", "Marksheets", "Aadhaar"],
        "keywords": ["scholarship", "student", "padhai", "education", "sc", "st", "obc", "school", "college", "exam", "padhna"],
        "for_gender": None, "for_occupation": ["student"], "max_income": 25000, "for_caste": ["SC", "ST", "OBC"]
    },
    {
        "name": "Central Sector Scholarship (Merit)", "hindi": "केंद्रीय क्षेत्र छात्रवृत्ति",
        "amount": "₹10,000 to ₹20,000/year", "for": "Meritorious students (Class 12 onwards)",
        "description": "Scholarship for top students from lower-income families based on class 12 merit",
        "how_to_apply": "Apply at scholarships.gov.in after Class 12 results",
        "documents": ["12th Marksheet", "Income certificate", "Aadhaar", "Bank account"],
        "keywords": ["scholarship", "merit", "topper", "student", "college", "degree", "12th"],
        "for_gender": None, "for_occupation": ["student"], "max_income": 25000, "for_caste": None
    },
    {
        "name": "Mahatma Gandhi NREGS", "hindi": "मनरेगा - राष्ट्रीय ग्रामीण रोजगार गारंटी",
        "amount": "100 days guaranteed work/year (₹200-300/day)", "for": "Rural job seekers",
        "description": "Guaranteed 100 days wage employment per year to rural households",
        "how_to_apply": "Register at Gram Panchayat office with Job Card application",
        "documents": ["Aadhaar", "Residence proof", "Passport photo"],
        "keywords": ["job", "nrega", "mgnrega", "work", "rozgaar", "employment", "rojgar", "mazdoor", "kaam"],
        "for_gender": None, "for_occupation": ["labor", "unemployed", "farmer"], "max_income": None, "for_caste": None
    },
    {
        "name": "PM Mudra Yojana", "hindi": "PM मुद्रा लोन",
        "amount": "Shishu: ₹50K | Kishore: ₹5L | Tarun: ₹10 lakh", "for": "Small business owners",
        "description": "Low-interest loans for non-farm small/micro enterprises without collateral",
        "how_to_apply": "Apply at any bank, NBFC, MFI or mudra.org.in",
        "documents": ["Aadhaar", "Business plan", "Bank statement", "PAN"],
        "keywords": ["business", "loan", "mudra", "shop", "dukan", "vyapar", "startup", "self employed"],
        "for_gender": None, "for_occupation": ["self-employed", "business"], "max_income": None, "for_caste": None
    },
    {
        "name": "Sukanya Samriddhi Yojana", "hindi": "सुकन्या समृद्धि योजना",
        "amount": "8.2% interest rate saving scheme (tax-free)", "for": "Girl child (below 10)",
        "description": "Savings scheme for girl child — high interest + tax benefit under 80C",
        "how_to_apply": "Open account at any post office or bank",
        "documents": ["Girl child birth certificate", "Parent Aadhaar"],
        "keywords": ["girl", "daughter", "beti", "ladki", "bachha", "sukanya", "child", "savings"],
        "for_gender": "female", "for_occupation": None, "max_income": None, "for_caste": None
    },
    {
        "name": "PM Kisan Maandhan (Pension)", "hindi": "PM किसान मानधन पेंशन",
        "amount": "₹3,000/month pension after age 60", "for": "Small farmers aged 18-40",
        "description": "Voluntary pension scheme for small/marginal farmers — ₹55-200/month contribution",
        "how_to_apply": "Visit CSC center or maandhan.in",
        "documents": ["Aadhaar", "Bank account", "Land records"],
        "keywords": ["pension", "old age", "retirement", "budhapa", "farmer pension"],
        "for_gender": None, "for_occupation": ["farmer"], "max_income": None, "for_caste": None
    },
    {
        "name": "Pradhan Mantri Matru Vandana Yojana", "hindi": "प्रधानमंत्री मातृ वंदना योजना",
        "amount": "₹5,000 in 3 installments", "for": "Pregnant/lactating women (first child)",
        "description": "Cash incentive of ₹5,000 to pregnant and lactating mothers for first living child",
        "how_to_apply": "Register at Anganwadi center / health facility",
        "documents": ["Aadhaar", "Bank account", "MCP card", "Marriage certificate"],
        "keywords": ["pregnant", "garbhvati", "maternity", "baby", "shishu", "mother", "maa"],
        "for_gender": "female", "for_occupation": None, "max_income": None, "for_caste": None
    },
    {
        "name": "PM SVANidhi (Street Vendor Loan)", "hindi": "पीएम स्वनिधि - रेहड़ी-पटरी ऋण",
        "amount": "₹10,000 → ₹20,000 → ₹50,000 (collateral-free)", "for": "Street vendors",
        "description": "Working capital loan for street vendors to restart/grow their business",
        "how_to_apply": "Apply at pmsvanidhi.mohua.gov.in or nearest bank",
        "documents": ["Aadhaar", "Vendor certificate from ULB", "Bank account"],
        "keywords": ["street vendor", "rehdi", "patri", "thela", "hawker", "small vendor", "dukan"],
        "for_gender": None, "for_occupation": ["street vendor", "hawker"], "max_income": None, "for_caste": None
    },
    {
        "name": "Atal Pension Yojana", "hindi": "अटल पेंशन योजना",
        "amount": "₹1,000–₹5,000/month guaranteed pension at 60", "for": "Unorganized sector workers",
        "description": "Government-backed pension scheme for workers without formal pension coverage",
        "how_to_apply": "Open at any bank or post office branch",
        "documents": ["Aadhaar", "Bank account", "Mobile number"],
        "keywords": ["pension", "retirement", "unorganized", "mazdoor", "worker", "monthly income"],
        "for_gender": None, "for_occupation": ["labor", "self-employed", "farmer"], "max_income": None, "for_caste": None
    },
]


# ============================================================
# MATCHING ENGINE — PROFILE-BASED
# ============================================================
def detect_language(text: str) -> str:
    hindi_chars = sum(1 for c in text if '\u0900' <= c <= '\u097F')
    return "hindi" if hindi_chars > 3 else "english"


def find_matching_schemes(
    query: str,
    age: Optional[int] = None,
    gender: Optional[str] = None,
    occupation: Optional[str] = None,
    income: Optional[float] = None,
    caste: Optional[str] = None,
    education: Optional[str] = None,
):
    query_lower = query.lower()
    matches = []

    for scheme in SCHEMES_DB:
        score = 0
        all_keywords = scheme.get("keywords", []) + scheme["name"].lower().split() + scheme["hindi"].lower().split()

        # Keyword match
        for kw in all_keywords:
            if kw in query_lower:
                score += 3

        # Age filter
        if age and "min_age" in scheme and age < scheme["min_age"]:
            continue

        # Gender match — strong boost if scheme targets specific gender
        scheme_gender = scheme.get("for_gender")
        if scheme_gender and gender:
            if gender.lower() in scheme_gender.lower():
                score += 8
        elif not scheme_gender:
            score += 1  # gender-neutral, small base score

        # Occupation match
        scheme_occupations = scheme.get("for_occupation")
        if scheme_occupations and occupation:
            if any(o in occupation.lower() for o in scheme_occupations):
                score += 8

        # Income match — if scheme has max_income and user income is below it
        max_income = scheme.get("max_income")
        if max_income and income and income <= max_income:
            score += 5
        elif income and not max_income:
            score += 1  # no income restriction = slightly better

        # Caste match
        scheme_caste = scheme.get("for_caste")
        if scheme_caste and caste:
            if caste.upper() in [c.upper() for c in scheme_caste]:
                score += 10

        # Education-based boost — students looking for scholarships
        if education and "student" in query_lower or (occupation and "student" in occupation.lower()):
            if "scholarship" in scheme["name"].lower() or "student" in str(scheme.get("for_occupation", "")):
                score += 4

        # General triggers
        general_triggers = ["scheme", "yojana", "help", "madad", "sarkari", "government", "benefit", "labh", "kya", "chahiye", "milega"]
        if any(t in query_lower for t in general_triggers):
            score += 1

        if score > 0:
            matches.append((score, scheme))

    matches.sort(key=lambda x: x[0], reverse=True)
    return [s for _, s in matches[:6]]


def generate_response(query: str, age: Optional[int], lang: str, matched: list) -> str:
    if lang == "hindi":
        if not matched:
            return (
                "माफ़ करें, आपकी जानकारी के आधार पर कोई योजना नहीं मिली। "
                "कृपया अपनी स्थिति बताएं जैसे: किसान हैं, छात्र हैं, बेरोजगार हैं, या घर चाहिए। "
                "मैं सही सरकारी योजना बताऊंगा और कैसे आवेदन करना है, वो भी बताऊंगा।"
            )
        resp = f"आपके profile के आधार पर **{len(matched)} सरकारी योजनाएं** मिली हैं:\n\n"
        for s in matched:
            resp += (
                f"### {s['name']}\n"
                f"**{s['hindi']}**\n"
                f"- **लाभ:** {s['amount']}\n"
                f"- **किसके लिए:** {s['for']}\n"
                f"- **विवरण:** {s['description']}\n"
                f"- **आवेदन कहाँ करें:** {s['how_to_apply']}\n"
                f"- **जरूरी दस्तावेज़:** {', '.join(s['documents'])}\n\n"
            )
        resp += "\n---\nक्या आप किसी योजना के बारे में विस्तार से जानना चाहते हैं? बताइए! 😊"
        return resp
    else:
        if not matched:
            return (
                "I couldn't find matching schemes for your profile. "
                "Please describe your situation (e.g., 'farmer', 'student', 'need house', 'no job') "
                "and I'll guide you to the right government scheme and how to apply."
            )
        resp = f"Based on your profile, I found **{len(matched)} government schemes** for you:\n\n"
        for s in matched:
            resp += (
                f"### {s['name']}\n"
                f"*{s['hindi']}*\n"
                f"- **Benefit:** {s['amount']}\n"
                f"- **For:** {s['for']}\n"
                f"- **Description:** {s['description']}\n"
                f"- **How to apply:** {s['how_to_apply']}\n"
                f"- **Documents needed:** {', '.join(s['documents'])}\n\n"
            )
        resp += "\n---\nWant details about any specific scheme? Just ask! 😊"
        return resp


# ============================================================
# API ENDPOINTS
# ============================================================
class ChatRequest(BaseModel):
    message: str
    age: Optional[int] = None
    gender: Optional[str] = None
    education: Optional[str] = None
    occupation: Optional[str] = None
    income_per_month: Optional[float] = None
    caste_category: Optional[str] = None
    category: Optional[str] = None   # legacy support
    lang: Optional[str] = None


@router.post("/chat")
def scheme_chat(req: ChatRequest):
    lang = req.lang or detect_language(req.message)
    matched = find_matching_schemes(
        query=req.message,
        age=req.age,
        gender=req.gender,
        occupation=req.occupation or req.category,
        income=req.income_per_month,
        caste=req.caste_category,
        education=req.education,
    )
    response = generate_response(req.message, req.age, lang, matched)
    return {
        "response": response,
        "lang": lang,
        "schemes_found": len(matched),
        "scheme_names": [s["name"] for s in matched],
        "schemes": matched
    }
