"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";
import { 
  LayoutDashboard, 
  Search, 
  Dna, 
  Rocket, 
  BarChart2, 
  Banknote, 
  Briefcase, 
  AlertTriangle,
  MessageCircle,
  Brain,
  Settings,
} from "lucide-react";
import { use } from "react";

const TABS = [
  { name: "Overview", href: "", icon: LayoutDashboard },
  { name: "Problem Discovery", href: "/problem-discovery", icon: Search },
  { name: "Innovation DNA", href: "/innovation-dna", icon: Dna },
  { name: "Startup Formation", href: "/startup-formation", icon: Rocket },
  { name: "Market Intelligence", href: "/market-intelligence", icon: BarChart2 },
  { name: "Financial Planner", href: "/financial-planner", icon: Banknote },
  { name: "Investor Hub", href: "/investor-hub", icon: Briefcase },
  { name: "Risks & Tasks", href: "/risks", icon: AlertTriangle },
  { name: "AI Mentor", href: "/ai-mentor", icon: Brain },
  { name: "AI Co-Founder", href: "/ai-cofounder", icon: MessageCircle },
  { name: "Settings", href: "/settings", icon: Settings },
];

export default function ProjectLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ id: string }>;
}) {
  const resolvedParams = use(params);
  const projectId = resolvedParams.id;
  const pathname = usePathname();

  return (
    <div className="flex flex-col h-full bg-gray-50 dark:bg-gray-900">
      {/* Tabs Header */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 overflow-x-auto no-scrollbar">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="-mb-px flex space-x-1" aria-label="Tabs">
            {TABS.map((tab) => {
              const fullHref = `/projects/${projectId}${tab.href}`;
              const isActive = tab.href === "" 
                ? pathname === `/projects/${projectId}`
                : pathname.startsWith(fullHref);

              const Icon = tab.icon;

              return (
                <Link
                  key={tab.name}
                  href={fullHref}
                  className={`
                    whitespace-nowrap flex items-center gap-1.5 py-4 px-3 border-b-2 font-medium text-xs transition-colors
                    ${isActive
                      ? "border-blue-500 text-blue-600 dark:text-blue-400"
                      : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300"
                    }
                  `}
                >
                  <Icon className={`h-3.5 w-3.5 ${isActive ? 'text-blue-500 dark:text-blue-400' : 'text-gray-400 dark:text-gray-500'}`} />
                  {tab.name}
                </Link>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Page Content */}
      <div className="flex-1 overflow-auto">
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
      </div>
    </div>
  );
}
