using AutoRag.Domain.Entities;
using AutoRag.Domain.Interfaces.Repositories;
using AutoRag.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;
using Pgvector;

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

    public async Task ReplaceAsync(Guid documentId,
                                   IEnumerable<string> texts,
                                   IEnumerable<IReadOnlyList<float>> embeddings,
                                   CancellationToken ct = default)
    {
        /* удалить старые записи */
        var existing = _ctx.DocumentEmbeddings.Where(e => e.DocumentId == documentId);
        _ctx.DocumentEmbeddings.RemoveRange(existing);

        /* добавить новые */
        int idx = 0;
        foreach (var pair in texts.Zip(embeddings))
        {
            var ent = new DocumentEmbedding
            {
                DocumentId = documentId,
                ChunkIndex = idx++,
                Content    = pair.First,
                Embedding  = new Vector(pair.Second.ToArray())
            };
            await _ctx.DocumentEmbeddings.AddAsync(ent, ct);
        }

        await _ctx.SaveChangesAsync(ct);
    }
}