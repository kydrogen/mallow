import { useState } from 'react'

export default function ArtifactPanel({ artifacts, onRefresh }) {
  const [expandedIdx, setExpandedIdx] = useState(null)

  return (
    <div className="card h-full flex flex-col overflow-hidden">
      <div className="p-4 border-b border-earth-200 flex justify-between items-center">
        <h2 className="text-lg font-serif">Artifacts Repository</h2>
        <button
          onClick={onRefresh}
          className="text-earth-600 hover:text-earth-800 text-sm"
          title="Refresh"
        >
          ↻
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {artifacts.length === 0 ? (
          <p className="text-earth-500 text-sm">No artifacts added yet</p>
        ) : (
          artifacts.map((artifact, idx) => (
            <div key={idx} className="bg-earth-50 rounded p-3 border border-earth-200">
              <button
                onClick={() => setExpandedIdx(expandedIdx === idx ? null : idx)}
                className="w-full text-left font-medium text-earth-800 hover:text-earth-900 flex justify-between items-center"
              >
                <span className="truncate">{artifact.name || artifact.details?.name || 'Unknown'}</span>
                <span className="text-xs text-earth-600">{expandedIdx === idx ? '▼' : '▶'}</span>
              </button>

              {expandedIdx === idx && (
                <div className="mt-2 text-sm text-earth-700 space-y-2 pt-2 border-t border-earth-200">
                  {artifact.details?.location && (
                    <p>
                      <span className="font-medium">Location:</span> {artifact.details.location}
                    </p>
                  )}
                  {artifact.details?.summary && (
                    <p>
                      <span className="font-medium">Summary:</span> {artifact.details.summary}
                    </p>
                  )}
                  {artifact.discovered_date && (
                    <p>
                      <span className="font-medium">Discovered:</span> {new Date(artifact.discovered_date).toLocaleDateString()}
                    </p>
                  )}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  )
}
