#pragma once

#include "CoreMinimal.h"
#include "Json.h"

class UBlueprint;
class UWorld;
class AActor;

/**
 * Handler class for Blueprint spawning-related MCP commands
 */
class UNREALMCP_API FUnrealMCPBlueprintSpawnCommands {
public:
	FUnrealMCPBlueprintSpawnCommands();

	// Handle blueprint spawning command
	static TSharedPtr<FJsonObject> HandleSpawnBlueprintActor(const TSharedPtr<FJsonObject>& Params);

private:
	// Actor spawning helper function
	static AActor* SpawnBlueprintActorSafely(
		const UBlueprint* Blueprint,
		const FString& ActorName,
		const FTransform& SpawnTransform,
		UWorld* World
	);
};
