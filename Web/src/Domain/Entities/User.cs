using AutoRag.Domain.Common;

namespace AutoRag.Domain.Entities;

public sealed class User : BaseEntity<Guid>
{
    public string FullName { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string? Organization { get; set; }
    public Guid RagId  { get; set; }
    public string Role { get; set; } = "owner";

    public UserCredential Credential { get; set; } = null!;
}
