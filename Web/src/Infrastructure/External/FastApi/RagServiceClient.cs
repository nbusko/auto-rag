using System.Net.Http.Json;
using System.Text.Json;
using System.Text.Json.Serialization;
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

        var dict = new Dictionary<string, object?>
        {
            ["chat_id"]  = dto.ChatId,
            ["user_message"] = dto.UserMessage,
            ["document_id"] = dto.DocumentId,
            ["embeddings"]  = dto.Embeddings,
            ["text_chunks"] = dto.TextChunks,
            ["top_k"] = dto.TopK,
            ["temperature"] = dto.Temperature,
            ["threshold"] = dto.Threshold
        };

        if (!string.IsNullOrWhiteSpace(dto.PromptRetrieve))
            dict["prompt_retrieve"] = dto.PromptRetrieve;

        if (!string.IsNullOrWhiteSpace(dto.PromptAugmentation))
            dict["prompt_augmentation"] = dto.PromptAugmentation;

        if (!string.IsNullOrWhiteSpace(dto.PromptGeneration))
            dict["prompt_generation"] = dto.PromptGeneration;

        if (!string.IsNullOrWhiteSpace(dto.LlmModel))
            dict["llm"] = dto.LlmModel;

        using var resp = await _http.PostAsJsonAsync(
            "api/v1/rag/process",
            dict,
            new JsonSerializerOptions(JsonSerializerDefaults.Web),
            ct);

        resp.EnsureSuccessStatusCode();

        var json = await resp.Content.ReadFromJsonAsync<RagResponse>(cancellationToken: ct);
        return json?.GeneratedAnswer ?? "🤖 error";
    }
}