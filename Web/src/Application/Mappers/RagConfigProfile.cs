using AutoMapper;
using AutoRag.Application.DTOs;
using AutoRag.Domain.Entities;

namespace AutoRag.Application.Mappers;

public sealed class RagConfigProfile : Profile
{
    public RagConfigProfile()
    {
        CreateMap<RagConfig, RagConfigDto>()
            .ForMember(d => d.SystemPrompt      , o => o.MapFrom(s => s.Prompt))
            .ForMember(d => d.SelectedDocumentId, o => o.MapFrom(s => s.DocumentId))
            .ForMember(d => d.TopK              , o => o.MapFrom(s => s.TopK))
            .ForMember(d => d.Temperature       , o => o.MapFrom(s => s.Temperature))
            .ForMember(d => d.Threshold         , o => o.MapFrom(s => s.Threshold))
            .ForMember(d => d.LlmModel          , o => o.MapFrom(s => s.LlmModel))
            .ForMember(d => d.RetrievePrompt    , o => o.MapFrom(s => s.RetrievePrompt))
            .ForMember(d => d.AugmentationPrompt, o => o.MapFrom(s => s.AugmentationPrompt))
            .ForMember(d => d.SplitMethod       , o => o.MapFrom(s => s.SplitMethod))
            .ForMember(d => d.BatchSize         , o => o.MapFrom(s => s.BatchSize))
            .ForMember(d => d.SplitPrompt       , o => o.MapFrom(s => s.SplitPrompt))
            .ForMember(d => d.TablePrompt       , o => o.MapFrom(s => s.TablePrompt));

        CreateMap<RagConfigDto, RagConfig>()
            .ForMember(d => d.Prompt            , o => o.MapFrom(s => s.SystemPrompt))
            .ForMember(d => d.DocumentId        , o => o.MapFrom(s => s.SelectedDocumentId))
            .ForMember(d => d.TopK              , o => o.MapFrom(s => s.TopK))
            .ForMember(d => d.Temperature       , o => o.MapFrom(s => s.Temperature))
            .ForMember(d => d.Threshold         , o => o.MapFrom(s => s.Threshold))
            .ForMember(d => d.LlmModel          , o => o.MapFrom(s =>
                string.IsNullOrWhiteSpace(s.LlmModel) ? "gpt-4o-mini" : s.LlmModel))
            .ForMember(d => d.RetrievePrompt    , o => o.MapFrom(s => s.RetrievePrompt))
            .ForMember(d => d.AugmentationPrompt, o => o.MapFrom(s => s.AugmentationPrompt))
            .ForMember(d => d.SplitMethod       , o => o.MapFrom(s => s.SplitMethod))
            .ForMember(d => d.BatchSize         , o => o.MapFrom(s => s.BatchSize))
            .ForMember(d => d.SplitPrompt       , o => o.MapFrom(s => s.SplitPrompt))
            .ForMember(d => d.TablePrompt       , o => o.MapFrom(s => s.TablePrompt));
    }
}
