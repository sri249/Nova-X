"use client";

import { useState, useEffect, use } from "react";
import { Loader2, Brain, Zap, AlertTriangle, TrendingUp, CheckSquare, Star } from "lucide-react";
import api from "@/lib/api";

export default function AIMentorPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const projectId = resolvedParams.id;
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [generateError, setGenerateError] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
  }, [projectId]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const res = await api.get(`/projects/${projectId}/ai-mentor`);
      setData(res.data);
    } catch (err: any) {
      if (err?.response?.status !== 404) console.error(err);
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    setGenerating(true);
    setGenerateError(null);
    try {
      await api.post(`/projects/${projectId}/ai-mentor`, {});
      await fetchData();
    } catch (err: any) {
      console.error(err);
      setGenerateError(err?.response?.data?.detail || 'Failed to generate mentor analysis.');
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 text-violet-600 animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-8 fade-in">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Brain className="w-6 h-6 text-violet-500" />
            AI Mentor
          </h1>
          <p className="text-gray-500 dark:text-gray-400 mt-1">
            AI-powered strategic analysis, risk alerts, and action priorities for your startup.
          </p>
        </div>
        <button
          onClick={handleGenerate}
          disabled={generating}
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-500 hover:to-purple-500 text-white text-sm font-semibold rounded-xl shadow-sm transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {generating ? (
            <><Loader2 className="w-4 h-4 animate-spin" /> Generating...</>
          ) : (
            <><Zap className="w-4 h-4" /> {data ? 'Regenerate Analysis' : 'Generate Mentor Analysis'}</>
          )}
        </button>
      </div>

      {generateError && (
        <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-red-600 dark:text-red-400 text-sm">
          {generateError}
        </div>
      )}

      {!data ? (
        <div className="text-center py-24 bg-white dark:bg-gray-800 rounded-2xl border-2 border-dashed border-gray-200 dark:border-gray-700">
          <div className="w-16 h-16 bg-violet-50 dark:bg-violet-900/20 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <Brain className="w-8 h-8 text-violet-500" />
          </div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2">No Mentor Analysis yet</h2>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-6 max-w-sm mx-auto">
            Get AI-powered strategic insights, risk alerts, strengths analysis, and recommended next actions.
          </p>
          <button
            onClick={handleGenerate}
            disabled={generating}
            className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-violet-600 to-purple-600 text-white font-semibold rounded-xl shadow-sm disabled:opacity-50"
          >
            {generating ? <><Loader2 className="w-4 h-4 animate-spin" /> Generating...</> : <><Brain className="w-4 h-4" /> Generate Mentor Analysis</>}
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Strengths */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
            <h3 className="text-base font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <Star className="w-5 h-5 text-yellow-500" />
              Strengths
            </h3>
            <ul className="space-y-2">
              {(data.strengths || []).map((s: any, i: number) => (
                <li key={i} className="flex items-start gap-2 text-sm text-gray-700 dark:text-gray-300">
                  <CheckSquare className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                  {typeof s === 'object' ? s.strength || Object.values(s).join(' - ') : s}
                </li>
              ))}
              {(!data.strengths || data.strengths.length === 0) && (
                <li className="text-sm text-gray-400 italic">No strengths identified.</li>
              )}
            </ul>
          </div>

          {/* Weaknesses */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
            <h3 className="text-base font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-orange-500" />
              Weaknesses
            </h3>
            <ul className="space-y-2">
              {(data.weaknesses || []).map((w: any, i: number) => (
                <li key={i} className="flex items-start gap-2 text-sm text-gray-700 dark:text-gray-300">
                  <AlertTriangle className="w-4 h-4 text-orange-400 mt-0.5 flex-shrink-0" />
                  {typeof w === 'object' ? w.weakness || Object.values(w).join(' - ') : w}
                </li>
              ))}
              {(!data.weaknesses || data.weaknesses.length === 0) && (
                <li className="text-sm text-gray-400 italic">No weaknesses identified.</li>
              )}
            </ul>
          </div>

          {/* Risk Alerts */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
            <h3 className="text-base font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-red-500" />
              Risk Alerts
            </h3>
            <ul className="space-y-2">
              {(data.risk_alerts || []).map((r: any, i: number) => (
                <li key={i} className="flex items-start gap-2 text-sm text-gray-700 dark:text-gray-300">
                  <span className="w-4 h-4 text-red-500 mt-0.5 flex-shrink-0">⚠</span>
                  {typeof r === 'object' ? r.alert || r.risk || Object.values(r).join(' - ') : r}
                </li>
              ))}
              {(!data.risk_alerts || data.risk_alerts.length === 0) && (
                <li className="text-sm text-gray-400 italic">No critical risk alerts.</li>
              )}
            </ul>
          </div>

          {/* Recommended Next Actions */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
            <h3 className="text-base font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-blue-500" />
              Recommended Next Actions
            </h3>
            <ul className="space-y-2">
              {(data.recommended_next_actions || []).map((a: any, i: number) => (
                <li key={i} className="flex items-start gap-2 text-sm text-gray-700 dark:text-gray-300">
                  <CheckSquare className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
                  {typeof a === 'object' ? a.action || Object.values(a).join(' - ') : a}
                </li>
              ))}
              {(!data.recommended_next_actions || data.recommended_next_actions.length === 0) && (
                <li className="text-sm text-gray-400 italic">No actions recommended yet.</li>
              )}
            </ul>
          </div>

          {/* Weekly Priorities */}
          <div className="lg:col-span-2 bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
            <h3 className="text-base font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <CheckSquare className="w-5 h-5 text-purple-500" />
              Weekly Priorities
            </h3>
            <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {(data.weekly_priorities || []).map((p: any, i: number) => (
                <li key={i} className="flex items-start gap-2 text-sm text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-900/50 p-3 rounded-lg">
                  <span className="font-bold text-purple-600 dark:text-purple-400 mr-1">{i + 1}.</span>
                  {typeof p === 'object' ? p.priority || Object.values(p).join(' - ') : p}
                </li>
              ))}
              {(!data.weekly_priorities || data.weekly_priorities.length === 0) && (
                <li className="text-sm text-gray-400 italic col-span-2">No weekly priorities set.</li>
              )}
            </ul>
          </div>

          {/* Missing Information */}
          {data.missing_information && data.missing_information.length > 0 && (
            <div className="lg:col-span-2 bg-amber-50 dark:bg-amber-900/20 rounded-2xl border border-amber-200 dark:border-amber-800 p-6">
              <h3 className="text-base font-bold text-amber-800 dark:text-amber-300 mb-4">
                Missing Information
              </h3>
              <ul className="space-y-1">
                {data.missing_information.map((m: any, i: number) => (
                  <li key={i} className="text-sm text-amber-700 dark:text-amber-400">
                    • {typeof m === 'object' ? m.item || Object.values(m).join(' - ') : m}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
