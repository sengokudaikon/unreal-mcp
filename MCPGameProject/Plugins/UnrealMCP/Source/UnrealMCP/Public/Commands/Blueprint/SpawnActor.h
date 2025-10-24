#pragma once

#include "CoreMinimal.h"

/**
 * Handles operations for spawning blueprint actors dynamically.
 */
class UNREALMCP_API FSpawnActor
{
public:
	FSpawnActor() = default;
	~FSpawnActor() = default;

	/**
	 * Handle blueprint spawning command
	 * @param Params JSON parameters containing blueprint_name, actor_name, and optional location/rotation
	 * @return JSON response with spawned actor data or error message
	 */
	static auto Handle(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;
};
