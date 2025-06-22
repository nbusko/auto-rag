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
        => await _ctx.RagConfigs.FirstOrDefaultAsync(ct);

    public async Task UpsertAsync(RagConfig cfg, CancellationToken ct = default)
    {
        if (await _ctx.RagConfigs.AnyAsync(ct))
            _ctx.RagConfigs.Update(cfg);
        else
            await _ctx.RagConfigs.AddAsync(cfg, ct);

        await _ctx.SaveChangesAsync(ct);
    }
}
