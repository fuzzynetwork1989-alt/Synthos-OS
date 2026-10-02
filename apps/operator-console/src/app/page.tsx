'use client'

import { useState, useEffect } from 'react'
import {
  Activity,
  Brain,
  Database,
  Settings,
  Cpu,
  MemoryStick,
  Network,
  Shield,
  Zap,
  Users,
  Globe,
  Clock,
  AlertTriangle,
  CheckCircle,
  XCircle,
  RefreshCw
} from 'lucide-react'
import { useSystemStatus } from '../hooks/useSystemStatus'
import RSIControlPanel from '../components/RSIControlPanel'
import { apiService } from '../services/api'

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('overview')
  const { status, loading: statusLoading } = useSystemStatus()
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [currentUser, setCurrentUser] = useState<any>(null)

  const tabs = [
    { id: 'overview', label: 'Overview', icon: Activity },
    { id: 'rsi', label: 'RSI Engine', icon: Brain },
    { id: 'cognitive', label: 'Cognitive Engine', icon: Brain },
    { id: 'memory', label: 'Memory System', icon: Database },
    { id: 'tools', label: 'Tool Gateway', icon: Zap },
    { id: 'users', label: 'Users', icon: Users },
    { id: 'network', label: 'Network', icon: Network },
    { id: 'security', label: 'Security', icon: Shield },
    { id: 'settings', label: 'Settings', icon: Settings },
  ]

  const systemStats = [
    { label: 'CPU Usage', value: `${status.cpuUsage.toFixed(1)}%`, icon: Cpu, trend: '+5%' },
    { label: 'Memory Usage', value: `${status.memoryUsage.toFixed(1)}%`, icon: MemoryStick, trend: '+2%' },
    { label: 'Active Connections', value: status.activeConnections.toString(), icon: Network, trend: '+12%' },
    { label: 'Response Time', value: `${status.responseTime}ms`, icon: Clock, trend: '-8%' },
  ]

  const recentActivity = [
    { id: 1, user: 'User123', action: 'Chat interaction', time: '2 min ago', status: 'success' },
    { id: 2, user: 'User456', action: 'Memory query', time: '5 min ago', status: 'success' },
    { id: 3, user: 'User789', action: 'Tool execution', time: '8 min ago', status: 'warning' },
    { id: 4, user: 'System', action: 'Memory cleanup', time: '15 min ago', status: 'info' },
  ]

  const renderStatusIcon = (isActive: boolean) => {
    return isActive ? (
      <CheckCircle className="w-5 h-5 text-green-500" />
    ) : (
      <XCircle className="w-5 h-5 text-red-500" />
    )
  }

  const handleEmergencyStop = async () => {
    if (confirm('Are you sure you want to initiate emergency stop? This will immediately halt all AI operations.')) {
      try {
        await apiService.emergencyStop()
        console.log('Emergency stop initiated')
        alert('Emergency stop executed successfully')
      } catch (error) {
        console.error('Failed to execute emergency stop:', error)
        alert('Failed to execute emergency stop. Check console for details.')
      }
    }
  }

  const renderCognitiveEngine = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Model Status</h3>
            {renderStatusIcon(status.localModel)}
          </div>
          <div className="text-3xl font-bold text-blue-500">Online</div>
          <div className="text-sm text-gray-400 mt-2">Llama2 7B</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Requests/sec</h3>
            <Clock className="w-5 h-5 text-gray-400" />
          </div>
          <div className="text-3xl font-bold">42.5</div>
          <div className="text-sm text-gray-400 mt-2">+15% from last hour</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Avg Latency</h3>
            <Zap className="w-5 h-5 text-gray-400" />
          </div>
          <div className="text-3xl font-bold">120ms</div>
          <div className="text-sm text-gray-400 mt-2">-8% from last hour</div>
        </div>
      </div>

      <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold mb-4">Model Performance</h3>
        <div className="h-64 flex items-center justify-center bg-gray-800 rounded-lg">
          <p className="text-gray-400">Performance metrics visualization</p>
        </div>
      </div>

      <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold mb-4">Active Models</h3>
        <div className="space-y-3">
          {['Llama2 7B', 'Mistral 7B', 'CodeLlama 7B'].map((model) => (
            <div key={model} className="flex items-center justify-between p-3 bg-gray-800 rounded-lg">
              <div className="flex items-center space-x-3">
                <Brain className="w-5 h-5 text-blue-500" />
                <span>{model}</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full" />
                <span className="text-sm text-gray-400">Active</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )

  const renderMemorySystem = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Total Memories</h3>
            <Database className="w-5 h-5 text-gray-400" />
          </div>
          <div className="text-3xl font-bold">12,458</div>
          <div className="text-sm text-gray-400 mt-2">+234 today</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Storage Used</h3>
            <MemoryStick className="w-5 h-5 text-gray-400" />
          </div>
          <div className="text-3xl font-bold">2.4 GB</div>
          <div className="text-sm text-gray-400 mt-2">of 10 GB total</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Retention Rate</h3>
            <Clock className="w-5 h-5 text-gray-400" />
          </div>
          <div className="text-3xl font-bold">94.2%</div>
          <div className="text-sm text-gray-400 mt-2">+2.1% from last week</div>
        </div>
      </div>

      <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold mb-4">Memory Distribution</h3>
        <div className="space-y-3">
          {[
            { type: 'Episodic', count: 4521, percentage: 36 },
            { type: 'Semantic', count: 6234, percentage: 50 },
            { type: 'Procedural', count: 1703, percentage: 14 },
          ].map((memory) => (
            <div key={memory.type} className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>{memory.type}</span>
                <span>{memory.count} ({memory.percentage}%)</span>
              </div>
              <div className="w-full bg-gray-800 rounded-full h-2">
                <div 
                  className="bg-blue-500 h-2 rounded-full" 
                  style={{ width: `${memory.percentage}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      {/* Header */}
      <header className="bg-gray-900 border-b border-gray-800 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Brain className="w-8 h-8 text-blue-500" />
              <div>
                <h1 className="text-xl font-bold">Synthos OS</h1>
                <p className="text-xs text-gray-400">Operator Console</p>
              </div>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 text-sm">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              <span className="text-gray-400">System Online</span>
            </div>
            <button
              className="bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center space-x-2"
              onClick={() => window.location.reload()}
            >
              <RefreshCw className="w-4 h-4" />
              <span>Refresh</span>
            </button>
            <button
              className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
              onClick={handleEmergencyStop}
            >
              Emergency Stop
            </button>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className="w-64 bg-gray-900 border-r border-gray-800 min-h-screen">
          <nav className="p-4 space-y-2">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                    activeTab === tab.id
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-400 hover:bg-gray-800 hover:text-gray-200'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span>{tab.label}</span>
                </button>
              )
            })}
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-6">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* Stats Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {systemStats.map((stat) => {
                  const Icon = stat.icon
                  return (
                    <div key={stat.label} className="bg-gray-900 border border-gray-800 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <Icon className="w-5 h-5 text-gray-400" />
                        <span className={`text-xs ${stat.trend.startsWith('+') ? 'text-green-400' : 'text-red-400'}`}>
                          {stat.trend}
                        </span>
                      </div>
                      <div className="text-2xl font-bold">{stat.value}</div>
                      <div className="text-sm text-gray-400">{stat.label}</div>
                    </div>
                  )
                })}
              </div>

              {/* System Health */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold">Local Model</h3>
                    {renderStatusIcon(status.localModel)}
                  </div>
                  <div className="text-sm text-gray-400">
                    {status.localModel ? 'Operational' : 'Offline'}
                  </div>
                </div>
                <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold">Memory Engine</h3>
                    {renderStatusIcon(status.memoryEngine)}
                  </div>
                  <div className="text-sm text-gray-400">
                    {status.memoryEngine ? 'Active' : 'Inactive'}
                  </div>
                </div>
                <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold">Tool Gateway</h3>
                    {renderStatusIcon(status.toolGateway)}
                  </div>
                  <div className="text-sm text-gray-400">
                    {status.toolGateway ? 'Ready' : 'Unavailable'}
                  </div>
                </div>
              </div>

              {/* Charts Section */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                  <h3 className="text-lg font-semibold mb-4">Cognitive Engine Load</h3>
                  <div className="h-64 flex items-center justify-center bg-gray-800 rounded-lg">
                    <p className="text-gray-400">Real-time load visualization</p>
                  </div>
                </div>
                <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                  <h3 className="text-lg font-semibold mb-4">Memory Usage Over Time</h3>
                  <div className="h-64 flex items-center justify-center bg-gray-800 rounded-lg">
                    <p className="text-gray-400">Memory trends visualization</p>
                  </div>
                </div>
              </div>

              {/* Recent Activity */}
              <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
                <div className="space-y-3">
                  {recentActivity.map((activity) => (
                    <div key={activity.id} className="flex items-center justify-between py-2 border-b border-gray-800 last:border-0">
                      <div className="flex items-center space-x-3">
                        <div className={`w-2 h-2 rounded-full ${
                          activity.status === 'success' ? 'bg-green-500' :
                          activity.status === 'warning' ? 'bg-yellow-500' :
                          'bg-blue-500'
                        }`} />
                        <div>
                          <div className="font-medium">{activity.user}</div>
                          <div className="text-sm text-gray-400">{activity.action}</div>
                        </div>
                      </div>
                      <div className="text-sm text-gray-400">{activity.time}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'rsi' && <RSIControlPanel />}
          {activeTab === 'cognitive' && renderCognitiveEngine()}
          {activeTab === 'memory' && renderMemorySystem()}

          {activeTab === 'tools' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold">Available Tools</h3>
                    <Zap className="w-5 h-5 text-gray-400" />
                  </div>
                  <div className="text-3xl font-bold">24</div>
                  <div className="text-sm text-gray-400 mt-2">All operational</div>
                </div>
                <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold">Executions/min</h3>
                    <Activity className="w-5 h-5 text-gray-400" />
                  </div>
                  <div className="text-3xl font-bold">156</div>
                  <div className="text-sm text-gray-400 mt-2">+12% from last hour</div>
                </div>
                <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold">Success Rate</h3>
                    <CheckCircle className="w-5 h-5 text-gray-400" />
                  </div>
                  <div className="text-3xl font-bold">98.5%</div>
                  <div className="text-sm text-gray-400 mt-2">-0.2% from last hour</div>
                </div>
                <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold">Avg Duration</h3>
                    <Clock className="w-5 h-5 text-gray-400" />
                  </div>
                  <div className="text-3xl font-bold">450ms</div>
                  <div className="text-sm text-gray-400 mt-2">-15% from last hour</div>
                </div>
              </div>

              <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4">Tool Registry</h3>
                <div className="space-y-3">
                  {['File Manager', 'Code Editor', 'Terminal', 'Browser', 'Calculator', 'Calendar'].map((tool) => (
                    <div key={tool} className="flex items-center justify-between p-3 bg-gray-800 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <Zap className="w-5 h-5 text-blue-500" />
                        <span>{tool}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-green-500 rounded-full" />
                        <span className="text-sm text-gray-400">Available</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'users' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold">Total Users</h3>
                    <Users className="w-5 h-5 text-gray-400" />
                  </div>
                  <div className="text-3xl font-bold">1,234</div>
                  <div className="text-sm text-gray-400 mt-2">+45 this week</div>
                </div>
                <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold">Active Now</h3>
                    <Activity className="w-5 h-5 text-gray-400" />
                  </div>
                  <div className="text-3xl font-bold">89</div>
                  <div className="text-sm text-gray-400 mt-2">Peak: 124</div>
                </div>
                <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold">Avg Session</h3>
                    <Clock className="w-5 h-5 text-gray-400" />
                  </div>
                  <div className="text-3xl font-bold">23m</div>
                  <div className="text-sm text-gray-400 mt-2">+5m from last week</div>
                </div>
              </div>

              <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4">Recent Users</h3>
                <div className="space-y-3">
                  {['user@example.com', 'admin@synthos.os', 'developer@test.com'].map((user) => (
                    <div key={user} className="flex items-center justify-between p-3 bg-gray-800 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                          {user.charAt(0).toUpperCase()}
                        </div>
                        <span>{user}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-green-500 rounded-full" />
                        <span className="text-sm text-gray-400">Online</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'network' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold">Bandwidth</h3>
                    <Network className="w-5 h-5 text-gray-400" />
                  </div>
                  <div className="text-3xl font-bold">1.2 GB/s</div>
                  <div className="text-sm text-gray-400 mt-2">Peak: 2.4 GB/s</div>
                </div>
                <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold">Latency</h3>
                    <Clock className="w-5 h-5 text-gray-400" />
                  </div>
                  <div className="text-3xl font-bold">12ms</div>
                  <div className="text-sm text-gray-400 mt-2">Avg: 15ms</div>
                </div>
                <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold">Uptime</h3>
                    <CheckCircle className="w-5 h-5 text-gray-400" />
                  </div>
                  <div className="text-3xl font-bold">99.9%</div>
                  <div className="text-sm text-gray-400 mt-2">Last 30 days</div>
                </div>
              </div>

              <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4">Network Topology</h3>
                <div className="h-64 flex items-center justify-center bg-gray-800 rounded-lg">
                  <p className="text-gray-400">Network visualization</p>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'security' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold">Security Score</h3>
                    <Shield className="w-5 h-5 text-gray-400" />
                  </div>
                  <div className="text-3xl font-bold text-green-500">A+</div>
                  <div className="text-sm text-gray-400 mt-2">Excellent</div>
                </div>
                <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold">Threats Blocked</h3>
                    <AlertTriangle className="w-5 h-5 text-gray-400" />
                  </div>
                  <div className="text-3xl font-bold">1,234</div>
                  <div className="text-sm text-gray-400 mt-2">Last 24 hours</div>
                </div>
                <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold">Active Sessions</h3>
                    <Users className="w-5 h-5 text-gray-400" />
                  </div>
                  <div className="text-3xl font-bold">89</div>
                  <div className="text-sm text-gray-400 mt-2">All verified</div>
                </div>
              </div>

              <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4">Security Events</h3>
                <div className="space-y-3">
                  {[
                    { event: 'Authentication attempt blocked', time: '2 min ago', severity: 'high' },
                    { event: 'API rate limit exceeded', time: '15 min ago', severity: 'medium' },
                    { event: 'Suspicious activity detected', time: '1 hour ago', severity: 'low' },
                  ].map((item) => (
                    <div key={item.event} className="flex items-center justify-between p-3 bg-gray-800 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <AlertTriangle className={`w-5 h-5 ${
                          item.severity === 'high' ? 'text-red-500' :
                          item.severity === 'medium' ? 'text-yellow-500' :
                          'text-blue-500'
                        }`} />
                        <span>{item.event}</span>
                      </div>
                      <span className="text-sm text-gray-400">{item.time}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'settings' && (
            <div className="space-y-6">
              <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4">System Configuration</h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-3 bg-gray-800 rounded-lg">
                    <span>Auto-scaling</span>
                    <button className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg text-sm">
                      Enabled
                    </button>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-gray-800 rounded-lg">
                    <span>Load Balancing</span>
                    <button className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg text-sm">
                      Enabled
                    </button>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-gray-800 rounded-lg">
                    <span>Monitoring</span>
                    <button className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg text-sm">
                      Enabled
                    </button>
                  </div>
                </div>
              </div>

              <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4">Model Configuration</h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-3 bg-gray-800 rounded-lg">
                    <span>Default Model</span>
                    <select className="bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-sm">
                      <option>Llama2 7B</option>
                      <option>Mistral 7B</option>
                      <option>CodeLlama 7B</option>
                    </select>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-gray-800 rounded-lg">
                    <span>Temperature</span>
                    <input type="range" min="0" max="1" step="0.1" value="0.7" className="w-32" />
                  </div>
                  <div className="flex items-center justify-between p-3 bg-gray-800 rounded-lg">
                    <span>Max Tokens</span>
                    <input type="number" value="2048" className="bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-sm w-24" />
                  </div>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}
