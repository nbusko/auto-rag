using AutoRag.Application.DTOs;
namespace AutoRag.Presentation.Web.ViewModels;
public sealed class YearDataPageVm
{
    public int Year { get; set; } = System.DateTime.Now.Year;
    public YearDataDto? Report { get; set; }
    public bool IsBusy { get; set; }
    public string? Error { get; set; }
}
