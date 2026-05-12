import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'

export default function Landing() {
  const navigate = useNavigate()
  const [cursor, setCursor] = useState({ x: 50, y: 24 })

  useEffect(() => {
    const updateCursor = (event) => {
      setCursor({ x: event.clientX, y: event.clientY })
    }

    window.addEventListener('pointermove', updateCursor)
    return () => window.removeEventListener('pointermove', updateCursor)
  }, [])

  const features = [
    {
      title: 'AI Ayurveda Consultation',
      text: 'A calm conversational guide that blends dosha-aware insights with practical wellness suggestions.',
      icon: '✦',
    },
    {
      title: 'Dosha Analysis',
      text: 'Lightweight guidance for Vata, Pitta, and Kapha balance with personalized intake and routines.',
      icon: '◌',
    },
    {
      title: 'Personalized Wellness Tips',
      text: 'Daily rhythm, diet, hydration, and rest recommendations tuned to your lifestyle and constitution.',
      icon: '❋',
    },
    {
      title: 'Natural Remedies',
      text: 'Herbal and traditional wellness suggestions presented clearly, without overwhelming detail.',
      icon: '❦',
    },
    {
      title: 'Smart Health Assistant',
      text: 'A responsive AI companion with fast loading, subtle motion, and a clean, modern health interface.',
      icon: '⌁',
    },
  ]

  const floatingLeaves = [
    { left: '8%', top: '18%', delay: 0 },
    { left: '18%', top: '64%', delay: 1.2 },
    { left: '78%', top: '22%', delay: 0.6 },
    { left: '86%', top: '70%', delay: 1.8 },
  ]

  return (
    <div className="min-h-screen overflow-hidden bg-[radial-gradient(circle_at_top,_rgba(188,214,176,0.2),_transparent_36%),linear-gradient(180deg,_#fbfaf4_0%,_#f3f0e6_38%,_#eef3ec_100%)] text-slate-900">
      <div
        className="pointer-events-none fixed inset-0 opacity-40"
        style={{
          background: `radial-gradient(circle at ${cursor.x}px ${cursor.y}px, rgba(147, 176, 126, 0.18), transparent 24%)`,
        }}
      />

      <nav className="sticky top-0 z-40 border-b border-white/60 bg-white/55 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4 sm:px-8 lg:px-10">
          <button className="flex items-center gap-3 text-left" onClick={() => navigate('/')}>
            <span className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-emerald-500 to-amber-200 text-lg font-semibold text-white shadow-[0_18px_35px_rgba(71,128,82,0.25)]">
              ॐ
            </span>
            <span className="hidden text-sm font-semibold tracking-[0.24em] text-emerald-900 sm:block">
              AYURAI
            </span>
          </button>

          <div className="flex items-center gap-2 sm:gap-3">
            <button
              onClick={() => navigate('/login')}
              className="rounded-full border border-emerald-200/70 bg-white/70 px-4 py-2 text-sm font-medium text-emerald-900 transition duration-300 hover:-translate-y-0.5 hover:border-emerald-300 hover:bg-white"
            >
              Sign in
            </button>
            <button
              onClick={() => navigate('/signup')}
              className="rounded-full bg-gradient-to-r from-emerald-600 via-emerald-500 to-amber-300 px-4 py-2 text-sm font-semibold text-white shadow-[0_14px_30px_rgba(75,145,89,0.28)] transition duration-300 hover:-translate-y-0.5 hover:shadow-[0_18px_35px_rgba(75,145,89,0.32)]"
            >
              Start consulting
            </button>
          </div>
        </div>
      </nav>

      <main>
        <section className="relative mx-auto max-w-7xl px-5 py-14 sm:px-8 sm:py-18 lg:px-10 lg:py-24">
          {floatingLeaves.map((leaf) => (
            <motion.span
              key={`${leaf.left}-${leaf.top}`}
              className="pointer-events-none absolute hidden text-2xl text-emerald-400/40 lg:block"
              style={{ left: leaf.left, top: leaf.top }}
              animate={{ y: [0, -12, 0], rotate: [0, 10, 0] }}
              transition={{ duration: 7, repeat: Infinity, delay: leaf.delay, ease: 'easeInOut' }}
            >
              ❋
            </motion.span>
          ))}

          <div className="grid items-center gap-14 lg:grid-cols-[1.05fr_0.95fr]">
            <motion.div
              initial={{ opacity: 0, y: 24 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, ease: 'easeOut' }}
              className="max-w-2xl"
            >
              <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-emerald-200/70 bg-white/70 px-4 py-2 text-xs font-medium tracking-[0.22em] text-emerald-800 shadow-sm backdrop-blur">
                <span className="h-2 w-2 rounded-full bg-emerald-500" />
                PREMIUM AYURVEDA AI
              </div>
              <h1 className="max-w-xl text-5xl font-semibold tracking-tight text-slate-950 sm:text-6xl lg:text-7xl">
                Calm, intelligent Ayurveda guidance for modern wellness.
              </h1>
              <p className="mt-6 max-w-xl text-lg leading-8 text-slate-600 sm:text-xl">
                A lightweight assistant for dosha insight, herbal suggestions, and personalized wellness support with a serene, premium interface.
              </p>

              <div className="mt-8 flex flex-col gap-3 sm:flex-row">
                <button
                  onClick={() => navigate('/signup')}
                  className="group inline-flex items-center justify-center rounded-full bg-gradient-to-r from-emerald-600 via-emerald-500 to-amber-300 px-6 py-3.5 text-sm font-semibold text-white shadow-[0_18px_40px_rgba(74,143,88,0.3)] transition duration-300 hover:-translate-y-0.5 hover:shadow-[0_22px_48px_rgba(74,143,88,0.36)]"
                >
                  <span>Begin your consultation</span>
                  <span className="ml-2 transition-transform duration-300 group-hover:translate-x-0.5">→</span>
                </button>
                <button
                  onClick={() => document.getElementById('features')?.scrollIntoView({ behavior: 'smooth', block: 'start' })}
                  className="rounded-full border border-emerald-200/80 bg-white/70 px-6 py-3.5 text-sm font-semibold text-emerald-900 transition duration-300 hover:-translate-y-0.5 hover:border-emerald-300 hover:bg-white"
                >
                  Explore features
                </button>
              </div>

              <div className="mt-10 grid gap-4 sm:grid-cols-3">
                {[
                  ['Fast response', 'Optimized for a light runtime and minimal UI overhead.'],
                  ['Natural tone', 'Gentle language with a healthcare-first presentation.'],
                  ['Responsive layout', 'Works smoothly from mobile to large desktop screens.'],
                ].map(([title, text]) => (
                  <div key={title} className="rounded-3xl border border-white/70 bg-white/70 p-4 shadow-[0_16px_30px_rgba(50,70,55,0.08)] backdrop-blur-sm">
                    <p className="text-sm font-semibold text-slate-900">{title}</p>
                    <p className="mt-2 text-sm leading-6 text-slate-600">{text}</p>
                  </div>
                ))}
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 24, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.7, ease: 'easeOut', delay: 0.08 }}
              className="relative"
            >
              <div className="absolute -inset-4 rounded-[2rem] bg-gradient-to-br from-emerald-200/40 via-white/40 to-amber-200/30 blur-2xl" />
              <div className="relative overflow-hidden rounded-[2rem] border border-white/70 bg-white/70 p-6 shadow-[0_28px_80px_rgba(58,78,62,0.12)] backdrop-blur-xl">
                <div className="flex items-center justify-between border-b border-slate-200/70 pb-4">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-[0.3em] text-emerald-700">AI Ayurveda assistant</p>
                    <p className="mt-1 text-sm text-slate-500">Calm diagnostics, natural guidance, and a premium chat experience.</p>
                  </div>
                  <div className="rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-800">
                    Live
                  </div>
                </div>

                <div className="mt-6 grid gap-4">
                  <div className="rounded-[1.75rem] bg-[linear-gradient(135deg,rgba(236,247,235,0.95),rgba(255,255,255,0.9))] p-5 shadow-[inset_0_1px_0_rgba(255,255,255,0.7)]">
                    <div className="flex items-center gap-4">
                      <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-emerald-500 to-amber-300 text-2xl text-white shadow-lg">
                        🌿
                      </div>
                      <div>
                        <p className="text-lg font-semibold text-slate-950">Smart Ayurvedic intake</p>
                        <p className="text-sm text-slate-600">Ask about dosha balance, daily routine, herbs, food, sleep, and self-care.</p>
                      </div>
                    </div>
                  </div>

                  <div className="grid gap-4 sm:grid-cols-2">
                    <div className="rounded-[1.5rem] border border-emerald-100 bg-white/80 p-4">
                      <p className="text-xs uppercase tracking-[0.24em] text-emerald-700">Dosha balance</p>
                      <p className="mt-3 text-sm leading-6 text-slate-600">A clear understanding of Vata, Pitta, and Kapha with soft, personalized guidance.</p>
                    </div>
                    <div className="rounded-[1.5rem] border border-amber-100 bg-white/80 p-4">
                      <p className="text-xs uppercase tracking-[0.24em] text-amber-700">Wellness rhythm</p>
                      <p className="mt-3 text-sm leading-6 text-slate-600">A modern health assistant that keeps the interface calm while keeping the answers useful.</p>
                    </div>
                  </div>

                  <div className="rounded-[1.75rem] border border-white/70 bg-gradient-to-r from-emerald-50 via-white to-amber-50 p-5">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-semibold text-slate-900">Typing animation</p>
                        <p className="text-sm text-slate-600">Soft, lightweight response reveal inside the chatbot window.</p>
                      </div>
                      <div className="flex gap-1.5 rounded-full bg-white/70 px-3 py-2 shadow-sm">
                        <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-500 [animation-delay:-0.2s]" />
                        <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-500 [animation-delay:-0.1s]" />
                        <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-500" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </section>

        <section id="features" className="mx-auto max-w-7xl px-5 pb-20 sm:px-8 lg:px-10">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.5 }}
            className="mb-8 flex items-end justify-between gap-6"
          >
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.32em] text-emerald-700">Designed for clarity</p>
              <h2 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">Minimal sections, premium transitions.</h2>
            </div>
            <p className="hidden max-w-lg text-sm leading-6 text-slate-600 md:block">
              The page stays deliberately sparse, with calm motion, glass surfaces, and only enough detail to feel luxurious without becoming busy.
            </p>
          </motion.div>

          <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
            {features.map((feature, index) => (
              <motion.article
                key={feature.title}
                initial={{ opacity: 0, y: 18, scale: 0.98 }}
                whileInView={{ opacity: 1, y: 0, scale: 1 }}
                viewport={{ once: true, amount: 0.22 }}
                transition={{ duration: 0.45, delay: index * 0.05 }}
                className="group rounded-[1.75rem] border border-white/80 bg-white/70 p-6 shadow-[0_18px_45px_rgba(63,82,68,0.08)] backdrop-blur-md transition duration-300 hover:-translate-y-1 hover:border-emerald-200 hover:shadow-[0_22px_55px_rgba(63,82,68,0.12)]"
              >
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-emerald-500/15 via-white to-amber-200/30 text-xl text-emerald-800 transition duration-300 group-hover:shadow-[0_0_0_1px_rgba(110,163,123,0.3)]">
                  {feature.icon}
                </div>
                <h3 className="mt-5 text-xl font-semibold text-slate-950">{feature.title}</h3>
                <p className="mt-3 text-sm leading-7 text-slate-600">{feature.text}</p>
              </motion.article>
            ))}
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-5 pb-20 sm:px-8 lg:px-10">
          <motion.div
            initial={{ opacity: 0, y: 18 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.5 }}
            className="overflow-hidden rounded-[2rem] border border-white/70 bg-gradient-to-r from-emerald-600 via-emerald-500 to-amber-300 px-6 py-10 text-white shadow-[0_26px_70px_rgba(71,128,82,0.24)] sm:px-10"
          >
            <div className="grid gap-8 lg:grid-cols-[1fr_auto] lg:items-center">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.32em] text-white/80">Ready when you are</p>
                <h2 className="mt-3 text-3xl font-semibold tracking-tight sm:text-4xl">Start a calm, intelligent Ayurveda conversation.</h2>
                <p className="mt-4 max-w-2xl text-sm leading-7 text-white/85 sm:text-base">
                  Keep the experience simple, natural, and responsive while the assistant guides users through personalized wellness suggestions.
                </p>
              </div>
              <button
                onClick={() => navigate('/signup')}
                className="rounded-full bg-white px-6 py-3.5 text-sm font-semibold text-emerald-900 transition duration-300 hover:-translate-y-0.5 hover:bg-emerald-50"
              >
                Get started free
              </button>
            </div>
          </motion.div>
        </section>
      </main>

      <footer className="border-t border-white/60 bg-white/55 px-5 py-8 text-center text-sm text-slate-500 backdrop-blur-xl sm:px-8">
        <p>© 2026 AyurAI. Calm AI guidance for modern wellness.</p>
      </footer>

      <motion.button
        onClick={() => navigate('/signup')}
        className="fixed bottom-5 right-5 z-40 inline-flex items-center gap-3 rounded-full bg-emerald-600 px-5 py-3 text-sm font-semibold text-white shadow-[0_18px_40px_rgba(53,116,74,0.28)] transition duration-300 hover:-translate-y-0.5 hover:bg-emerald-500"
        animate={{ y: [0, -4, 0], boxShadow: ['0 18px 40px rgba(53,116,74,0.28)', '0 22px 48px rgba(53,116,74,0.34)', '0 18px 40px rgba(53,116,74,0.28)'] }}
        transition={{ duration: 3.2, repeat: Infinity, ease: 'easeInOut' }}
      >
        <span className="flex h-8 w-8 items-center justify-center rounded-full bg-white/20 text-base">✦</span>
        Chat now
      </motion.button>
    </div>
  )
}
