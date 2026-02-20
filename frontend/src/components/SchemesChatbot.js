import React, { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { askSchemeBot } from "../api";

const STEPS = ["profile", "results", "chat"];

const OCCUPATIONS = ["Farmer / किसान", "Student / छात्र", "Labor / मजदूर", "Self-Employed / व्यापारी", "Housewife / गृहिणी", "Street Vendor / रेहड़ी", "Unemployed / बेरोजगार", "Other / अन्य"];
const CASTES = ["General / सामान्य", "OBC", "SC / अनुसूचित जाति", "ST / अनुसूचित जनजाति"];
const EDUCATIONS = ["Illiterate / अनपढ़", "Primary (1-5)", "Middle (6-8)", "Matriculate (10th)", "Intermediate (12th)", "Graduate / स्नातक", "Post-Graduate / परास्नातक"];

const FIELD = ({ label, children }) => (
    <div className="space-y-1.5">
        <label className="block text-[10px] font-black text-emerald-600 uppercase tracking-[0.2em]">{label}</label>
        {children}
    </div>
);

const SELECT_CLS = "w-full bg-white/50 border border-gray-200 p-3.5 rounded-2xl text-sm font-semibold text-gray-800 focus:outline-none focus:border-emerald-500 transition-all appearance-none cursor-pointer";
const INPUT_CLS = "w-full bg-white/50 border border-gray-200 p-3.5 rounded-2xl text-sm font-semibold text-gray-800 focus:outline-none focus:border-emerald-500 transition-all placeholder:text-gray-400";

export default function SchemesChatbot({ onClose }) {
    const [step, setStep] = useState("profile");
    const [lang, setLang] = useState("hindi");
    const [loading, setLoading] = useState(false);
    const [profile, setProfile] = useState({ name: "", age: "", gender: "", education: "", occupation: "", income: "", caste: "" });
    const [schemes, setSchemes] = useState([]);
    const [chatHistory, setChatHistory] = useState([]);
    const [chatInput, setChatInput] = useState("");
    const chatEndRef = useRef(null);

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [chatHistory]);

    const handleProfile = (k, v) => setProfile(p => ({ ...p, [k]: v }));

    const getSchemes = async () => {
        if (!profile.age || !profile.gender || !profile.occupation) {
            alert("कृपया Age, Gender और Occupation जरूर भरें।");
            return;
        }
        setLoading(true);
        const res = await askSchemeBot({ ...profile, lang }, lang === "hindi" ? "मुझे मेरे लिए सरकारी योजनाएं बताइए" : "Show me government schemes for my profile");
        setLoading(false);
        if (res) {
            setSchemes(res.schemes || []);
            setChatHistory([{ role: "bot", text: res.response }]);
            setStep("results");
        }
    };

    const sendChat = async () => {
        if (!chatInput.trim()) return;
        const userMsg = chatInput.trim();
        setChatInput("");
        setChatHistory(h => [...h, { role: "user", text: userMsg }]);
        setLoading(true);
        const res = await askSchemeBot({ ...profile, lang }, userMsg);
        setLoading(false);
        if (res) {
            setChatHistory(h => [...h, { role: "bot", text: res.response }]);
        }
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
            <motion.div
                initial={{ opacity: 0, scale: 0.92, y: 30 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.92 }}
                className="relative w-full max-w-2xl max-h-[92vh] flex flex-col rounded-[40px] overflow-hidden shadow-[0_40px_80px_rgba(0,0,0,0.4)] border border-white/20"
                style={{ background: "linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 40%, #fffbeb 100%)" }}
            >
                {/* Header */}
                <div className="px-8 pt-8 pb-4 flex items-center justify-between flex-shrink-0">
                    <div className="flex items-center gap-4">
                        <div className="w-14 h-14 rounded-[20px] bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center text-3xl shadow-xl shadow-emerald-500/30">
                            🤖
                        </div>
                        <div>
                            <h2 className="text-2xl font-black text-gray-900 tracking-tighter">Yojana Saathi</h2>
                            <p className="text-xs font-black text-emerald-600 uppercase tracking-[0.2em]">AI Government Scheme Advisor</p>
                        </div>
                    </div>
                    <div className="flex items-center gap-3">
                        {/* Language Toggle */}
                        <button
                            onClick={() => setLang(l => l === "hindi" ? "english" : "hindi")}
                            className="px-4 py-2 rounded-xl bg-white/60 border border-gray-200 text-xs font-black text-gray-700 uppercase tracking-widest hover:bg-emerald-50 transition-all"
                        >
                            {lang === "hindi" ? "EN" : "हि"}
                        </button>
                        <button
                            onClick={onClose}
                            className="w-10 h-10 rounded-2xl bg-white/60 border border-gray-200 flex items-center justify-center text-gray-500 hover:text-rose-600 hover:bg-rose-50 transition-all font-black text-lg"
                        >
                            ✕
                        </button>
                    </div>
                </div>

                {/* Step Indicator */}
                <div className="px-8 pb-4 flex items-center gap-3 flex-shrink-0">
                    {[
                        { id: "profile", label: lang === "hindi" ? "प्रोफाइल" : "Profile", num: 1 },
                        { id: "results", label: lang === "hindi" ? "योजनाएं" : "Schemes", num: 2 },
                        { id: "chat", label: lang === "hindi" ? "सवाल पूछें" : "Ask More", num: 3 },
                    ].map((s, i) => (
                        <React.Fragment key={s.id}>
                            <button
                                onClick={() => (step === "results" || step === "chat") && setStep(s.id)}
                                disabled={s.id === "results" && step === "profile"}
                                className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-black uppercase tracking-widest transition-all ${step === s.id
                                        ? "bg-emerald-600 text-white shadow-lg shadow-emerald-500/25"
                                        : "bg-white/50 text-gray-400 border border-gray-200"
                                    }`}
                            >
                                <span className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] ${step === s.id ? "bg-white/20" : "bg-gray-100"
                                    }`}>{s.num}</span>
                                {s.label}
                            </button>
                            {i < 2 && <div className="flex-1 h-px bg-gray-200" />}
                        </React.Fragment>
                    ))}
                </div>

                {/* Content */}
                <div className="flex-1 overflow-y-auto px-8 pb-8 min-h-0">
                    <AnimatePresence mode="wait">

                        {/* STEP 1: Profile Form */}
                        {step === "profile" && (
                            <motion.div key="profile" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 20 }} className="space-y-5">
                                <div className="bg-emerald-50 border border-emerald-100 rounded-2xl p-4 text-sm text-emerald-700 font-semibold leading-relaxed">
                                    {lang === "hindi"
                                        ? "🙏 नमस्ते! मैं Yojana Saathi हूं। आपकी जानकारी देकर पता करें — आपके लिए कौन-कौन सी सरकारी योजनाएं हैं और उनका कैसे फायदा उठाएं।"
                                        : "🙏 Hello! I'm Yojana Saathi. Fill in your basic details and I'll tell you exactly which government schemes you're eligible for and how to avail them."}
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <FIELD label={lang === "hindi" ? "नाम (वैकल्पिक)" : "Name (optional)"}>
                                        <input className={INPUT_CLS} placeholder={lang === "hindi" ? "आपका नाम" : "Your name"}
                                            value={profile.name} onChange={e => handleProfile("name", e.target.value)} />
                                    </FIELD>
                                    <FIELD label={lang === "hindi" ? "आयु *" : "Age *"}>
                                        <input className={INPUT_CLS} type="number" placeholder="e.g. 28"
                                            value={profile.age} onChange={e => handleProfile("age", e.target.value)} />
                                    </FIELD>
                                    <FIELD label={lang === "hindi" ? "लिंग *" : "Gender *"}>
                                        <select className={SELECT_CLS} value={profile.gender} onChange={e => handleProfile("gender", e.target.value)}>
                                            <option value="">-- {lang === "hindi" ? "चुनें" : "Select"} --</option>
                                            <option value="male">{lang === "hindi" ? "पुरुष" : "Male"}</option>
                                            <option value="female">{lang === "hindi" ? "महिला" : "Female"}</option>
                                            <option value="other">{lang === "hindi" ? "अन्य" : "Other"}</option>
                                        </select>
                                    </FIELD>
                                    <FIELD label={lang === "hindi" ? "शिक्षा" : "Education"}>
                                        <select className={SELECT_CLS} value={profile.education} onChange={e => handleProfile("education", e.target.value)}>
                                            <option value="">-- {lang === "hindi" ? "चुनें" : "Select"} --</option>
                                            {EDUCATIONS.map(e => <option key={e} value={e}>{e}</option>)}
                                        </select>
                                    </FIELD>
                                    <FIELD label={lang === "hindi" ? "व्यवसाय *" : "Occupation *"}>
                                        <select className={SELECT_CLS} value={profile.occupation} onChange={e => handleProfile("occupation", e.target.value)}>
                                            <option value="">-- {lang === "hindi" ? "चुनें" : "Select"} --</option>
                                            {OCCUPATIONS.map(o => <option key={o} value={o}>{o}</option>)}
                                        </select>
                                    </FIELD>
                                    <FIELD label={lang === "hindi" ? "मासिक आय (₹)" : "Monthly Income (₹)"}>
                                        <input className={INPUT_CLS} type="number" placeholder="e.g. 8000"
                                            value={profile.income} onChange={e => handleProfile("income", e.target.value)} />
                                    </FIELD>
                                    <FIELD label={lang === "hindi" ? "जाति वर्ग" : "Caste Category"}>
                                        <select className={SELECT_CLS} value={profile.caste} onChange={e => handleProfile("caste", e.target.value)}>
                                            <option value="">-- {lang === "hindi" ? "चुनें" : "Select"} --</option>
                                            {CASTES.map(c => <option key={c} value={c}>{c}</option>)}
                                        </select>
                                    </FIELD>
                                </div>

                                <motion.button
                                    whileHover={{ scale: 1.02 }}
                                    whileTap={{ scale: 0.98 }}
                                    onClick={getSchemes}
                                    disabled={loading}
                                    className="w-full py-5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white rounded-2xl font-black uppercase tracking-widest text-sm shadow-xl shadow-emerald-500/25 transition-all flex items-center justify-center gap-3"
                                >
                                    {loading
                                        ? <><div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" /> {lang === "hindi" ? "खोज रहे हैं..." : "Searching..."}</>
                                        : <>{lang === "hindi" ? "🔍 मेरे लिए योजनाएं खोजें" : "🔍 Find My Schemes"}</>
                                    }
                                </motion.button>
                            </motion.div>
                        )}

                        {/* STEP 2: Results */}
                        {step === "results" && (
                            <motion.div key="results" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-5">
                                <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-4 flex items-center justify-between">
                                    <div>
                                        <p className="text-emerald-700 font-black text-lg">{schemes.length} {lang === "hindi" ? "योजनाएं मिलीं" : "Schemes Found"}</p>
                                        <p className="text-emerald-600 text-xs font-semibold mt-0.5">{lang === "hindi" ? `${profile.name || "आपके"} profile के अनुसार` : `Matched for ${profile.name || "your"} profile`}</p>
                                    </div>
                                    <button
                                        onClick={() => setStep("chat")}
                                        className="px-5 py-2.5 bg-emerald-600 text-white rounded-xl font-black uppercase tracking-widest text-[10px] hover:bg-emerald-700 transition-all shadow-lg shadow-emerald-500/25"
                                    >
                                        {lang === "hindi" ? "सवाल पूछें →" : "Ask Questions →"}
                                    </button>
                                </div>

                                {schemes.length === 0 && (
                                    <div className="text-center py-10 text-gray-400 font-black uppercase tracking-widest">
                                        {lang === "hindi" ? "अधिक जानकारी के लिए Chat tab में जाएं" : "Go to Chat tab for more details"}
                                    </div>
                                )}

                                {schemes.map((s, i) => (
                                    <motion.div
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: i * 0.08 }}
                                        key={i}
                                        className="bg-white/70 backdrop-blur-sm border border-white rounded-[24px] p-6 shadow-lg hover:shadow-xl transition-all"
                                    >
                                        <div className="flex items-start justify-between gap-3 mb-4">
                                            <div>
                                                <h3 className="font-black text-gray-900 text-base leading-tight">{s.name}</h3>
                                                <p className="text-emerald-600 text-sm font-bold mt-0.5">{s.hindi}</p>
                                            </div>
                                            <div className="bg-emerald-100 text-emerald-700 text-[10px] font-black px-3 py-1.5 rounded-xl border border-emerald-200 whitespace-nowrap">
                                                #{i + 1}
                                            </div>
                                        </div>

                                        <div className="grid grid-cols-1 gap-2 mb-4">
                                            <div className="flex items-start gap-2">
                                                <span className="text-lg flex-shrink-0">💰</span>
                                                <div>
                                                    <span className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Benefit / लाभ</span>
                                                    <p className="text-sm font-black text-gray-900">{s.amount}</p>
                                                </div>
                                            </div>
                                            <div className="flex items-start gap-2">
                                                <span className="text-lg flex-shrink-0">📋</span>
                                                <div>
                                                    <span className="text-[10px] font-black text-gray-400 uppercase tracking-widest">How to Apply / कैसे करें</span>
                                                    <p className="text-sm font-semibold text-gray-700">{s.how_to_apply}</p>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="bg-amber-50 border border-amber-100 rounded-2xl p-3">
                                            <p className="text-[10px] font-black text-amber-600 uppercase tracking-widest mb-1">Documents / दस्तावेज़</p>
                                            <div className="flex flex-wrap gap-1.5">
                                                {s.documents.map((d, j) => (
                                                    <span key={j} className="bg-white text-gray-700 text-[10px] font-black px-2.5 py-1 rounded-lg border border-amber-100">{d}</span>
                                                ))}
                                            </div>
                                        </div>
                                    </motion.div>
                                ))}
                            </motion.div>
                        )}

                        {/* STEP 3: Chat */}
                        {step === "chat" && (
                            <motion.div key="chat" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="flex flex-col gap-4 h-full">
                                <div className="space-y-3 min-h-[250px] max-h-[350px] overflow-y-auto pr-1">
                                    {chatHistory.map((msg, i) => (
                                        <motion.div
                                            key={i}
                                            initial={{ opacity: 0, y: 8 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                                        >
                                            {msg.role === "bot" && (
                                                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center text-sm mr-2 flex-shrink-0">🤖</div>
                                            )}
                                            <div className={`max-w-[85%] px-4 py-3 rounded-2xl text-sm font-medium leading-relaxed whitespace-pre-wrap ${msg.role === "user"
                                                    ? "bg-emerald-600 text-white rounded-br-sm"
                                                    : "bg-white/80 text-gray-800 rounded-bl-sm border border-gray-100 shadow-sm"
                                                }`}>
                                                {msg.text}
                                            </div>
                                        </motion.div>
                                    ))}
                                    {loading && (
                                        <div className="flex justify-start">
                                            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center text-sm mr-2">🤖</div>
                                            <div className="bg-white/80 px-4 py-3 rounded-2xl rounded-bl-sm border border-gray-100 shadow-sm">
                                                <div className="flex gap-1.5 items-center">
                                                    <div className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                                                    <div className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                                                    <div className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                                                </div>
                                            </div>
                                        </div>
                                    )}
                                    <div ref={chatEndRef} />
                                </div>

                                {/* Chat Suggestions */}
                                <div className="flex gap-2 flex-wrap">
                                    {(lang === "hindi"
                                        ? ["मुझे घर चाहिए", "रोजगार कैसे मिलेगा?", "स्वास्थ्य बीमा", "लड़की के लिए योजना"]
                                        : ["I need housing", "Job opportunities?", "Health insurance", "Women schemes"]
                                    ).map(suggestion => (
                                        <button
                                            key={suggestion}
                                            onClick={() => { setChatInput(suggestion); }}
                                            className="px-3 py-1.5 bg-white/60 border border-gray-200 rounded-xl text-xs font-bold text-gray-600 hover:bg-emerald-50 hover:border-emerald-200 hover:text-emerald-700 transition-all"
                                        >
                                            {suggestion}
                                        </button>
                                    ))}
                                </div>

                                <div className="flex gap-3">
                                    <input
                                        className="flex-1 bg-white/70 border border-gray-200 px-5 py-3.5 rounded-2xl text-sm font-semibold text-gray-800 focus:outline-none focus:border-emerald-500 transition-all placeholder:text-gray-400"
                                        placeholder={lang === "hindi" ? "कोई भी सवाल पूछें..." : "Ask anything about schemes..."}
                                        value={chatInput}
                                        onChange={e => setChatInput(e.target.value)}
                                        onKeyPress={e => e.key === "Enter" && sendChat()}
                                    />
                                    <motion.button
                                        whileTap={{ scale: 0.95 }}
                                        onClick={sendChat}
                                        disabled={loading || !chatInput.trim()}
                                        className="px-6 py-3.5 bg-gradient-to-r from-emerald-600 to-teal-600 text-white rounded-2xl font-black text-sm shadow-lg shadow-emerald-500/25 disabled:opacity-40 transition-all hover:from-emerald-500 hover:to-teal-500"
                                    >
                                        ➤
                                    </motion.button>
                                </div>
                            </motion.div>
                        )}

                    </AnimatePresence>
                </div>
            </motion.div>
        </div>
    );
}
