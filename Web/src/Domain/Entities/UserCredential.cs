namespace AutoRag.Domain.Entities;

public sealed class UserCredential
{
    public Guid UserId        { get; set; }
    public string PasswordHash{ get; set; } = string.Empty;

    public User User { get; set; } = null!;
}