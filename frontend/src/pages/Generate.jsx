import React, { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Textarea } from '../components/ui/textarea'
import { Alert, AlertTitle, AlertDescription } from '../components/ui/alert'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../components/ui/tabs'
import { Sparkles, FileText, Loader2, CheckCircle, AlertCircle, Download } from 'lucide-react'
import { generateSingle, generateAll, listUploadedFiles, downloadFile } from '../lib/api'

export default function Generate() {
  const navigate = useNavigate()
  const location = useLocation()
  const [tab, setTab] = useState('single')
  const [files, setFiles] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)
  const [batchResult, setBatchResult] = useState(null)

  const [form, setForm] = useState({
    nome_empresa: '',
    segmento: '',
    cidade: '',
    diferenciais: '',
    publico_alvo: '',
  })

  const [selectedFile, setSelectedFile] = useState('')

  useEffect(() => {
    listUploadedFiles().then(data => {
      setFiles(data.files || [])
      if (location.state?.filename) {
        setSelectedFile(location.state.filename)
        setTab('batch')
      }
    }).catch(() => {})
  }, [location.state])

  const handleSingle = async () => {
    if (!form.nome_empresa || !form.segmento || !form.cidade) {
      setError('Preencha nome, segmento e cidade')
      return
    }
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const data = await generateSingle(form)
      setResult(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const handleBatch = async () => {
    if (!selectedFile) {
      setError('Selecione um arquivo CSV')
      return
    }
    setLoading(true)
    setError(null)
    setBatchResult(null)
    try {
      const data = await generateAll(selectedFile)
      setBatchResult(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Gerar Conteúdo SEO</h1>
        <p className="text-muted-foreground">Crie descrições, FAQs e posts para Google Meu Negócio</p>
      </div>

      <Tabs value={tab} onValueChange={setTab}>
        <TabsList>
          <TabsTrigger value="single">Empresa Individual</TabsTrigger>
          <TabsTrigger value="batch">Lote (CSV)</TabsTrigger>
        </TabsList>

        <TabsContent value="single">
          <Card>
            <CardHeader>
              <CardTitle>Dados da Empresa</CardTitle>
              <CardDescription>Preencha as informações para gerar o conteúdo SEO</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <label className="text-sm font-medium">Nome da Empresa *</label>
                  <Input placeholder="Ex: Padaria Doce Sabor" value={form.nome_empresa} onChange={e => setForm({...form, nome_empresa: e.target.value})} />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Segmento *</label>
                  <Input placeholder="Ex: Panificadora" value={form.segmento} onChange={e => setForm({...form, segmento: e.target.value})} />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Cidade *</label>
                  <Input placeholder="Ex: São Paulo - SP" value={form.cidade} onChange={e => setForm({...form, cidade: e.target.value})} />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Público-Alvo</label>
                  <Input placeholder="Ex: Famílias da região" value={form.publico_alvo} onChange={e => setForm({...form, publico_alvo: e.target.value})} />
                </div>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Diferenciais</label>
                <Textarea placeholder="Ex: Produtos artesanais, entrega grátis" value={form.diferenciais} onChange={e => setForm({...form, diferenciais: e.target.value})} />
              </div>
              <Button onClick={handleSingle} disabled={loading} className="w-full">
                {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Sparkles className="mr-2 h-4 w-4" />}
                {loading ? 'Gerando...' : 'Gerar Conteúdo SEO'}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="batch">
          <Card>
            <CardHeader>
              <CardTitle>Processar CSV</CardTitle>
              <CardDescription>Selecione um arquivo enviado para gerar conteúdo de todas as empresas</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {files.length === 0 ? (
                <Alert>
                  <AlertCircle className="h-4 w-4" />
                  <AlertTitle>Nenhum arquivo</AlertTitle>
                  <AlertDescription>Faça upload de um CSV primeiro na seção Upload CSV.</AlertDescription>
                </Alert>
              ) : (
                <div className="space-y-2">
                  <label className="text-sm font-medium">Selecione o arquivo</label>
                  <select
                    className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm"
                    value={selectedFile}
                    onChange={e => setSelectedFile(e.target.value)}
                  >
                    <option value="">Selecione...</option>
                    {files.map(f => <option key={f.name} value={f.name}>{f.name}</option>)}
                  </select>
                </div>
              )}
              <Button onClick={handleBatch} disabled={loading || !selectedFile} className="w-full">
                {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <FileText className="mr-2 h-4 w-4" />}
                {loading ? 'Processando...' : 'Processar Todas as Empresas'}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Erro</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {result && (
        <ResultDisplay result={result} />
      )}

      {batchResult && (
        <div className="space-y-4">
          <Alert>
            <CheckCircle className="h-4 w-4" />
            <AlertTitle>Processamento Concluído</AlertTitle>
            <AlertDescription>{batchResult.total} empresas processadas com sucesso!</AlertDescription>
          </Alert>
          <Button onClick={() => window.open(downloadFile(batchResult.output_file), '_blank')}>
            <Download className="mr-2 h-4 w-4" /> Baixar CSV Completo
          </Button>
          <div className="space-y-4">
            {batchResult.results?.map((r, i) => (
              <ResultDisplay key={i} result={r} />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function ResultDisplay({ result }) {
  const tabs = [
    { value: 'descricao', label: 'Descrição SEO', content: result.descricao_seo },
    { value: 'faqs', label: 'FAQs', content: result.faqs },
    { value: 'posts', label: 'Posts GBP', content: result.posts_gbp },
  ]
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <CheckCircle className="h-5 w-5 text-green-500" />
          {result.nome_empresa}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="descricao">
          <TabsList>
            {tabs.map(t => <TabsTrigger key={t.value} value={t.value}>{t.label}</TabsTrigger>)}
          </TabsList>
          {tabs.map(t => (
            <TabsContent key={t.value} value={t.value}>
              <div className="rounded-md bg-muted p-4 whitespace-pre-wrap text-sm">{t.content}</div>
            </TabsContent>
          ))}
        </Tabs>
      </CardContent>
    </Card>
  )
}
