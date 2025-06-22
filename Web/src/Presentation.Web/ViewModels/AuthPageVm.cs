using AutoRag.Application.DTOs;

namespace AutoRag.Presentation.Web.ViewModels;

public sealed class AuthPageVm
{
    public bool IsLogin { get; set; } = false;
    public string? FullName { get; set; }
    public string Email { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;

    public bool IsBusy { get; set; }
    public string? Message { get; set; }
}

