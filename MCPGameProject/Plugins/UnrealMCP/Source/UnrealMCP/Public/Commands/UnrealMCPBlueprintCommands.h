#pragma once

#include "CoreMinimal.h"
#include "Json.h"

/**
 * Handler class for Blueprint-related MCP commands
 */
class UNREALMCP_API FUnrealMCPBlueprintCommands {
public:
	FUnrealMCPBlueprintCommands();

	TSharedPtr<FJsonObject> HandleCommand(const FString& CommandType, const TSharedPtr<FJsonObject>& Params);

private:
	auto HandleAddComponentToBlueprint(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;

	auto HandleSetComponentProperty(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;

	auto HandleSetPhysicsProperties(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;

	auto HandleSetBlueprintProperty(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;

	auto HandleSetStaticMeshProperties(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;

	auto HandleSetPawnProperties(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;

	auto AddComponentToBlueprint(
		const FString& BlueprintName,
		const FString& ComponentType,
		const FString& ComponentName,
		const FString& MeshType,
		const TArray<float>& Location,
		const TArray<float>& Rotation,
		const TArray<float>& Scale,
		const TSharedPtr<FJsonObject>& ComponentProperties
	) -> TSharedPtr<FJsonObject>;
};
