import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Alert, AlertTitle, AlertDescription } from '../components/ui/alert'
import { FileText, Download, ArrowLeft } from 'lucide-react'
import { downloadFile, getHistory } from '../lib/api'

export default function Results() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [history, setHistory] = useState(null)

  useEffect(() => {
    if (id) {
      getHistory().then(data => {
        const entry = data.history?.find(h => h.id === id)
        if (entry) setHistory(entry)
      }).catch(() => {})
    }
  }, [id])

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => navigate('/history')}>
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Resultados</h1>
          <p className="text-muted-foreground">Conteúdo SEO gerado</p>
        </div>
      </div>

      {history ? (
        <Card>
          <CardHeader>
            <CardTitle>Detalhes da Geração</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <p><strong>ID:</strong> {history.id}</p>
            <p><strong>Arquivo:</strong> {history.filename}</p>
            <p><strong>Empresas:</strong> {history.total}</p>
            <p><strong>Data:</strong> {new Date(history.timestamp).toLocaleString('pt-BR')}</p>
            <Button className="mt-4" onClick={() => window.open(downloadFile(history.output), '_blank')}>
              <Download className="mr-2 h-4 w-4" /> Baixar CSV
            </Button>
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardContent className="py-12 text-center">
            <FileText className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
            <p className="text-muted-foreground">Selecione um resultado do histórico para visualizar os detalhes.</p>
            <Button className="mt-4" onClick={() => navigate('/history')}>Ver Histórico</Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
