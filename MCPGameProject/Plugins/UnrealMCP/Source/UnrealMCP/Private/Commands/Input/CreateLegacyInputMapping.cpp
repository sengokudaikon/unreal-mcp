#include "Commands/Input/CreateLegacyInputMapping.h"
#include "Commands/CommonUtils.h"
#include "Services/InputService.h"
#include "Core/MCPTypes.h"

auto FCreateLegacyInputMapping::Handle(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject> {
	// Parse JSON to params struct
	UnrealMCP::TResult<UnrealMCP::FLegacyInputMappingParams> ParamsResult =
		UnrealMCP::FLegacyInputMappingParams::FromJson(Params);

	if (ParamsResult.IsFailure()) {
		return FCommonUtils::CreateErrorResponse(ParamsResult.GetError());
	}

	const UnrealMCP::FVoidResult Result =
		UnrealMCP::FInputService::CreateLegacyInputMapping(ParamsResult.GetValue());

	if (Result.IsFailure()) {
		return FCommonUtils::CreateErrorResponse(Result.GetError());
	}

	// Build JSON response
	const UnrealMCP::FLegacyInputMappingParams& ParsedParams = ParamsResult.GetValue();

	TSharedPtr<FJsonObject> Response = MakeShared<FJsonObject>();
	Response->SetStringField(TEXT("action_name"), ParsedParams.ActionName);
	Response->SetStringField(TEXT("key"), ParsedParams.Key);
	Response->SetBoolField(TEXT("shift"), ParsedParams.bShift);
	Response->SetBoolField(TEXT("ctrl"), ParsedParams.bCtrl);
	Response->SetBoolField(TEXT("alt"), ParsedParams.bAlt);
	Response->SetBoolField(TEXT("cmd"), ParsedParams.bCmd);
	return Response;
}