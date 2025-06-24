using System.Text.Json;
using AutoRag.Application.DTOs;

namespace AutoRag.Application.Interfaces;

public interface IRagService
{
    Task<string> GenerateAnswerAsync(RagRequestDto dto, CancellationToken ct = default);
}

public sealed record RagRequestDto(
    string ChatId,
    string UserMessage,
    Guid   DocumentId,
    IReadOnlyList<IReadOnlyList<float>> Embeddings,
    IReadOnlyList<string> TextChunks,
    int    TopK,
    float  Temperature,
    float  Threshold);
