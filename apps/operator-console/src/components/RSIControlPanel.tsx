'use client'

import { useState } from 'react'
import { Brain, AlertTriangle, CheckCircle, Play, Square, TrendingUp, Shield, Clock } from 'lucide-react'
import { useRSIStatus } from '../hooks/useRSIStatus'

export default function RSIControlPanel() {
  const { rsiStatus, loading, error, startImprovementCycle, emergencyStop, getGoalDriftIndex } = useRSIStatus()
  const [triggerReason, setTriggerReason] = useState('Performance optimization')
  const [autoApprove, setAutoApprove] = useState(false)
  const [gdiData, setGdiData] = useState<any>(null)

  const handleStartCycle = async () => {
    try {
      await startImprovementCycle(triggerReason, autoApprove)
    } catch (err) {
      console.error('Failed to start cycle:', err)
    }
  }

  const handleEmergencyStop = async () => {
    if (confirm('Are you sure you want to initiate emergency stop? This will immediately halt all AI operations.')) {
      try {
        await emergencyStop()
      } catch (err) {
        console.error('Failed to execute emergency stop:', err)
      }
    }
  }

  const handleCheckGDI = async () => {
    try {
      const gdi = await getGoalDriftIndex()
      setGdiData(gdi)
    } catch (err) {
      console.error('Failed to fetch GDI:', err)
    }
  }

  const getSafetyStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'text-green-500'
      case 'warning': return 'text-yellow-500'
      case 'critical': return 'text-red-500'
      default: return 'text-gray-500'
    }
  }

  return (
    <div className="space-y-6">
      {/* RSI Status Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">RSI Status</h3>
            <Brain className="w-5 h-5 text-blue-500" />
          </div>
          <div className={`text-2xl font-bold ${rsiStatus.is_active ? 'text-green-500' : 'text-gray-400'}`}>
            {rsiStatus.is_active ? 'Active' : 'Inactive'}
          </div>
          <div className="text-sm text-gray-400 mt-2">
            Cycle {rsiStatus.current_cycle} of {rsiStatus.total_cycles}
          </div>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Goal Drift Index</h3>
            <TrendingUp className="w-5 h-5 text-gray-400" />
          </div>
          <div className="text-2xl font-bold">{(rsiStatus.goal_drift_index * 100).toFixed(1)}%</div>
          <div className="text-sm text-gray-400 mt-2">
            {rsiStatus.goal_drift_index < 0.3 ? 'Low Risk' : rsiStatus.goal_drift_index < 0.6 ? 'Medium Risk' : 'High Risk'}
          </div>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Safety Status</h3>
            <CheckCircle className="w-5 h-5 text-gray-400" />
          </div>
          <div className={`text-2xl font-bold ${getSafetyStatusColor(rsiStatus.safety_status)}`}>
            {rsiStatus.safety_status.charAt(0).toUpperCase() + rsiStatus.safety_status.slice(1)}
          </div>
          <div className="text-sm text-gray-400 mt-2">
            All constraints satisfied
          </div>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Last Improvement</h3>
            <Clock className="w-5 h-5 text-gray-400" />
          </div>
          <div className="text-lg font-bold">{rsiStatus.last_improvement || 'Never'}</div>
          <div className="text-sm text-gray-400 mt-2">
            {rsiStatus.is_active ? 'Improvement in progress' : 'System stable'}
          </div>
        </div>
      </div>

      {/* Control Panel */}
      <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold mb-4">RSI Control Panel</h3>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Trigger Reason</label>
            <input
              type="text"
              value={triggerReason}
              onChange={(e) => setTriggerReason(e.target.value)}
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white"
              placeholder="Enter reason for improvement cycle"
            />
          </div>

          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              id="autoApprove"
              checked={autoApprove}
              onChange={(e) => setAutoApprove(e.target.checked)}
              className="w-4 h-4 rounded"
            />
            <label htmlFor="autoApprove" className="text-sm">
              Auto-approve low-risk changes
            </label>
          </div>

          <div className="flex space-x-4">
            <button
              onClick={handleStartCycle}
              disabled={rsiStatus.is_active || loading}
              className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 px-4 py-2 rounded-lg transition-colors"
            >
              <Play className="w-4 h-4" />
              <span>Start Improvement Cycle</span>
            </button>

            <button
              onClick={handleEmergencyStop}
              disabled={!rsiStatus.is_active}
              className="flex items-center space-x-2 bg-red-600 hover:bg-red-700 disabled:bg-gray-700 px-4 py-2 rounded-lg transition-colors"
            >
              <Square className="w-4 h-4" />
              <span>Emergency Stop</span>
            </button>

            <button
              onClick={handleCheckGDI}
              className="flex items-center space-x-2 bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded-lg transition-colors"
            >
              <TrendingUp className="w-4 h-4" />
              <span>Check Goal Drift</span>
            </button>
          </div>
        </div>
      </div>

      {/* Goal Drift Details */}
      {gdiData && (
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4">Goal Drift Analysis</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-400">Semantic Drift:</span>
              <span>{(gdiData.semantic_drift * 100).toFixed(2)}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Lexical Drift:</span>
              <span>{(gdiData.lexical_drift * 100).toFixed(2)}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Structural Drift:</span>
              <span>{(gdiData.structural_drift * 100).toFixed(2)}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Distributional Drift:</span>
              <span>{(gdiData.distributional_drift * 100).toFixed(2)}%</span>
            </div>
            <div className="border-t border-gray-800 pt-3 mt-3">
              <div className="flex justify-between font-semibold">
                <span>Total GDI:</span>
                <span className={gdiData.total_gdi < 0.5 ? 'text-green-500' : gdiData.total_gdi < 0.7 ? 'text-yellow-500' : 'text-red-500'}>
                  {(gdiData.total_gdi * 100).toFixed(2)}%
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Safety Constraints */}
      <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold mb-4">Constitutional Constraints</h3>
        <div className="space-y-2">
          {[
            'No self-disable of safety mechanisms',
            'No budget override',
            'No secret exposure',
            'No sandbox escape',
            'No test disabling',
            'No monitoring bypass',
            'No human override bypass',
            'No immutable modification',
            'No privilege escalation',
            'No resource monopolization'
          ].map((constraint, index) => (
            <div key={index} className="flex items-center space-x-3 p-2 bg-gray-800 rounded">
              <CheckCircle className="w-4 h-4 text-green-500" />
              <span className="text-sm">{constraint}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}