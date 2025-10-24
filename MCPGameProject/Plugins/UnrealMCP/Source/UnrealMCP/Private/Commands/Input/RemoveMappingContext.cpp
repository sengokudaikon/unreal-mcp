#include "Commands/Input/RemoveMappingContext.h"
#include "Commands/CommonUtils.h"
#include "Services/InputService.h"
#include "Core/MCPTypes.h"

auto FRemoveMappingContext::Handle(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject> {
	// Parse JSON to params struct
	UnrealMCP::TResult<UnrealMCP::FRemoveMappingContextParams> ParamsResult =
		UnrealMCP::FRemoveMappingContextParams::FromJson(Params);

	if (ParamsResult.IsFailure()) {
		return FCommonUtils::CreateErrorResponse(ParamsResult.GetError());
	}

	const UnrealMCP::FVoidResult Result =
		UnrealMCP::FInputService::RemoveMappingContext(ParamsResult.GetValue());

	if (Result.IsFailure()) {
		return FCommonUtils::CreateErrorResponse(Result.GetError());
	}

	// Build JSON response
	const UnrealMCP::FRemoveMappingContextParams& ParsedParams = ParamsResult.GetValue();

	TSharedPtr<FJsonObject> Response = MakeShared<FJsonObject>();
	Response->SetStringField(TEXT("context_path"), ParsedParams.ContextPath);
	return Response;
}
