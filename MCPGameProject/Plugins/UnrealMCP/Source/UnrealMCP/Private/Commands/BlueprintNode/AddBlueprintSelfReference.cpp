#include "Commands/BlueprintNode/AddBlueprintSelfReference.h"
#include "Commands/CommonUtils.h"
#include "Services/BlueprintGraphService.h"
#include "K2Node_Self.h"

auto FAddBlueprintSelfReference::Handle(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject> {
	// Parse parameters
	FString BlueprintName;
	if (!Params->TryGetStringField(TEXT("blueprint_name"), BlueprintName)) {
		return FCommonUtils::CreateErrorResponse(TEXT("Missing 'blueprint_name' parameter"));
	}

	FVector2D NodePosition(0.0f, 0.0f);
	if (Params->HasField(TEXT("node_position"))) {
		NodePosition = FCommonUtils::GetVector2DFromJson(Params, TEXT("node_position"));
	}

	const UnrealMCP::TResult<UK2Node_Self*> Result = UnrealMCP::FBlueprintGraphService::AddSelfReferenceNode(
		BlueprintName,
		NodePosition
	);

	if (Result.IsFailure()) {
		return FCommonUtils::CreateErrorResponse(Result.GetError());
	}

	// Build JSON response
	TSharedPtr<FJsonObject> Response = MakeShared<FJsonObject>();
	Response->SetStringField(TEXT("node_id"), Result.GetValue()->NodeGuid.ToString());
	return Response;
}
