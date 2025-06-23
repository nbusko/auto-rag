using AutoRag.Domain.Entities;

namespace AutoRag.Domain.Interfaces.Repositories;

public interface IRagConfigRepository
{
    Task<RagConfig?> GetAsync(Guid ragId, CancellationToken ct = default);
    Task UpsertAsync(Guid ragId, RagConfig cfg, CancellationToken ct = default);
}