using System.Net.Http.Json;
using System.Text.Json.Serialization;
using AutoRag.Application.DTOs;
using AutoRag.Application.Interfaces;

namespace AutoRag.Infrastructure.External.FastApi;

public sealed class RagServiceClient : IRagService
{
    private readonly HttpClient _http;
    public RagServiceClient(HttpClient http) => _http = http;

    private sealed record RagResponse(
        [property: JsonPropertyName("generated_answer")]
        string GeneratedAnswer);

    public async Task<string> GenerateAnswerAsync(RagRequestDto dto, CancellationToken ct = default)
    {
        /* формируем payload сразу в snake_case */
        var payload = new
        {
            chat_id      = dto.ChatId,
            user_message = dto.UserMessage,
            document_id  = dto.DocumentId,
            embeddings   = dto.Embeddings,
            text_chunks  = dto.TextChunks,
            top_k        = dto.TopK,
            temperature  = dto.Temperature,
            threshold    = dto.Threshold
        };

        using var resp = await _http.PostAsJsonAsync("api/v1/rag/process", payload, ct);
        resp.EnsureSuccessStatusCode();

        var json = await resp.Content.ReadFromJsonAsync<RagResponse>(cancellationToken: ct);
        return json?.GeneratedAnswer ?? "🤖 error";
    }
}