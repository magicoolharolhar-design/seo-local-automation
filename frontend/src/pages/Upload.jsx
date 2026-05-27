import React, { useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Alert, AlertTitle, AlertDescription } from '../components/ui/alert'
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '../components/ui/table'
import { Badge } from '../components/ui/badge'
import { Upload as UploadIcon, FileText, CheckCircle, AlertCircle, Eye } from 'lucide-react'
import { uploadCsv, previewCsv, listUploadedFiles } from '../lib/api'

export default function Upload() {
  const navigate = useNavigate()
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState(null)
  const [error, setError] = useState(null)
  const [preview, setPreview] = useState(null)
  const [files, setFiles] = useState([])

  const loadFiles = useCallback(async () => {
    try {
      const data = await listUploadedFiles()
      setFiles(data.files || [])
    } catch {}
  }, [])

  React.useEffect(() => { loadFiles() }, [loadFiles])

  const handleUpload = async () => {
    if (!file) return
    setUploading(true)
    setError(null)
    setMessage(null)
    try {
      await uploadCsv(file)
      setMessage(`Arquivo "${file.name}" enviado com sucesso!`)
      setFile(null)
      await loadFiles()
    } catch (e) {
      setError(e.message)
    } finally {
      setUploading(false)
    }
  }

  const handlePreview = async (filename) => {
    try {
      const data = await previewCsv(filename)
      setPreview(data)
    } catch (e) {
      setError(e.message)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Upload CSV</h1>
        <p className="text-muted-foreground">Envie o arquivo com os dados das empresas</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Selecionar Arquivo</CardTitle>
          <CardDescription>Formato: CSV com colunas nome_empresa, segmento, cidade, diferenciais, publico_alvo</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center gap-4">
            <input
              type="file"
              accept=".csv"
              onChange={e => setFile(e.target.files[0])}
              className="block w-full text-sm text-muted-foreground file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-primary file:text-primary-foreground hover:file:bg-primary/90"
            />
            <Button onClick={handleUpload} disabled={!file || uploading}>
              <UploadIcon className="mr-2 h-4 w-4" />
              {uploading ? 'Enviando...' : 'Upload'}
            </Button>
          </div>
          {message && (
            <Alert>
              <CheckCircle className="h-4 w-4" />
              <AlertTitle>Sucesso</AlertTitle>
              <AlertDescription>{message}</AlertDescription>
            </Alert>
          )}
          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertTitle>Erro</AlertTitle>
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>

      {files.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Arquivos Enviados</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Arquivo</TableHead>
                  <TableHead>Tamanho</TableHead>
                  <TableHead>Ações</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {files.map(f => (
                  <TableRow key={f.name}>
                    <TableCell className="font-medium"><FileText className="inline h-4 w-4 mr-2" />{f.name}</TableCell>
                    <TableCell>{(f.size / 1024).toFixed(1)} KB</TableCell>
                    <TableCell>
                      <div className="flex gap-2">
                        <Button variant="outline" size="sm" onClick={() => handlePreview(f.name)}>
                          <Eye className="h-4 w-4 mr-1" /> Visualizar
                        </Button>
                        <Button size="sm" onClick={() => navigate('/generate', { state: { filename: f.name } })}>
                          Gerar
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

      {preview && (
        <Card>
          <CardHeader>
            <CardTitle>Pré-visualização: {preview.businesses?.[0]?.nome_empresa ? `${preview.count} empresas` : ''}</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Empresa</TableHead>
                  <TableHead>Segmento</TableHead>
                  <TableHead>Cidade</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {preview.businesses?.slice(0, 10).map((b, i) => (
                  <TableRow key={i}>
                    <TableCell>{b.nome_empresa}</TableCell>
                    <TableCell>{b.segmento}</TableCell>
                    <TableCell>{b.cidade}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
            {preview.count > 10 && <p className="text-sm text-muted-foreground mt-2">Mostrando 10 de {preview.count} empresas</p>}
            <div className="flex gap-2 mt-4">
              <Badge>{preview.count} empresas</Badge>
              <Button size="sm" onClick={() => navigate('/generate', { state: { filename: preview.businesses?.[0]?.nome_empresa ? files.find(f => true)?.name : null } })}>
                Gerar Conteúdo para Todos
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
