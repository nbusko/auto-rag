using AutoRag.Application.DTOs;
using AutoRag.Application.Interfaces;

namespace AutoRag.Infrastructure.ServicesStub;

public sealed class AccountServiceStub : IAccountService
{
    private AccountDto _profile = new()
    {
        FullName = "John Doe",
        Email = "john@doe.io",
        Organization = "Acme Inc"
    };

    public Task<AccountDto> GetAsync(CancellationToken ct = default)
        => Task.FromResult(_profile);

    public Task<bool> UpdateAsync(AccountDto dto, CancellationToken ct = default)
    {
        _profile = dto;
        return Task.FromResult(true);
    }
}
