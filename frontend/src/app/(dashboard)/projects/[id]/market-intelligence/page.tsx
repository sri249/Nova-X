"use client";

import { useEffect, useState, use } from "react";
import { Loader2, BarChart2, Zap } from "lucide-react";
import api from "@/lib/api";
import { EditableField } from "@/components/ui/EditableField";
import { MarketSizeChart } from "@/components/charts/MarketSizeChart";

export default function MarketIntelligencePage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
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
      const res = await api.get(`/projects/${projectId}/market-intelligence`);
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
      await api.post(`/projects/${projectId}/market-intelligence`, {});
      await fetchData();
    } catch (err: any) {
      console.error(err);
      setGenerateError(err?.response?.data?.detail || 'Failed to generate market intelligence.');
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 text-blue-500 animate-spin" />
      </div>
    );
  }

  const tamSamSomData = data ? [
    { name: "TAM", value: parseFloat(data.tam_sam_som?.TAM?.replace(/[^0-9.-]+/g,"")) || 0 },
    { name: "SAM", value: parseFloat(data.tam_sam_som?.SAM?.replace(/[^0-9.-]+/g,"")) || 0 },
    { name: "SOM", value: parseFloat(data.tam_sam_som?.SOM?.replace(/[^0-9.-]+/g,"")) || 0 },
  ] : [];

  return (
    <div className="space-y-8 fade-in">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <BarChart2 className="w-6 h-6 text-blue-500" />
            Market Intelligence
          </h1>
          <p className="text-gray-500 dark:text-gray-400 mt-1">
            Deep analysis of market size, trends, and competitors.
          </p>
        </div>
        <button
          onClick={handleGenerate}
          disabled={generating}
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white text-sm font-semibold rounded-xl shadow-sm transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {generating ? (
            <><Loader2 className="w-4 h-4 animate-spin" /> Generating...</>
          ) : (
            <><Zap className="w-4 h-4" /> {data ? 'Regenerate' : 'Generate Intelligence'}</>
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
          <div className="w-16 h-16 bg-blue-50 dark:bg-blue-900/20 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <BarChart2 className="w-8 h-8 text-blue-500" />
          </div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2">No Market Intelligence yet</h2>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-6 max-w-sm mx-auto">
            Generate TAM/SAM/SOM analysis, market trends, competitive matrix, and market readiness score.
          </p>
          <button
            onClick={handleGenerate}
            disabled={generating}
            className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold rounded-xl shadow-sm disabled:opacity-50"
          >
            {generating ? <><Loader2 className="w-4 h-4 animate-spin" /> Generating...</> : <><Zap className="w-4 h-4" /> Generate Market Intelligence</>}
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 lg:col-span-2">
             <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">TAM / SAM / SOM</h3>
             <MarketSizeChart data={tamSamSomData} />
             <div className="mt-4">
               <EditableField projectId={projectId} module="market-intelligence" fieldName="tam_sam_som" initialValue={data.tam_sam_som} type="json" />
             </div>
          </div>

          <EditableField projectId={projectId} module="market-intelligence" fieldName="industry_growth_rate" initialValue={data.industry_growth_rate} label="Industry Growth Rate" />
          <EditableField projectId={projectId} module="market-intelligence" fieldName="cagr" initialValue={data.cagr} label="CAGR" />
          <EditableField projectId={projectId} module="market-intelligence" fieldName="market_maturity" initialValue={data.market_maturity} label="Market Maturity" />
          <EditableField projectId={projectId} module="market-intelligence" fieldName="adoption_curve" initialValue={data.adoption_curve} label="Adoption Curve" />
          
          <div className="lg:col-span-2">
            <EditableField projectId={projectId} module="market-intelligence" fieldName="customer_personas" initialValue={data.customer_personas} label="Customer Personas" type="json" />
          </div>
          
          <div className="lg:col-span-2">
            <EditableField projectId={projectId} module="market-intelligence" fieldName="market_trends" initialValue={data.market_trends} label="Market Trends" type="json" />
          </div>
          
          <div className="lg:col-span-2">
            <EditableField projectId={projectId} module="market-intelligence" fieldName="competitor_matrix" initialValue={data.competitor_matrix} label="Competitor Matrix" type="json" />
          </div>

          <div className="lg:col-span-2">
            <EditableField projectId={projectId} module="market-intelligence" fieldName="market_gap_analysis" initialValue={data.market_gap_analysis} label="Market Gap Analysis" type="textarea" />
          </div>
          
          <div className="lg:col-span-2">
            <EditableField projectId={projectId} module="market-intelligence" fieldName="swot_analysis" initialValue={data.swot_analysis} label="Market SWOT Analysis" type="json" />
          </div>
          
          <EditableField projectId={projectId} module="market-intelligence" fieldName="barriers_to_entry" initialValue={data.barriers_to_entry} label="Barriers to Entry" type="json" />
          <EditableField projectId={projectId} module="market-intelligence" fieldName="regulatory_risks" initialValue={data.regulatory_risks} label="Regulatory Risks" type="json" />
          <EditableField projectId={projectId} module="market-intelligence" fieldName="geographic_expansion" initialValue={data.geographic_expansion} label="Geographic Expansion" type="json" />
          <EditableField projectId={projectId} module="market-intelligence" fieldName="emerging_technologies" initialValue={data.emerging_technologies} label="Emerging Technologies" type="json" />
        </div>
      )}
      
      {data?.ai_metadata && (
        <div className="text-xs text-gray-400 mt-8 flex gap-4">
           <span>Confidence: {data.ai_metadata.confidence_score}%</span>
           <span>Model: {data.ai_metadata.model_version}</span>
        </div>
      )}
    </div>
  );
}
