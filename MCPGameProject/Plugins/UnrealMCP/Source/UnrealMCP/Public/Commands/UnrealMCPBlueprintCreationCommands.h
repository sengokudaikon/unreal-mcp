#pragma once

#include "CoreMinimal.h"
#include "Json.h"

class UNREALMCP_API FUnrealMCPBlueprintCreationCommands {
public:
	FUnrealMCPBlueprintCreationCommands() = default;
	~FUnrealMCPBlueprintCreationCommands() = default;

	static auto HandleCommand(const FString& CommandType, const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;

private:
	static auto HandleCreateBlueprint(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;
	static auto HandleCompileBlueprint(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;
	static auto HandleSpawnBlueprintActor(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;

	static auto SpawnBlueprintActorSafely(UBlueprint* Blueprint, const FString& ActorName, const FTransform& SpawnTransform, UWorld* World) -> AActor*;

	static auto FindParentClass(const FString& ParentClassName) -> UClass*;
};