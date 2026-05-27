import React, { useState } from "react"
import { cn } from "../../lib/utils"

const TabsContext = React.createContext(null)

function Tabs({ defaultValue, value, onValueChange, className, children, ...props }) {
  const [tab, setTab] = useState(value || defaultValue)
  const activeTab = value !== undefined ? value : tab
  const setActiveTab = onValueChange || setTab

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className={cn("", className)} {...props}>{children}</div>
    </TabsContext.Provider>
  )
}

function TabsList({ className, children, ...props }) {
  return (
    <div className={cn("inline-flex h-9 items-center justify-center rounded-lg bg-muted p-1 text-muted-foreground", className)} {...props}>
      {children}
    </div>
  )
}

function TabsTrigger({ value, className, children, ...props }) {
  const { activeTab, setActiveTab } = React.useContext(TabsContext)
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center whitespace-nowrap rounded-md px-3 py-1 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
        activeTab === value && "bg-background text-foreground shadow",
        className
      )}
      onClick={() => setActiveTab(value)}
      {...props}
    >
      {children}
    </button>
  )
}

function TabsContent({ value, className, children, ...props }) {
  const { activeTab } = React.useContext(TabsContext)
  if (activeTab !== value) return null
  return (
    <div className={cn("mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2", className)} {...props}>
      {children}
    </div>
  )
}

export { Tabs, TabsList, TabsTrigger, TabsContent }
