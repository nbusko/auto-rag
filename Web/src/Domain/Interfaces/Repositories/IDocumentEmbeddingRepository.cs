using AutoRag.Domain.Entities;

namespace AutoRag.Domain.Interfaces.Repositories;

public interface IDocumentEmbeddingRepository
{
    Task<IReadOnlyList<DocumentEmbedding>> GetByDocumentIdAsync(Guid docId, CancellationToken ct = default);
}
