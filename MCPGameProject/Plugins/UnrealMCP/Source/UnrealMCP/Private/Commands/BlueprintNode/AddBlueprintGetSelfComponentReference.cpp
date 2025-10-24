#include "Commands/BlueprintNode/AddBlueprintGetSelfComponentReference.h"
#include "Commands/CommonUtils.h"
#include "Engine/Blueprint.h"
#include "EdGraph/EdGraph.h"
#include "K2Node_VariableGet.h"
#include "Kismet2/BlueprintEditorUtils.h"

auto FAddBlueprintGetSelfComponentReference::Handle(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject> {
	// Get required parameters
	FString BlueprintName;
	if (!Params->TryGetStringField(TEXT("blueprint_name"), BlueprintName)) {
		return FCommonUtils::CreateErrorResponse(TEXT("Missing 'blueprint_name' parameter"));
	}

	FString ComponentName;
	if (!Params->TryGetStringField(TEXT("component_name"), ComponentName)) {
		return FCommonUtils::CreateErrorResponse(TEXT("Missing 'component_name' parameter"));
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

	// Create the variable get node directly
	UK2Node_VariableGet* GetComponentNode = NewObject<UK2Node_VariableGet>(EventGraph);
	if (!GetComponentNode) {
		return FCommonUtils::CreateErrorResponse(TEXT("Failed to create get component node"));
	}

	// Set up the variable reference properly for UE5.5
	FMemberReference& VarRef = GetComponentNode->VariableReference;
	VarRef.SetSelfMember(FName(*ComponentName));

	// Set node position
	GetComponentNode->NodePosX = NodePosition.X;
	GetComponentNode->NodePosY = NodePosition.Y;

	// Add to graph
	EventGraph->AddNode(GetComponentNode);
	GetComponentNode->CreateNewGuid();
	GetComponentNode->PostPlacedNewNode();
	GetComponentNode->AllocateDefaultPins();

	// Explicitly reconstruct node for UE5.5
	GetComponentNode->ReconstructNode();

	// Mark the blueprint as modified
	FBlueprintEditorUtils::MarkBlueprintAsModified(Blueprint);

	TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
	ResultObj->SetStringField(TEXT("node_id"), GetComponentNode->NodeGuid.ToString());
	return ResultObj;
}
