"use client"

import { useAuth } from '@/contexts/AuthContext';
import { Bell, LogOut, Settings, UserCircle, ChevronDown } from 'lucide-react';
import { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import api from '@/lib/api';

function getBreadcrumb(pathname: string): string {
  const segments = pathname.split('/').filter(Boolean);
  if (segments.length === 0) return 'Dashboard';
  const last = segments[segments.length - 1];
  // Convert slug to title
  return last
    .replace(/-/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

function getProjectId(pathname: string): string | null {
  const segments = pathname.split('/').filter(Boolean);
  return segments[0] === 'projects' && segments[1] ? segments[1] : null;
}

interface ProjectSummary {
  id: string;
  name: string;
}

export default function Navbar() {
  const { user, logout } = useAuth();
  const [profileOpen, setProfileOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const pathname = usePathname();
  const projectId = getProjectId(pathname);
  const [project, setProject] = useState<ProjectSummary | null>(null);
  const [projectLoading, setProjectLoading] = useState(Boolean(projectId));

  useEffect(() => {
    let cancelled = false;

    if (!projectId) {
      setProject(null);
      setProjectLoading(false);
      return;
    }

    const loadProject = async () => {
      setProject(null);
      setProjectLoading(true);
      try {
        const response = await api.get<ProjectSummary>(`/projects/${projectId}`);
        if (!cancelled) setProject(response.data);
      } catch {
        // The page-specific view handles the detailed 401/404 error. The navbar
        // intentionally keeps a stable, non-technical breadcrumb fallback.
        if (!cancelled) setProject(null);
      } finally {
        if (!cancelled) setProjectLoading(false);
      }
    };

    loadProject();
    return () => {
      cancelled = true;
    };
  }, [projectId]);

  useEffect(() => {
    const handleProjectUpdated = (event: Event) => {
      const detail = (event as CustomEvent<ProjectSummary>).detail;
      if (detail?.id === projectId && detail.name?.trim()) {
        setProject(detail);
        setProjectLoading(false);
      }
    };

    window.addEventListener('novax-project-updated', handleProjectUpdated);
    return () => window.removeEventListener('novax-project-updated', handleProjectUpdated);
  }, [projectId]);

  // Close dropdown on outside click
  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setProfileOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  const initials = user?.full_name
    ? user.full_name.split(' ').map((n: string) => n[0]).join('').toUpperCase().slice(0, 2)
    : user?.email?.[0]?.toUpperCase() ?? '?';

  const displayName = user?.full_name || user?.email?.split('@')[0] || 'User';
  const moduleName = pathname.split('/').length > 3 ? getBreadcrumb(pathname) : '';
  const breadcrumb = projectId
    ? projectLoading || project?.id !== projectId
      ? 'Loading project...'
      : `${project?.name?.trim() || 'Project'}${moduleName ? ` / ${moduleName}` : ''}`
    : getBreadcrumb(pathname);

  return (
    <header className="flex-shrink-0 h-16 bg-white dark:bg-gray-950 border-b border-gray-200 dark:border-gray-800 flex items-center justify-between px-4 sm:px-6 lg:px-8">
      {/* Breadcrumb */}
      <div className="flex items-center gap-2 text-sm">
        <span className="text-gray-400 dark:text-gray-600 hidden sm:inline">NOVA X</span>
        <span className="text-gray-300 dark:text-gray-700 hidden sm:inline">/</span>
        <span className="font-semibold text-gray-800 dark:text-gray-200">
          {breadcrumb}
        </span>
      </div>

      {/* Right side */}
      <div className="flex items-center gap-3">
        {/* Notification bell */}
        <button
          id="navbar-notifications"
          className="relative p-2 rounded-xl text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          title="Notifications"
        >
          <Bell className="h-5 w-5" />
          {/* Notification dot */}
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-blue-500 rounded-full" />
        </button>

        {/* Profile dropdown */}
        <div className="relative" ref={dropdownRef}>
          <button
            id="navbar-profile"
            onClick={() => setProfileOpen(!profileOpen)}
            className="flex items-center gap-2.5 px-2 py-1.5 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center text-white text-xs font-bold flex-shrink-0">
              {initials}
            </div>
            <span className="hidden sm:block text-sm font-medium text-gray-700 dark:text-gray-300 max-w-[120px] truncate">
              {displayName}
            </span>
            <ChevronDown className={`hidden sm:block w-3.5 h-3.5 text-gray-400 transition-transform ${profileOpen ? 'rotate-180' : ''}`} />
          </button>

          {profileOpen && (
            <div className="absolute right-0 mt-2 w-56 rounded-xl shadow-lg bg-white dark:bg-gray-800 ring-1 ring-black/5 dark:ring-white/10 border border-gray-100 dark:border-gray-700 z-50 overflow-hidden">
              {/* User info header */}
              <div className="px-4 py-3 border-b border-gray-100 dark:border-gray-700">
                <p className="text-xs font-semibold text-gray-900 dark:text-white truncate">
                  {user?.full_name || 'User'}
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400 truncate mt-0.5">
                  {user?.email}
                </p>
              </div>

              {/* Menu items */}
              <div className="py-1">
                <Link
                  href="/settings"
                  onClick={() => setProfileOpen(false)}
                  className="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700/60 transition-colors"
                >
                  <Settings className="w-4 h-4 text-gray-400" />
                  Account Settings
                </Link>
              </div>

              <div className="border-t border-gray-100 dark:border-gray-700 py-1">
                <button
                  id="navbar-logout"
                  onClick={() => { setProfileOpen(false); logout(); }}
                  className="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                  Sign out
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
