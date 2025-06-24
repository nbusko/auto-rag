using AutoRag.Domain.Entities;

namespace AutoRag.Domain.Interfaces.Repositories;

public interface IChatHistoryRepository
{
    Task AddAsync(ChatMessage msg, CancellationToken ct = default);

    Task<IReadOnlyList<ChatMessage>> GetByRagAndUserAsync(
        Guid ragId,
        Guid userId,
        CancellationToken ct = default);
}