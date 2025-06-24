namespace AutoRag.Application.DTOs;

public sealed record DocumentInfoDto(Guid Id, string FileName, long Size)
{
    public DateTime UploadedAt { get; init; } = DateTime.UtcNow;
}

public class RagConfigDto
{
    public Guid? SelectedDocumentId { get; set; }
    public string SystemPrompt { get; set; } = string.Empty;
    public int TopK { get; set; } = 3;
    public decimal Temperature { get; set; } = 0.7m;
    public decimal Threshold { get; set; } = 0.0m;

    public RagConfigDto() { }

    public RagConfigDto(Guid? selectedDocumentId,
                        string systemPrompt,
                        int topK,
                        decimal temperature = 0.7m,
                        decimal threshold   = 0.0m)
        => (SelectedDocumentId, SystemPrompt, TopK, Temperature, Threshold)
         = (selectedDocumentId, systemPrompt, topK, temperature, threshold);
}

