using AutoRag.Application.DTOs;

namespace AutoRag.Application.Interfaces;

public interface IAuthService
{
    /* обычная регистрация */
    Task<AuthResultDto> RegisterAsync(RegisterDto dto, CancellationToken ct = default);

    /* регистрация по расшаренной ссылке (token может быть null) */
    Task<AuthResultDto> RegisterAsync(RegisterDto dto, Guid? shareToken, CancellationToken ct = default);

    Task<AuthResultDto> LoginAsync(LoginDto dto, CancellationToken ct = default);
}
