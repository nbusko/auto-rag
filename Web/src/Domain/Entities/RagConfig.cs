using AutoRag.Domain.Common;

namespace AutoRag.Domain.Entities;

public sealed class RagConfig : BaseEntity<Guid>
{
    public string Prompt { get; set; } = string.Empty;
    public Guid? DocumentId { get; set; }

    public int TopK { get; set; } = 3;
    public decimal Temperature { get; set; } = 0.7m;
    public decimal Threshold   { get; set; } = 0.0m;
}

