import React, { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Alert, AlertTitle, AlertDescription } from '../components/ui/alert'
import { Settings as SettingsIcon, CheckCircle, AlertCircle, Eye, EyeOff, Save } from 'lucide-react'
import { getSettings, updateSettings } from '../lib/api'

export default function Settings() {
  const [form, setForm] = useState({
    openai_api_key: '',
    openai_model: 'gpt-4o-mini',
    content_language: 'pt-BR',
  })
  const [showKey, setShowKey] = useState(false)
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    getSettings().then(data => {
      setForm(prev => ({ ...prev, ...data }))
    }).catch(() => {})
  }, [])

  const handleSave = async () => {
    setSaving(true)
    setError(null)
    setMessage(null)
    try {
      await updateSettings(form)
      setMessage('Configurações salvas com sucesso!')
    } catch (e) {
      setError(e.message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Configurações</h1>
        <p className="text-muted-foreground">Gerencie sua integração com a OpenAI</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>API OpenAI</CardTitle>
          <CardDescription>Configure sua chave de API para gerar conteúdo com IA</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">Chave da API OpenAI</label>
            <div className="flex gap-2">
              <Input
                type={showKey ? 'text' : 'password'}
                placeholder="sk-..."
                value={form.openai_api_key}
                onChange={e => setForm({...form, openai_api_key: e.target.value})}
                className="flex-1"
              />
              <Button variant="outline" size="icon" onClick={() => setShowKey(!showKey)}>
                {showKey ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </Button>
            </div>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Modelo</label>
            <select
              className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm"
              value={form.openai_model}
              onChange={e => setForm({...form, openai_model: e.target.value})}
            >
              <option value="gpt-4o-mini">GPT-4o Mini (Rápido)</option>
              <option value="gpt-4o">GPT-4o (Potente)</option>
              <option value="gpt-3.5-turbo">GPT-3.5 Turbo (Econômico)</option>
            </select>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Idioma do Conteúdo</label>
            <Input value={form.content_language} onChange={e => setForm({...form, content_language: e.target.value})} />
          </div>
          <Button onClick={handleSave} disabled={saving} className="w-full">
            <Save className="mr-2 h-4 w-4" />
            {saving ? 'Salvando...' : 'Salvar Configurações'}
          </Button>
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
    </div>
  )
}
