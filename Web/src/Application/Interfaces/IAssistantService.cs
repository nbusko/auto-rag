namespace AutoRag.Application.Interfaces;

public interface IAssistantService
{
    Task<string> GetAnswerAsync(Guid messageId, CancellationToken ct = default);
}