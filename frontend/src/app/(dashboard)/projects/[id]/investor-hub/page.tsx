"use client";

import { useEffect, useState, use } from "react";
import { Loader2, Briefcase, FileText, FileJson, CheckCircle2 } from "lucide-react";
import api from "@/lib/api";
import { EditableField } from "@/components/ui/EditableField";

export default function InvestorHubPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const resolvedParams = use(params);
  const projectId = resolvedParams.id;
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    fetchData();
  }, [projectId]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await api.get(`/projects/${projectId}/investor-hub`);
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
    try {
      await api.post(`/projects/${projectId}/investor-hub`, {});
      await fetchData();
    } catch (err: any) {
      if (err?.response?.status !== 404) console.error(err);
    } finally {
      setGenerating(false);
    }
  };

  const exportPitchDeck = () => {
    if (!data?.pitch_deck) return;
    const blob = new Blob([JSON.stringify(data.pitch_deck, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `pitch_deck_${projectId}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  if (loading && !data) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 text-blue-500 animate-spin" />
      </div>
    );
  }

  if (!data && !loading) {
    return (
      <div className="text-center py-16 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
        <Briefcase className="mx-auto h-16 w-16 text-gray-400 mb-4" />
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Investor Hub</h2>
        <p className="text-gray-500 dark:text-gray-400 mb-6 max-w-md mx-auto">Generate structured investment materials, pitch decks, and memos based on your complete startup profile.</p>
        <button 
          onClick={handleGenerate} 
          disabled={generating}
          className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-lg shadow-sm text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
        >
          {generating ? <><Loader2 className="animate-spin mr-2 h-5 w-5"/> Generating...</> : "Generate Investor Materials"}
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-8 fade-in">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Briefcase className="w-6 h-6 text-indigo-500" />
            Investor Hub
          </h1>
          <p className="text-gray-500 dark:text-gray-400 mt-1">
            Memos, Executive Summaries, and Pitch Deck generator.
          </p>
        </div>
        <div className="flex gap-2">
           <button onClick={handleGenerate} disabled={generating} className="flex items-center gap-2 px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-700">
             {generating ? <Loader2 className="w-4 h-4 animate-spin"/> : <Briefcase className="w-4 h-4"/>}
             Regenerate All
           </button>
           <button onClick={exportPitchDeck} className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700">
             <FileJson className="w-4 h-4"/>
             Export Pitch Deck JSON
           </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="lg:col-span-2">
          <EditableField projectId={projectId} module="investor-hub" fieldName="executive_summary" initialValue={data.executive_summary} label="Executive Summary" type="textarea" />
        </div>
        <div className="lg:col-span-2">
          <EditableField projectId={projectId} module="investor-hub" fieldName="investment_memo" initialValue={data.investment_memo} label="Investment Memo" type="textarea" />
        </div>
        
        <EditableField projectId={projectId} module="investor-hub" fieldName="funding_strategy" initialValue={data.funding_strategy} label="Funding Strategy" type="textarea" />
        <EditableField projectId={projectId} module="investor-hub" fieldName="one_page_profile" initialValue={data.one_page_profile} label="One-Page Profile" type="json" />
        <EditableField projectId={projectId} module="investor-hub" fieldName="due_diligence_checklist" initialValue={data.due_diligence_checklist} label="Due Diligence Checklist" type="json" />
        <EditableField projectId={projectId} module="investor-hub" fieldName="milestone_roadmap" initialValue={data.milestone_roadmap} label="Milestone Roadmap" type="json" />

        {/* Pitch Deck Preview */}
        <div className="lg:col-span-2 bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700">
           <h3 className="text-lg font-bold mb-4 flex items-center gap-2"><FileText className="text-indigo-500 w-5 h-5"/> Pitch Deck Preview</h3>
           <div className="space-y-4 max-h-[600px] overflow-y-auto pr-2">
             {data.pitch_deck && Object.keys(data.pitch_deck).map((slideKey) => {
               const slide = data.pitch_deck[slideKey];
               return (
                 <div key={slideKey} className="p-4 border border-gray-100 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-900/50">
                   <h4 className="font-bold text-gray-900 dark:text-white capitalize">{slideKey.replace('_', ' ')}: {slide.title}</h4>
                   {slide.subtitle && <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{slide.subtitle}</p>}
                   <ul className="mt-3 space-y-1">
                     {slide.bullet_points?.map((bp: string, i: number) => (
                       <li key={i} className="text-sm flex items-start gap-2 text-gray-700 dark:text-gray-300">
                         <CheckCircle2 className="w-4 h-4 text-indigo-500 mt-0.5 flex-shrink-0" />
                         <span>{bp}</span>
                       </li>
                     ))}
                   </ul>
                 </div>
               )
             })}
           </div>
        </div>
      </div>
      
      {data.ai_metadata && (
        <div className="text-xs text-gray-400 mt-8 flex gap-4">
           <span>Confidence: {data.ai_metadata.confidence_score}%</span>
           <span>Model: {data.ai_metadata.model_version}</span>
        </div>
      )}
    </div>
  );
}
