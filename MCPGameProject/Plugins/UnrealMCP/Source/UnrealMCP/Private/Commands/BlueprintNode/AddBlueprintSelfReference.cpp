#include "Commands/BlueprintNode/AddBlueprintSelfReference.h"
#include "Commands/CommonUtils.h"
#include "Engine/Blueprint.h"
#include "EdGraph/EdGraph.h"
#include "K2Node_Self.h"
#include "Kismet2/BlueprintEditorUtils.h"

auto FAddBlueprintSelfReference::Handle(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject> {
	// Get required parameters
	FString BlueprintName;
	if (!Params->TryGetStringField(TEXT("blueprint_name"), BlueprintName)) {
		return FCommonUtils::CreateErrorResponse(TEXT("Missing 'blueprint_name' parameter"));
	}

	// Get position parameters (optional)
	FVector2D NodePosition(0.0f, 0.0f);
	if (Params->HasField(TEXT("node_position"))) {
		NodePosition = FCommonUtils::GetVector2DFromJson(Params, TEXT("node_position"));
	}

	// Find the blueprint
	UBlueprint* Blueprint = FCommonUtils::FindBlueprint(BlueprintName);
	if (!Blueprint) {
		return FCommonUtils::CreateErrorResponse(
			FString::Printf(TEXT("Blueprint not found: %s"), *BlueprintName));
	}

	// Get the event graph
	UEdGraph* EventGraph = FCommonUtils::FindOrCreateEventGraph(Blueprint);
	if (!EventGraph) {
		return FCommonUtils::CreateErrorResponse(TEXT("Failed to get event graph"));
	}

	// Create the self node
	UK2Node_Self* SelfNode = FCommonUtils::CreateSelfReferenceNode(EventGraph, NodePosition);
	if (!SelfNode) {
		return FCommonUtils::CreateErrorResponse(TEXT("Failed to create self node"));
	}

	// Mark the blueprint as modified
	FBlueprintEditorUtils::MarkBlueprintAsModified(Blueprint);

	TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
	ResultObj->SetStringField(TEXT("node_id"), SelfNode->NodeGuid.ToString());
	return ResultObj;
}
