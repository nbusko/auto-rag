using AutoRag.Domain.Entities;

namespace AutoRag.Domain.Interfaces.Repositories;

public interface IRagConfigRepository
{
    Task<RagConfig?> GetAsync(CancellationToken ct = default);
    Task UpsertAsync(RagConfig cfg, CancellationToken ct = default);
}
