using AutoRag.Application.DTOs;
namespace AutoRag.Application.Interfaces;

public interface IRagConfigService
{
    Task<RagConfigDto?> GetAsync(CancellationToken ct = default);
    Task<bool> SaveAsync(RagConfigDto dto, CancellationToken ct = default);
}
