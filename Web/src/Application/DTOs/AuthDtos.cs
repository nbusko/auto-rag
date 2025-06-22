namespace AutoRag.Application.DTOs;  

public sealed record RegisterDto(string FullName, string Email, string Password);
public sealed record LoginDto(string Email, string Password);
public sealed record AuthResultDto(string UserId, string Token, string Message);

