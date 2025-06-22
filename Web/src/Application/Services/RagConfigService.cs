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
    public RagConfigService(IRagConfigRepository r, IMapper m) => (_repo, _mapper) = (r, m);

    public async Task<RagConfigDto?> GetAsync(CancellationToken ct = default)
        => _mapper.Map<RagConfigDto?>(await _repo.GetAsync(ct));

    public async Task<bool> SaveAsync(RagConfigDto dto, CancellationToken ct = default)
    {
        var entity = _mapper.Map<RagConfig>(dto);
        await _repo.UpsertAsync(entity, ct);
        return true;
    }
}
