using AutoRag.Application.Interfaces;
using System.Net.Http.Json;

namespace AutoRag.Infrastructure.External.FastApi;

public sealed class AssistantClient : IAssistantService
{
    private readonly HttpClient _http;
    public AssistantClient(HttpClient http) => _http = http;

    public async Task<string> GetAnswerAsync(Guid messageId, CancellationToken ct = default)
    {
        var res = await _http.GetFromJsonAsync<AssistantResponse>(
            $"get_answer_by_message_id/{messageId}", ct);

        return res?.Answer ?? "🤖 error";
    }

    private sealed record AssistantResponse(string Answer);
}