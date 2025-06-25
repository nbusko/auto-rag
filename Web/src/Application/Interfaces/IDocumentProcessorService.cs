namespace AutoRag.Application.Interfaces;

using AutoRag.Application.DTOs;

public interface IDocumentProcessorService
{
    /// <summary>
    /// Отправить документ в python-сервис вместе со ВСЕМИ
    /// параметрами, заданными в RagConfigDto.
    /// </summary>
    Task<DocumentProcessorResult> ProcessDocumentAsync(
        Guid   documentId,
        Stream fileContent,
        RagConfigDto cfg,
        CancellationToken ct = default);
}

public sealed record DocumentProcessorResult(
    string   Status,
    string   Message,
    IReadOnlyList<string>?               Texts,
    IReadOnlyList<IReadOnlyList<float>>? Embeddings);