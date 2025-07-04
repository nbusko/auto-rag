﻿using Microsoft.EntityFrameworkCore;
using AutoRag.Domain.Entities;

namespace AutoRag.Infrastructure.Persistence;

public sealed class AutoRagContext : DbContext
{
    public AutoRagContext(DbContextOptions<AutoRagContext> options) : base(options) { }

    public DbSet<RagConfig> RagConfigs  => Set<RagConfig>();
    public DbSet<DocumentEmbedding> DocumentEmbeddings => Set<DocumentEmbedding>();
    public DbSet<YearData> YearDatas => Set<YearData>();
    public DbSet<ChatMessage> ChatMessages => Set<ChatMessage>();
    public DbSet<User> Users => Set<User>();
    public DbSet<UserCredential> UserCredentials=> Set<UserCredential>();

    protected override void OnModelCreating(ModelBuilder m)
        => m.ApplyConfigurationsFromAssembly(typeof(AutoRagContext).Assembly);
}

