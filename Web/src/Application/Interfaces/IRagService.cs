using AutoRag.Application.DTOs;

namespace AutoRag.Application.Interfaces;

public interface IRagService
{
    Task<string> GenerateAnswerAsync(RagRequestDto dto, CancellationToken ct = default);
}

public sealed record RagRequestDto(
    string ChatId,
    string UserMessage,
    Guid DocumentId,
    IReadOnlyList<IReadOnlyList<float>> Embeddings,
    IReadOnlyList<string> TextChunks,
    int TopK,
    float Temperature,
    float Threshold)
{
    public string? PromptRetrieve { get; init; }
    public string? PromptAugmentation { get; init; }
    public string? PromptGeneration { get; init; }
    public string? LlmModel { get; init; }
}

