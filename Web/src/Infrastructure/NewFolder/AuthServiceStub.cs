using AutoRag.Application.DTOs;
using AutoRag.Application.Interfaces;

namespace AutoRag.Infrastructure.ServicesStub;

public sealed class AuthServiceStub : IAuthService
{
    public Task<AuthResultDto> RegisterAsync(RegisterDto dto, CancellationToken ct = default)
        => Task.FromResult(new AuthResultDto("user-123", "fake-token", "Registration successful"));
    public Task<AuthResultDto> LoginAsync(LoginDto dto, CancellationToken ct = default)
        => Task.FromResult(new AuthResultDto("user-123", "fake-token", "Login ok"));
}

