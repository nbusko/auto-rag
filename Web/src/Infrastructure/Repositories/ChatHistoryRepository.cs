using AutoRag.Domain.Entities;
using AutoRag.Domain.Interfaces.Repositories;
using AutoRag.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;

namespace AutoRag.Infrastructure.Repositories;

public sealed class ChatHistoryRepository : IChatHistoryRepository
{
    private readonly AutoRagContext _ctx;
    public ChatHistoryRepository(AutoRagContext ctx) => _ctx = ctx;

    public async Task AddAsync(ChatMessage msg, CancellationToken ct = default)
    {
        await _ctx.ChatMessages.AddAsync(msg, ct);
        await _ctx.SaveChangesAsync(ct);
    }

    public async Task<IReadOnlyList<ChatMessage>> GetByRagIdAsync(Guid ragId, CancellationToken ct = default)
        => await _ctx.ChatMessages.AsNoTracking()
               .Where(x => x.RagId == ragId)
               .OrderBy(x => x.Id)
               .ToListAsync(ct);
}