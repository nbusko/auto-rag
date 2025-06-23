namespace AutoRag.Application.Interfaces;

public interface ICurrentUser
{
    Guid? UserId { get; set; }
    Guid? RagId  { get; set; }
    string Role  { get; set; }
    bool IsOwner { get; }
}