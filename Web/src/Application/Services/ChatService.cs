using AutoRag.Application.DTOs;
using AutoRag.Application.Interfaces;
using AutoRag.Domain.Entities;
using AutoRag.Domain.Interfaces.Repositories;

namespace AutoRag.Application.Services;

public sealed class ChatService : IChatService
{
    private static readonly Guid _ragId = Guid.Empty;   // пока одна-единственная сессия

    private readonly IChatHistoryRepository _repo;
    private readonly IAssistantService      _assistant;

    public ChatService(IChatHistoryRepository r, IAssistantService a) => (_repo, _assistant) = (r, a);

    /* ---------- отправка ---------- */
    public async Task<ChatResponseDto> SendAsync(ChatRequestDto req, CancellationToken ct = default)
    {
        var userMsg = new ChatMessage
        {
            Id          = Guid.NewGuid(),
            RagId       = _ragId,
            MessageType = "user",
            Text        = req.Message
        };
        await _repo.AddAsync(userMsg, ct);

        var answer = await _assistant.GetAnswerAsync(userMsg.Id, ct);

        var assistantMsg = new ChatMessage
        {
            Id          = Guid.NewGuid(),
            RagId       = _ragId,
            MessageType = "assistant",
            Text        = answer
        };
        await _repo.AddAsync(assistantMsg, ct);

        return new ChatResponseDto(answer);
    }

    /* ---------- история ---------- */
    public async Task<IReadOnlyList<ChatMessageDto>> GetHistoryAsync(CancellationToken ct = default)
    {
        var list = await _repo.GetByRagIdAsync(_ragId, ct);

        return list
            .OrderBy(m => m.Id)
            .Select(m => new ChatMessageDto(
                            m.MessageType,
                            m.Text,
                            DateTime.UtcNow))   // точной даты в модели нет
            .ToList()
            .AsReadOnly();
    }
}
