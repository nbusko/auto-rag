namespace AutoRag.Application.DTOs;

/// <summary>
/// Информация о загруженном документе
/// </summary>
public sealed record DocumentInfoDto(Guid Id, string FileName, long Size)
{
     // когда не задаётся явно – проставляется текущее время
     public DateTime UploadedAt { get; init; } = DateTime.UtcNow;
}
/// <summary>
/// Конфигурация RAG-системы (mutable, требуется двусторонний data-binding в Blazor)
/// </summary>
public class RagConfigDto
{
    public Guid? SelectedDocumentId { get; set; }
    public string SystemPrompt { get; set; } = string.Empty;
    public int TopK { get; set; } = 3;

    public RagConfigDto() { }

    public RagConfigDto(Guid? selectedDocumentId, string systemPrompt, int topK)
        => (SelectedDocumentId, SystemPrompt, TopK) = (selectedDocumentId, systemPrompt, topK);
}

