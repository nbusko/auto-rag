using AutoRag.Domain.Common;
namespace AutoRag.Domain.Entities;
public sealed class YearData : BaseEntity<int>
{
    public int Year { get; set; }
    public decimal Income  { get; set; }
    public decimal Expense { get; set; }
}
