"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Loader2, CheckCircle2, ChevronRight, AlertCircle } from "lucide-react";
import api from "@/lib/api";

const STEPS = [
  "Details",
  "Discovery",
  "DNA",
  "Formation",
  "Market",
  "Financials",
  "Health",
  "Complete",
];

export default function CreateProjectWizard() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Form Data
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    industry: "",
    country: "",
    target_users: "",
    existing_solutions: "",
    pain_points: "",
  });

  // Generated Data References
  const [projectId, setProjectId] = useState<string | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const startGenerationFlow = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    let currentProjectId = projectId;

    try {
      // Step 1: Create Project if it doesn't exist
      if (!currentProjectId) {
        const projRes = await api.post("/projects", {
          name: formData.title,
          description: formData.description,
          status: "Generating",
        });
        currentProjectId = projRes.data.id;
        setProjectId(currentProjectId);
      }

      // Step 2: Problem Discovery
      setCurrentStep(1); // Analyzing Problem
      await api.post(`/projects/${currentProjectId}/problem-discovery`, formData);

      // Step 3: Innovation DNA
      setCurrentStep(2); // Innovation DNA
      await api.post(`/projects/${currentProjectId}/innovation-dna`, {});

      // Step 4: Startup Formation
      setCurrentStep(3); // Startup Formation
      await api.post(`/projects/${currentProjectId}/startup-formation`, {});

      // Step 5: Market Intelligence
      setCurrentStep(4);
      await api.post(`/projects/${currentProjectId}/market-intelligence`, {});

      // Step 6: Financial Planner
      setCurrentStep(5);
      await api.post(`/projects/${currentProjectId}/financial-planner`, {});

      // Step 7: Startup Health Engine
      setCurrentStep(6);
      await api.post(`/projects/${currentProjectId}/generate-health-score`, {});

      // Extra Step: Generate Investor Hub, Risks, and Tasks so they aren't 'Pending'
      await api.post(`/projects/${currentProjectId}/investor-hub`, {});
      await api.post(`/projects/${currentProjectId}/risk-engine`, {});
      await api.post(`/projects/${currentProjectId}/task-planner`, {});

      // Step 8: Complete
      setCurrentStep(7);
      
      // Update Project Status
      await api.put(`/projects/${currentProjectId}`, {
        status: "Completed",
        completion_percentage: 100
      });

    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || "An error occurred during generation.");
    } finally {
      setLoading(false);
    }
  };

  const handleRetry = () => {
    startGenerationFlow({ preventDefault: () => {} } as React.FormEvent);
  };

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      {/* Progress Bar */}
      <div className="mb-8 relative">
        <div className="overflow-hidden h-2 mb-4 text-xs flex rounded bg-gray-200 dark:bg-gray-700">
          <div
            style={{ width: `${(currentStep / (STEPS.length - 1)) * 100}%` }}
            className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-blue-600 transition-all duration-500 ease-in-out"
          ></div>
        </div>
        <div className="flex justify-between text-xs font-medium text-gray-500 dark:text-gray-400">
          {STEPS.map((step, idx) => (
            <span key={idx} className={idx <= currentStep ? "text-blue-600 dark:text-blue-400 font-bold" : ""}>
              {step}
            </span>
          ))}
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden border border-gray-100 dark:border-gray-700 p-8">
        {error && (
          <div className="mb-6 bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-lg p-4 flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400 mt-0.5" />
            <div className="flex-1">
              <h3 className="text-sm font-medium text-red-800 dark:text-red-300">Generation Error</h3>
              <p className="mt-1 text-sm text-red-700 dark:text-red-400">{error}</p>
              <button onClick={handleRetry} className="mt-3 text-sm font-medium text-red-600 hover:text-red-500 dark:text-red-400">
                Try Again
              </button>
            </div>
          </div>
        )}

        {currentStep === 0 && (
          <form onSubmit={startGenerationFlow} className="space-y-6 fade-in">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Describe Your Problem Space</h2>
              <p className="mt-2 text-gray-600 dark:text-gray-400">Tell us what you want to solve. Our AI will analyze the market and build a startup around it.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2 md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Project Title</label>
                <input required name="title" value={formData.title} onChange={handleInputChange} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white" placeholder="e.g. NextGen Logistics" />
              </div>

              <div className="space-y-2 md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Brief Description</label>
                <textarea required name="description" value={formData.description} onChange={handleInputChange} rows={2} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white" placeholder="What is the general idea?" />
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Industry</label>
                <input required name="industry" value={formData.industry} onChange={handleInputChange} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white" placeholder="e.g. Healthcare, EdTech" />
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Target Country/Region</label>
                <input required name="country" value={formData.country} onChange={handleInputChange} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white" placeholder="e.g. Global, USA, India" />
              </div>

              <div className="space-y-2 md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Target Users</label>
                <input required name="target_users" value={formData.target_users} onChange={handleInputChange} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white" placeholder="Who faces this problem?" />
              </div>

              <div className="space-y-2 md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Pain Points</label>
                <textarea required name="pain_points" value={formData.pain_points} onChange={handleInputChange} rows={3} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white" placeholder="What specifically is frustrating or inefficient?" />
              </div>

              <div className="space-y-2 md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Existing Solutions</label>
                <textarea required name="existing_solutions" value={formData.existing_solutions} onChange={handleInputChange} rows={2} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white" placeholder="How do people solve it today? What are the competitors?" />
              </div>
            </div>

            <div className="pt-6 flex justify-end">
              <button type="submit" className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-lg shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
                Generate Startup
                <ChevronRight className="ml-2 -mr-1 w-5 h-5" />
              </button>
            </div>
          </form>
        )}

        {(currentStep >= 1 && currentStep <= 6) && !error && (
          <div className="flex flex-col items-center justify-center py-20 fade-in text-center">
            <div className="relative w-24 h-24 mb-8">
              <div className="absolute inset-0 border-4 border-blue-100 dark:border-blue-900 rounded-full"></div>
              <div className="absolute inset-0 border-4 border-blue-600 rounded-full border-t-transparent animate-spin"></div>
              <div className="absolute inset-0 flex items-center justify-center">
                <Loader2 className="w-8 h-8 text-blue-600 animate-pulse" />
              </div>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              {currentStep === 1 && "Discovering the Problem Space..."}
              {currentStep === 2 && "Synthesizing Innovation DNA..."}
              {currentStep === 3 && "Forging Startup Profile & Business Model..."}
              {currentStep === 4 && "Conducting Market Intelligence..."}
              {currentStep === 5 && "Developing Financial Plan..."}
              {currentStep === 6 && "Calculating Startup Health Score..."}
            </h2>
            <p className="text-gray-500 dark:text-gray-400 max-w-md mx-auto">
              Our AI is analyzing millions of data points to generate high-quality insights. This usually takes about 10-15 seconds per step.
            </p>
          </div>
        )}

        {currentStep === 7 && (
          <div className="flex flex-col items-center justify-center py-16 fade-in text-center">
            <div className="w-20 h-20 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mb-6">
              <CheckCircle2 className="w-10 h-10 text-green-600 dark:text-green-400" />
            </div>
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">Startup Successfully Generated!</h2>
            <p className="text-gray-600 dark:text-gray-400 mb-8 max-w-md mx-auto">
              Your comprehensive startup blueprint is ready. You can now review, edit, and export your project.
            </p>
            <button
              onClick={() => router.push(`/projects/${projectId}/overview`)}
              className="px-8 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 shadow-md transition-colors"
            >
              Go to Project Dashboard
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

