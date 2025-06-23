using AutoRag.Domain.Common;

namespace AutoRag.Domain.Entities;

public sealed class ChatMessage : BaseEntity<Guid>
{
    public Guid RagId       { get; set; }
    public string MessageType { get; set; } = string.Empty; // 'user' | 'assistant'
    public Guid? UserId     { get; set; }                   // автор (null для assistant)
    public string Text      { get; set; } = string.Empty;
}