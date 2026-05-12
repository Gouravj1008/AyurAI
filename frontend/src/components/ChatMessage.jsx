export default function ChatMessage({ message }) {
  const isBot = message.type === 'bot'

  return (
    <div className={`flex ${isBot ? 'justify-start' : 'justify-end'}`}>
      <div
        className={`flex gap-3 max-w-2xl ${
          isBot ? '' : 'flex-row-reverse'
        }`}
      >
        {/* Avatar */}
        <div
          className={`flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-full shadow-sm ${
            isBot
              ? 'bg-gradient-to-br from-emerald-600 to-emerald-400 text-white'
              : 'bg-white text-emerald-700 border border-emerald-100'
          }`}
        >
          {isBot ? (
            <span className="text-sm font-bold">J</span>
          ) : (
            <span className="text-sm">🧑</span>
          )}
        </div>

        {/* Message Content */}
        <div
          className={`rounded-[1.5rem] border px-4 py-3 shadow-[0_12px_30px_rgba(62,78,65,0.08)] ${
            isBot
              ? 'border-white/70 bg-white/80 text-slate-800 backdrop-blur-sm'
              : 'border-emerald-500/10 bg-gradient-to-br from-emerald-600 via-emerald-500 to-amber-300 text-white'
          }`}
        >
          <p className="text-sm leading-7">{message.content}</p>
          <p className={`mt-2 text-xs ${isBot ? 'text-slate-400' : 'text-white/75'}`}>
            {message.timestamp.toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </p>
        </div>
      </div>
    </div>
  )
}
