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

    private Guid RagId => _current.RagId ?? throw new InvalidOperationException("Not authenticated");

    public async Task<ChatResponseDto> SendAsync(ChatRequestDto req, CancellationToken ct = default)
    {
        var userMsg = new ChatMessage
        {
            Id          = Guid.NewGuid(),
            RagId       = RagId,
            MessageType = "user",
            UserId      = _current.UserId,
            Text        = req.Message
        };

        await _repo.AddAsync(userMsg, ct);

        var answer = await _assistant.GetAnswerAsync(userMsg.Id, ct);

        var assistantMsg = new ChatMessage
        {
            Id          = Guid.NewGuid(),
            RagId       = RagId,
            MessageType = "assistant",
            UserId      = null,
            Text        = answer
        };
        
        await _repo.AddAsync(assistantMsg, ct);

        return new ChatResponseDto(answer);
    }

    public async Task<IReadOnlyList<ChatMessageDto>> GetHistoryAsync(CancellationToken ct = default)
    {
        var list = await _repo.GetByRagIdAsync(RagId, ct);

        return list
            .OrderBy(m => m.Id)
            .Select(m => new ChatMessageDto(m.MessageType, m.Text, DateTime.UtcNow))
            .ToList()
            .AsReadOnly();
    }
}
