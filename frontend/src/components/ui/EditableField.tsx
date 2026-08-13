import React, { useState } from 'react';
import { Edit2, Save, RefreshCw, X } from 'lucide-react';
import api from '@/lib/api';

interface EditableFieldProps {
  label?: string;
  initialValue: string | string[] | any;
  updateUrl?: string;       // e.g. /projects/123/problem-discovery/core_problem
  regenerateUrl?: string;   // e.g. /projects/123/problem-discovery/core_problem/regenerate
  isJson?: boolean;
  
  // Phase 4 additions: alternative to updateUrl/regenerateUrl
  projectId?: string;
  module?: string;
  fieldName?: string;
  type?: "text" | "textarea" | "json";
}

export function EditableField(props: EditableFieldProps) {
  const { initialValue } = props;
  const isJson = props.type === "json" || props.isJson === true;
  const label = props.label || (props.fieldName ? props.fieldName.replace(/_/g, " ").toUpperCase() : "Field");
  
  const finalUpdateUrl = props.updateUrl || (props.projectId && props.module && props.fieldName ? `/projects/${props.projectId}/${props.module}/${props.fieldName}` : "");
  const finalRegenUrl = props.regenerateUrl || (props.projectId && props.module && props.fieldName ? `/projects/${props.projectId}/${props.module}/${props.fieldName}/regenerate` : "");

  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [value, setValue] = useState(initialValue);
  const [editValue, setEditValue] = useState(
    isJson ? JSON.stringify(initialValue, null, 2) : 
    Array.isArray(initialValue) ? initialValue.join('\n') : initialValue
  );

  const handleSave = async () => {
    setIsLoading(true);
    try {
      let payloadToSave: any = editValue;
      
      if (isJson) {
        payloadToSave = JSON.parse(editValue as string);
      } else if (Array.isArray(initialValue)) {
        payloadToSave = (editValue as string).split('\n').filter(s => s.trim() !== '');
      }

      await api.put(finalUpdateUrl, { content: payloadToSave });
      setValue(payloadToSave);
      setIsEditing(false);
    } catch (err) {
      console.error("Failed to save", err);
      alert("Failed to save changes. Please make sure JSON is valid if editing a JSON field.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegenerate = async () => {
    setIsLoading(true);
    try {
      const res = await api.post(finalRegenUrl);
      const newContent = res.data.new_content;
      setValue(newContent);
      setEditValue(
        isJson ? JSON.stringify(newContent, null, 2) : 
        Array.isArray(newContent) ? newContent.join('\n') : newContent
      );
    } catch (err) {
      console.error("Failed to regenerate", err);
      alert("Failed to regenerate field.");
    } finally {
      setIsLoading(false);
    }
  };

  const renderObject = (obj: any): React.ReactNode => {
    if (typeof obj !== 'object' || obj === null) return String(obj);
    
    if (Array.isArray(obj)) {
      return (
        <div className="flex flex-col gap-3 mt-2">
          {obj.map((item, idx) => (
            <div key={idx} className="bg-gray-50 dark:bg-gray-900/50 rounded-lg border border-gray-100 dark:border-gray-800 p-4">
              {renderObject(item)}
            </div>
          ))}
        </div>
      );
    }

    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-2">
        {Object.entries(obj).map(([k, v]) => (
          <div key={k} className="bg-gray-50 dark:bg-gray-900/50 rounded-lg border border-gray-100 dark:border-gray-800 p-4 flex flex-col gap-1.5">
            <span className="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider">{k.replace(/_/g, ' ')}</span>
            <div className="text-sm text-gray-800 dark:text-gray-200 whitespace-pre-wrap">
              {typeof v === 'object' && v !== null ? renderObject(v) : String(v)}
            </div>
          </div>
        ))}
      </div>
    );
  };

  const renderValue = () => {
    // Handle empty objects and empty arrays
    if (typeof value === 'object' && value !== null) {
      if (Array.isArray(value)) {
        if (value.length === 0) {
          return <p className="text-gray-400 italic">No items yet</p>;
        }
        return renderObject(value);
      }
      // For objects (dicts)
      if (Object.keys(value).length === 0) {
        return <p className="text-gray-400 italic">No data yet - click Regenerate to generate content</p>;
      }
      return renderObject(value);
    }
    
    if (!value) {
      return <p className="text-gray-400 italic">No data</p>;
    }
    
    return <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">{String(value)}</p>;
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden mb-6 transition-all hover:shadow-md group">
      <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-800/50">
        <h3 className="text-sm font-bold tracking-wide text-gray-900 dark:text-gray-100 uppercase">{label}</h3>
        <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
          {isEditing ? (
            <>
              <button 
                onClick={handleSave} 
                disabled={isLoading}
                className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-white bg-green-600 hover:bg-green-700 rounded-md disabled:opacity-50 transition-colors"
              >
                {isLoading ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Save className="w-3.5 h-3.5" />}
                Save
              </button>
              <button 
                onClick={() => setIsEditing(false)} 
                disabled={isLoading}
                className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-gray-700 bg-white border border-gray-300 hover:bg-gray-50 dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600 dark:hover:bg-gray-600 rounded-md disabled:opacity-50 transition-colors"
              >
                <X className="w-3.5 h-3.5" />
                Cancel
              </button>
            </>
          ) : (
            <>
              <button 
                onClick={() => setIsEditing(true)}
                disabled={isLoading}
                className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-gray-700 bg-white border border-gray-300 hover:bg-gray-50 dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600 dark:hover:bg-gray-600 rounded-md transition-colors shadow-sm"
              >
                <Edit2 className="w-3.5 h-3.5" />
                Edit
              </button>
              <button 
                onClick={handleRegenerate}
                disabled={isLoading}
                className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-blue-700 bg-blue-50 border border-blue-200 hover:bg-blue-100 dark:bg-blue-900/30 dark:text-blue-300 dark:border-blue-800 dark:hover:bg-blue-900/50 rounded-md transition-colors shadow-sm disabled:opacity-50"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
                {isLoading ? 'Regenerating...' : 'Regenerate'}
              </button>
            </>
          )}
        </div>
      </div>
      
      <div className="p-6">
        {isEditing ? (
          <textarea
            value={editValue}
            onChange={(e) => setEditValue(e.target.value)}
            className="w-full min-h-[150px] p-4 text-sm bg-gray-50 dark:bg-gray-900 border border-blue-300 dark:border-blue-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:text-gray-200 font-mono transition-all"
            placeholder={isJson ? "Enter valid JSON..." : "Enter text..."}
          />
        ) : (
          renderValue()
        )}
      </div>
    </div>
  );
}
