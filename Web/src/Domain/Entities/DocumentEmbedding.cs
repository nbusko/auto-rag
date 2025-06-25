using Pgvector;

namespace AutoRag.Domain.Entities;

public sealed class DocumentEmbedding
{
    public Guid DocumentId { get; set; }
    public int ChunkIndex { get; set; }
    public string Content { get; set; } = string.Empty;

    public Vector Embedding { get; set; }
}
