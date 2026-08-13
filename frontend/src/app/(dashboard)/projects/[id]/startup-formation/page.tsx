"use client";

import { useState, useEffect } from 'react';
import api from '@/lib/api';
import { use } from 'react';
import { EditableField } from '@/components/ui/EditableField';
import { Loader2, Rocket, Zap } from 'lucide-react';

export default function StartupFormationPage({ params }: { params: Promise<{ id: string }> }) {
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
      const res = await api.get(`/projects/${projectId}/startup-formation`);
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
      await api.post(`/projects/${projectId}/startup-formation`, {});
      await fetchData();
    } catch (err: any) {
      console.error(err);
      const detail = err?.response?.data?.detail;
      setGenerateError(
        typeof detail === 'string'
          ? detail
          : 'Failed to generate. Make sure Problem Discovery and Innovation DNA are generated first.'
      );
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader2 className="w-8 h-8 text-green-600 animate-spin" />
      </div>
    );
  }

  const profile = data?.profile;
  const business_model = data?.business_model;

  return (
    <div className="space-y-8 fade-in pb-16">
      <div className="mb-8 flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Startup Formation</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">Generate the complete startup profile, business model, and branding.</p>
        </div>
        <button
          onClick={handleGenerate}
          disabled={generating}
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 text-white text-sm font-semibold rounded-xl shadow-sm transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {generating ? (
            <><Loader2 className="w-4 h-4 animate-spin" /> Generating...</>
          ) : (
            <><Rocket className="w-4 h-4" /> {data ? 'Regenerate' : 'Generate Formation'}</>
          )}
        </button>
      </div>

      {generateError && (
        <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-red-600 dark:text-red-400 text-sm">
          {generateError}
        </div>
      )}

      {!profile ? (
        <div className="text-center py-24 bg-white dark:bg-gray-800 rounded-2xl border-2 border-dashed border-gray-200 dark:border-gray-700">
          <div className="w-16 h-16 bg-green-50 dark:bg-green-900/20 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <Rocket className="w-8 h-8 text-green-500" />
          </div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Startup Formation not generated</h2>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-2 max-w-sm mx-auto">
            Generate your complete startup profile, business model, and branding strategy.
          </p>
          <p className="text-xs text-gray-400 dark:text-gray-500 mb-6">
            Requires Problem Discovery & Innovation DNA to be generated first.
          </p>
          <button
            onClick={handleGenerate}
            disabled={generating}
            className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white font-semibold rounded-xl shadow-sm disabled:opacity-50"
          >
            {generating ? <><Loader2 className="w-4 h-4 animate-spin" /> Generating...</> : <><Rocket className="w-4 h-4" /> Generate Formation</>}
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Profile Section */}
          <div className="space-y-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white border-b pb-2">Brand Identity</h2>
            
            <EditableField 
              label="Startup Name" 
              initialValue={profile.name} 
              updateUrl={`/projects/${projectId}/startup-formation/profile/name`}
              regenerateUrl={`/projects/${projectId}/startup-formation/profile/name/regenerate`}
            />
            
            <EditableField 
              label="Tagline" 
              initialValue={profile.tagline} 
              updateUrl={`/projects/${projectId}/startup-formation/profile/tagline`}
              regenerateUrl={`/projects/${projectId}/startup-formation/profile/tagline/regenerate`}
            />
            
            <EditableField 
              label="Elevator Pitch" 
              initialValue={profile.elevator_pitch} 
              updateUrl={`/projects/${projectId}/startup-formation/profile/elevator_pitch`}
              regenerateUrl={`/projects/${projectId}/startup-formation/profile/elevator_pitch/regenerate`}
            />
            
            <EditableField 
              label="Mission Statement" 
              initialValue={profile.mission_statement} 
              updateUrl={`/projects/${projectId}/startup-formation/profile/mission_statement`}
              regenerateUrl={`/projects/${projectId}/startup-formation/profile/mission_statement/regenerate`}
            />
            
            <EditableField 
              label="Brand Personality" 
              initialValue={profile.brand_personality} 
              updateUrl={`/projects/${projectId}/startup-formation/profile/brand_personality`}
              regenerateUrl={`/projects/${projectId}/startup-formation/profile/brand_personality/regenerate`}
            />
            
            <EditableField 
              label="Color Palette" 
              initialValue={profile.color_palette || []} 
              updateUrl={`/projects/${projectId}/startup-formation/profile/color_palette`}
              regenerateUrl={`/projects/${projectId}/startup-formation/profile/color_palette/regenerate`}
            />
            
            <EditableField 
              label="Logo Prompt" 
              initialValue={profile.logo_prompt} 
              updateUrl={`/projects/${projectId}/startup-formation/profile/logo_prompt`}
              regenerateUrl={`/projects/${projectId}/startup-formation/profile/logo_prompt/regenerate`}
            />
          </div>
          
          {/* Business Model Section */}
          <div className="space-y-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white border-b pb-2">Business Strategy</h2>
            
            {business_model && (
              <>
                <EditableField 
                  label="Value Proposition" 
                  initialValue={profile.value_proposition} 
                  updateUrl={`/projects/${projectId}/startup-formation/profile/value_proposition`}
                  regenerateUrl={`/projects/${projectId}/startup-formation/profile/value_proposition/regenerate`}
                />

                <EditableField 
                  label="Unique Selling Proposition" 
                  initialValue={profile.unique_selling_proposition} 
                  updateUrl={`/projects/${projectId}/startup-formation/profile/unique_selling_proposition`}
                  regenerateUrl={`/projects/${projectId}/startup-formation/profile/unique_selling_proposition/regenerate`}
                />

                <EditableField 
                  label="Pricing Strategy" 
                  initialValue={business_model.pricing_strategy} 
                  updateUrl={`/projects/${projectId}/startup-formation/business_model/pricing_strategy`}
                  regenerateUrl={`/projects/${projectId}/startup-formation/business_model/pricing_strategy/regenerate`}
                />
                
                <EditableField 
                  label="Revenue Model (JSON)" 
                  initialValue={business_model.revenue_model || {}} 
                  updateUrl={`/projects/${projectId}/startup-formation/business_model/revenue_model`}
                  regenerateUrl={`/projects/${projectId}/startup-formation/business_model/revenue_model/regenerate`}
                  isJson={true}
                />
                
                <EditableField 
                  label="Business Model Canvas (JSON)" 
                  initialValue={business_model.business_model_canvas || {}} 
                  updateUrl={`/projects/${projectId}/startup-formation/business_model/business_model_canvas`}
                  regenerateUrl={`/projects/${projectId}/startup-formation/business_model/business_model_canvas/regenerate`}
                  isJson={true}
                />
              </>
            )}

            <h2 className="text-xl font-semibold text-gray-900 dark:text-white border-b pb-2 mt-8">Execution</h2>

            <EditableField 
              label="Product Roadmap (JSON)" 
              initialValue={profile.product_roadmap || []} 
              updateUrl={`/projects/${projectId}/startup-formation/profile/product_roadmap`}
              regenerateUrl={`/projects/${projectId}/startup-formation/profile/product_roadmap/regenerate`}
              isJson={true}
            />

            <EditableField 
              label="Launch Checklist" 
              initialValue={profile.launch_checklist || []} 
              updateUrl={`/projects/${projectId}/startup-formation/profile/launch_checklist`}
              regenerateUrl={`/projects/${projectId}/startup-formation/profile/launch_checklist/regenerate`}
            />

          </div>
        </div>
      )}
    </div>
  );
}
