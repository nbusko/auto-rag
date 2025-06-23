using AutoRag.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace AutoRag.Infrastructure.Persistence.Configurations;

internal sealed class ChatMessageConfiguration : IEntityTypeConfiguration<ChatMessage>
{
    public void Configure(EntityTypeBuilder<ChatMessage> b)
    {
        b.ToTable("chat_history");
        b.HasKey(x => x.Id);
        b.Property(x => x.Id).HasColumnName("message_id");
        b.Property(x => x.RagId).HasColumnName("rag_id");
        b.Property(x => x.MessageType).HasColumnName("message_type");
        b.Property(x => x.UserId).HasColumnName("user_id");
        b.Property(x => x.Text).HasColumnName("text");
    }
}