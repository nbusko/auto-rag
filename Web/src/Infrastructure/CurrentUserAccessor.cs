using AutoRag.Application.Interfaces;

namespace AutoRag.Infrastructure;

public sealed class CurrentUserAccessor : ICurrentUser
{
    public Guid? UserId { get; set; }
    public Guid? RagId  { get; set; }
    public string Role  { get; set; } = "owner";

    public bool IsOwner => Role == "owner";
}