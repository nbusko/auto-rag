using AutoMapper;
using AutoRag.Application.DTOs;
using AutoRag.Application.Interfaces;
using AutoRag.Domain.Entities;
using AutoRag.Domain.Interfaces.Repositories;

namespace AutoRag.Application.Services;

public sealed class RagConfigService : IRagConfigService
{
    private readonly IRagConfigRepository _repo;
    private readonly IMapper _mapper;
    private readonly ICurrentUser _current;
    public RagConfigService(IRagConfigRepository r, IMapper m, ICurrentUser cur)
        => (_repo,_mapper,_current) = (r,m,cur);

    private Guid RagId => _current.RagId ?? throw new InvalidOperationException("Not authenticated");

    public async Task<RagConfigDto?> GetAsync(CancellationToken ct = default)
        => _mapper.Map<RagConfigDto?>(await _repo.GetAsync(RagId, ct));

    public async Task<bool> SaveAsync(RagConfigDto dto, CancellationToken ct = default)
    {
        var entity = _mapper.Map<RagConfig>(dto);
        await _repo.UpsertAsync(RagId, entity, ct);
        return true;
    }
}