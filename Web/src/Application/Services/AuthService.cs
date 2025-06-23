using AutoRag.Application.DTOs;
using AutoRag.Application.Interfaces;
using AutoRag.Domain.Entities;
using AutoRag.Domain.Interfaces.Repositories;
using BCrypt.Net;

namespace AutoRag.Application.Services;

public sealed class AuthService : IAuthService
{
    private readonly IUserRepository _users;
    private readonly ICurrentUser    _current;

    public AuthService(IUserRepository u, ICurrentUser cur) => (_users,_current) = (u,cur);

    public async Task<AuthResultDto> RegisterAsync(RegisterDto dto, CancellationToken ct = default)
    {
        if (await _users.GetByEmailAsync(dto.Email, ct) is not null)
            return new AuthResultDto(string.Empty, string.Empty, "E-mail already registered");

        var ragId = Guid.NewGuid();
        var user  = new User
        {
            FullName     = dto.FullName,
            Email        = dto.Email,
            Organization = null,
            RagId        = ragId
        };

        var hash = BCrypt.Net.BCrypt.HashPassword(dto.Password);
        await _users.AddAsync(user, hash, ct);

        _current.UserId = user.Id;
        _current.RagId  = ragId;

        return new AuthResultDto(user.Id.ToString(), "dummy-token", "Registration successful");
    }

    public async Task<AuthResultDto> LoginAsync(LoginDto dto, CancellationToken ct = default)
    {
        var user = await _users.GetByEmailAsync(dto.Email, ct);
        if (user is null)
            return new AuthResultDto(string.Empty, string.Empty, "User not found");

        var ok = await _users.ValidateCredentialsAsync(dto.Email, dto.Password, ct);
        if (!ok)
            return new AuthResultDto(string.Empty, string.Empty, "Wrong password");

        _current.UserId = user.Id;
        _current.RagId  = user.RagId;

        return new AuthResultDto(user.Id.ToString(), "dummy-token", "Login ok");
    }
}