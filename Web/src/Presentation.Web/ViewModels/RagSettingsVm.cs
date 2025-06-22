using AutoRag.Application.DTOs;

namespace AutoRag.Presentation.Web.ViewModels;

public class RagSettingsVm
{
    public IReadOnlyList<DocumentInfoDto> Documents { get; set; } = [];
    public RagConfigDto Config { get; set; } = new(null, "You are RAG system", 3);

    public bool IsBusy { get; set; }
    public string? Message { get; set; }
}
