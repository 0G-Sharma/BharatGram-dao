import React, { useEffect, useState } from "react";
import { verifyProjectOnChain } from "../api";
import { FaShieldAlt, FaCheckCircle, FaExclamationTriangle, FaExternalLinkAlt } from "react-icons/fa";

export default function BlockchainVerifier({ projectId, localBudget }) {
    const [chainData, setChainData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);

    useEffect(() => {
        async function checkChain() {
            setLoading(true);
            const data = await verifyProjectOnChain(projectId);
            if (data) {
                setChainData(data);
                setError(false);
            } else {
                setError(true);
            }
            setLoading(false);
        }
        checkChain();
    }, [projectId]);

    if (loading) return <div className="text-sm text-gray-500 animate-pulse flex items-center gap-2"><div className="w-2 h-2 bg-teal-500 rounded-full animate-bounce"></div> Verifying on Algorand Blockchain...</div>;

    if (error || !chainData) {
        return (
            <div className="flex items-center gap-3 bg-amber-50 border border-amber-200 p-4 rounded-2xl">
                <FaExclamationTriangle className="text-amber-500 text-xl" />
                <div>
                    <p className="text-amber-800 font-bold text-sm">Not yet synced with Blockchain</p>
                    <p className="text-amber-600 text-[10px]">Data is currently only stored in local database.</p>
                </div>
            </div>
        );
    }

    const isMatch = parseInt(chainData.budget) === parseInt(localBudget);

    return (
        <div className={`p-4 rounded-2xl border-2 transition-all ${isMatch ? 'bg-teal-50 border-teal-100' : 'bg-red-50 border-red-100'}`}>
            <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                    <FaShieldAlt className={isMatch ? "text-teal-600" : "text-red-500"} />
                    <span className="font-bold text-sm text-gray-800 uppercase tracking-wider">Algorand Transparency Check</span>
                </div>
                {isMatch ? (
                    <span className="bg-teal-600 text-white text-[10px] px-2 py-1 rounded-full font-bold flex items-center gap-1">
                        <FaCheckCircle /> VERIFIED
                    </span>
                ) : (
                    <span className="bg-red-600 text-white text-[10px] px-2 py-1 rounded-full font-bold flex items-center gap-1">
                        <FaExclamationTriangle /> MISMATCH ALERT
                    </span>
                )}
            </div>

            <div className="grid grid-cols-2 gap-4 mt-3">
                <div className="bg-white/50 p-2 rounded-xl border border-white">
                    <p className="text-[10px] text-gray-400 uppercase font-bold">On-Chain Budget</p>
                    <p className="text-lg font-mono font-bold text-gray-700">₹{chainData.budget.toLocaleString()}</p>
                </div>
                <div className="bg-white/50 p-2 rounded-xl border border-white">
                    <p className="text-[10px] text-gray-400 uppercase font-bold">Project ID</p>
                    <p className="text-lg font-mono font-bold text-gray-700">#{projectId}</p>
                </div>
            </div>

            <div className="mt-3 pt-3 border-t border-white/40 flex items-center justify-between">
                <div className="flex flex-col">
                    <span className="text-[10px] text-gray-400">Status Hash</span>
                    <code className="text-[8px] text-gray-400 break-all">{chainData.hash}</code>
                </div>
                <a
                    href="https://lora.algokit.io/testnet"
                    target="_blank"
                    rel="noreferrer"
                    className="text-teal-600 hover:text-teal-700 text-xs flex items-center gap-1 font-bold underline whitespace-nowrap ml-2"
                >
                    View Explorer <FaExternalLinkAlt size={10} />
                </a>
            </div>

            {!isMatch && (
                <p className="mt-2 text-[10px] text-red-600 font-bold bg-red-100 p-2 rounded-lg">
                    WARNING: Local data does not match the blockchain records! Possible data tampering detected.
                </p>
            )}
        </div>
    );
}
