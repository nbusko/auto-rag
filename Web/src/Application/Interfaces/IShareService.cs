using AutoRag.Application.DTOs;

namespace AutoRag.Application.Interfaces;

public interface IShareService
{
    Task<ShareLinkDto> GetOrCreateLinkAsync(CancellationToken ct = default);
    Task<bool> EnableLinkAsync(bool enable, CancellationToken ct = default);

    Task<IReadOnlyList<SubUserDto>>  ListUsersAsync(CancellationToken ct = default);
    Task<bool> AddUserAsync (CreateSubUserDto dto, CancellationToken ct = default);
    Task<bool> RemoveUserAsync(string userId, CancellationToken ct = default);
}