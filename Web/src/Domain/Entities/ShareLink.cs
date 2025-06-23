using AutoRag.Domain.Common;

namespace AutoRag.Domain.Entities;

public sealed class ShareLink : BaseEntity<Guid>      // Id == token
{
    public Guid RagId   { get; set; }
    public bool Enabled { get; set; } = true;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}