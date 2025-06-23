namespace AutoRag.Application.DTOs;

/* ссылка-приглашение */
public sealed record ShareLinkDto(Guid Token, bool Enabled, DateTime CreatedAt);

/* пользователь-участник */
public sealed record SubUserDto(string Id, string FullName, string Email);

/* данные для ручного добавления участника (mutable – требуется data-binding) */
public sealed class CreateSubUserDto
{
    public string FullName { get; set; } = string.Empty;
    public string Email    { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;
}