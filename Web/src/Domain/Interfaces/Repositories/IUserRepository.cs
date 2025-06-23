using AutoRag.Domain.Entities;

namespace AutoRag.Domain.Interfaces.Repositories;

public interface IUserRepository
{
    Task<User?> GetByEmailAsync(string email, CancellationToken ct = default);
    Task<User?> GetByIdAsync(Guid id, CancellationToken ct = default);

    Task AddAsync(User user, string passwordHash, CancellationToken ct = default);

    Task<bool> ValidateCredentialsAsync(string email, string passwordHash, CancellationToken ct = default);
    Task UpdateAsync(User user, CancellationToken ct = default);
}