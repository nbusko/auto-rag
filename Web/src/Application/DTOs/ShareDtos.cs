namespace AutoRag.Application.DTOs;

public sealed record ShareLinkDto(Guid Token, bool Enabled, DateTime CreatedAt);

public sealed record SubUserDto(string Id, string FullName, string Email);

public sealed class CreateSubUserDto
{
    public string FullName { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;
}