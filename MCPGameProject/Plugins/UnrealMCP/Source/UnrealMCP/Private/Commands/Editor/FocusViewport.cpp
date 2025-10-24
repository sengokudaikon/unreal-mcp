#include "Commands/Editor/FocusViewport.h"
#include "Commands/CommonUtils.h"
#include "Services/ViewportService.h"
#include "Core/MCPTypes.h"

auto FFocusViewport::Handle(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject> {
	// Parse optional parameters
	TOptional<FString> TargetActor;
	if (Params->HasField(TEXT("target"))) {
		FString Target;
		if (Params->TryGetStringField(TEXT("target"), Target)) {
			TargetActor = Target;
		}
	}

	TOptional<FVector> Location;
	if (Params->HasField(TEXT("location"))) {
		Location = FCommonUtils::GetVectorFromJson(Params, TEXT("location"));
	}

	// Validate that we have at least one target
	if (!TargetActor.IsSet() && !Location.IsSet()) {
		return FCommonUtils::CreateErrorResponse(TEXT("Either 'target' or 'location' must be provided"));
	}

	const UnrealMCP::FVoidResult Result = UnrealMCP::FViewportService::FocusViewport(
		TargetActor,
		Location
	);

	if (Result.IsFailure()) {
		return FCommonUtils::CreateErrorResponse(Result.GetError());
	}

	// Build JSON response
	TSharedPtr<FJsonObject> Response = MakeShared<FJsonObject>();
	Response->SetBoolField(TEXT("success"), true);

	if (TargetActor.IsSet()) {
		Response->SetStringField(TEXT("focused_on"), TargetActor.GetValue());
	}

	return Response;
}