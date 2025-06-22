using AutoMapper;
using AutoRag.Application.DTOs;
using AutoRag.Domain.Entities;

namespace AutoRag.Application.Mappers;

public sealed class RagConfigProfile : Profile
{
    public RagConfigProfile()
    {
        CreateMap<RagConfig, RagConfigDto>()
            .ForMember(d => d.SystemPrompt,       o => o.MapFrom(s => s.Prompt))
            .ForMember(d => d.SelectedDocumentId, o => o.MapFrom(s => s.DocumentId));

        CreateMap<RagConfigDto, RagConfig>()
            .ForMember(d => d.Prompt,     o => o.MapFrom(s => s.SystemPrompt))
            .ForMember(d => d.DocumentId, o => o.MapFrom(s => s.SelectedDocumentId));
    }
}
