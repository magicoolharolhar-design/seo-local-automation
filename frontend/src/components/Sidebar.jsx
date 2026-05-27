import React from 'react'
import { NavLink } from 'react-router-dom'
import { cn } from '../lib/utils'
import {
  LayoutDashboard,
  Upload,
  FileText,
  History,
  Settings,
  Sparkles,
} from 'lucide-react'

const links = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/upload', icon: Upload, label: 'Upload CSV' },
  { to: '/generate', icon: FileText, label: 'Gerar Conteúdo' },
  { to: '/history', icon: History, label: 'Histórico' },
  { to: '/settings', icon: Settings, label: 'Configurações' },
]

export default function Sidebar({ collapsed, onToggle }) {
  return (
    <aside className={cn(
      "fixed inset-y-0 left-0 z-30 flex flex-col border-r bg-card transition-all duration-300",
      collapsed ? "w-16" : "w-64"
    )}>
      <div className="flex h-14 items-center gap-2 border-b px-4">
        <Sparkles className="h-6 w-6 text-primary shrink-0" />
        {!collapsed && <span className="font-bold text-lg truncate">SEO Local</span>}
      </div>
      <nav className="flex-1 space-y-1 p-2">
        {links.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) => cn(
              "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
              isActive
                ? "bg-primary/10 text-primary"
                : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
            )}
          >
            <Icon className="h-5 w-5 shrink-0" />
            {!collapsed && <span>{label}</span>}
          </NavLink>
        ))}
      </nav>
      <div className="border-t p-2">
        <button
          onClick={onToggle}
          className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-muted-foreground hover:bg-accent"
        >
          <span className="text-xs">{collapsed ? '→' : '←'}</span>
          {!collapsed && <span>Recolher</span>}
        </button>
      </div>
    </aside>
  )
}
