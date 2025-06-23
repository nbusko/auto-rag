using AutoRag.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace AutoRag.Infrastructure.Persistence.Configurations;

internal sealed class ShareLinkConfiguration : IEntityTypeConfiguration<ShareLink>
{
    public void Configure(EntityTypeBuilder<ShareLink> b)
    {
        b.ToTable("share_links");
        b.HasKey(x => x.Id);
        b.Property(x => x.Id).HasColumnName("token");
        b.Property(x => x.RagId).HasColumnName("rag_id");
        b.Property(x => x.Enabled).HasColumnName("enabled");
        b.Property(x => x.CreatedAt).HasColumnName("created_at");
    }
}
