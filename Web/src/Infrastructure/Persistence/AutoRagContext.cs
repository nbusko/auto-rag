using Microsoft.EntityFrameworkCore;
using AutoRag.Domain.Entities;

namespace AutoRag.Infrastructure.Persistence;

public sealed class AutoRagContext : DbContext
{
    public AutoRagContext(DbContextOptions<AutoRagContext> options) : base(options) { }

    public DbSet<RagConfig>    RagConfigs    => Set<RagConfig>();
    public DbSet<YearData>     YearDatas     => Set<YearData>();
    public DbSet<ChatMessage>  ChatMessages  => Set<ChatMessage>();

    protected override void OnModelCreating(ModelBuilder m) => 
        m.ApplyConfigurationsFromAssembly(typeof(AutoRagContext).Assembly);
}
