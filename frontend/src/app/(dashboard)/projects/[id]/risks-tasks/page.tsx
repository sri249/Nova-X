"use client";

import { useEffect, useState, use } from "react";
import { Loader2, AlertTriangle, CheckSquare, Zap } from "lucide-react";
import api from "@/lib/api";
import { EditableField } from "@/components/ui/EditableField";

export default function RisksAndTasksPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const resolvedParams = use(params);
  const projectId = resolvedParams.id;
  const [riskData, setRiskData] = useState<any>(null);
  const [taskData, setTaskData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [generatingRisks, setGeneratingRisks] = useState(false);
  const [generatingTasks, setGeneratingTasks] = useState(false);
  const [riskError, setRiskError] = useState<string | null>(null);
  const [taskError, setTaskError] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
  }, [projectId]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [r, t] = await Promise.all([
        api.get(`/projects/${projectId}/risk-engine`).catch(() => ({ data: null })),
        api.get(`/projects/${projectId}/task-planner`).catch(() => ({ data: null }))
      ]);
      setRiskData(r.data);
      setTaskData(t.data);
    } catch (err: any) {
      if (err?.response?.status !== 404) console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateRisks = async () => {
    setGeneratingRisks(true);
    setRiskError(null);
    try {
      await api.post(`/projects/${projectId}/risk-engine`, {});
      const res = await api.get(`/projects/${projectId}/risk-engine`).catch(() => ({ data: null }));
      setRiskData(res.data);
    } catch (err: any) {
      console.error(err);
      setRiskError(err?.response?.data?.detail || 'Failed to generate risks.');
    } finally {
      setGeneratingRisks(false);
    }
  };

  const handleGenerateTasks = async () => {
    setGeneratingTasks(true);
    setTaskError(null);
    try {
      await api.post(`/projects/${projectId}/task-planner`, {});
      const res = await api.get(`/projects/${projectId}/task-planner`).catch(() => ({ data: null }));
      setTaskData(res.data);
    } catch (err: any) {
      console.error(err);
      setTaskError(err?.response?.data?.detail || 'Failed to generate tasks.');
    } finally {
      setGeneratingTasks(false);
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
    <div className="space-y-12 fade-in">
      
      {/* Risk Engine Section */}
      <section>
        <div className="flex justify-between items-start mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
              <AlertTriangle className="w-6 h-6 text-red-500" />
              Risk Engine
            </h2>
            <p className="text-gray-500 dark:text-gray-400 mt-1">Identification and mitigation of core startup risks.</p>
          </div>
          <button
            onClick={handleGenerateRisks}
            disabled={generatingRisks}
            className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-500 hover:to-orange-500 text-white text-sm font-semibold rounded-xl shadow-sm transition-all disabled:opacity-50"
          >
            {generatingRisks ? (
              <><Loader2 className="w-4 h-4 animate-spin" /> Generating...</>
            ) : (
              <><Zap className="w-4 h-4" /> {riskData ? 'Regenerate Risks' : 'Generate Risks'}</>
            )}
          </button>
        </div>

        {riskError && (
          <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-red-600 dark:text-red-400 text-sm">
            {riskError}
          </div>
        )}

        {!riskData ? (
          <div className="text-center p-12 bg-white dark:bg-gray-800 rounded-2xl border-2 border-dashed border-gray-200 dark:border-gray-700">
            <AlertTriangle className="w-12 h-12 text-gray-400 mx-auto mb-3" />
            <p className="text-gray-500 dark:text-gray-400 mb-4">No risk profile generated yet.</p>
            <button
              onClick={handleGenerateRisks}
              disabled={generatingRisks}
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-red-600 to-orange-600 text-white font-semibold rounded-xl shadow-sm disabled:opacity-50"
            >
              {generatingRisks ? <><Loader2 className="w-4 h-4 animate-spin" /> Generating...</> : <><Zap className="w-4 h-4" /> Generate Risk Profile</>}
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <EditableField projectId={projectId} module="risk-engine" fieldName="market_risks" initialValue={riskData.market_risks} label="Market Risks" type="json" />
            <EditableField projectId={projectId} module="risk-engine" fieldName="financial_risks" initialValue={riskData.financial_risks} label="Financial Risks" type="json" />
            <EditableField projectId={projectId} module="risk-engine" fieldName="technical_risks" initialValue={riskData.technical_risks} label="Technical Risks" type="json" />
            <EditableField projectId={projectId} module="risk-engine" fieldName="execution_risks" initialValue={riskData.execution_risks} label="Execution Risks" type="json" />
            <EditableField projectId={projectId} module="risk-engine" fieldName="legal_risks" initialValue={riskData.legal_risks} label="Legal Risks" type="json" />
            <EditableField projectId={projectId} module="risk-engine" fieldName="hiring_risks" initialValue={riskData.hiring_risks} label="Hiring Risks" type="json" />
          </div>
        )}
      </section>

      <hr className="border-gray-200 dark:border-gray-700" />

      {/* Task Planner Section */}
      <section>
        <div className="flex justify-between items-start mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
              <CheckSquare className="w-6 h-6 text-green-500" />
              Task Planner & Roadmaps
            </h2>
            <p className="text-gray-500 dark:text-gray-400 mt-1">Actionable timelines and immediate priorities.</p>
          </div>
          <button
            onClick={handleGenerateTasks}
            disabled={generatingTasks}
            className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 text-white text-sm font-semibold rounded-xl shadow-sm transition-all disabled:opacity-50"
          >
            {generatingTasks ? (
              <><Loader2 className="w-4 h-4 animate-spin" /> Generating...</>
            ) : (
              <><Zap className="w-4 h-4" /> {taskData ? 'Regenerate Tasks' : 'Generate Tasks'}</>
            )}
          </button>
        </div>

        {taskError && (
          <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-red-600 dark:text-red-400 text-sm">
            {taskError}
          </div>
        )}

        {!taskData ? (
          <div className="text-center p-12 bg-white dark:bg-gray-800 rounded-2xl border-2 border-dashed border-gray-200 dark:border-gray-700">
            <CheckSquare className="w-12 h-12 text-gray-400 mx-auto mb-3" />
            <p className="text-gray-500 dark:text-gray-400 mb-4">No task planner generated yet.</p>
            <button
              onClick={handleGenerateTasks}
              disabled={generatingTasks}
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-green-600 to-emerald-600 text-white font-semibold rounded-xl shadow-sm disabled:opacity-50"
            >
              {generatingTasks ? <><Loader2 className="w-4 h-4 animate-spin" /> Generating...</> : <><Zap className="w-4 h-4" /> Generate Task Roadmap</>}
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <EditableField projectId={projectId} module="task-planner" fieldName="immediate_tasks" initialValue={taskData.immediate_tasks} label="Immediate Tasks" type="json" />
            <EditableField projectId={projectId} module="task-planner" fieldName="day_30_plan" initialValue={taskData.day_30_plan} label="30-Day Plan" type="json" />
            <EditableField projectId={projectId} module="task-planner" fieldName="day_90_plan" initialValue={taskData.day_90_plan} label="90-Day Plan" type="json" />
            <EditableField projectId={projectId} module="task-planner" fieldName="month_6_plan" initialValue={taskData.month_6_plan} label="6-Month Plan" type="json" />
            
            <div className="lg:col-span-2">
              <EditableField projectId={projectId} module="task-planner" fieldName="product_timeline" initialValue={taskData.product_timeline} label="Product Timeline" type="json" />
              <EditableField projectId={projectId} module="task-planner" fieldName="fundraising_timeline" initialValue={taskData.fundraising_timeline} label="Fundraising Timeline" type="json" />
            </div>
          </div>
        )}
      </section>

    </div>
  );
}
