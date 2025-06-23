namespace AutoRag.Application.Interfaces;

public interface ICurrentUser
{
    Guid? UserId { get; set; }
    Guid? RagId  { get; set; }
}