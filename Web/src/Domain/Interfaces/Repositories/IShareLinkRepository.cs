using AutoRag.Domain.Entities;

namespace AutoRag.Domain.Interfaces.Repositories;

public interface IShareLinkRepository
{
    Task<ShareLink?> GetByRagIdAsync(Guid ragId, CancellationToken ct = default);
    Task<ShareLink?> GetByTokenAsync(Guid token,  CancellationToken ct = default);
    Task<ShareLink> CreateAsync(Guid ragId, CancellationToken ct = default);
    Task<bool> EnableAsync (Guid ragId, bool enable, CancellationToken ct = default);
}