import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '../components/ui/table'
import { Badge } from '../components/ui/badge'
import { History as HistoryIcon, Download, Eye, FileText } from 'lucide-react'
import { getHistory, downloadFile } from '../lib/api'

export default function History() {
  const navigate = useNavigate()
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getHistory().then(data => {
      setHistory(data.history || [])
    }).catch(() => {}).finally(() => setLoading(false))
  }, [])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Histórico</h1>
        <p className="text-muted-foreground">Gerações anteriores de conteúdo SEO</p>
      </div>

      {loading ? (
        <Card>
          <CardContent className="py-12 text-center text-muted-foreground">Carregando...</CardContent>
        </Card>
      ) : history.length === 0 ? (
        <Card>
          <CardContent className="py-12 text-center">
            <HistoryIcon className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
            <p className="text-muted-foreground">Nenhuma geração encontrada. Faça sua primeira geração!</p>
            <Button className="mt-4" onClick={() => navigate('/generate')}>Ir para Gerar Conteúdo</Button>
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardHeader>
            <CardTitle>Todas as Gerações</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>ID</TableHead>
                  <TableHead>Data</TableHead>
                  <TableHead>Arquivo</TableHead>
                  <TableHead>Empresas</TableHead>
                  <TableHead>Ações</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {history.map((h, i) => (
                  <TableRow key={h.id || i}>
                    <TableCell className="font-mono text-xs">{h.id}</TableCell>
                    <TableCell>{new Date(h.timestamp).toLocaleString('pt-BR')}</TableCell>
                    <TableCell><FileText className="inline h-4 w-4 mr-1" />{h.filename}</TableCell>
                    <TableCell><Badge variant="secondary">{h.total}</Badge></TableCell>
                    <TableCell>
                      <div className="flex gap-2">
                        <Button variant="outline" size="sm" onClick={() => navigate(`/results/${h.id}`)}>
                          <Eye className="h-4 w-4" />
                        </Button>
                        <Button variant="outline" size="sm" onClick={() => window.open(downloadFile(h.output), '_blank')}>
                          <Download className="h-4 w-4" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
