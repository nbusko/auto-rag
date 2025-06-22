using AutoMapper;
using AutoRag.Application.DTOs;
using AutoRag.Domain.Entities;

namespace AutoRag.Application.Mappers;

public sealed class RagConfigProfile : Profile
{
    public RagConfigProfile()
    {
        CreateMap<RagConfig, RagConfigDto>().ReverseMap();
    }
}

