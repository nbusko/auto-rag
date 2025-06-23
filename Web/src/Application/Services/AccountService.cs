using AutoRag.Application.DTOs;
using AutoRag.Application.Interfaces;
using AutoRag.Domain.Interfaces.Repositories;
using BCrypt.Net;

namespace AutoRag.Application.Services;

public sealed class AccountService : IAccountService
{
    private readonly IUserRepository _users;
    private readonly ICurrentUser    _current;

    public AccountService(IUserRepository u, ICurrentUser cur) => (_users,_current)=(u,cur);

    public async Task<AccountDto> GetAsync(CancellationToken ct = default)
    {
        var id = _current.UserId ?? throw new InvalidOperationException("Not authenticated");
        var u  = await _users.GetByIdAsync(id, ct) ?? throw new KeyNotFoundException();
        return new AccountDto
        {
            FullName     = u.FullName,
            Email        = u.Email,
            Organization = u.Organization
        };
    }

    public async Task<bool> UpdateAsync(AccountDto dto, CancellationToken ct = default)
    {
        var id = _current.UserId ?? throw new InvalidOperationException("Not authenticated");
        var u  = await _users.GetByIdAsync(id, ct) ?? throw new KeyNotFoundException();

        u.FullName     = dto.FullName;
        u.Organization = dto.Organization;
        await _users.UpdateAsync(u, ct);
        return true;
    }

    public async Task<bool> ChangePasswordAsync(string currentPassword, string newPassword, CancellationToken ct = default)
    {
        var id   = _current.UserId ?? throw new InvalidOperationException("Not authenticated");
        var user = await _users.GetByIdAsync(id, ct) ?? throw new KeyNotFoundException();

        if (!BCrypt.Net.BCrypt.Verify(currentPassword, user.Credential.PasswordHash))
            return false;

        var newHash = BCrypt.Net.BCrypt.HashPassword(newPassword);
        await _users.UpdatePasswordAsync(id, newHash, ct);
        return true;
    }
}