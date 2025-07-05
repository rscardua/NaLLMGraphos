# Integração com Google Gemini

Este projeto agora suporta tanto OpenAI quanto Google Gemini como provedores de LLM.

## Configuração

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

As dependências incluem:
- `google-generativeai==0.8.5`
- `requests==2.31.0`

### 2. Configurar variáveis de ambiente

Adicione no arquivo `.env`:

```env
GEMINI_API_KEY=sua_chave_do_gemini_aqui
```

### 3. Obter chave da API do Gemini

1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crie uma nova chave de API
3. Copie e cole no arquivo `.env`

## Uso

### Via API REST

```json
{
  "question": "Sua pergunta aqui",
  "llm_provider": "gemini",
  "api_key": "sua_chave_aqui",
  "model_name": "gemini-pro"
}
```

### Via WebSocket

```json
{
  "type": "question",
  "question": "Sua pergunta aqui",
  "llm_provider": "gemini",
  "api_key": "sua_chave_aqui",
  "model_name": "gemini-pro"
}
```

## Modelos Disponíveis

### OpenAI

- `gpt-3.5-turbo` (padrão)
- `gpt-3.5-turbo-0613`
- `gpt-3.5-turbo-16k`
- `gpt-4`

### Gemini

- `gemini-pro` (padrão)
- `gemini-1.5-pro`

## Verificar Provedores Disponíveis

Use o endpoint `/available_providers` para verificar quais provedores têm chaves configuradas:

```bash
curl http://localhost:7860/available_providers
```

Resposta:

```json
{
  "providers": {
    "openai": true,
    "gemini": false
  }
}
```

## Implementação Técnica

A integração do Gemini usa a **API REST** diretamente para máxima compatibilidade com a versão `google-generativeai==0.8.5`. Isso garante:

- ✅ Compatibilidade total com a versão especificada
- ✅ Sem problemas de importação de módulos
- ✅ Controle total sobre requisições e respostas
- ✅ Suporte a streaming simulado para manter compatibilidade com o frontend

## Notas Importantes

1. **Limites de Tokens**: 
   - Gemini Pro: 32,768 tokens
   - Gemini 1.5 Pro: 1,048,576 tokens (1M)

2. **Streaming**: O Gemini usa streaming simulado para manter compatibilidade com a interface existente

3. **Tratamento de Erros**: Inclui tratamento específico para:
   - Chaves de API inválidas
   - Quotas excedidas
   - Filtros de segurança

4. **Fallback**: Se nenhum provedor for especificado, o OpenAI será usado como padrão

5. **Formato de Mensagens**: Conversão automática do formato OpenAI para Gemini
