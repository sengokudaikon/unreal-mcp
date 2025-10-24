#pragma once

#include "CoreMinimal.h"
#include "Json.h"

/**
 * Handler class for Blueprint Node-related MCP commands
 */
class UNREALMCP_API FUnrealMCPBlueprintNodeCommands {
public:
	FUnrealMCPBlueprintNodeCommands();

	auto HandleCommand(const FString& CommandType, const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;

private:
	static auto HandleConnectBlueprintNodes(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;

	static auto HandleAddBlueprintGetSelfComponentReference(
		const TSharedPtr<FJsonObject>& Params
	) -> TSharedPtr<FJsonObject>;

	static auto HandleAddBlueprintEvent(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;

	static auto HandleAddBlueprintFunctionCall(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;

	static auto HandleAddBlueprintVariable(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;

	static auto HandleAddBlueprintInputActionNode(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;

	static auto HandleAddBlueprintSelfReference(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;

	static auto HandleFindBlueprintNodes(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;
};
