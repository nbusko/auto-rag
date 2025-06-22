using AutoRag.Application.DTOs;

namespace AutoRag.Application.Interfaces;

public interface IChatService
{
    Task<ChatResponseDto> SendAsync(ChatRequestDto req, CancellationToken ct = default);
}
