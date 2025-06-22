using AutoRag.Application.DTOs;
using AutoRag.Application.Interfaces;

namespace AutoRag.Infrastructure.ServicesStub;

public sealed class ChatServiceStub : IChatService
{
    public Task<ChatResponseDto> SendAsync(ChatRequestDto req, CancellationToken ct = default)
        => Task.FromResult(new ChatResponseDto($"Echo: {req.Message}"));
}
