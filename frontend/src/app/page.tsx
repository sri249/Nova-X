import Link from 'next/link';
import { ArrowRight, Zap, Brain, TrendingUp, Shield, Users, BarChart3, Rocket, CheckCircle } from 'lucide-react';

const features = [
  {
    icon: Brain,
    title: 'Problem Discovery',
    desc: 'AI maps root causes, stakeholders, and calculates an Opportunity Score.',
    color: 'from-blue-500 to-cyan-500',
  },
  {
    icon: Zap,
    title: 'Innovation DNA',
    desc: 'Identify unfair advantages, patent potential, and your unique value proposition.',
    color: 'from-purple-500 to-pink-500',
  },
  {
    icon: Rocket,
    title: 'Startup Formation',
    desc: 'Generate mission, brand identity, business model canvas, and product roadmap.',
    color: 'from-green-500 to-emerald-500',
  },
  {
    icon: TrendingUp,
    title: 'Market Intelligence',
    desc: 'TAM/SAM/SOM analysis, SWOT, competitor matrix, and market readiness scoring.',
    color: 'from-orange-500 to-amber-500',
  },
  {
    icon: BarChart3,
    title: 'Financial Planner',
    desc: 'Burn rate, runway, break-even forecasting, and funding requirements.',
    color: 'from-teal-500 to-green-500',
  },
  {
    icon: Shield,
    title: 'Risk Engine',
    desc: 'Identify and mitigate technical, financial, market, and execution risks.',
    color: 'from-red-500 to-rose-500',
  },
  {
    icon: Users,
    title: 'Investor Hub',
    desc: 'Generate pitch decks, investment memos, and due diligence packages.',
    color: 'from-indigo-500 to-violet-500',
  },
  {
    icon: Brain,
    title: 'AI Co-Founder',
    desc: 'Context-aware AI mentor with full knowledge of your startup profile.',
    color: 'from-blue-600 to-indigo-600',
  },
];

const stats = [
  { label: 'AI Modules', value: '8+' },
  { label: 'Startup Insights', value: '100+' },
  { label: 'Analysis Frameworks', value: '15+' },
  { label: 'Export Formats', value: 'JSON & PDF' },
];

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-950 text-white overflow-hidden">
      {/* Animated background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-indigo-500/20 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-purple-500/10 rounded-full blur-3xl" />
      </div>

      {/* Header */}
      <header className="relative z-10 flex items-center justify-between px-6 py-5 max-w-7xl mx-auto">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
            <Zap className="w-5 h-5 text-white" />
          </div>
          <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
            NOVA X
          </span>
        </div>
        <div className="flex items-center gap-3">
          <Link
            href="/login"
            className="text-sm font-medium text-gray-400 hover:text-white transition-colors px-4 py-2"
          >
            Sign In
          </Link>
          <Link
            href="/register"
            className="text-sm font-medium bg-white/10 hover:bg-white/20 border border-white/20 text-white px-4 py-2 rounded-lg transition-all"
          >
            Get Started
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <main className="relative z-10 max-w-7xl mx-auto px-6 pt-20 pb-32 text-center">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 bg-blue-500/10 border border-blue-500/30 text-blue-300 text-xs font-semibold px-4 py-1.5 rounded-full mb-8">
          <Zap className="w-3 h-3" />
          AI-Powered Startup Incubator
        </div>

        <h1 className="text-5xl sm:text-7xl font-black tracking-tight mb-6 leading-tight">
          Your AI
          <span className="block bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent">
            Co-Founder
          </span>
          <span className="block text-4xl sm:text-5xl font-bold text-gray-300 mt-2">
            is ready to build.
          </span>
        </h1>

        <p className="text-lg sm:text-xl text-gray-400 max-w-2xl mx-auto mb-12 leading-relaxed">
          NOVA X transforms your startup idea into a complete, investor-ready blueprint â€” 
          from problem discovery to pitch deck â€” powered by advanced AI.
        </p>

        {/* CTAs */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
          <Link
            href="/login?demo=true"
            className="group inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold rounded-xl text-base shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50 transition-all duration-300"
          >
            <Zap className="w-4 h-4" />
            Try Demo â€” Free
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </Link>
          <Link
            href="/register"
            className="inline-flex items-center gap-2 px-8 py-4 bg-white/5 hover:bg-white/10 border border-white/10 hover:border-white/20 text-white font-semibold rounded-xl text-base transition-all duration-300"
          >
            Create Account
          </Link>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-2xl mx-auto mb-24">
          {stats.map((stat) => (
            <div key={stat.label} className="bg-white/5 border border-white/10 rounded-xl p-4">
              <div className="text-2xl font-black bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
                {stat.value}
              </div>
              <div className="text-xs text-gray-500 mt-1 font-medium">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Features Grid */}
        <div className="text-left">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
              Everything you need to launch
            </h2>
            <p className="text-gray-400 max-w-xl mx-auto">
              8 AI-powered modules that take you from raw idea to investor-ready startup in minutes.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {features.map((feature, idx) => (
              <div
                key={feature.title}
                className="group bg-white/5 hover:bg-white/10 border border-white/10 hover:border-white/20 rounded-2xl p-6 transition-all duration-300 hover:-translate-y-1"
              >
                <div className={`w-10 h-10 bg-gradient-to-br ${feature.color} rounded-xl flex items-center justify-center mb-4 shadow-lg`}>
                  <feature.icon className="w-5 h-5 text-white" />
                </div>
                <h3 className="text-sm font-bold text-white mb-2">{feature.title}</h3>
                <p className="text-xs text-gray-500 leading-relaxed">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* How it works */}
        <div className="mt-28">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4 text-center">
            From idea to pitch in minutes
          </h2>
          <p className="text-gray-400 mb-16 text-center max-w-lg mx-auto">
            Our AI pipeline processes your inputs and generates a complete startup dossier automatically.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            {[
              { step: '01', title: 'Describe your idea', desc: 'Tell NOVA X your problem space, target users, pain points, and industry.' },
              { step: '02', title: 'AI generates everything', desc: 'Watch as 8 AI modules analyze, score, and generate your complete startup profile in real-time.' },
              { step: '03', title: 'Export & pitch', desc: 'Review, edit, and export your pitch deck, investment memo, and financial plan.' },
            ].map((item) => (
              <div key={item.step} className="text-center">
                <div className="w-14 h-14 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-4 text-white font-black text-lg shadow-lg shadow-blue-500/30">
                  {item.step}
                </div>
                <h3 className="text-lg font-bold text-white mb-2">{item.title}</h3>
                <p className="text-sm text-gray-500 leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Final CTA */}
        <div className="mt-28 bg-gradient-to-r from-blue-600/20 to-indigo-600/20 border border-blue-500/30 rounded-3xl p-12">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Ready to build your startup?
          </h2>
          <p className="text-gray-400 mb-8 max-w-lg mx-auto">
            Join entrepreneurs using NOVA X to transform ideas into investor-ready companies.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href="/login?demo=true"
              className="group inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold rounded-xl transition-all duration-300 shadow-lg shadow-blue-500/30"
            >
              <Zap className="w-4 h-4" />
              Try Demo Now â€” Free
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link href="/register" className="text-sm text-gray-400 hover:text-white transition-colors">
              Create free account â†’
            </Link>
          </div>
          <div className="flex items-center justify-center gap-6 mt-8 text-xs text-gray-600">
            {['No credit card required', 'AI-powered generation', 'Export to JSON & PDF'].map((item) => (
              <div key={item} className="flex items-center gap-1.5">
                <CheckCircle className="w-3 h-3 text-green-500" />
                {item}
              </div>
            ))}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="relative z-10 border-t border-white/10 py-8 px-6">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-md flex items-center justify-center">
              <Zap className="w-3.5 h-3.5 text-white" />
            </div>
            <span className="text-sm font-bold text-gray-400">NOVA X</span>
          </div>
          <p className="text-xs text-gray-600">
            Â© 2026 NOVA X â€” AI Innovation & Startup Operating System
          </p>
          <div className="flex items-center gap-4 text-xs text-gray-600">
            <Link href="/login" className="hover:text-gray-400 transition-colors">Sign In</Link>
            <Link href="/register" className="hover:text-gray-400 transition-colors">Register</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}

