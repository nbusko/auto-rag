using AutoRag.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace AutoRag.Infrastructure.Persistence.Configurations;

internal sealed class DocumentEmbeddingConfiguration : IEntityTypeConfiguration<DocumentEmbedding>
{
    public void Configure(EntityTypeBuilder<DocumentEmbedding> b)
    {
        b.ToTable("document_embeddings");
        b.HasKey(x => new { x.DocumentId, x.ChunkIndex });
        b.Property(x => x.DocumentId).HasColumnName("document_id");
        b.Property(x => x.ChunkIndex).HasColumnName("chunk_index");
        b.Property(x => x.Content).HasColumnName("content");
        b.Property(x => x.Embedding)
         .HasColumnName("embedding")
         .HasColumnType("vector(312)");
    }
}