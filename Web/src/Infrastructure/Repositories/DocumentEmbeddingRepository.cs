using AutoRag.Domain.Entities;
using AutoRag.Domain.Interfaces.Repositories;
using AutoRag.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;

namespace AutoRag.Infrastructure.Repositories;

public sealed class DocumentEmbeddingRepository : IDocumentEmbeddingRepository
{
    private readonly AutoRagContext _ctx;
    public DocumentEmbeddingRepository(AutoRagContext ctx)=>_ctx=ctx;

    public async Task<IReadOnlyList<DocumentEmbedding>> GetByDocumentIdAsync(Guid docId, CancellationToken ct = default)
        => await _ctx.DocumentEmbeddings
                     .AsNoTracking()
                     .Where(e => e.DocumentId == docId)
                     .OrderBy(e => e.ChunkIndex)
                     .ToListAsync(ct);
}