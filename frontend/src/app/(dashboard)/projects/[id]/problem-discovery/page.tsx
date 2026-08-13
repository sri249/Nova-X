"use client";

import { useState, useEffect } from 'react';
import api from '@/lib/api';
import { use } from 'react';
import { EditableField } from '@/components/ui/EditableField';
import { Loader2, Zap, RefreshCw } from 'lucide-react';

export default function ProblemDiscoveryPage({ params }: { params: Promise<{ id: string }> }) {
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
      const res = await api.get(`/projects/${projectId}/problem-discovery`);
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
      // Fetch project details first to get title/description
      const projectRes = await api.get(`/projects/${projectId}`);
      const project = projectRes.data;
      await api.post(`/projects/${projectId}/problem-discovery`, {
        title: project.name,
        description: project.description,
        industry: 'Not specified',
        country: 'Not specified',
        target_users: 'Not specified',
        existing_solutions: 'Not specified',
        pain_points: 'Not specified'
      });
      await fetchData();
    } catch (err: any) {
      console.error(err);
      setGenerateError(err?.response?.data?.detail || 'Failed to generate. Please try again.');
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-8 fade-in pb-16">
      <div className="mb-8 flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Problem Discovery</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">Analyze the root problem, market gap, and opportunity score.</p>
        </div>
        <button
          onClick={handleGenerate}
          disabled={generating}
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-sm font-semibold rounded-xl shadow-sm transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {generating ? (
            <><Loader2 className="w-4 h-4 animate-spin" /> Generating...</>
          ) : (
            <><Zap className="w-4 h-4" /> {data ? 'Regenerate' : 'Generate Analysis'}</>
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
            <Zap className="w-8 h-8 text-blue-500" />
          </div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2">No analysis yet</h2>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-6 max-w-sm mx-auto">
            Click "Generate Analysis" to let NOVA X AI discover the core problem, root causes, and opportunity score.
          </p>
          <button
            onClick={handleGenerate}
            disabled={generating}
            className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl shadow-sm disabled:opacity-50"
          >
            {generating ? <><Loader2 className="w-4 h-4 animate-spin" /> Generating...</> : <><Zap className="w-4 h-4" /> Generate Analysis</>}
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-6">
            <EditableField 
              label="Core Problem Summary" 
              initialValue={data.problem_summary || data.core_problem} 
              updateUrl={`/projects/${projectId}/problem-discovery/problem_summary`}
              regenerateUrl={`/projects/${projectId}/problem-discovery/problem_summary/regenerate`}
            />
            
            <EditableField 
              label="Root Cause Analysis" 
              initialValue={data.root_cause_analysis} 
              updateUrl={`/projects/${projectId}/problem-discovery/root_cause_analysis`}
              regenerateUrl={`/projects/${projectId}/problem-discovery/root_cause_analysis/regenerate`}
              isJson={true}
            />
            
            <EditableField 
              label="Impact Analysis" 
              initialValue={data.impact_analysis} 
              updateUrl={`/projects/${projectId}/problem-discovery/impact_analysis`}
              regenerateUrl={`/projects/${projectId}/problem-discovery/impact_analysis/regenerate`}
              isJson={true}
            />
            
            <EditableField 
              label="Key Insights" 
              initialValue={data.key_insights || []} 
              updateUrl={`/projects/${projectId}/problem-discovery/key_insights`}
              regenerateUrl={`/projects/${projectId}/problem-discovery/key_insights/regenerate`}
            />
          </div>
          
          <div className="space-y-6">
            <div className="bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl p-6 text-white shadow-lg">
              <h3 className="text-sm font-medium opacity-80 uppercase tracking-wide">Opportunity Score</h3>
              <div className="mt-2 flex items-baseline gap-2">
                <span className="text-5xl font-extrabold">{data.opportunity_score || 0}</span>
                <span className="text-xl opacity-80">/ 100</span>
              </div>
              <p className="mt-4 text-sm opacity-90">A measure of the market size and urgency of the problem.</p>
            </div>

            <EditableField 
              label="SDG Alignment" 
              initialValue={data.sdg_alignment || []} 
              updateUrl={`/projects/${projectId}/problem-discovery/sdg_alignment`}
              regenerateUrl={`/projects/${projectId}/problem-discovery/sdg_alignment/regenerate`}
            />

            <EditableField 
              label="Stakeholders" 
              initialValue={data.stakeholders || []} 
              updateUrl={`/projects/${projectId}/problem-discovery/stakeholders`}
              regenerateUrl={`/projects/${projectId}/problem-discovery/stakeholders/regenerate`}
            />
          </div>
        </div>
      )}
    </div>
  );
}
