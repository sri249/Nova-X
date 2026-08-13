"use client";

import { useEffect, useState, use } from "react";
import { Loader2, Banknote, Zap } from "lucide-react";
import api from "@/lib/api";
import { EditableField } from "@/components/ui/EditableField";
import { RevenueForecastChart } from "@/components/charts/RevenueForecastChart";

export default function FinancialPlannerPage({
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
      const res = await api.get(`/projects/${projectId}/financial-planner`);
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
      await api.post(`/projects/${projectId}/financial-planner`, {});
      await fetchData();
    } catch (err: any) {
      console.error(err);
      setGenerateError(err?.response?.data?.detail || 'Failed to generate financial plan.');
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

  return (
    <div className="space-y-8 fade-in">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Banknote className="w-6 h-6 text-green-500" />
            Financial Planner
          </h1>
          <p className="text-gray-500 dark:text-gray-400 mt-1">
            Revenue forecasts, cost structures, and investment requirements.
          </p>
        </div>
        <button
          onClick={handleGenerate}
          disabled={generating}
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 text-white text-sm font-semibold rounded-xl shadow-sm transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {generating ? (
            <><Loader2 className="w-4 h-4 animate-spin" /> Generating...</>
          ) : (
            <><Zap className="w-4 h-4" /> {data ? 'Regenerate' : 'Generate Financial Plan'}</>
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
          <div className="w-16 h-16 bg-green-50 dark:bg-green-900/20 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <Banknote className="w-8 h-8 text-green-500" />
          </div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2">No Financial Plan yet</h2>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-6 max-w-sm mx-auto">
            Generate revenue forecasts, startup costs, burn rate, runway, and funding requirements.
          </p>
          <button
            onClick={handleGenerate}
            disabled={generating}
            className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white font-semibold rounded-xl shadow-sm disabled:opacity-50"
          >
            {generating ? <><Loader2 className="w-4 h-4 animate-spin" /> Generating...</> : <><Zap className="w-4 h-4" /> Generate Financial Plan</>}
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 lg:col-span-2">
             <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Revenue vs Expenses</h3>
             <RevenueForecastChart data={data.revenue_forecast || []} />
             <div className="mt-4">
               <EditableField projectId={projectId} module="financial-planner" fieldName="revenue_forecast" initialValue={data.revenue_forecast} type="json" />
             </div>
          </div>

          <EditableField projectId={projectId} module="financial-planner" fieldName="burn_rate" initialValue={data.burn_rate} label="Burn Rate" />
          <EditableField projectId={projectId} module="financial-planner" fieldName="runway" initialValue={data.runway} label="Runway" />
          <EditableField projectId={projectId} module="financial-planner" fieldName="break_even_month" initialValue={data.break_even_month} label="Break-Even Month" />
          <EditableField projectId={projectId} module="financial-planner" fieldName="funding_requirement" initialValue={data.funding_requirement} label="Funding Requirement" />
          
          <div className="lg:col-span-2">
            <EditableField projectId={projectId} module="financial-planner" fieldName="funding_recommendation" initialValue={data.funding_recommendation} label="Funding Recommendation" type="textarea" />
          </div>
          
          <EditableField projectId={projectId} module="financial-planner" fieldName="roi_projection" initialValue={data.roi_projection} label="ROI Projection" />
          
          <div className="lg:col-span-2">
            <EditableField projectId={projectId} module="financial-planner" fieldName="startup_costs" initialValue={data.startup_costs} label="Startup Costs" type="json" />
          </div>
          <div className="lg:col-span-2">
            <EditableField projectId={projectId} module="financial-planner" fieldName="monthly_operating_costs" initialValue={data.monthly_operating_costs} label="Monthly Operating Costs" type="json" />
          </div>
          <div className="lg:col-span-2">
            <EditableField projectId={projectId} module="financial-planner" fieldName="hiring_costs" initialValue={data.hiring_costs} label="Hiring Costs" type="json" />
          </div>
          <div className="lg:col-span-2">
            <EditableField projectId={projectId} module="financial-planner" fieldName="marketing_budget" initialValue={data.marketing_budget} label="Marketing Budget" type="json" />
          </div>
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
