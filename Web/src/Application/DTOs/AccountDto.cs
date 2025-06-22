namespace AutoRag.Application.DTOs;

public record class AccountDto
{
    public string FullName { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string? Organization { get; set; }
}
