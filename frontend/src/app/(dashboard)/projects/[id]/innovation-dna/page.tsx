"use client";

import { useState, useEffect } from 'react';
import api from '@/lib/api';
import { use } from 'react';
import { EditableField } from '@/components/ui/EditableField';
import { Loader2, Dna, Zap } from 'lucide-react';

export default function InnovationDNAPage({ params }: { params: Promise<{ id: string }> }) {
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
      const res = await api.get(`/projects/${projectId}/innovation-dna`);
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
      await api.post(`/projects/${projectId}/innovation-dna`, {});
      await fetchData();
    } catch (err: any) {
      console.error(err);
      setGenerateError(err?.response?.data?.detail || 'Failed to generate. Make sure Problem Discovery is generated first.');
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader2 className="w-8 h-8 text-purple-600 animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-8 fade-in pb-16">
      <div className="mb-8 flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Innovation DNA</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">Identify unfair advantages, unique value propositions, and differentiation.</p>
        </div>
        <button
          onClick={handleGenerate}
          disabled={generating}
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white text-sm font-semibold rounded-xl shadow-sm transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {generating ? (
            <><Loader2 className="w-4 h-4 animate-spin" /> Generating...</>
          ) : (
            <><Dna className="w-4 h-4" /> {data ? 'Regenerate' : 'Generate Innovation DNA'}</>
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
          <div className="w-16 h-16 bg-purple-50 dark:bg-purple-900/20 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <Dna className="w-8 h-8 text-purple-500" />
          </div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Innovation DNA not generated</h2>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-6 max-w-sm mx-auto">
            Generate Innovation DNA to identify your unfair advantages, value propositions, and differentiation strategy.
          </p>
          <button
            onClick={handleGenerate}
            disabled={generating}
            className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl shadow-sm disabled:opacity-50"
          >
            {generating ? <><Loader2 className="w-4 h-4 animate-spin" /> Generating...</> : <><Dna className="w-4 h-4" /> Generate Innovation DNA</>}
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-6">
            <EditableField 
              label="Unique Value Proposition" 
              initialValue={data.unique_value_proposition} 
              updateUrl={`/projects/${projectId}/innovation-dna/unique_value_proposition`}
              regenerateUrl={`/projects/${projectId}/innovation-dna/unique_value_proposition/regenerate`}
            />
            
            <EditableField 
              label="Unfair Advantage / Market Gap" 
              initialValue={data.market_gap || data.unfair_advantage} 
              updateUrl={`/projects/${projectId}/innovation-dna/market_gap`}
              regenerateUrl={`/projects/${projectId}/innovation-dna/market_gap/regenerate`}
            />
            
            <EditableField 
              label="Novelty Analysis" 
              initialValue={data.novelty_analysis} 
              updateUrl={`/projects/${projectId}/innovation-dna/novelty_analysis`}
              regenerateUrl={`/projects/${projectId}/innovation-dna/novelty_analysis/regenerate`}
            />
            
            <EditableField 
              label="Differentiation" 
              initialValue={data.differentiation || []} 
              updateUrl={`/projects/${projectId}/innovation-dna/differentiation`}
              regenerateUrl={`/projects/${projectId}/innovation-dna/differentiation/regenerate`}
            />
            
            <EditableField 
              label="Competitor Overview" 
              initialValue={data.competitor_overview || []} 
              updateUrl={`/projects/${projectId}/innovation-dna/competitor_overview`}
              regenerateUrl={`/projects/${projectId}/innovation-dna/competitor_overview/regenerate`}
            />
          </div>
          
          <div className="space-y-6">
            <div className="bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl p-6 text-white shadow-lg">
              <h3 className="text-sm font-medium opacity-80 uppercase tracking-wide">Innovation Score</h3>
              <div className="mt-2 flex items-baseline gap-2">
                <span className="text-5xl font-extrabold">{data.innovation_score || 0}</span>
                <span className="text-xl opacity-80">/ 100</span>
              </div>
              <div className="mt-4 pt-4 border-t border-white/20 flex justify-between items-center">
                <span className="text-sm font-medium opacity-90">Originality Score</span>
                <span className="text-xl font-bold">{data.originality_score || 0}/100</span>
              </div>
            </div>

            <EditableField 
              label="Patent Potential" 
              initialValue={data.patent_potential_indicator} 
              updateUrl={`/projects/${projectId}/innovation-dna/patent_potential_indicator`}
              regenerateUrl={`/projects/${projectId}/innovation-dna/patent_potential_indicator/regenerate`}
            />

            <EditableField 
              label="Innovation Radar (JSON)" 
              initialValue={data.innovation_radar_visualization || {}} 
              updateUrl={`/projects/${projectId}/innovation-dna/innovation_radar_visualization`}
              regenerateUrl={`/projects/${projectId}/innovation-dna/innovation_radar_visualization/regenerate`}
              isJson={true}
            />
          </div>
        </div>
      )}
    </div>
  );
}
