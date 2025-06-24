using AutoRag.Application.DTOs;
using AutoRag.Application.Interfaces;
using AutoRag.Domain.Entities;
using AutoRag.Domain.Interfaces.Repositories;

namespace AutoRag.Application.Services;

public sealed class ChatService : IChatService
{
    private readonly IChatHistoryRepository _repo;
    private readonly IAssistantService      _assistant;
    private readonly ICurrentUser           _current;

    public ChatService(IChatHistoryRepository r,
                       IAssistantService a,
                       ICurrentUser c)
                       => (_repo,_assistant,_current) = (r,a,c);

    private Guid RagId   => _current.RagId  ?? throw new InvalidOperationException("Not authenticated");
    private Guid UserId  => _current.UserId ?? throw new InvalidOperationException("Not authenticated");

    public async Task<ChatResponseDto> SendAsync(ChatRequestDto req, CancellationToken ct = default)
    {
        /* сообщение пользователя */
        var userMsg = new ChatMessage
        {
            Id          = Guid.NewGuid(),
            RagId       = RagId,
            MessageType = "user",
            UserId      = UserId,
            Text        = req.Message
        };
        await _repo.AddAsync(userMsg, ct);

        /* ответ ассистента */
        var answer = await _assistant.GetAnswerAsync(userMsg.Id, ct);

        var assistantMsg = new ChatMessage
        {
            Id          = Guid.NewGuid(),
            RagId       = RagId,
            MessageType = "assistant",
            UserId      = UserId,          // << теперь сохраняем того же пользователя
            Text        = answer
        };
        await _repo.AddAsync(assistantMsg, ct);

        return new ChatResponseDto(answer);
    }

    public async Task<IReadOnlyList<ChatMessageDto>> GetHistoryAsync(CancellationToken ct = default)
    {
        var list = await _repo.GetByRagAndUserAsync(RagId, UserId, ct);

        return list
            .OrderBy(m => m.Id)
            .Select(m => new ChatMessageDto(m.MessageType, m.Text, DateTime.UtcNow))
            .ToList()
            .AsReadOnly();
    }
}