using AutoRag.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace AutoRag.Infrastructure.Persistence.Configurations;

internal sealed class RagConfigConfiguration : IEntityTypeConfiguration<RagConfig>
{
    public void Configure(EntityTypeBuilder<RagConfig> b)
    {
        b.ToTable("rag_settings");
        b.HasKey(x => x.Id);
        b.Property(x => x.Id).HasColumnName("rag_id");
        b.Property(x => x.Prompt).HasColumnName("prompt");
        b.Property(x => x.DocumentId).HasColumnName("document_id");
        b.Property(x => x.TopK).HasColumnName("top_k");
        b.Property(x => x.Temperature).HasColumnName("temperature");
        b.Property(x => x.Threshold).HasColumnName("threshold");
    }
}
