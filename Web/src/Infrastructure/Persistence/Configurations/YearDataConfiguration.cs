using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using AutoRag.Domain.Entities;
namespace AutoRag.Infrastructure.Persistence.Configurations;
internal sealed class YearDataConfiguration : IEntityTypeConfiguration<YearData>
{
    public void Configure(EntityTypeBuilder<YearData> b)
    {
        b.ToTable("year_data");
        b.HasKey(x=>x.Id);
        b.Property(x=>x.Id).HasColumnName("id");
        b.Property(x=>x.Year).HasColumnName("year");
        b.Property(x=>x.Income).HasColumnName("income");
        b.Property(x=>x.Expense).HasColumnName("expense");
    }
}
