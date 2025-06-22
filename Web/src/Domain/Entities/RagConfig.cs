using AutoRag.Domain.Common;

namespace AutoRag.Domain.Entities;

public sealed class RagConfig : BaseEntity<Guid>
{
    public string Prompt { get; set; } = string.Empty;
    public Guid? DocumentId { get; set; }
}

