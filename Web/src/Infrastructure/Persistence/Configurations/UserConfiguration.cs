using AutoRag.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace AutoRag.Infrastructure.Persistence.Configurations;

internal sealed class UserConfiguration : IEntityTypeConfiguration<User>
{
    public void Configure(EntityTypeBuilder<User> b)
    {
        b.ToTable("users");
        b.HasKey(x => x.Id);
        b.Property(x => x.Id).HasColumnName("user_id");
        b.Property(x => x.FullName).HasColumnName("full_name");
        b.Property(x => x.Email).HasColumnName("email");
        b.Property(x => x.Organization).HasColumnName("organization");
        b.Property(x => x.RagId).HasColumnName("rag_id");

        b.HasOne(x => x.Credential)
         .WithOne(c => c.User)
         .HasForeignKey<UserCredential>(c => c.UserId);
    }
}