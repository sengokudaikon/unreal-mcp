#include "Commands/BlueprintNode/ConnectBlueprintNodes.h"
#include "Commands/CommonUtils.h"
#include "Engine/Blueprint.h"
#include "EdGraph/EdGraph.h"
#include "EdGraph/EdGraphNode.h"
#include "Kismet2/BlueprintEditorUtils.h"

auto FConnectBlueprintNodes::Handle(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject> {
	// Get required parameters
	FString BlueprintName;
	if (!Params->TryGetStringField(TEXT("blueprint_name"), BlueprintName)) {
		return FCommonUtils::CreateErrorResponse(TEXT("Missing 'blueprint_name' parameter"));
	}

	FString SourceNodeId;
	if (!Params->TryGetStringField(TEXT("source_node_id"), SourceNodeId)) {
		return FCommonUtils::CreateErrorResponse(TEXT("Missing 'source_node_id' parameter"));
	}

	FString TargetNodeId;
	if (!Params->TryGetStringField(TEXT("target_node_id"), TargetNodeId)) {
		return FCommonUtils::CreateErrorResponse(TEXT("Missing 'target_node_id' parameter"));
	}

	FString SourcePinName;
	if (!Params->TryGetStringField(TEXT("source_pin"), SourcePinName)) {
		return FCommonUtils::CreateErrorResponse(TEXT("Missing 'source_pin' parameter"));
	}

	FString TargetPinName;
	if (!Params->TryGetStringField(TEXT("target_pin"), TargetPinName)) {
		return FCommonUtils::CreateErrorResponse(TEXT("Missing 'target_pin' parameter"));
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

	// Find the nodes
	UEdGraphNode* SourceNode = nullptr;
	UEdGraphNode* TargetNode = nullptr;
	for (UEdGraphNode* Node : EventGraph->Nodes) {
		if (Node->NodeGuid.ToString() == SourceNodeId) {
			SourceNode = Node;
		}
		else if (Node->NodeGuid.ToString() == TargetNodeId) {
			TargetNode = Node;
		}
	}

	if (!SourceNode || !TargetNode) {
		return FCommonUtils::CreateErrorResponse(TEXT("Source or target node not found"));
	}

	// Connect the nodes
	if (FCommonUtils::ConnectGraphNodes(EventGraph, SourceNode, SourcePinName, TargetNode, TargetPinName)) {
		// Mark the blueprint as modified
		FBlueprintEditorUtils::MarkBlueprintAsModified(Blueprint);

		TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
		ResultObj->SetStringField(TEXT("source_node_id"), SourceNodeId);
		ResultObj->SetStringField(TEXT("target_node_id"), TargetNodeId);
		return ResultObj;
	}

	return FCommonUtils::CreateErrorResponse(TEXT("Failed to connect nodes"));
}
