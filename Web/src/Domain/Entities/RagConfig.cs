using AutoRag.Domain.Common;

namespace AutoRag.Domain.Entities;

public sealed class RagConfig : BaseEntity<Guid>
{
    public string Prompt { get; set; } = string.Empty;
    public string? RetrievePrompt { get; set; }
    public string? AugmentationPrompt { get; set; }
    public string  LlmModel { get; set; } = "gpt-4o-mini";

    public Guid?  DocumentId { get; set; }
    public int TopK { get; set; } = 3;
    public decimal Temperature { get; set; } = 0.7m;
    public decimal Threshold { get; set; } = 0.0m;

    public string SplitMethod { get; set; } = "batch";
    public int BatchSize { get; set; } = 1000;
    public string? SplitPrompt { get; set; }
    public string? TablePrompt { get; set; }
}


