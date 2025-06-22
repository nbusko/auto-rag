using AutoRag.Application.DTOs;
using AutoRag.Application.Interfaces;

namespace AutoRag.Infrastructure.ServicesStub;

public sealed class RagConfigServiceStub : IRagConfigService
{
    private RagConfigDto? _stored;
    public Task<RagConfigDto?> GetAsync(CancellationToken ct = default) => Task.FromResult(_stored);
    public Task<bool> SaveAsync(RagConfigDto dto, CancellationToken ct = default)
    { _stored = dto; return Task.FromResult(true); }
}
