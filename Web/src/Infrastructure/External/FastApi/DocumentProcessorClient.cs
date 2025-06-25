using System.Net.Http.Headers;
using System.Net.Http.Json;
using AutoRag.Application.Interfaces;

namespace AutoRag.Infrastructure.External.FastApi;

public sealed class DocumentProcessorClient : IDocumentProcessorService
{
    private readonly HttpClient _http;
    public DocumentProcessorClient(HttpClient http)=>_http=http;

    private sealed record DpResponse(
        string Status,
        string Message,
        IReadOnlyList<string>?              Texts,
        IReadOnlyList<IReadOnlyList<float>>?Embeddings);

    public async Task<DocumentProcessorResult> ProcessDocumentAsync(
        Guid   documentId,
        Stream fileContent,
        CancellationToken ct = default)
    {
        using var form = new MultipartFormDataContent
        {
            { new StringContent(documentId.ToString()), "document_id" },
            { new StringContent("batch"),               "split_method" },
            { new StringContent("1000"),                "batch_size" }
        };

        var filePart = new StreamContent(fileContent);
        filePart.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");
        form.Add(filePart, "document", "file.bin");

        using var resp = await _http.PostAsync("api/v1/documents/process", form, ct);
        resp.EnsureSuccessStatusCode();

        var dto = await resp.Content.ReadFromJsonAsync<DpResponse>(cancellationToken: ct)
                  ?? throw new InvalidOperationException("Empty response");

        return new DocumentProcessorResult(dto.Status, dto.Message, dto.Texts, dto.Embeddings);
    }
}