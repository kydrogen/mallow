import ReactMarkdown from 'react-markdown'

export default function MessageBubble({ role, content }) {
  const isUser = role === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`rounded-lg px-4 py-3 max-w-md ${
          isUser
            ? 'bg-earth-600 text-white'
            : 'bg-earth-100 text-earth-900'
        }`}
      >
        <div className="text-sm leading-relaxed">
          {isUser ? (
            <p>{content}</p>
          ) : (
            <ReactMarkdown
              components={{
                p: ({ node, ...props }) => <p className="mb-2 last:mb-0" {...props} />,
                h3: ({ node, ...props }) => <h3 className="font-semibold mt-3 mb-2" {...props} />,
                ul: ({ node, ...props }) => <ul className="list-disc list-inside mb-2" {...props} />,
                li: ({ node, ...props }) => <li className="mb-1" {...props} />,
              }}
            >
              {content}
            </ReactMarkdown>
          )}
        </div>
      </div>
    </div>
  )
}
