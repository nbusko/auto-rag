using AutoRag.Domain.Entities;
using AutoRag.Domain.Interfaces.Repositories;
using AutoRag.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;
using BCrypt.Net;

namespace AutoRag.Infrastructure.Repositories;

public sealed class UserRepository : IUserRepository
{
    private readonly AutoRagContext _ctx;
    public UserRepository(AutoRagContext ctx)=>_ctx=ctx;

    public async Task<User?> GetByEmailAsync(string email, CancellationToken ct = default)
        => await _ctx.Users.Include(u=>u.Credential)
                           .FirstOrDefaultAsync(u => u.Email == email, ct);

    public async Task<User?> GetByIdAsync(Guid id, CancellationToken ct = default)
        => await _ctx.Users.Include(u=>u.Credential)
                           .FirstOrDefaultAsync(u => u.Id == id, ct);

    public async Task AddAsync(User user, string passwordHash, CancellationToken ct = default)
    {
        user.Id = Guid.NewGuid();
        var cred = new UserCredential { UserId = user.Id, PasswordHash = passwordHash };
        user.Credential = cred;

        await _ctx.Users.AddAsync(user, ct);
        await _ctx.SaveChangesAsync(ct);
    }

    public async Task<bool> ValidateCredentialsAsync(string email, string password, CancellationToken ct = default)
    {
        var user = await GetByEmailAsync(email, ct);
        if (user is null) return false;

        return BCrypt.Net.BCrypt.Verify(password, user.Credential.PasswordHash);
    }

    public async Task UpdateAsync(User user, CancellationToken ct = default)
    {
        _ctx.Users.Update(user);
        await _ctx.SaveChangesAsync(ct);
    }
}
