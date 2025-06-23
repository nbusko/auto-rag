using AutoRag.Domain.Entities;
using AutoRag.Domain.Interfaces.Repositories;
using AutoRag.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;

namespace AutoRag.Infrastructure.Repositories;

public sealed class ShareLinkRepository : IShareLinkRepository
{
    private readonly AutoRagContext _ctx;
    public ShareLinkRepository(AutoRagContext ctx)=>_ctx=ctx;

    public async Task<ShareLink?> GetByRagIdAsync(Guid ragId, CancellationToken ct = default)
        => await _ctx.Set<ShareLink>().FirstOrDefaultAsync(x => x.RagId == ragId, ct);

    public async Task<ShareLink?> GetByTokenAsync(Guid token, CancellationToken ct = default)
        => await _ctx.Set<ShareLink>().FirstOrDefaultAsync(x => x.Id == token && x.Enabled, ct);

    public async Task<ShareLink> CreateAsync(Guid ragId, CancellationToken ct = default)
    {
        var l = new ShareLink { RagId = ragId };
        await _ctx.AddAsync(l, ct);
        await _ctx.SaveChangesAsync(ct);
        return l;
    }

    public async Task<bool> EnableAsync(Guid ragId, bool enable, CancellationToken ct = default)
    {
        var link = await GetByRagIdAsync(ragId, ct);
        if (link is null) return false;
        link.Enabled = enable;
        await _ctx.SaveChangesAsync(ct);
        return true;
    }
}