#pragma once

#include "CoreMinimal.h"
#include "Json.h"

/**
 * Command handler for blueprint spawning operations
 * Thin layer that converts JSON to typed parameters and delegates to BlueprintService
 */
class UNREALMCP_API FSpawnBlueprint
{
public:
	FSpawnBlueprint() = default;
	~FSpawnBlueprint() = default;

	/**
	 * Handle blueprint spawning command
	 * @param Params JSON parameters containing blueprint_name, actor_name, and optional location/rotation
	 * @return JSON response with spawned actor data or error message
	 */
	static auto Handle(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;
};
