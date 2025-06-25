using System.Globalization;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using AutoRag.Application.DTOs;
using AutoRag.Application.Interfaces;

namespace AutoRag.Infrastructure.External.FastApi;

public sealed class DocumentProcessorClient : IDocumentProcessorService
{
    private readonly HttpClient _http;
    public DocumentProcessorClient(HttpClient http) => _http = http;

    /* десериализация ответа python-сервиса */
    private sealed record DpResponse(
        string Status,
        string Message,
        IReadOnlyList<string>?               Texts,
        IReadOnlyList<IReadOnlyList<float>>? Embeddings);

    public async Task<DocumentProcessorResult> ProcessDocumentAsync(
        Guid   documentId,
        Stream fileContent,
        RagConfigDto cfg,
        CancellationToken ct = default)
    {
        /* -------- multipart-form для FastAPI -------- */
        using var form = new MultipartFormDataContent
        {
            { new StringContent(documentId.ToString()),          "document_id"  },
            { new StringContent(cfg.SplitMethod),                "split_method" },
            { new StringContent(cfg.BatchSize.ToString()),       "batch_size"   },
            { new StringContent(cfg.LlmModel ?? "gpt-4o-mini"),  "llm_model"    },
            { new StringContent(cfg.Temperature
                    .ToString(CultureInfo.InvariantCulture)),    "temperature"  }
        };

        if (!string.IsNullOrWhiteSpace(cfg.SplitPrompt))
            form.Add(new StringContent(cfg.SplitPrompt!), "prompt_split");

        if (!string.IsNullOrWhiteSpace(cfg.TablePrompt))
            form.Add(new StringContent(cfg.TablePrompt!), "prompt_table");

        var filePart = new StreamContent(fileContent);
        filePart.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");
        form.Add(filePart, "document", "file.bin");

        /* -------- вызов python-сервиса -------- */
        using var resp = await _http.PostAsync("api/v1/documents/process", form, ct);
        resp.EnsureSuccessStatusCode();

        var dto = await resp.Content.ReadFromJsonAsync<DpResponse>(cancellationToken: ct)
                  ?? throw new InvalidOperationException("Empty response");

        return new DocumentProcessorResult(dto.Status, dto.Message, dto.Texts, dto.Embeddings);
    }
}