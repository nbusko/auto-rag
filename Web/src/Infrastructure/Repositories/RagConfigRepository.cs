using AutoRag.Domain.Entities;
using AutoRag.Domain.Interfaces.Repositories;
using AutoRag.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;

namespace AutoRag.Infrastructure.Repositories;

public sealed class RagConfigRepository : IRagConfigRepository
{
    private readonly AutoRagContext _ctx;
    public RagConfigRepository(AutoRagContext ctx) => _ctx = ctx;

    public async Task<RagConfig?> GetAsync(CancellationToken ct = default)
        => await _ctx.RagConfigs.AsNoTracking().FirstOrDefaultAsync(ct);

    public async Task UpsertAsync(RagConfig cfg, CancellationToken ct = default)
    {
        var existing = await _ctx.RagConfigs.FirstOrDefaultAsync(ct);

        if (existing is null)
        {
            // первая запись
            cfg.Id = Guid.NewGuid();
            await _ctx.RagConfigs.AddAsync(cfg, ct);
        }
        else
        {
            // обновляем поля
            existing.Prompt     = cfg.Prompt;
            existing.DocumentId = cfg.DocumentId;
            _ctx.RagConfigs.Update(existing);
        }

        await _ctx.SaveChangesAsync(ct);
    }
}