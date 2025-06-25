namespace AutoRag.Application.Interfaces;

public interface IDocumentProcessorService
{
    Task<DocumentProcessorResult> ProcessDocumentAsync(
        Guid   documentId,
        Stream fileContent,
        CancellationToken ct = default);
}

public sealed record DocumentProcessorResult(
    string   Status,
    string   Message,
    IReadOnlyList<string>?              Texts,
    IReadOnlyList<IReadOnlyList<float>>? Embeddings);