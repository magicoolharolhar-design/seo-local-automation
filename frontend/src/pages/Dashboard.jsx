import React, { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Badge } from '../components/ui/badge'
import { Upload, FileText, History as HistoryIcon, Settings, ArrowRight, Sparkles } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { getHistory } from '../lib/api'

export default function Dashboard() {
  const navigate = useNavigate()
  const [stats, setStats] = useState({ total: 0, lastRun: null })

  useEffect(() => {
    getHistory().then(data => {
      if (data.history?.length) {
        setStats({
          total: data.history.reduce((acc, h) => acc + (h.total || 0), 0),
          lastRun: data.history[0],
        })
      }
    }).catch(() => {})
  }, [])

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-muted-foreground">Bem-vindo ao SEO Local Automation</p>
        </div>
        <Sparkles className="h-8 w-8 text-primary" />
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Conteúdos Gerados</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Arquivos Processados</CardTitle>
            <HistoryIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.lastRun ? 1 : 0}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Status</CardTitle>
            <Badge variant="secondary" className="h-4 w-4" />
          </CardHeader>
          <CardContent>
            <Badge variant="outline" className="text-green-600 border-green-600">Online</Badge>
          </CardContent>
        </Card>
      </div>

      {stats.lastRun && (
        <Card>
          <CardHeader>
            <CardTitle>Última Execução</CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            <p>Arquivo: <strong>{stats.lastRun.filename}</strong></p>
            <p>Empresas: <strong>{stats.lastRun.total}</strong></p>
            <p>Data: {new Date(stats.lastRun.timestamp).toLocaleString('pt-BR')}</p>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-4 md:grid-cols-3">
        <Card className="hover:shadow-md transition-shadow cursor-pointer" onClick={() => navigate('/upload')}>
          <CardHeader>
            <Upload className="h-8 w-8 text-primary mb-2" />
            <CardTitle>Upload CSV</CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            Faça upload da planilha com dados das empresas
          </CardContent>
        </Card>
        <Card className="hover:shadow-md transition-shadow cursor-pointer" onClick={() => navigate('/generate')}>
          <CardHeader>
            <FileText className="h-8 w-8 text-primary mb-2" />
            <CardTitle>Gerar Conteúdo</CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            Gere descrições SEO, FAQs e posts automaticamente
          </CardContent>
        </Card>
        <Card className="hover:shadow-md transition-shadow cursor-pointer" onClick={() => navigate('/settings')}>
          <CardHeader>
            <Settings className="h-8 w-8 text-primary mb-2" />
            <CardTitle>Configurações</CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            Configure sua chave da API OpenAI
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
