using AutoRag.Application.DTOs;

namespace AutoRag.Application.Interfaces;

public interface IAccountService
{
    Task<AccountDto> GetAsync(CancellationToken ct = default);
    Task<bool> UpdateAsync(AccountDto dto, CancellationToken ct = default);
}

