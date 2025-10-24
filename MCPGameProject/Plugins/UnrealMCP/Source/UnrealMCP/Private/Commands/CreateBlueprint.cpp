#include "Commands/CreateBlueprint.h"
#include "Commands/CommonUtils.h"
#include "Services/BlueprintCreationService.h"
#include "Core/MCPTypes.h"

auto FCreateBlueprint::Handle(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject> {
	// Parse JSON to params struct
	UnrealMCP::TResult<UnrealMCP::FBlueprintCreationParams> ParamsResult =
		UnrealMCP::FBlueprintCreationParams::FromJson(Params);

	if (ParamsResult.IsFailure()) {
		return FCommonUtils::CreateErrorResponse(ParamsResult.GetError());
	}

	// Delegate to service
	UnrealMCP::TResult<UBlueprint*> Result =
		UnrealMCP::FBlueprintCreationService::CreateBlueprint(ParamsResult.GetValue());

	if (Result.IsFailure()) {
		return FCommonUtils::CreateErrorResponse(Result.GetError());
	}

	// Build JSON response
	const UnrealMCP::FBlueprintCreationParams& ParsedParams = ParamsResult.GetValue();
	const UBlueprint* Blueprint = Result.GetValue();

	TSharedPtr<FJsonObject> Response = MakeShared<FJsonObject>();
	Response->SetStringField(TEXT("name"), ParsedParams.Name);
	Response->SetStringField(TEXT("path"), ParsedParams.PackagePath + ParsedParams.Name);
	Response->SetStringField(
		TEXT("parent_class"),
		Blueprint->ParentClass ? Blueprint->ParentClass->GetName() : TEXT("AActor")
	);
	return Response;
}
