import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'

export default function Sidebar({ isOpen, onNewChat, onLogout, user, onClose }) {
  return (
    <>
      {/* Overlay for mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 z-30 bg-slate-900/25 backdrop-blur-[2px] md:hidden"
          onClick={onClose}
        ></div>
      )}

      {/* Sidebar */}
      <motion.aside
        className={`fixed z-40 flex h-screen w-72 flex-col border-r border-white/70 bg-[linear-gradient(180deg,rgba(255,255,255,0.88),rgba(243,247,239,0.92))] shadow-[0_22px_70px_rgba(69,89,68,0.14)] backdrop-blur-xl md:relative ${
          isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        }`}
        initial={false}
        animate={{ x: isOpen ? 0 : '-100%' }}
        transition={{ duration: 0.28, ease: 'easeOut' }}
      >
        {/* Header */}
        <div className="border-b border-white/70 p-4">
          <button
            onClick={onNewChat}
            className="flex w-full items-center justify-center gap-2 rounded-2xl border border-emerald-100 bg-white px-4 py-3 font-medium text-emerald-900 shadow-sm transition duration-300 hover:-translate-y-0.5 hover:border-emerald-200 hover:bg-emerald-50"
          >
            <span className="text-lg leading-none">+</span>
            <span>New Chat</span>
          </button>
        </div>

        {/* Chat History */}
        <div className="flex-1 space-y-2 overflow-y-auto p-4">
          <h3 className="mb-3 px-2 text-xs font-semibold uppercase tracking-[0.28em] text-slate-500">
            Today
          </h3>
          <div className="space-y-2">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className="cursor-pointer truncate rounded-2xl border border-transparent px-3 py-2 text-sm text-slate-600 transition duration-300 hover:border-emerald-100 hover:bg-white hover:text-slate-900"
              >
                Chat about Ayurveda wellness...
              </div>
            ))}
          </div>

          <h3 className="mb-3 mt-6 px-2 text-xs font-semibold uppercase tracking-[0.28em] text-slate-500">
            Previous 7 days
          </h3>
          <div className="space-y-2">
            {[1, 2].map((i) => (
              <div
                key={i}
                className="cursor-pointer truncate rounded-2xl border border-transparent px-3 py-2 text-sm text-slate-600 transition duration-300 hover:border-emerald-100 hover:bg-white hover:text-slate-900"
              >
                Dosha assessment discussion
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="space-y-3 border-t border-white/70 p-4">
          {/* User Info */}
          <div className="rounded-2xl border border-white/80 bg-white/80 px-3 py-3 shadow-sm">
            <p className="text-xs text-slate-500">Logged in as</p>
            <p className="truncate text-sm font-medium text-slate-900">
              {user?.name || user?.email}
            </p>
            {user?.dosha && (
              <p className="mt-1 text-xs font-semibold uppercase tracking-[0.2em] text-emerald-700">{user.dosha} dosha</p>
            )}
          </div>

          {/* Quick Links */}
          <div className="space-y-2">
            <button className="w-full rounded-2xl px-3 py-2 text-left text-sm text-slate-600 transition duration-300 hover:bg-white hover:text-slate-900">
              Settings
            </button>
            <button className="w-full rounded-2xl px-3 py-2 text-left text-sm text-slate-600 transition duration-300 hover:bg-white hover:text-slate-900">
              Help & Feedback
            </button>
            <button
              onClick={onLogout}
              className="w-full rounded-2xl px-3 py-2 text-left text-sm text-rose-500 transition duration-300 hover:bg-rose-500/10"
            >
              Logout
            </button>
          </div>
        </div>
      </motion.aside>
    </>
  )
}
