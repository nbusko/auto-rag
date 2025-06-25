namespace AutoRag.Application.Interfaces;

using AutoRag.Application.DTOs;

public interface IDocumentProcessorService
{
    Task<DocumentProcessorResult> ProcessDocumentAsync(
        Guid documentId,
        Stream fileContent,
        RagConfigDto cfg,
        CancellationToken ct = default);
}

public sealed record DocumentProcessorResult(
    string Status,
    string Message,
    IReadOnlyList<string>? Texts,
    IReadOnlyList<IReadOnlyList<float>>? Embeddings);