#pragma once

#include "CoreMinimal.h"
#include "Json.h"

namespace UnrealMCP
{
	class FBlueprintService;
}

/**
 * Command handler for blueprint spawning operations
 * Thin layer that converts JSON to typed parameters and delegates to BlueprintService
 */
class UNREALMCP_API FUnrealMCPBlueprintSpawnCommands
{
public:
	FUnrealMCPBlueprintSpawnCommands();

	/**
	 * Handle blueprint spawning command
	 * @param Params JSON parameters containing blueprint_name, actor_name, and optional location/rotation
	 * @return JSON response with spawned actor data or error message
	 */
	static TSharedPtr<FJsonObject> HandleSpawnBlueprintActor(const TSharedPtr<FJsonObject>& Params);

private:
	/** Shared service instance for blueprint operations */
	static TSharedPtr<UnrealMCP::FBlueprintService> GetService();
};
