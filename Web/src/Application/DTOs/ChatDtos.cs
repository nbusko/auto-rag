namespace AutoRag.Application.DTOs;

public sealed record ChatMessageDto(string Role, string Content, DateTime Timestamp);
public sealed record ChatRequestDto(string Message);
public sealed record ChatResponseDto(string Message);
