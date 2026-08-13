"use client";

import { useState, useEffect } from "react";
import api from "@/lib/api";
import { use } from "react";
import { 
  ArrowRight, 
  Lightbulb, 
  Activity, 
  Rocket, 
  DownloadCloud, 
  Settings, 
  CheckCircle2, 
  Clock, 
  TrendingUp,
  BarChart2,
  Dna,
  Banknote,
  ShieldAlert,
  Briefcase,
  AlertTriangle,
  MessageCircle
} from "lucide-react";
import Link from "next/link";
import { format } from "date-fns";
import { StartupHealthRadar } from "@/components/charts/StartupHealthRadar";

export default function ProjectHub({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const projectId = resolvedParams.id;
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchProjectData();
  }, [projectId]);

  const fetchProjectData = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await api.get(`/projects/${projectId}/export`);
      setData(res.data);
    } catch (err: any) {
      if (err?.response?.status === 401) {
        setError("Authentication error. Please log in again.");
      } else if (err?.response?.status === 404) {
        setError("Project not found.");
      } else {
        setError("Failed to load project data.");
        console.error(err);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleExport = () => {
    if (!data) return;
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${data.project?.name || 'startup'}_export.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return <div className="p-8 text-center text-red-500 font-medium">{error}</div>;
  }

  if (!data || !data.project) return <div className="p-8 text-center text-gray-500">Project not found</div>;

  const { 
    project, problem_discovery, innovation_dna, startup_profile, 
    market_intelligence, financial_planner, startup_score,
    investor_hub, risk_profile, task_planner, ai_mentor_analysis
  } = data;

  const problemScore = problem_discovery?.opportunity_score || 0;
  const innovationScore = innovation_dna?.innovation_score || 0;
  
  // Use actual overall score if available, otherwise fallback
  const overallScore = startup_score?.overall_score || Math.round((problemScore + innovationScore) / 2) || 0;

  const radarData = startup_score ? [
    { subject: 'Innovation', A: startup_score.innovation_score, fullMark: 100 },
    { subject: 'Market', A: startup_score.market_score, fullMark: 100 },
    { subject: 'Business', A: startup_score.business_score, fullMark: 100 },
    { subject: 'Financial', A: startup_score.financial_score, fullMark: 100 },
    { subject: 'Technology', A: startup_score.technology_score, fullMark: 100 },
    { subject: 'Scalability', A: startup_score.scalability_score, fullMark: 100 },
    { subject: 'Execution', A: startup_score.execution_score, fullMark: 100 },
  ] : [];

  return (
    <div className="space-y-8 fade-in">
      {/* Header & Status */}
      <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">{project.name}</h1>
            <span className={`px-3 py-1 text-xs font-medium rounded-full ${
              project.status === 'Completed' ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' :
              project.status === 'Generating' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400' :
              'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300'
            }`}>
              {project.status || 'Draft'}
            </span>
          </div>
          <p className="text-gray-600 dark:text-gray-400 max-w-2xl">{project.description}</p>
          <div className="flex items-center gap-4 mt-4 text-sm text-gray-500 dark:text-gray-400">
            <div className="flex items-center gap-1">
              <Clock className="w-4 h-4" />
              <span>Updated {format(new Date(project.updated_at || project.created_at), 'MMM d, yyyy')}</span>
            </div>
            <div className="flex items-center gap-1">
              <CheckCircle2 className="w-4 h-4 text-green-500" />
              <span>{project.completion_percentage || 0}% Complete</span>
            </div>
          </div>
        </div>

        <div className="flex gap-3">
          <button onClick={handleExport} className="flex items-center gap-2 px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors shadow-sm">
            <DownloadCloud className="w-4 h-4" /> Export JSON
          </button>
          <Link href={`/projects/${projectId}/settings`} className="flex items-center gap-2 px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors shadow-sm">
            <Settings className="w-4 h-4" /> Settings
          </Link>
        </div>
      </div>

      {/* Executive Summary Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
          <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Startup Health</p>
          <h3 className="text-3xl font-bold text-gray-900 dark:text-white mt-1">{overallScore}<span className="text-lg text-gray-400">/100</span></h3>
        </div>
        
        <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
          <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Market Readiness</p>
          <h3 className="text-3xl font-bold text-gray-900 dark:text-white mt-1">{market_intelligence?.market_readiness_score || 0}<span className="text-lg text-gray-400">/100</span></h3>
        </div>
        
        <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
          <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Funding Needed</p>
          <h3 className="text-2xl font-bold text-gray-900 dark:text-white mt-2">{financial_planner?.funding_requirement || "N/A"}</h3>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
          <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Runway</p>
          <h3 className="text-2xl font-bold text-gray-900 dark:text-white mt-2">{financial_planner?.runway || "N/A"}</h3>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
            <Activity className="w-5 h-5 text-blue-500" />
            Startup Health Radar
          </h2>
          {radarData.length > 0 ? (
            <StartupHealthRadar data={radarData} />
          ) : (
            <div className="flex items-center justify-center h-[300px] text-gray-400">
              Complete generation to view health radar
            </div>
          )}
        </div>
        <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-y-auto max-h-[400px]">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-yellow-500" />
            AI Recommendations
          </h2>
          {ai_mentor_analysis ? (
             <div className="space-y-4">
               <div>
                 <h4 className="text-sm font-semibold text-red-500 flex items-center gap-1"><AlertTriangle className="w-4 h-4"/> Critical Risks</h4>
                 <ul className="list-disc pl-5 mt-1 text-sm text-gray-600 dark:text-gray-400">
                   {ai_mentor_analysis.risk_alerts?.map((r: any, i: number) => <li key={i}>{r.alert || r}</li>)}
                 </ul>
               </div>
               <div>
                 <h4 className="text-sm font-semibold text-yellow-500">Highest Priority Actions</h4>
                 <ul className="list-disc pl-5 mt-1 text-sm text-gray-600 dark:text-gray-400">
                   {ai_mentor_analysis.recommended_next_actions?.map((r: any, i: number) => <li key={i}>{r.action || r}</li>)}
                 </ul>
               </div>
               <div className="mt-4 pt-4 border-t border-gray-100 dark:border-gray-700">
                 <Link href={`/projects/${projectId}/chat`} className="text-blue-500 text-sm font-medium hover:underline flex items-center gap-1">
                   Chat with AI Co-Founder <ArrowRight className="w-4 h-4"/>
                 </Link>
               </div>
             </div>
          ) : startup_score?.ai_recommendations ? (
             <div className="space-y-4">
               <div>
                 <h4 className="text-sm font-semibold text-red-500">Critical Risks</h4>
                 <ul className="list-disc pl-5 mt-1 text-sm text-gray-600 dark:text-gray-400">
                   {startup_score.ai_recommendations.critical_risks?.map((r: string, i: number) => <li key={i}>{r}</li>)}
                 </ul>
               </div>
               <div>
                 <h4 className="text-sm font-semibold text-yellow-500">Immediate Actions</h4>
                 <ul className="list-disc pl-5 mt-1 text-sm text-gray-600 dark:text-gray-400">
                   {startup_score.ai_recommendations.immediate_actions?.map((r: string, i: number) => <li key={i}>{r}</li>)}
                 </ul>
               </div>
             </div>
          ) : (
            <div className="text-sm text-gray-400 space-y-4">
              <p>No recommendations available.</p>
              <button 
                onClick={async () => {
                  await api.post(`/projects/${projectId}/ai-mentor`, {});
                  window.location.reload();
                }}
                className="text-blue-500 font-medium hover:underline"
              >
                Generate Mentor Analysis
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Modules */}
      <h2 className="text-xl font-bold text-gray-900 dark:text-white mt-8 mb-4">Project Modules</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        <Link href={`/projects/${projectId}/problem-discovery`} className="group block bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md hover:border-blue-500 transition-all">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-xl">
              <Lightbulb className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
            {problem_discovery ? (
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            ) : (
              <span className="text-xs font-medium text-gray-400 border border-gray-200 dark:border-gray-700 px-2 py-1 rounded-md">Pending</span>
            )}
          </div>
          <h3 className="text-lg font-bold text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">Problem Discovery</h3>
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-400 line-clamp-2">
            {problem_discovery?.problem_summary || "Analyze the root problem, market gap, and calculate the opportunity score."}
          </p>
          <div className="mt-4 flex items-center text-sm font-medium text-blue-600 dark:text-blue-400">
            View Details <ArrowRight className="ml-1 w-4 h-4 transform group-hover:translate-x-1 transition-transform" />
          </div>
        </Link>

        <Link href={`/projects/${projectId}/innovation-dna`} className="group block bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md hover:border-purple-500 transition-all">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-purple-50 dark:bg-purple-900/20 rounded-xl">
              <Dna className="w-6 h-6 text-purple-600 dark:text-purple-400" />
            </div>
            {innovation_dna ? (
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            ) : (
              <span className="text-xs font-medium text-gray-400 border border-gray-200 dark:border-gray-700 px-2 py-1 rounded-md">Pending</span>
            )}
          </div>
          <h3 className="text-lg font-bold text-gray-900 dark:text-white group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">Innovation DNA</h3>
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-400 line-clamp-2">
            {innovation_dna?.unique_value_proposition || "Identify unfair advantages, unique value propositions, and differentiation."}
          </p>
          <div className="mt-4 flex items-center text-sm font-medium text-purple-600 dark:text-purple-400">
            View Details <ArrowRight className="ml-1 w-4 h-4 transform group-hover:translate-x-1 transition-transform" />
          </div>
        </Link>

        <Link href={`/projects/${projectId}/startup-formation`} className="group block bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md hover:border-green-500 transition-all">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-green-50 dark:bg-green-900/20 rounded-xl">
              <Rocket className="w-6 h-6 text-green-600 dark:text-green-400" />
            </div>
            {startup_profile ? (
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            ) : (
              <span className="text-xs font-medium text-gray-400 border border-gray-200 dark:border-gray-700 px-2 py-1 rounded-md">Pending</span>
            )}
          </div>
          <h3 className="text-lg font-bold text-gray-900 dark:text-white group-hover:text-green-600 dark:group-hover:text-green-400 transition-colors">Startup Formation</h3>
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-400 line-clamp-2">
            {startup_profile?.elevator_pitch || "Generate the complete startup profile, business model, and branding."}
          </p>
          <div className="mt-4 flex items-center text-sm font-medium text-green-600 dark:text-green-400">
            View Details <ArrowRight className="ml-1 w-4 h-4 transform group-hover:translate-x-1 transition-transform" />
          </div>
        </Link>

        <Link href={`/projects/${projectId}/market-intelligence`} className="group block bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md hover:border-blue-500 transition-all">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-xl">
              <BarChart2 className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
            {market_intelligence ? (
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            ) : (
              <span className="text-xs font-medium text-gray-400 border border-gray-200 dark:border-gray-700 px-2 py-1 rounded-md">Pending</span>
            )}
          </div>
          <h3 className="text-lg font-bold text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">Market Intelligence</h3>
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-400 line-clamp-2">
            {market_intelligence?.market_gap_analysis || "TAM/SAM/SOM, Trends, Competitor Matrix."}
          </p>
          <div className="mt-4 flex items-center text-sm font-medium text-blue-600 dark:text-blue-400">
            View Details <ArrowRight className="ml-1 w-4 h-4 transform group-hover:translate-x-1 transition-transform" />
          </div>
        </Link>

        <Link href={`/projects/${projectId}/financial-planner`} className="group block bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md hover:border-green-500 transition-all">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-green-50 dark:bg-green-900/20 rounded-xl">
              <Banknote className="w-6 h-6 text-green-600 dark:text-green-400" />
            </div>
            {financial_planner ? (
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            ) : (
              <span className="text-xs font-medium text-gray-400 border border-gray-200 dark:border-gray-700 px-2 py-1 rounded-md">Pending</span>
            )}
          </div>
          <h3 className="text-lg font-bold text-gray-900 dark:text-white group-hover:text-green-600 dark:group-hover:text-green-400 transition-colors">Financial Planner</h3>
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-400 line-clamp-2">
            {financial_planner?.funding_recommendation || "Revenue forecasts, operating costs, and runway."}
          </p>
          <div className="mt-4 flex items-center text-sm font-medium text-green-600 dark:text-green-400">
            View Details <ArrowRight className="ml-1 w-4 h-4 transform group-hover:translate-x-1 transition-transform" />
          </div>
        </Link>

        {/* Phase 5 Modules */}
        <Link href={`/projects/${projectId}/investor-hub`} className="group block bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md hover:border-indigo-500 transition-all">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-indigo-50 dark:bg-indigo-900/20 rounded-xl">
              <Briefcase className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
            </div>
            {investor_hub ? (
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            ) : (
              <span className="text-xs font-medium text-gray-400 border border-gray-200 dark:border-gray-700 px-2 py-1 rounded-md">Pending</span>
            )}
          </div>
          <h3 className="text-lg font-bold text-gray-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">Investor Hub</h3>
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-400 line-clamp-2">
            Pitch Deck, Investment Memo, and Due Diligence prep.
          </p>
          <div className="mt-4 flex items-center text-sm font-medium text-indigo-600 dark:text-indigo-400">
            View Details <ArrowRight className="ml-1 w-4 h-4 transform group-hover:translate-x-1 transition-transform" />
          </div>
        </Link>

        <Link href={`/projects/${projectId}/risks-tasks`} className="group block bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md hover:border-red-500 transition-all">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-red-50 dark:bg-red-900/20 rounded-xl">
              <AlertTriangle className="w-6 h-6 text-red-600 dark:text-red-400" />
            </div>
            {risk_profile || task_planner ? (
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            ) : (
              <span className="text-xs font-medium text-gray-400 border border-gray-200 dark:border-gray-700 px-2 py-1 rounded-md">Pending</span>
            )}
          </div>
          <h3 className="text-lg font-bold text-gray-900 dark:text-white group-hover:text-red-600 dark:group-hover:text-red-400 transition-colors">Risks & Tasks</h3>
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-400 line-clamp-2">
            Identify core risks and generate actionable 30/90-day roadmaps.
          </p>
          <div className="mt-4 flex items-center text-sm font-medium text-red-600 dark:text-red-400">
            View Details <ArrowRight className="ml-1 w-4 h-4 transform group-hover:translate-x-1 transition-transform" />
          </div>
        </Link>
      </div>
    </div>
  );
}
