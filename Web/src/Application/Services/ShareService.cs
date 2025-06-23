using AutoRag.Application.DTOs;
using AutoRag.Application.Interfaces;
using AutoRag.Domain.Entities;
using AutoRag.Domain.Interfaces.Repositories;

namespace AutoRag.Application.Services;

public sealed class ShareService : IShareService
{
    private readonly IShareLinkRepository _links;
    private readonly IUserRepository      _users;
    private readonly ICurrentUser         _current;

    public ShareService(IShareLinkRepository l, IUserRepository u, ICurrentUser cur)
        => (_links,_users,_current) = (l,u,cur);

    private Guid RagId => _current.RagId ?? throw new InvalidOperationException("Not authenticated");

    public async Task<ShareLinkDto> GetOrCreateLinkAsync(CancellationToken ct = default)
    {
        var link = await _links.GetByRagIdAsync(RagId, ct) ?? await _links.CreateAsync(RagId, ct);
        return new ShareLinkDto(link.Id, link.Enabled, link.CreatedAt);
    }

    public Task<bool> EnableLinkAsync(bool enable, CancellationToken ct = default)
        => _links.EnableAsync(RagId, enable, ct);

    public async Task<IReadOnlyList<SubUserDto>> ListUsersAsync(CancellationToken ct = default)
    {
        var list = await _users.GetByRagIdAsync(RagId, ct);
        return list.Where(u => u.Role == "member")
                   .Select(u => new SubUserDto(u.Id.ToString(), u.FullName, u.Email))
                   .ToList()
                   .AsReadOnly();
    }

    public async Task<bool> AddUserAsync(CreateSubUserDto dto, CancellationToken ct = default)
    {
        if (await _users.GetByEmailAsync(dto.Email, ct) is not null) return false;

        var pwdHash = BCrypt.Net.BCrypt.HashPassword(dto.Password);
        var user = new User
        {
            FullName = dto.FullName,
            Email    = dto.Email,
            RagId    = RagId,
            Role     = "member"
        };
        await _users.AddAsync(user, pwdHash, ct);
        return true;
    }

    public async Task<bool> RemoveUserAsync(string userId, CancellationToken ct = default)
    {
        if(!Guid.TryParse(userId, out var id)) return false;
        await _users.DeleteAsync(id, ct);
        return true;
    }
}