#include "Commands/BlueprintNode/FindBlueprintNodes.h"
#include "Commands/CommonUtils.h"
#include "Engine/Blueprint.h"
#include "EdGraph/EdGraph.h"
#include "K2Node_Event.h"
#include "Kismet2/BlueprintEditorUtils.h"

auto FFindBlueprintNodes::Handle(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject> {
	// Get required parameters
	FString BlueprintName;
	if (!Params->TryGetStringField(TEXT("blueprint_name"), BlueprintName)) {
		return FCommonUtils::CreateErrorResponse(TEXT("Missing 'blueprint_name' parameter"));
	}

	FString NodeType;
	if (!Params->TryGetStringField(TEXT("node_type"), NodeType)) {
		return FCommonUtils::CreateErrorResponse(TEXT("Missing 'node_type' parameter"));
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

	// Create a JSON array for the node GUIDs
	TArray<TSharedPtr<FJsonValue>> NodeGuidArray;

	// Filter nodes by the exact requested type
	if (NodeType == TEXT("Event")) {
		FString EventName;
		if (!Params->TryGetStringField(TEXT("event_name"), EventName)) {
			return FCommonUtils::CreateErrorResponse(
				TEXT("Missing 'event_name' parameter for Event node search"));
		}

		// Look for nodes with exact event name (e.g., ReceiveBeginPlay)
		for (UEdGraphNode* Node : EventGraph->Nodes) {
			UK2Node_Event* EventNode = Cast<UK2Node_Event>(Node);
			if (EventNode && EventNode->EventReference.GetMemberName() == FName(*EventName)) {
				UE_LOG(LogTemp,
				       Display,
				       TEXT("Found event node with name %s: %s"),
				       *EventName,
				       *EventNode->NodeGuid.ToString());
				NodeGuidArray.Add(MakeShared<FJsonValueString>(EventNode->NodeGuid.ToString()));
			}
		}
	}
	// Add other node types as needed (InputAction, etc.)

	TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
	ResultObj->SetArrayField(TEXT("node_guids"), NodeGuidArray);

	return ResultObj;
}
