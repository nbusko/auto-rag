using AutoRag.Application.DTOs;

namespace AutoRag.Application.Interfaces;

public interface IAuthService
{
    Task<AuthResultDto> RegisterAsync(RegisterDto dto, CancellationToken ct = default);

    Task<AuthResultDto> RegisterAsync(RegisterDto dto, Guid? shareToken, CancellationToken ct = default);

    Task<AuthResultDto> LoginAsync(LoginDto dto, CancellationToken ct = default);
}
